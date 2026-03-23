#!/usr/bin/env python3

import os
import re
import sys
from pathlib import Path

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

COMMON_ROOTS = [
    "/usr",
    "/usr/local",
    "/opt",
    "/usr/lib",
    "/usr/include",
    "/tmp"
]

ENV_ROOT_VARS = [
    "CUDA_HOME",
    "CUDA_PATH",
    "CUDNN_ROOT",
    "TENSORRT_ROOT",
]

HEADER_CANDIDATES = {
    "cuda": ["cuda.h"],
    "cudnn": ["cudnn_version.h", "cudnn.h"],
    "tensorrt": ["NvInferVersion.h"],
}

MAX_SEARCH_DEPTH = 6


# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def collect_search_roots():
    roots = set(COMMON_ROOTS)

    for var in ENV_ROOT_VARS:
        value = os.environ.get(var)
        if value:
            roots.add(value)

    # Add LD_LIBRARY_PATH directories
    ld_paths = os.environ.get("LD_LIBRARY_PATH", "")
    for p in ld_paths.split(":"):
        if p:
            roots.add(p)

    return [Path(r) for r in roots if Path(r).exists()]


def find_headers(header_names):
    found = []
    roots = collect_search_roots()

    for root in roots:
        for path in root.rglob("*"):
            if path.name in header_names:
                if len(path.relative_to(root).parts) <= MAX_SEARCH_DEPTH:
                    found.append(path)

    return list(set(found))


def extract_macro_value(content, macro):
    match = re.search(rf"#define\s+{macro}\s+(\d+)", content)
    if match:
        return int(match.group(1))
    return None


# ------------------------------------------------------------
# CUDA Version
# ------------------------------------------------------------

def parse_cuda_version(header_path):
    try:
        text = header_path.read_text(errors="ignore")
        value = extract_macro_value(text, "CUDA_VERSION")
        if value:
            major = value // 1000
            minor = (value % 1000) // 10
            return f"{major}.{minor}"
    except Exception:
        pass
    return None


# ------------------------------------------------------------
# cuDNN Version
# ------------------------------------------------------------

def parse_cudnn_version(header_path):
    try:
        text = header_path.read_text(errors="ignore")

        major = extract_macro_value(text, "CUDNN_MAJOR")
        minor = extract_macro_value(text, "CUDNN_MINOR")
        patch = extract_macro_value(text, "CUDNN_PATCHLEVEL")

        if major is not None:
            return f"{major}.{minor}.{patch}"
    except Exception:
        pass
    return None


# ------------------------------------------------------------
# TensorRT Version
# ------------------------------------------------------------

def parse_tensorrt_version(header_path):
    try:
        text = header_path.read_text(errors="ignore")

        major = extract_macro_value(text, "NV_TENSORRT_MAJOR")
        minor = extract_macro_value(text, "NV_TENSORRT_MINOR")
        patch = extract_macro_value(text, "NV_TENSORRT_PATCH")

        if major is not None:
            return f"{major}.{minor}.{patch}"
    except Exception:
        pass
    return None


# ------------------------------------------------------------
# Main Logic
# ------------------------------------------------------------

def detect_library(name, parser):
    headers = find_headers(HEADER_CANDIDATES[name])
    versions = []

    for h in headers:
        version = parser(h)
        if version:
            versions.append((str(h), version))

    return versions


def main():
    print("Searching for CUDA, cuDNN, and TensorRT versions...\n")

    results = {
        "CUDA": detect_library("cuda", parse_cuda_version),
        "cuDNN": detect_library("cudnn", parse_cudnn_version),
        "TensorRT": detect_library("tensorrt", parse_tensorrt_version),
    }

    for lib, entries in results.items():
        print(f"=== {lib} ===")
        if not entries:
            print("Not found\n")
            continue

        for path, version in entries:
            print(f"Version: {version}")
            print(f"Header:  {path}")
            print()
    print("Done.")


if __name__ == "__main__":
    main()

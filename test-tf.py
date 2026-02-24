import tensorflow as tf
from tensorflow.python.compiler.tensorrt import trt_convert
import os
import sys, subprocess

exts = [(n, m.__file__) for n,m in sys.modules.items() if getattr(m, "__file__", None) and m.__file__.lower().endswith((".so", ".pyd", ".dll", ".dylib"))]
for name, path in exts:
    print(name, path)
    subprocess.run(["sh", "-c", f"ldd {path} | grep 'not found'"])

os.system('find /usr -name "libcudart.so*" 2>/dev/null')
os.system('find /usr -name "libcudnn.so*" 2>/dev/null')
os.system("grep -Rw --include 'cudart*.h' '#define\s\+CUDA_\(MAJOR\|MINOR\|PATCHLEVEL\)' /usr 2>/dev/null")
os.system("grep -Rw --include 'cudnn*.h' '#define\s\+CUDNN_\(MAJOR\|MINOR\|PATCHLEVEL\)' /usr 2>/dev/null")
os.system('nvidia-smi')


print(tf.config.list_physical_devices('GPU'))
print(tf.sysconfig.get_build_info())
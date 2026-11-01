import os
import ctypes
import sys

# Preload native libs Chaquopy biar gak error dlopen
def preload_libs():
    base = "/data/data/com.yadev.ubea/files/chaquopy/AssetFinder"
    # cari semua .so yang ada libjpeg_chaquopy
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.startswith("libjpeg") or f.startswith("libopenjp2") or f.startswith("libxcb"):
                try:
                    ctypes.CDLL(os.path.join(root, f))
                except:
                    pass

preload_libs()

# stub brotli kalau masih error
try:
    import brotli
except:
    import types
    brotli = types.ModuleType("brotli")
    brotli.decompress = lambda d: (_ for _ in ()).throw(RuntimeError("brotli not available"))
    sys.modules['brotli'] = brotli

def hello():
    return "hello"

def test_unitypy():
    try:
        # coba preload lagi sebelum import UnityPy
        preload_libs()
        import UnityPy
        info = f"UnityPy {UnityPy.__version__} loaded!\n"
        info += "Pillow + libjpeg OK!\n"
        info += "Ready to extract .bundle files!\n"
        return info
    except Exception as e:
        import traceback
        return f"Error: {e}\n{traceback.format_exc()}"
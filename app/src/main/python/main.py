import os
import sys
import shutil
import ctypes

BASE = "/data/data/com.yadev.ubea/files/chaquopy/AssetFinder"

def fix_native_libs():
    pil_dir = None
    libjpeg_src = None
    # cari lokasi
    for root, dirs, files in os.walk(BASE):
        if "_imaging.so" in files and root.endswith("PIL"):
            pil_dir = root
        if "libjpeg_chaquopy.so" in files and libjpeg_src is None:
            libjpeg_src = os.path.join(root, files[files.index("libjpeg_chaquopy.so")])
        # preload semua chaquopy libs biar gak missing
        for f in files:
            if f.endswith("_chaquopy.so"):
                try:
                    ctypes.CDLL(os.path.join(root, f))
                except:
                    pass
    
    # copy libjpeg ke folder PIL biar _imaging.so bisa lihat via $ORIGIN
    if pil_dir and libjpeg_src:
        dest = os.path.join(pil_dir, "libjpeg_chaquopy.so")
        if not os.path.exists(dest):
            try:
                shutil.copy(libjpeg_src, dest)
                ctypes.CDLL(dest)
            except Exception as e:
                print(f"copy libjpeg failed: {e}")

# jalanin fix SEBELUM import apapun
fix_native_libs()

# stub brotli
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
        fix_native_libs() # coba lagi sebelum import
        import UnityPy
        from PIL import Image
        info = f"Python OK\n"
        info += f"UnityPy {UnityPy.__version__} loaded!\n"
        info += f"Pillow {Image.__version__} + libjpeg FIXED!\n"
        info += "Siap extract .bundle!\n"
        return info
    except Exception as e:
        import traceback
        return f"Error: {e}\n{traceback.format_exc()}"
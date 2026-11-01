# Dummy PIL package - bypass all native libs
import sys
import types

def _make_dummy_module(full_name):
    mod = types.ModuleType(full_name)
    # Any attribute access returns a dummy class/callable
    class Dummy:
        def __init__(self, *a, **k): pass
        def __call__(self, *a, **k): return Dummy()
        def __getattr__(self, name): return Dummy()
        def __getattribute__(self, name): 
            return object.__getattribute__(self, name) if name in ('__class__', '__call__') else Dummy()
    
    # Make every attribute return Dummy
    def __getattr__(name):
        return Dummy()
    
    mod.__getattr__ = __getattr__
    return mod

# List semua submodule PIL yang mungkin di-import UnityPy
for sub in [
    "ImageDraw", "ImageOps", "ImageFile", "ImageChops", 
    "ImageEnhance", "ImageFilter", "ImageMath", "ImagePalette",
    "ImagePath", "ImageSequence", "ImageStat", "ImageColor",
    "ImageCms", "ImageFont", "JpegImagePlugin", "PngImagePlugin"
]:
    full = f"PIL.{sub}"
    if full not in sys.modules:
        sys.modules[full] = _make_dummy_module(full)

# Also make top-level PIL attributes work
def __getattr__(name):
    if name in sys.modules:
        return sys.modules[name]
    dummy_mod = _make_dummy_module(f"PIL.{name}")
    sys.modules[f"PIL.{name}"] = dummy_mod
    return dummy_mod
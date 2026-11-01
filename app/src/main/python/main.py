import sys

# Bikin stub brotli biar UnityPy gak crash kalau import brotli
try:
    import brotli
except Exception:
    print("brotli native not available, using stub")
    class DummyBrotli:
        def decompress(self, data): 
            raise RuntimeError("Bundle uses brotli compression - not supported on this build")
        def compress(self, data):
            raise RuntimeError("brotli not available")
    sys.modules['brotli'] = DummyBrotli()
    # fake module
    import types
    brotli = types.ModuleType("brotli")
    brotli.decompress = lambda d: (_ for _ in ()).throw(RuntimeError("brotli not available"))
    sys.modules['brotli'] = brotli

def hello():
    return "hello"

def test_unitypy():
    try:
        import UnityPy
        import sys
        info = f"Python {sys.version.split()[0]}\n"
        info += f"UnityPy {UnityPy.__version__} loaded!\n"
        info += "Ready to extract .bundle files!\n"
        info += "brotli: stub (ok for most bundles)\n"
        return info
    except Exception as e:
        import traceback
        return f"Error: {e}\n{traceback.format_exc()}"
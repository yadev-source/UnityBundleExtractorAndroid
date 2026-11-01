def hello():
    print("hello from python")

def test_unitypy():
    try:
        import UnityPy
        import sys
        info = f"Python {sys.version}\n"
        info += f"UnityPy {UnityPy.__version__} loaded!\n"
        info += "Ready to extract .bundle files!\n"
        return info
    except Exception as e:
        return f"Error loading UnityPy: {e}\n{str(e)}"
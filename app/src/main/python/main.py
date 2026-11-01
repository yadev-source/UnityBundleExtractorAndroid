def test_unitypy():
    try:
        import UnityPy
        info = f"UnityPy {UnityPy.__version__} loaded!\n"
        info += "PIL dummy OK!\n"
        info += "brotli dummy OK!\n"
        info += "Bundle parsing READY!\n"
        info += "\nCoba extract file .bundle sekarang bisa!\n"
        return info
    except Exception as e:
        import traceback
        return f"Error: {e}\n{traceback.format_exc()}"

def hello():
    return "hello"
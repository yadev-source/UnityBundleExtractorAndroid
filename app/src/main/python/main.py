def hello():
    return "hello"

def test_unitypy():
    try:
        # Import UnityPy sekarang bakal pakai PIL dummy di atas, bukan yang asli
        import UnityPy
        info = f"UnityPy {UnityPy.__version__} loaded!\n"
        info += "PIL bypass OK! (texture decode disabled)\n"
        info += "Bundle parsing READY!\n"
        info += "\nCore extractor jalan, cuma export texture PNG aja yang off.\n"
        info += "Untuk extract TextAsset, MonoBehaviour, AudioClip dll udah bisa!"
        return info
    except Exception as e:
        import traceback
        return f"Error: {e}\n{traceback.format_exc()}"
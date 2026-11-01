import os

def test_unitypy():
    import UnityPy
    return f"UnityPy {UnityPy.__version__} loaded!\nBundle parsing READY!\n"

def extract_bundle(bundle_path, output_dir):
    try:
        import UnityPy
        env = UnityPy.load(bundle_path)
        
        result = f"Loaded: {os.path.basename(bundle_path)}\n"
        result += f"Files: {len(env.files)}\n\n"
        
        count = 0
        os.makedirs(output_dir, exist_ok=True)
        
        for obj in env.objects:
            if obj.type.name in ["TextAsset", "MonoBehaviour", "Texture2D", "AudioClip"]:
                try:
                    data = obj.read()
                    name = getattr(data, 'm_Name', f"obj_{obj.path_id}")
                    
                    if obj.type.name == "TextAsset":
                        path = os.path.join(output_dir, f"{name}.txt")
                        # TextAsset
                        script = data.m_Script
                        if isinstance(script, str):
                            script = script.encode('utf-8', 'surrogateescape')
                        with open(path, 'wb') as f:
                            f.write(script if isinstance(script, bytes) else str(script).encode())
                    
                    elif obj.type.name == "Texture2D":
                        # cuma info aja karena PIL dummy
                        path = os.path.join(output_dir, f"{name}_info.txt")
                        with open(path, 'w') as f:
                            f.write(f"Texture: {name}\nWidth: {data.m_Width}\nHeight: {data.m_Height}\n")
                    
                    count += 1
                except Exception as e:
                    result += f"Skip {obj.type.name}: {e}\n"
        
        result += f"\nExtracted {count} assets to:\n{output_dir}\n"
        return result
        
    except Exception as e:
        import traceback
        return f"Extract failed: {e}\n{traceback.format_exc()}"
import os
import json

def test_unitypy():
    import UnityPy
    return f"UnityPy {UnityPy.__version__} loaded!\n.unity3d parsing READY!\n"

def extract_bundle(bundle_path, output_dir):
    try:
        import UnityPy
        env = UnityPy.load(bundle_path)
        
        file_name = os.path.basename(bundle_path)
        result = f"Loaded: {file_name}\n"
        result += f"Files in bundle: {len(env.files)}\n"
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Hitung semua tipe object buat .unity3d
        type_count = {}
        all_objects = list(env.objects)
        for obj in all_objects:
            t = obj.type.name
            type_count[t] = type_count.get(t, 0) + 1
        
        result += f"Total objects: {len(all_objects)}\n\nTypes found:\n"
        for t, c in sorted(type_count.items()):
            result += f" - {t}: {c}\n"
        
        result += f"\nExtracting...\n"
        
        count = 0
        # Buat folder khusus per tipe
        for obj in all_objects:
            try:
                tname = obj.type.name
                # Buat .unity3d kita extract semua yang penting
                if tname in ["GameObject", "Transform", "MonoBehaviour", "TextAsset", "Mesh", "Texture2D", "AudioClip", "Shader", "Font", "Material", "MeshRenderer", "BoxCollider"]:
                    data = obj.read()
                    m_name = getattr(data, 'm_Name', f"{tname}_{obj.path_id}")
                    if not m_name: m_name = f"{tname}_{obj.path_id}"
                    
                    # Save typetree sebagai json biar bisa dibaca
                    try:
                        tree = obj.read_typetree()
                        # Bersihin nama file
                        safe_name = "".join([c if c.isalnum() or c in "_-" else "_" for c in m_name])[:50]
                        out_path = os.path.join(output_dir, f"{safe_name}_{tname}_{obj.path_id}.json")
                        with open(out_path, 'w', encoding='utf-8', errors='ignore') as f:
                            json.dump(tree, f, indent=2, ensure_ascii=False, default=str)
                        count += 1
                    except Exception as e:
                        # Fallback txt
                        safe_name = "".join([c if c.isalnum() or c in "_-" else "_" for c in m_name])[:50]
                        out_path = os.path.join(output_dir, f"{safe_name}_{tname}_{obj.path_id}.txt")
                        with open(out_path, 'w', encoding='utf-8', errors='ignore') as f:
                            f.write(f"Name: {m_name}\nType: {tname}\nPathID: {obj.path_id}\n")
                            f.write(f"Error typetree: {e}\n")
                        count += 1
            except Exception as e:
                continue
        
        # Special handling buat Yin_beidong.unity3d
        result += f"\nExtracted {count} objects to:\n{output_dir}\n"
        result += f"\nTip: .unity3d biasanya isinya GameObject + MonoBehaviour\n"
        result += f"Cek file .json buat liat data Yin_beidong!\n"
        return result
        
    except Exception as e:
        import traceback
        return f"Extract failed: {e}\n{traceback.format_exc()}"
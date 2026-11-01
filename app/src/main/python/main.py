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
        os.makedirs(output_dir, exist_ok=True)
        
        type_count = {}
        objs = list(env.objects)
        for o in objs:
            type_count[o.type.name] = type_count.get(o.type.name, 0) + 1
        
        result = f"Loaded: {file_name}\nFiles: {len(env.files)}\nTotal: {len(objs)}\n\nTypes:\n"
        for k,v in sorted(type_count.items()):
            result += f"{k}: {v}\n"
        
        count = 0
        errors = []
        for obj in objs:
            try:
                t = obj.type.name
                # Buat .unity3d kita coba baca semua
                data = obj.read()
                name = getattr(data, 'm_Name', '') or f"{t}_{obj.path_id}"
                safe = "".join(c if c.isalnum() or c in "_-." else "_" for c in name)[:80]
                
                # Coba typetree dulu
                try:
                    tree = obj.read_typetree()
                    with open(os.path.join(output_dir, f"{safe}_{t}_{obj.path_id}.json"), 'w', encoding='utf-8', errors='ignore') as f:
                        json.dump(tree, f, indent=2, ensure_ascii=False, default=str)
                    count += 1
                except Exception as e1:
                    # Kalau typetree gagal, save info minimal
                    with open(os.path.join(output_dir, f"{safe}_{t}_{obj.path_id}.txt"), 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(f"Name: {name}\nType: {t}\nPathID: {obj.path_id}\n\nData dir: {dir(data)}\n")
                        # Coba tulis m_Name dll
                        try:
                            f.write(f"\nAttributes:\n")
                            for attr in ['m_Name', 'm_Tag', 'm_Layer', 'm_IsActive']:
                                if hasattr(data, attr):
                                    f.write(f"{attr}: {getattr(data, attr)}\n")
                        except:
                            pass
                    count += 1
                    errors.append(f"{t} {name}: {e1}")
            except Exception as e:
                errors.append(f"Fail {obj.type.name} {obj.path_id}: {e}")
                continue
        
        result += f"\nExtracted: {count}\nDir: {output_dir}\n"
        if errors:
            result += f"\nErrors (first 5):\n" + "\n".join(errors[:5])
        
        # Selalu bikin 1 file summary
        with open(os.path.join(output_dir, "_summary.txt"), 'w') as f:
            f.write(result)
        
        return result
        
    except Exception as e:
        import traceback
        return f"FAILED: {e}\n{traceback.format_exc()}"
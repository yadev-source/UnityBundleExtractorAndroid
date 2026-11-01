import os
import json

def test_unitypy():
    import UnityPy
    return f"UnityPy {UnityPy.__version__} - Full Extractor Ready!\nSupport: Texture2D, Mesh OBJ, AudioClip, TextAsset"

def extract_bundle(bundle_path, output_dir):
    try:
        import UnityPy
        env = UnityPy.load(bundle_path)
        file_name = os.path.basename(bundle_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Bikin subfolder kayak lenzarchive
        for sub in ["Texture2D", "Mesh", "AudioClip", "TextAsset", "MonoBehaviour", "GameObject", "Sprite", "Material", "Font", "Shader"]:
            os.makedirs(os.path.join(output_dir, sub), exist_ok=True)
        
        type_count = {}
        objs = list(env.objects)
        for o in objs:
            type_count[o.type.name] = type_count.get(o.type.name, 0) + 1
        
        result = f"Loaded: {file_name}\nTotal objects: {len(objs)}\n\nTypes:\n"
        for k,v in sorted(type_count.items()):
            result += f"  {k}: {v}\n"
        
        count = {"Texture2D":0, "Mesh":0, "AudioClip":0, "TextAsset":0, "Other":0}
        
        for obj in objs:
            try:
                t = obj.type.name
                data = obj.read()
                m_name = getattr(data, 'm_Name', '') or f"{t}_{obj.path_id}"
                safe = "".join(c if c.isalnum() or c in "_-." else "_" for c in m_name)[:60]
                if not safe: safe = f"{t}_{obj.path_id}"
                
                # === TEXTURE2D - Adaptasi dari lenzarchive ===
                if t == "Texture2D":
                    try:
                        # Coba pakai PIL dummy dulu, kalau gagal save raw
                        sub_dir = os.path.join(output_dir, "Texture2D")
                        # UnityPy punya data.image yang butuh PIL, kita bypass pakai raw data
                        # Kalau PIL dummy, kita save info aja + raw bytes kalau ada
                        info = {
                            "m_Name": m_name,
                            "m_Width": getattr(data, 'm_Width', 0),
                            "m_Height": getattr(data, 'm_Height', 0),
                            "m_TextureFormat": str(getattr(data, 'm_TextureFormat', '')),
                            "path_id": obj.path_id
                        }
                        with open(os.path.join(sub_dir, f"{safe}_info.json"), 'w', encoding='utf-8') as f:
                            json.dump(info, f, indent=2, default=str)
                        
                        # Coba save image kalau PIL asli available, kalau dummy bakal error tapi kita tangkep
                        try:
                            img = data.image
                            img.save(os.path.join(sub_dir, f"{safe}.png"))
                            count["Texture2D"] += 1
                        except Exception as e:
                            # Fallback: save raw image data kalau ada
                            if hasattr(data, 'image_data') and data.image_data:
                                with open(os.path.join(sub_dir, f"{safe}.raw"), 'wb') as f:
                                    f.write(data.image_data)
                            count["Texture2D"] += 1
                    except Exception as e:
                        pass
                
                # === MESH -> OBJ (kayak lenzarchive) ===
                elif t == "Mesh":
                    try:
                        sub_dir = os.path.join(output_dir, "Mesh")
                        obj_data = data.export()
                        if obj_data:
                            with open(os.path.join(sub_dir, f"{safe}.obj"), 'w', encoding='utf-8', newline='') as f:
                                f.write(obj_data)
                            # info json
                            info = {"m_Name": m_name, "path_id": obj.path_id, "vertex_count": len(getattr(data, 'm_Vertices', []))}
                            with open(os.path.join(sub_dir, f"{safe}_info.json"), 'w') as jf:
                                json.dump(info, jf, indent=2, default=str)
                            count["Mesh"] += 1
                    except:
                        pass
                
                # === AUDIOCLIP -> WAV ===
                elif t == "AudioClip":
                    try:
                        sub_dir = os.path.join(output_dir, "AudioClip")
                        for clip_name, clip_data in data.samples.items():
                            clip_safe = "".join(c if c.isalnum() or c in "_-." else "_" for c in clip_name)[:50]
                            ext = ".wav"
                            if clip_name.endswith(".ogg"): ext = ".ogg"
                            with open(os.path.join(sub_dir, f"{clip_safe}{ext}"), 'wb') as f:
                                f.write(clip_data)
                        count["AudioClip"] += 1
                    except:
                        pass
                
                # === TEXTASSET ===
                elif t == "TextAsset":
                    try:
                        sub_dir = os.path.join(output_dir, "TextAsset")
                        script = data.m_Script
                        if isinstance(script, str):
                            with open(os.path.join(sub_dir, f"{safe}.txt"), 'w', encoding='utf-8', errors='surrogateescape') as f:
                                f.write(script)
                        else:
                            with open(os.path.join(sub_dir, f"{safe}.bin"), 'wb') as f:
                                f.write(script if isinstance(script, bytes) else str(script).encode())
                        count["TextAsset"] += 1
                    except:
                        pass
                
                else:
                    # Yang lain jadi JSON kayak sebelumnya
                    try:
                        tree = obj.read_typetree()
                        with open(os.path.join(output_dir, t, f"{safe}_{obj.path_id}.json"), 'w', encoding='utf-8', errors='ignore') as f:
                            json.dump(tree, f, indent=2, ensure_ascii=False, default=str)
                        count["Other"] += 1
                    except:
                        pass
            except:
                continue
        
        result += f"\nExtracted:\n"
        for k,v in count.items():
            if v>0: result += f"  {k}: {v}\n"
        result += f"\nOutput: {output_dir}\n"
        result += f"Structured like lenzarchive!\n"
        
        with open(os.path.join(output_dir, "_summary.txt"), 'w') as f:
            f.write(result)
        
        return result
    except Exception as e:
        import traceback
        return f"FAILED: {e}\n{traceback.format_exc()}"
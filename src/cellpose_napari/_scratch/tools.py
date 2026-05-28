from pathlib import Path

def is_data(folder_path):
    if not folder_path.is_dir():
        return False
    if not any(f.name.startswith("c1") and f.name.endswith(".tif") for f in folder_path.iterdir() if f.is_file()):
        return False
    return True

def recursive_folder_exploration(root, folders):
    if not root.is_dir():
        return
    if is_data(root):
        folders.append(root)
    for child in root.iterdir():
        recursive_folder_exploration(child, folders)

def probe_folder(root_folder):
    folders = []
    recursive_folder_exploration(root_folder, folders)
    return folders

def remove_root(p1, p2):
    # Removes the parts that both folders have in common in p2
    p1_parts = p1.parts
    p2_parts = p2.parts
    kept = []
    is_root = True
    
    for i, p in enumerate(p2_parts):
        if not is_root:
            kept.append(p)
            continue
        if i >= len(p1_parts) or p != p1_parts[i]:
            is_root = False
            kept.append(p)
    return Path(*kept)
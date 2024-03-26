import os
import shutil
import glob
from tqdm import tqdm

files = glob.glob("exports/*/**/*.*", recursive=True)
dirs_to_remove = set()
for x in tqdm(files):
    doc_name = x.split("/")[2]
    to_delete_dir = os.path.join(*x.split("/")[:3])
    dirs_to_remove.add(to_delete_dir)
    new_path = x.replace(f"{doc_name}/", "")
    new_path_dir, _ = os.path.split(new_path)
    os.makedirs(new_path_dir, exist_ok=True)
    shutil.move(x, new_path)

print("delete not needed doc directories")
for x in dirs_to_remove:
    print(f"removing {x}")
    shutil.rmtree(x, ignore_errors=True)

import os
import shutil
import glob
from tqdm import tqdm

files = glob.glob("exports/*/**/*.*", recursive=True)
for x in tqdm(files):
    doc_name = x.split("/")[2]
    to_delete_dir = os.path.join(*x.split("/")[:3])
    new_path = x.replace(f"{doc_name}/", "")
    new_path_dir, _ = os.path.split(new_path)
    os.makedirs(new_path_dir, exist_ok=True)
    shutil.move(x, new_path)
    shutil.rmtree(to_delete_dir, ignore_errors=True)

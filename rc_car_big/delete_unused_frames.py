from glob import glob
from send2trash import send2trash
import os
import pandas as pd

os.chdir(os.path.dirname(__file__))

for dir in glob('unwrapped_2021*'):
    df = pd.read_csv(os.path.join(dir, 'database_entries.csv'))
    all_files = glob(os.path.join(dir, '*.jpg'))
    used_files = df.Filename.to_list()

    count = 0
    for fpath in all_files:
        if os.path.basename(fpath) not in used_files:
            count += 1
            send2trash(fpath)
    if count:
        print(f'Deleted {count}/{len(all_files)} files from {dir}')

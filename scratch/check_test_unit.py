import os
import glob
import pandas as pd
import random

base_dir = "scratch/data_set/Extended_TravisTorrent/test_info_logs"
projects = os.listdir(base_dir)
random.seed(42)
sampled_projects = random.sample(projects, 5)

print("Checking test units...")

for p in sampled_projects:
    print(f"\nProject: {p}")
    files = glob.glob(os.path.join(base_dir, p, "*.csv"))
    if not files:
        print("No CSVs.")
        continue
        
    sampled_files = random.sample(files, min(3, len(files)))
    for f in sampled_files:
        print(f"  File: {os.path.basename(f)}")
        try:
            df = pd.read_csv(f, header=None, on_bad_lines='skip')
            print(f"    Total Rows: {len(df)}")
            print(f"    Sample test_name values:")
            for val in df[1].head(3):
                print(f"      {val}")
            
            # Check if any row has total_tests > 1
            multi_test_rows = df[df[2] > 1]
            if len(multi_test_rows) > 0:
                print(f"    Rows with total_tests > 1 exist (e.g. {multi_test_rows.iloc[0, 1]} has {multi_test_rows.iloc[0, 2]} tests).")
            else:
                print(f"    All rows have total_tests = 1.")
        except Exception as e:
            print(f"    Error reading: {e}")

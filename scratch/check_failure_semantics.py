import os
import glob
import pandas as pd

base_dir = "scratch/data_set/Extended_TravisTorrent"
test_log_dir = os.path.join(base_dir, "test_info_logs")
mach_dir = os.path.join(base_dir, "Machalica19_git_result")
projects = os.listdir(test_log_dir)

found_failed = False
found_error = False

for p in projects:
    if found_failed and found_error:
        break
    files = glob.glob(os.path.join(test_log_dir, p, "*.csv"))
    for f in files:
        idx = os.path.basename(f)
        try:
            df = pd.read_csv(f, header=None, on_bad_lines='skip')
            mach_f = os.path.join(mach_dir, p, idx)
            df_mach = pd.read_csv(mach_f, header=None, on_bad_lines='skip')
            
            # test log format: project_prefix, test_name, total_tests, skipped, failed, errors, passed, duration
            # machalica format: test_name, total_runs, failure_status, changed_files...
            
            df_failed = df[df[4] > 0]
            df_error = df[df[5] > 0]
            
            if len(df_failed) > 0 and not found_failed:
                print(f"FAILED ROWS in {p}/{idx}")
                for _, row in df_failed.head(1).iterrows():
                    test_name = row[1]
                    print(f"  Test Log Row: {row.tolist()}")
                    mach_row = df_mach[df_mach[0] == test_name]
                    if len(mach_row) > 0:
                        print(f"  Machalica Row: {mach_row.iloc[0].tolist()[:3]}")
                found_failed = True
                
            if len(df_error) > 0 and not found_error:
                print(f"ERROR ROWS in {p}/{idx}")
                for _, row in df_error.head(1).iterrows():
                    test_name = row[1]
                    print(f"  Test Log Row: {row.tolist()}")
                    mach_row = df_mach[df_mach[0] == test_name]
                    if len(mach_row) > 0:
                        print(f"  Machalica Row: {mach_row.iloc[0].tolist()[:3]}")
                found_error = True
        except Exception as e:
            continue

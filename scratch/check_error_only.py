import os
import glob
import pandas as pd

base_dir = "scratch/data_set/Extended_TravisTorrent"
test_log_dir = os.path.join(base_dir, "test_info_logs")
mach_dir = os.path.join(base_dir, "Machalica19_git_result")
projects = os.listdir(test_log_dir)

for p in projects:
    files = glob.glob(os.path.join(test_log_dir, p, "*.csv"))
    for f in files:
        try:
            df = pd.read_csv(f, header=None, on_bad_lines='skip')
            # Look for errors > 0 AND failed == 0
            df_error_only = df[(df[5] > 0) & ((df[4] == 0) | df[4].isna())]
            
            if len(df_error_only) > 0:
                idx = os.path.basename(f)
                mach_f = os.path.join(mach_dir, p, idx)
                df_mach = pd.read_csv(mach_f, header=None, on_bad_lines='skip')
                print(f"ERROR ONLY ROWS in {p}/{idx}")
                for _, row in df_error_only.head(1).iterrows():
                    test_name = row[1]
                    print(f"  Test Log Row: {row.tolist()}")
                    mach_row = df_mach[df_mach[0] == test_name]
                    if len(mach_row) > 0:
                        print(f"  Machalica Row: {mach_row.iloc[0].tolist()[:3]}")
                exit(0)
        except Exception as e:
            continue

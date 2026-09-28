import os
import glob
import pandas as pd

base_dir = "scratch/data_set/Extended_TravisTorrent"
projects = os.listdir(os.path.join(base_dir, "test_info_logs"))

data = []
for p in projects:
    git_csv = os.path.join(base_dir, "Abdalkareem19_git_result", p + ".csv")
    if not os.path.exists(git_csv):
        # Some are named differently?
        # e.g., square_okhttp -> okhttp.csv
        p_short = p.split("_")[-1] + ".csv"
        git_csv = os.path.join(base_dir, "Abdalkareem19_git_result", p_short)
        
    num_commits = 0
    if os.path.exists(git_csv):
        try:
            with open(git_csv, 'r', encoding='utf-8') as f:
                num_commits = sum(1 for line in f)
        except Exception:
            pass
            
    test_files = glob.glob(os.path.join(base_dir, "test_info_logs", p, "*.csv"))
    num_builds = len(test_files)
    
    data.append({"Project": p, "Total_Commits": num_commits, "Parsed_Builds": num_builds})

df = pd.DataFrame(data)
df.to_csv("scratch/cibench_stats.csv", index=False)
print(f"Total Projects: {len(df)}")
print(f"Total Commits: {df['Total_Commits'].sum()}")
print(f"Total Parsed Builds (Test Logs): {df['Parsed_Builds'].sum()}")

import os
import pandas as pd

base_dir = "scratch/data_set/Extended_TravisTorrent"
csv_dir = os.path.join(base_dir, "Abdalkareem19_git_result")
projects = os.listdir(csv_dir)

results = []

for p in projects:
    if not p.endswith(".csv"): continue
    df = pd.read_csv(os.path.join(csv_dir, p), header=None, names=["commit_hash", "message", "is_skipped"])
    total_rows = len(df)
    unique_shas = df["commit_hash"].nunique()
    duplicates = total_rows - unique_shas
    
    # Check if test_info_logs correspond to these rows
    test_logs_path = os.path.join(base_dir, "test_info_logs", p.replace(".csv", ""))
    
    # We don't have project names exactly matching test_info_logs sometimes?
    # Actually, Abdalkareem19_git_result has okhttp.csv, test_info_logs has square_okhttp.
    
    results.append({
        "Project_File": p,
        "Total_Rows": total_rows,
        "Unique_SHAs": unique_shas,
        "Duplicate_SHAs": duplicates
    })

df_res = pd.DataFrame(results)
print(f"Total Rows: {df_res['Total_Rows'].sum()}")
print(f"Unique SHAs: {df_res['Unique_SHAs'].sum()}")
print(f"Duplicates: {df_res['Duplicate_SHAs'].sum()}")

# View an example of duplicates
for p in projects:
    if not p.endswith(".csv"): continue
    df = pd.read_csv(os.path.join(csv_dir, p), header=None, names=["commit_hash", "message", "is_skipped"])
    if df["commit_hash"].duplicated().any():
        print(f"\nDuplicates in {p}:")
        dups = df[df["commit_hash"].duplicated(keep=False)]
        print(dups.head(6))
        break

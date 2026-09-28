import os
import subprocess
import pandas as pd
import shutil

projects_to_audit = {
    "okhttp.csv": "https://github.com/square/okhttp.git",
    "picasso.csv": "https://github.com/square/picasso.git"
}

base_dir = "scratch/data_set/Extended_TravisTorrent/Abdalkareem19_git_result"

results = []

for p, url in projects_to_audit.items():
    csv_path = os.path.join(base_dir, p)
    df = pd.read_csv(csv_path, header=None, names=["commit_hash", "message", "is_skipped"])
    
    # Take a sample of 10 commits
    sample_commits = df["commit_hash"].dropna().sample(10, random_state=42).tolist()
    
    repo_name = url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join("scratch", repo_name)
    
    if not os.path.exists(repo_path):
        subprocess.run(["git", "clone", url, repo_path], check=True)
        
    for sha in sample_commits:
        # Check if commit exists
        cmd = ["git", "-C", repo_path, "show", "-s", "--format=%ct", sha]
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        if res.returncode == 0:
            timestamp = res.stdout.strip()
            status = "MATCH"
        else:
            timestamp = "N/A"
            status = "MISSING"
            
        is_dup = (df["commit_hash"] == sha).sum() > 1
        
        results.append({
            "project": p,
            "commit_hash": sha,
            "status": status,
            "timestamp": timestamp,
            "is_duplicate_in_dataset": is_dup
        })

res_df = pd.DataFrame(results)
res_df.to_csv("literature/e11_git_linkage_audit.csv", index=False)
print("Git linkage audit complete.")

import os
import pandas as pd
import json
import glob
from collections import defaultdict
import subprocess

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    return res.stdout.strip(), res.returncode

def main():
    base_dir = "scratch/data_set"
    test_logs_dir = os.path.join(base_dir, "Extended_TravisTorrent/test_info_logs")
    abdalkareem_dir = os.path.join(base_dir, "Extended_TravisTorrent/Abdalkareem19_git_result")
    machalica_dir = os.path.join(base_dir, "Extended_TravisTorrent/Machalica19_git_result")
    
    os.makedirs("data", exist_ok=True)
    
    builds_data = []
    test_classes_data = []
    sha_counts = defaultdict(list)
    git_linkage = []
    
    projects = [d for d in os.listdir(test_logs_dir) if os.path.isdir(os.path.join(test_logs_dir, d))]
    
    for proj in projects:
        proj_dir = os.path.join(test_logs_dir, proj)
        abd_file = os.path.join(abdalkareem_dir, f"{proj}.csv")
        # handle mismatches like okhttp vs square_okhttp
        if not os.path.exists(abd_file):
            proj_name = proj.split("_", 1)[-1]
            abd_file = os.path.join(abdalkareem_dir, f"{proj_name}.csv")
            
        if not os.path.exists(abd_file):
            continue
            
        df_abd = pd.read_csv(abd_file, header=None, on_bad_lines='skip')
        repo_name = proj.split("_", 1)[-1]
        repo_path = f"scratch/clones_bare/{repo_name}_bare"
        has_repo = os.path.exists(repo_path)
        
        csv_files = glob.glob(f"{proj_dir}/*.csv")
        for csv_file in csv_files:
            try:
                build_id_str = os.path.basename(csv_file).replace(".csv", "")
                cibench_row = int(build_id_str)
            except:
                continue
                
            # fetch SHA from Abdalkareem19
            # CIBench rows are 1-indexed, meaning row 1 is index 0
            if cibench_row < 1 or cibench_row > len(df_abd):
                continue
                
            row_abd = df_abd.iloc[cibench_row - 1]
            sha = str(row_abd[0])
            
            # git linkage
            git_status = "UNKNOWN"
            timestamp = "UNKNOWN"
            parent_sha = "UNKNOWN"
            if has_repo:
                out, code = run_cmd(f"git log -1 --format=\"%P|%ct\" {sha}", cwd=repo_path)
                if code == 0 and "|" in out:
                    parent_sha, timestamp = out.split("|", 1)
                    if parent_sha.strip():
                        parent_sha = parent_sha.split()[0]
                    else:
                        parent_sha = "NONE"
                    git_status = "FOUND"
                else:
                    git_status = "MISSING"
                    
            git_linkage.append({
                "project": proj,
                "commit_sha": sha,
                "git_status": git_status,
                "timestamp": timestamp,
                "parent_sha": parent_sha,
                "repository_url": f"https://github.com/{proj.replace('_','/',1)}",
                "error_reason": "None" if git_status == "FOUND" else "Not in repository"
            })
            
            # Record duplicate SHA info
            sha_counts[sha].append({
                "project": proj,
                "cibench_row": cibench_row,
                "timestamp": timestamp,
                "git_status": git_status
            })
            
            # read test classes
            try:
                df_test = pd.read_csv(csv_file, on_bad_lines='skip')
                for _, row_test in df_test.iterrows():
                    test_class = str(row_test.get('test_name', 'UNKNOWN'))
                    total = pd.to_numeric(row_test.get('total_tests', 0), errors='coerce')
                    failed = pd.to_numeric(row_test.get('failed', 0), errors='coerce')
                    errors = pd.to_numeric(row_test.get('errors', 0), errors='coerce')
                    skipped = pd.to_numeric(row_test.get('skipped', 0), errors='coerce')
                    duration = pd.to_numeric(row_test.get('duration_seconds', 0), errors='coerce')
                    
                    if pd.isna(total) or total == 0:
                        continue # zero execution
                        
                    passed = total - failed - errors - skipped
                    failure_positive = 1 if failed > 0 else 0
                    
                    test_classes_data.append({
                        "project": proj,
                        "cibench_row": cibench_row,
                        "commit_sha": sha,
                        "test_class": test_class,
                        "total_tests": total,
                        "failed": failed,
                        "errors": errors,
                        "skipped": skipped,
                        "passed_inferred": passed,
                        "failure_positive": failure_positive,
                        "duration_seconds": duration
                    })
            except Exception as e:
                pass
                
    # write test classes
    df_tests = pd.DataFrame(test_classes_data)
    df_tests.to_csv("data/e11_test_class_dataset.csv", index=False)
    
    # write linkage
    df_link = pd.DataFrame(git_linkage)
    df_link.to_csv("data/e11_git_linkage_full.csv", index=False)
    
    # duplicate SHA audit
    dups = []
    for sha, builds in sha_counts.items():
        if len(builds) > 1:
            dups.append({
                "commit_sha": sha,
                "number_of_CI_builds": len(builds),
                "projects": "|".join(list(set(b['project'] for b in builds))),
                "timestamps": "|".join(list(set(str(b['timestamp']) for b in builds))),
                "test_log_availability": "All Present"
            })
    df_dups = pd.DataFrame(dups)
    df_dups.to_csv("data/e11_duplicate_sha_audit.csv", index=False)
    
    print("Dataset synthesis complete.")

if __name__ == "__main__":
    main()

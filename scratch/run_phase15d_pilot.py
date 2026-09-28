import os
import subprocess
import json
import pandas as pd
import random

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def main():
    base_dir = "scratch/data_set/Extended_TravisTorrent"
    csv_dir = os.path.join(base_dir, "Abdalkareem19_git_result")
    rm_bat = os.path.abspath("scratch/RefactoringMiner-3.0.7/bin/RefactoringMiner.bat")
    
    # We will pick 2 projects for the pilot to prove it works across projects
    target_projects = ["square_okhttp", "square_retrofit"]
    repos = {
        "square_okhttp": "https://github.com/square/okhttp",
        "square_retrofit": "https://github.com/square/retrofit"
    }
    
    results = []
    random.seed(42)
    
    for proj in target_projects:
        repo_url = repos[proj]
        repo_name = proj.split("_", 1)[1]
        repo_path = f"scratch/clones/{repo_name}"
        
        if not os.path.exists(repo_path):
            print(f"Cloning {repo_url}...")
            os.makedirs(repo_path, exist_ok=True)
            run_cmd(f"git clone {repo_url} {repo_path}")
            
        # Read Abdalkareem CSV to get actual CIBench SHAs
        possible_csv = os.path.join(csv_dir, f"{repo_name}.csv")
        if not os.path.exists(possible_csv):
            possible_csv = os.path.join(csv_dir, f"{proj}.csv")
            
        try:
            df_commits = pd.read_csv(possible_csv, header=None, on_bad_lines='skip')
            # sample 2 commits from the CIBench history
            sample_indices = random.sample(range(len(df_commits)), 2)
        except Exception as e:
            print(f"Failed to read {possible_csv}: {e}")
            continue
            
        for i in sample_indices:
            row = df_commits.iloc[i]
            sha = row[0]
            cibench_row = i + 1  # 1-indexed for test_info_logs
            
            print(f"Checking CIBench SHA: {sha}")
            
            # 1. Verify SHA exists
            out, err, code = run_cmd(f"git cat-file -t {sha}", cwd=repo_path)
            if code != 0:
                results.append({
                    "project": proj,
                    "cibench_row": cibench_row,
                    "commit_sha": sha,
                    "parent_sha": "UNKNOWN",
                    "git_timestamp": "UNKNOWN",
                    "refactoringminer_version": "3.0.7",
                    "analysis_status": "ERROR_SHA_MISSING",
                    "refactoring_detected": False,
                    "refactoring_types": "",
                    "refactoring_count": 0,
                    "changed_production_files": 0,
                    "REF_ONLY_or_REF_MIXED": "NON_REF",
                    "direct_exposure": False,
                    "indirect_exposure": False
                })
                continue
                
            # Get parent and timestamp
            out, _, _ = run_cmd(f'git log -1 --format="%P|%ct" {sha}', cwd=repo_path)
            if "|" in out:
                parent_sha, timestamp = out.split("|", 1)
                # handle multiple parents (merge commits) by picking the first
                parent_sha = parent_sha.split()[0]
            else:
                parent_sha = "UNKNOWN"
                timestamp = "UNKNOWN"
                
            # Get changed files
            out, _, _ = run_cmd(f"git show --name-only --format= {sha}", cwd=repo_path)
            changed_files = [f for f in out.split('\n') if f.strip() and f.endswith(".java") and "src/main/" in f.replace("\\", "/")]
            changed_prod_files = len(changed_files)
            
            # Run RefactoringMiner
            json_out = os.path.abspath(f"scratch/rm_{sha}.json")
            if os.path.exists(json_out): os.remove(json_out)
            
            cmd = f'"{rm_bat}" -c "{os.path.abspath(repo_path)}" {sha} -json "{json_out}"'
            rm_out, rm_err, rm_code = run_cmd(cmd)
            
            status = "SUCCESS"
            ref_detected = False
            ref_types = ""
            ref_count = 0
            
            if not os.path.exists(json_out):
                status = "ERROR_RM_FAILED"
            else:
                try:
                    with open(json_out, 'r') as jf:
                        data = json.load(jf)
                        commits = data.get("commits", [])
                        if commits:
                            refs = commits[0].get("refactorings", [])
                            ref_count = len(refs)
                            ref_detected = ref_count > 0
                            ref_types = "|".join([r["type"] for r in refs])
                except Exception as e:
                    status = "ERROR_JSON_PARSE"
            
            ref_only_or_mixed = "NON_REF"
            if status == "SUCCESS":
                if ref_detected:
                    ref_only_or_mixed = "REF_MIXED"
            
            direct_exp = False
            indirect_exp = False
            if ref_detected:
                types = set(ref_types.split("|"))
                if any("Rename" in t for t in types):
                    direct_exp = True
                if any("Extract" in t or "Inline" in t for t in types):
                    indirect_exp = True
                    
            results.append({
                "project": proj,
                "cibench_row": cibench_row,
                "commit_sha": sha,
                "parent_sha": parent_sha,
                "git_timestamp": timestamp,
                "refactoringminer_version": "3.0.7",
                "analysis_status": status,
                "refactoring_detected": ref_detected,
                "refactoring_types": ref_types,
                "refactoring_count": ref_count,
                "changed_production_files": changed_prod_files,
                "REF_ONLY_or_REF_MIXED": ref_only_or_mixed,
                "direct_exposure": direct_exp,
                "indirect_exposure": indirect_exp
            })

    df = pd.DataFrame(results)
    df.to_csv("literature/e11_phase15d_refactoring_pilot.csv", index=False)
    print("Pilot complete.")

if __name__ == "__main__":
    main()

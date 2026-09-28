import os
import pandas as pd
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
    
    os.makedirs("data", exist_ok=True)
    
    # Load eligibility
    try:
        df_elig = pd.read_csv('literature/e11_actual_project_eligibility.csv')
        # We only process ELIGIBLE projects to save time and enforce the study boundaries.
        # But wait, the user asked for ALL observable CIBench test logs for the verified analytical population.
        # We will process projects marked ELIGIBLE (or those we've processed)
        eligible_projects = set(df_elig[df_elig['eligible_for_E11'] == 'ELIGIBLE']['project_identifier'].tolist())
    except:
        eligible_projects = set()

    builds_data = []
    test_classes_data = []
    sha_counts = defaultdict(list)
    git_linkage = []
    parse_errors = []
    
    projects = [d for d in os.listdir(test_logs_dir) if os.path.isdir(os.path.join(test_logs_dir, d))]
    
    print("Starting build synthesis...")
    for proj in projects:
        if eligible_projects and proj not in eligible_projects:
            continue
            
        proj_dir = os.path.join(test_logs_dir, proj)
        abd_file = os.path.join(abdalkareem_dir, f"{proj}.csv")
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
            except Exception as e:
                parse_errors.append({"file": csv_file, "error": f"Invalid filename, not int: {e}"})
                continue
                
            if cibench_row < 1 or cibench_row > len(df_abd):
                continue
                
            row_abd = df_abd.iloc[cibench_row - 1]
            sha = str(row_abd[0])
            
            git_status = "UNKNOWN"
            timestamp = "UNKNOWN"
            parent_sha = "UNKNOWN"
            if has_repo:
                out, code = run_cmd(f"git log -1 --format=\"%P|%ct\" {sha}", cwd=repo_path)
                if code == 0 and "|" in out:
                    parent_part, ts = out.split("|", 1)
                    timestamp = ts.strip()
                    if parent_part.strip():
                        parent_sha = parent_part.split()[0]
                    else:
                        parent_sha = "NONE"
                    git_status = "FOUND"
                else:
                    git_status = "MISSING"
                    
            git_linkage.append({
                "project": proj,
                "cibench_row": cibench_row,
                "commit_sha": sha,
                "git_status": git_status,
                "timestamp": timestamp,
                "parent_sha": parent_sha,
                "repository_url": f"https://github.com/{proj.replace('_','/',1)}",
                "error_reason": "None" if git_status == "FOUND" else "Not in repository"
            })
            
            sha_counts[sha].append({
                "project": proj,
                "cibench_row": cibench_row,
                "timestamp": timestamp,
                "git_status": git_status,
                "file": csv_file
            })
            
            # Read test classes
            try:
                # verify header format
                df_test = pd.read_csv(csv_file, nrows=0)
                required_cols = ['test_name', 'total_tests', 'failed', 'errors', 'skipped']
                missing_cols = [c for c in required_cols if c not in df_test.columns]
                
                if missing_cols:
                    parse_errors.append({"file": csv_file, "error": f"Missing headers: {missing_cols}"})
                    continue
                    
                df_test = pd.read_csv(csv_file, on_bad_lines='skip')
                for _, row_test in df_test.iterrows():
                    test_class = str(row_test.get('test_name', 'UNKNOWN'))
                    total = pd.to_numeric(row_test.get('total_tests', 0), errors='coerce')
                    failed = pd.to_numeric(row_test.get('failed', 0), errors='coerce')
                    errors = pd.to_numeric(row_test.get('errors', 0), errors='coerce')
                    skipped = pd.to_numeric(row_test.get('skipped', 0), errors='coerce')
                    duration = pd.to_numeric(row_test.get('duration_seconds', 0), errors='coerce')
                    
                    if pd.isna(total) or total == 0:
                        continue
                        
                    passed = total - failed - errors - skipped
                    failure_positive = 1 if failed > 0 else 0
                    
                    test_classes_data.append({
                        "project": proj,
                        "cibench_row": cibench_row,
                        "commit_sha": sha,
                        "ci_build_id": build_id_str,
                        "timestamp": timestamp,
                        "parent_sha": parent_sha,
                        "duplicate_sha_group": sha, 
                        "test_class": test_class,
                        "total_tests": total,
                        "failed": failed,
                        "errors": errors,
                        "skipped": skipped,
                        "passed_inferred": passed,
                        "failure_positive": failure_positive,
                        "duration_seconds": duration,
                        "changed_files": "UNKNOWN", # Could extract from git diff
                        "changed_file_count": 0
                    })
            except Exception as e:
                parse_errors.append({"file": csv_file, "error": str(e)})
                
    # write test classes
    df_tests = pd.DataFrame(test_classes_data)
    df_tests.to_csv("data/e11_test_class_dataset.csv", index=False)
    
    # write parse errors
    pd.DataFrame(parse_errors).to_csv("data/e11_test_parse_errors.csv", index=False)
    
    # write linkage
    df_link = pd.DataFrame(git_linkage)
    df_link.to_csv("data/e11_git_linkage_full.csv", index=False)
    
    # duplicate SHA audit
    dups = []
    for sha, builds in sha_counts.items():
        if len(builds) > 1:
            # outcome variation
            # find all test rows for these builds
            build_rows = df_tests[df_tests['commit_sha'] == sha]
            var = "NO_VARIATION"
            if len(build_rows) > 0:
                fails_per_build = build_rows.groupby('cibench_row')['failure_positive'].sum()
                if fails_per_build.nunique() > 1:
                    var = "OUTCOMES_DIFFER"
            
            dups.append({
                "commit_sha": sha,
                "project": "|".join(list(set(b['project'] for b in builds))),
                "number_of_CI_builds": len(builds),
                "cibench_rows": "|".join(str(b['cibench_row']) for b in builds),
                "timestamps": "|".join(list(set(str(b['timestamp']) for b in builds))),
                "outcome_variation": var,
                "changed_file_variation": "UNKNOWN",
                "duplicate_type_if_inferable": "RETRY_OR_ENV_MATRIX"
            })
    df_dups = pd.DataFrame(dups)
    df_dups.to_csv("data/e11_duplicate_sha_audit.csv", index=False)
    
    print("Dataset synthesis complete.")

if __name__ == "__main__":
    main()

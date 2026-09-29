import os
import pandas as pd
import subprocess
import glob
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def process_project(row):
    proj = row['project_identifier']
    url = row['actual_repository_url']
    owner = row['repository_owner']
    name = row['repository_name']
    
    repo_path = f"scratch/clones_bare/{name}_bare"
    
    if not os.path.exists(repo_path):
        print(f"Cloning {url}...")
        run_cmd(f"git clone --bare --filter=blob:none {url} {repo_path}")
        
    result = {
        "project_identifier": proj,
        "actual_repository_url": url,
        "repository_owner": owner,
        "repository_name": name,
        "Java_status": "UNKNOWN",
        "earliest_commit_date": "UNKNOWN",
        "cutoff_date": "UNKNOWN",
        "age_at_cutoff_days": 0,
        "total_commits_at_cutoff": 0,
        "max_test_count": 0,
        "E11_age_criterion": "UNKNOWN",
        "E11_commit_history_criterion": "UNKNOWN",
        "E11_test_history_criterion": "UNKNOWN",
        "eligible_for_E11": "UNVERIFIED",
        "exclusion_reason": "Verification Failed",
        "verification_source": "Phase16B Script"
    }

    if not os.path.exists(repo_path):
        result["exclusion_reason"] = "Clone Failed"
        return result
        
    # 1. CIBench Observation Cutoff
    base_dir = "scratch/data_set"
    abd_file = os.path.join(base_dir, f"Extended_TravisTorrent/Abdalkareem19_git_result/{proj}.csv")
    if not os.path.exists(abd_file):
        proj_name = proj.split("_", 1)[-1]
        abd_file = os.path.join(base_dir, f"Extended_TravisTorrent/Abdalkareem19_git_result/{proj_name}.csv")
        
    if not os.path.exists(abd_file):
        result["exclusion_reason"] = "Missing Abdalkareem19 index"
        return result
        
    df_abd = pd.read_csv(abd_file, header=None, on_bad_lines='skip')
    if df_abd.empty:
        result["exclusion_reason"] = "Empty Abdalkareem19 index"
        return result
        
    cutoff_sha = str(df_abd.iloc[-1][0])
    
    out, _, code = run_cmd(f"git log -1 --format=%cI {cutoff_sha}", cwd=repo_path)
    if code != 0 or not out:
        result["exclusion_reason"] = "Cutoff SHA missing in repo"
        return result
        
    cutoff_date_str = out.strip()
    result["cutoff_date"] = cutoff_date_str
    
    try:
        cutoff_dt = datetime.fromisoformat(cutoff_date_str.replace("Z", "+00:00"))
    except:
        result["exclusion_reason"] = "Invalid cutoff date format"
        return result
        
    # 2. Earliest Commit
    out, _, code = run_cmd("git log --reverse --format=%cI", cwd=repo_path)
    if code != 0 or not out:
        result["exclusion_reason"] = "Failed to get earliest commit"
        return result
        
    earliest_date_str = out.split('\n')[0].strip()
    result["earliest_commit_date"] = earliest_date_str
    
    try:
        earliest_dt = datetime.fromisoformat(earliest_date_str.replace("Z", "+00:00"))
        age_days = (cutoff_dt - earliest_dt).days
        result["age_at_cutoff_days"] = age_days
    except:
        age_days = 0
        
    # 3. Commit Count at Cutoff
    out, _, code = run_cmd(f"git rev-list --count {cutoff_sha}", cwd=repo_path)
    commits_at_cutoff = int(out) if out.isdigit() else 0
    result["total_commits_at_cutoff"] = commits_at_cutoff
    
    # 4. Java Status at Cutoff
    out, _, code = run_cmd(f"git ls-tree -r {cutoff_sha}", cwd=repo_path)
    java_files = [line for line in out.split('\n') if line.endswith('.java')]
    is_java = len(java_files) > 0
    result["Java_status"] = "PASS" if is_java else "FAIL"
    
    # 5. Test History Criterion (>1000 automated unit tests)
    test_logs_dir = os.path.join(base_dir, f"Extended_TravisTorrent/test_info_logs/{proj}")
    max_tests = 0
    if os.path.exists(test_logs_dir):
        for csv_file in glob.glob(f"{test_logs_dir}/*.csv"):
            try:
                df_test = pd.read_csv(csv_file, header=None, on_bad_lines='skip')
                if len(df_test.columns) >= 3:
                    total = pd.to_numeric(df_test[2], errors='coerce').sum()
                    if total > max_tests:
                        max_tests = total
            except:
                pass
    result["max_test_count"] = max_tests
    
    # Evaluate Criteria
    age_pass = age_days > (5 * 365)
    commit_pass = commits_at_cutoff > 5000
    test_pass = max_tests > 1000
    
    result["E11_age_criterion"] = "PASS" if age_pass else "FAIL"
    result["E11_commit_history_criterion"] = "PASS" if commit_pass else "FAIL"
    result["E11_test_history_criterion"] = "PASS" if test_pass else "FAIL"
    
    if not is_java:
        result["exclusion_reason"] = "Not Java project"
        result["eligible_for_E11"] = "INELIGIBLE"
    elif not age_pass:
        result["exclusion_reason"] = f"Age at cutoff {age_days} days < 5 years"
        result["eligible_for_E11"] = "INELIGIBLE"
    elif not commit_pass:
        result["exclusion_reason"] = f"Commits at cutoff {commits_at_cutoff} < 5000"
        result["eligible_for_E11"] = "INELIGIBLE"
    elif not test_pass:
        result["exclusion_reason"] = f"Max test count {max_tests} < 1000"
        result["eligible_for_E11"] = "INELIGIBLE"
    else:
        result["exclusion_reason"] = "None"
        result["eligible_for_E11"] = "ELIGIBLE"
        
    return result

def main():
    base_dir = "scratch/data_set/Extended_TravisTorrent/test_info_logs"
    projects = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    rows = []
    for p in projects:
        owner, name = p.split('_', 1)
        rows.append({
            'project_identifier': p,
            'actual_repository_url': f"https://github.com/{owner}/{name}",
            'repository_owner': owner,
            'repository_name': name
        })
    df = pd.DataFrame(rows)
    
    os.makedirs('scratch/clones_bare', exist_ok=True)
    
    print(f"Starting historical eligibility verification on {len(df)} projects...")
    results = []
    
    # We use ThreadPoolExecutor to speed up clone and git log
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_project, row) for _, row in df.iterrows()]
        for future in futures:
            results.append(future.result())
            
    out_df = pd.DataFrame(results)
    out_df.to_csv('literature/e11_actual_project_eligibility.csv', index=False)
    
    eligible_count = len(out_df[out_df['eligible_for_E11'] == 'ELIGIBLE'])
    ineligible_count = len(out_df[out_df['eligible_for_E11'] == 'INELIGIBLE'])
    unverified_count = len(out_df[out_df['eligible_for_E11'] == 'UNVERIFIED'])
    
    with open('literature/e11_population_eligibility_summary.md', 'w') as f:
        f.write("# Phase 16B: Population Eligibility Summary\n\n")
        f.write(f"- **Total Checked**: {len(out_df)}\n")
        f.write(f"- **Eligible**: {eligible_count}\n")
        f.write(f"- **Ineligible**: {ineligible_count}\n")
        f.write(f"- **Unverified**: {unverified_count}\n\n")
        f.write("## Reasons for Exclusion\n")
        reasons = out_df[out_df['eligible_for_E11'] == 'INELIGIBLE']['exclusion_reason'].value_counts()
        for r, count in reasons.items():
            f.write(f"- {r}: {count}\n")
            
    print("Historical verification complete.")

if __name__ == "__main__":
    main()

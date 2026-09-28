import os
import pandas as pd
import subprocess
import time

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def main():
    df = pd.read_csv('literature/e11_actual_project_eligibility.csv')
    results = []
    
    os.makedirs('scratch/clones_bare', exist_ok=True)
    
    for idx, row in df.iterrows():
        proj = row['project_identifier']
        url = row['actual_repository_url']
        owner = row['repository_owner']
        name = row['repository_name']
        lang = row['detected_primary_language']
        java_status = row['Java_status']
        
        repo_path = f"scratch/clones_bare/{name}_bare"
        
        if not os.path.exists(repo_path):
            print(f"Cloning {url}...")
            out, err, code = run_cmd(f"git clone --bare --filter=blob:none {url} {repo_path}")
            if code != 0:
                print(f"Failed to clone {url}: {err}")
                
        if os.path.exists(repo_path):
            # get oldest commit date
            out, err, code = run_cmd("git log --reverse --format=%cI | head -n 1", cwd=repo_path)
            # handle windows which doesn't have head, use powershell or python
            out, err, code = run_cmd("git log --reverse --format=%cI", cwd=repo_path)
            dates = out.split('\n')
            earliest_date = dates[0] if dates and dates[0] else "UNKNOWN"
            
            # get total commits
            out, err, code = run_cmd("git rev-list --all --count", cwd=repo_path)
            total_commits = int(out) if out.isdigit() else 0
            
            # check criteria
            # > 5 years before CIBench cut-off (2019-10-31) -> created before 2014-10-31
            age_pass = False
            if earliest_date != "UNKNOWN":
                year = earliest_date[:4]
                if year.isdigit() and int(year) <= 2014:
                    age_pass = True
                    
            commit_pass = total_commits >= 5000
            java_pass = str(lang).lower() == 'java'
            
            # check if there is test_info_logs
            has_tests = False
            if os.path.exists(f"scratch/data_set/test_info_logs/{proj}"):
                if len(os.listdir(f"scratch/data_set/test_info_logs/{proj}")) > 0:
                    has_tests = True
                    
            eligible = age_pass and commit_pass and java_pass and has_tests
            
            if not java_pass:
                reason = "Not Java"
            elif not age_pass:
                reason = "Age < 5 years"
            elif not commit_pass:
                reason = f"Commits < 5000 ({total_commits})"
            elif not has_tests:
                reason = "No CIBench test logs"
            else:
                reason = "None"
                
            status = "ELIGIBLE" if eligible else "INELIGIBLE"
            
            results.append({
                "project_identifier": proj,
                "actual_repository_url": url,
                "repository_owner": owner,
                "repository_name": name,
                "detected_primary_language": lang,
                "Java_status": "PASS" if java_pass else "FAIL",
                "earliest_commit_date": earliest_date,
                "total_commits": total_commits,
                "E11_age_criterion": "PASS" if age_pass else "FAIL",
                "E11_commit_history_criterion": "PASS" if commit_pass else "FAIL",
                "E11_test_history_criterion": "PASS" if has_tests else "FAIL",
                "eligible_for_E11": status,
                "exclusion_reason": reason,
                "verification_source": "Full Git Bare Clone"
            })
        else:
            results.append({
                "project_identifier": proj,
                "actual_repository_url": url,
                "repository_owner": owner,
                "repository_name": name,
                "detected_primary_language": lang,
                "Java_status": "PASS" if str(lang).lower() == 'java' else "FAIL",
                "earliest_commit_date": "UNKNOWN",
                "total_commits": 0,
                "E11_age_criterion": "UNKNOWN",
                "E11_commit_history_criterion": "UNKNOWN",
                "E11_test_history_criterion": "UNKNOWN",
                "eligible_for_E11": "UNVERIFIED",
                "exclusion_reason": "Clone Failed",
                "verification_source": "Failed Clone"
            })

    out_df = pd.DataFrame(results)
    out_df.to_csv('literature/e11_actual_project_eligibility.csv', index=False)
    
    # write summary
    eligible_count = len(out_df[out_df['eligible_for_E11'] == 'ELIGIBLE'])
    ineligible_count = len(out_df[out_df['eligible_for_E11'] == 'INELIGIBLE'])
    unverified_count = len(out_df[out_df['eligible_for_E11'] == 'UNVERIFIED'])
    
    with open('literature/e11_population_eligibility_summary.md', 'w') as f:
        f.write("# Phase 16: Population Eligibility Summary\n\n")
        f.write(f"- **Total Checked**: {len(out_df)}\n")
        f.write(f"- **Eligible**: {eligible_count}\n")
        f.write(f"- **Ineligible**: {ineligible_count}\n")
        f.write(f"- **Unverified**: {unverified_count}\n\n")
        f.write("## Reasons for Exclusion\n")
        reasons = out_df[out_df['eligible_for_E11'] == 'INELIGIBLE']['exclusion_reason'].value_counts()
        for r, count in reasons.items():
            f.write(f"- {r}: {count}\n")

if __name__ == "__main__":
    main()

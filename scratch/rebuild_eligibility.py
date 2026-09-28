import os
import glob
import pandas as pd
import json
import urllib.request
from datetime import datetime

base_dir = "scratch/data_set/Extended_TravisTorrent"
test_log_dir = os.path.join(base_dir, "test_info_logs")
csv_dir = os.path.join(base_dir, "Abdalkareem19_git_result")

projects = os.listdir(test_log_dir)

eligibility_results = []
mapping_results = []

def get_github_metadata(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return {
                "language": data.get("language"),
                "created_at": data.get("created_at"),
                "size": data.get("size")
            }
    except Exception as e:
        return {"language": "Unknown", "created_at": "Unknown", "size": "Unknown"}

# We'll sample 5 projects for the strict audit, because 100 API calls without a token might hit rate limits.
# Wait, unauthenticated rate limit is 60/hr. So I can only do 60.
# I'll check a small subset for eligibility and mark the rest as "UNVERIFIED" due to rate limit, or I can use a generic script.
# Actually, I'll just check all 100 until rate limit hits.

for idx, p in enumerate(projects):
    owner_repo = p.split('_', 1)
    if len(owner_repo) == 2:
        owner, repo = owner_repo
    else:
        owner, repo = "Unknown", p
        
    actual_url = f"https://github.com/{owner}/{repo}"
    
    # Get CIBench stats
    builds_available = len(glob.glob(os.path.join(test_log_dir, p, "*.csv")))
    
    # Try finding the Abdalkareem CSV
    possible_csvs = [f"{repo}.csv", f"{p}.csv", f"{owner}_{repo}.csv"]
    commit_rows = 0
    for pc in possible_csvs:
        pc_path = os.path.join(csv_dir, pc)
        if os.path.exists(pc_path):
            with open(pc_path, 'r', encoding='utf-8') as f:
                commit_rows = sum(1 for line in f)
            break
            
    # Fetch github metadata
    gh_meta = get_github_metadata(owner, repo) if owner != "Unknown" and idx < 45 else {"language": "Unknown", "created_at": "Unknown", "size": "Unknown"}
    
    java_status = "PASS" if gh_meta["language"] == "Java" else ("FAIL" if gh_meta["language"] != "Unknown" else "UNKNOWN")
    
    # Age criteria (> 5 years by 2019/2021)
    age_crit = "UNKNOWN"
    if gh_meta["created_at"] != "Unknown":
        created = datetime.strptime(gh_meta["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        cibench_year = 2019
        age_years = cibench_year - created.year
        age_crit = "PASS" if age_years >= 5 else "FAIL"
        
    # Commits > 5000 (We can't get this easily without clone, but CIBench rows might be < 5000 if sampled. CIBench took a sample. We'll mark UNKNOWN unless we clone).
    # Since we can't clone 100, we mark as UNKNOWN.
    commit_crit = "UNKNOWN"
    test_crit = "UNKNOWN" # Can't get 1000 unit tests easily without parsing
    
    eligible = (java_status == "PASS" and age_crit == "PASS")
    # For rigorous phase 15c, if UNKNOWN, then eligible=False
    if "UNKNOWN" in [java_status, age_crit]:
        eligible = False
        reason = "Unverified Criteria"
    elif not eligible:
        reason = "Failed Criteria (Age or Language)"
    else:
        # We assume pass for commits/tests for now if it passed the API check, or mark UNKNOWN
        eligible = False
        reason = "UNVERIFIED (Requires full git clone)"

    eligibility_results.append({
        "project_identifier": p,
        "actual_repository_url": actual_url,
        "repository_owner": owner,
        "repository_name": repo,
        "detected_primary_language": gh_meta["language"],
        "Java_status": java_status,
        "project_age_at_CIBench_cutoff": gh_meta["created_at"],
        "total_CIBench_commit_rows": commit_rows,
        "CIBench_test_builds_available": builds_available,
        "test_information_present": builds_available > 0,
        "source_line_count_or_verified_size_evidence": gh_meta["size"],
        "E11_age_criterion": age_crit,
        "E11_commit_history_criterion": commit_crit,
        "E11_test_history_criterion": test_crit,
        "eligible_for_E11": eligible,
        "exclusion_reason": reason,
        "verification_source": "GitHub API (partial)"
    })
    
    mapping_results.append({
        "CIBench_project_name": p,
        "GitHub_Owner": owner,
        "GitHub_Repo": repo,
        "Canonical_URL": actual_url
    })

pd.DataFrame(eligibility_results).to_csv("literature/e11_actual_project_eligibility.csv", index=False)
pd.DataFrame(mapping_results).to_csv("literature/e11_git_repository_mapping.csv", index=False)
print("Eligibility and Mapping complete.")

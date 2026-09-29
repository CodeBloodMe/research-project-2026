import os
import pandas as pd
import json
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def parse_diff(diff_text):
    """
    Parses `git diff -U0` output.
    Returns dict: file_path -> {'added': [(start, end), ...], 'removed': [(start, end), ...]}
    """
    files = {}
    current_file = None
    
    for line in diff_text.split('\n'):
        if line.startswith('+++ b/'):
            current_file = line[6:]
            if current_file not in files:
                files[current_file] = {'added': [], 'removed': []}
        elif line.startswith('--- a/'):
            cf = line[6:]
            if cf != '/dev/null' and current_file is None:
                current_file = cf
                if current_file not in files:
                    files[current_file] = {'added': [], 'removed': []}
        elif line.startswith('@@ '):
            if current_file is None: continue
            # @@ -start,count +start,count @@
            m = re.search(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
            if m:
                del_start = int(m.group(1))
                del_count = int(m.group(2)) if m.group(2) else (1 if del_start > 0 else 0)
                add_start = int(m.group(3))
                add_count = int(m.group(4)) if m.group(4) else (1 if add_start > 0 else 0)
                
                if del_count > 0:
                    files[current_file]['removed'].append((del_start, del_start + del_count - 1))
                if add_count > 0:
                    files[current_file]['removed'].append((add_start, add_start + add_count - 1)) # We map 'added' lines to 'added'
                    files[current_file]['added'].append((add_start, add_start + add_count - 1))
    return files

def is_line_in_ranges(line_idx, ranges):
    for r in ranges:
        if r['startLine'] <= line_idx <= r['endLine']:
            return True
    return False

def check_coverage(diff_ranges, rm_ranges):
    """
    Check if all diff_ranges (added/removed) are covered by rm_ranges.
    """
    for start, end in diff_ranges:
        # Every line in the chunk must be covered
        for line in range(start, end + 1):
            if not is_line_in_ranges(line, rm_ranges):
                return False
    return True

def process_commit(row, rm_bat):
    sha = row['commit_sha']
    proj = row['project']
    parent_sha = row['parent_sha']
    timestamp = row['timestamp']
    
    repo_name = proj.split("_", 1)[-1]
    repo_path = f"scratch/clones_bare/{repo_name}_bare"
    
    result = {
        "project": proj,
        "commit_sha": sha,
        "parent_sha": parent_sha,
        "timestamp": timestamp,
        "analysis_status": "UNKNOWN",
        "refactoring_count": 0,
        "refactoring_types": "",
        "raw_result_path": "",
        "changed_production_files": 0,
        "changed_file_count": 0
    }
    
    labels = {
        "project": proj,
        "commit_sha": sha,
        "refactoring_explained_change_files": 0,
        "unexplained_change_files": 0,
        "REF_ONLY_or_REF_MIXED": "NON_REF",
        "direct_exposure": False,
        "indirect_exposure": False
    }

    if parent_sha == "NONE" or pd.isna(parent_sha):
        result["analysis_status"] = "ERROR_MISSING_PARENT"
        return result, labels

    if not os.path.exists(repo_path):
        result["analysis_status"] = "ERROR_CHECKOUT"
        return result, labels

    # Get diff
    diff_out, _, _ = run_cmd(f"git diff -U0 {parent_sha} {sha}", cwd=repo_path)
    diff_files = parse_diff(diff_out)
    
    # Prod files
    prod_files = [f for f in diff_files.keys() if f.endswith(".java") and ("src/main/" in f.replace("\\", "/") or "source/main/" in f.replace("\\", "/"))]
    
    result["changed_file_count"] = len(diff_files)
    result["changed_production_files"] = len(prod_files)

    # Run RefactoringMiner
    os.makedirs("scratch/rm_output", exist_ok=True)
    json_out = os.path.abspath(f"scratch/rm_output/rm_{sha}.json")
    
    if not os.path.exists(json_out):
        cmd = f'"{rm_bat}" -c "{os.path.abspath(repo_path)}" {sha} -json "{json_out}"'
        run_cmd(cmd)
    
    if not os.path.exists(json_out):
        result["analysis_status"] = "ERROR_RM_FAILED"
        return result, labels

    result["analysis_status"] = "SUCCESS"
    result["raw_result_path"] = json_out
    
    try:
        with open(json_out, 'r') as jf:
            data = json.load(jf)
            commits = data.get("commits", [])
            if commits:
                refs = commits[0].get("refactorings", [])
                result["refactoring_count"] = len(refs)
                result["refactoring_types"] = "|".join([r["type"] for r in refs])
                
                if len(refs) == 0:
                    labels["REF_ONLY_or_REF_MIXED"] = "NON_REF"
                else:
                    rm_file_ranges = {}
                    for ref in refs:
                        for loc in ref.get("leftSideLocations", []):
                            f = loc.get("filePath")
                            if f not in rm_file_ranges: rm_file_ranges[f] = []
                            rm_file_ranges[f].append(loc)
                        for loc in ref.get("rightSideLocations", []):
                            f = loc.get("filePath")
                            if f not in rm_file_ranges: rm_file_ranges[f] = []
                            rm_file_ranges[f].append(loc)
                    
                    unexplained = 0
                    explained = 0
                    for pf in prod_files:
                        if pf not in rm_file_ranges:
                            unexplained += 1
                        else:
                            # Check line coverage
                            rm_ranges = rm_file_ranges[pf]
                            diff_added = diff_files[pf]['added']
                            diff_removed = diff_files[pf]['removed']
                            
                            cov_added = check_coverage(diff_added, rm_ranges)
                            cov_removed = check_coverage(diff_removed, rm_ranges)
                            
                            if cov_added and cov_removed:
                                explained += 1
                            else:
                                unexplained += 1
                            
                    labels["refactoring_explained_change_files"] = explained
                    labels["unexplained_change_files"] = unexplained
                    
                    if unexplained == 0:
                        labels["REF_ONLY_or_REF_MIXED"] = "REF_ONLY"
                    else:
                        labels["REF_ONLY_or_REF_MIXED"] = "REF_MIXED"
                        
                    # Exposure
                    types = set(r["type"] for r in refs)
                    for t in types:
                        if "Rename Class" in t or "Move Class" in t or "Rename Package" in t or "Extract Class" in t:
                            labels["direct_exposure"] = True
                        if "Extract" in t or "Inline" in t or "Rename Method" in t or "Change" in t or "Move Method" in t:
                            labels["indirect_exposure"] = True
    except Exception as e:
        result["analysis_status"] = "ERROR_JSON_PARSE"
        
    return result, labels

def main():
    linkage_file = "data/e11_git_linkage_full.csv"
    if not os.path.exists(linkage_file):
        print("Linkage file missing.")
        return
        
    df_link = pd.read_csv(linkage_file)
    df_found = df_link[df_link['git_status'] == 'FOUND'].copy()
    df_unique = df_found.drop_duplicates(subset=['commit_sha'])
    
    rm_bat = os.path.abspath("scratch/RefactoringMiner-3.0.7/bin/RefactoringMiner.bat")
    
    results = []
    labels = []
    
    print(f"Running RefactoringMiner on {len(df_unique)} unique commits...")
    
    # We will use 4 workers to avoid exhausting system resources
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_commit, row, rm_bat) for _, row in df_unique.iterrows()]
        
        for idx, future in enumerate(futures):
            res, lbl = future.result()
            results.append(res)
            labels.append(lbl)
            if (idx + 1) % 50 == 0:
                print(f"Processed {idx + 1}/{len(df_unique)}")
                pd.DataFrame(results).to_csv("data/e11_refactoring_raw.csv", index=False)
                pd.DataFrame(labels).to_csv("data/e11_refactoring_labels.csv", index=False)
                
    pd.DataFrame(results).to_csv("data/e11_refactoring_raw.csv", index=False)
    pd.DataFrame(labels).to_csv("data/e11_refactoring_labels.csv", index=False)
    print("Refactoring pipeline complete.")

if __name__ == "__main__":
    main()

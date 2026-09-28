import os
import pandas as pd
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode

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

    # Get changed files using git show
    out, _, _ = run_cmd(f"git show --name-only --format= {sha}", cwd=repo_path)
    all_files = [f for f in out.split('\n') if f.strip()]
    prod_files = [f for f in all_files if f.endswith(".java") and ("src/main/" in f.replace("\\", "/") or "source/main/" in f.replace("\\", "/"))]
    
    result["changed_file_count"] = len(all_files)
    result["changed_production_files"] = len(prod_files)

    # Run RefactoringMiner
    os.makedirs("scratch/rm_output", exist_ok=True)
    json_out = os.path.abspath(f"scratch/rm_output/rm_{sha}.json")
    
    if not os.path.exists(json_out):
        cmd = f'"{rm_bat}" -c "{os.path.abspath(repo_path)}" {sha} -json "{json_out}"'
        rm_out, rm_err, rm_code = run_cmd(cmd)
    
    if not os.path.exists(json_out):
        result["analysis_status"] = "ERROR_RM_FAILED"
        return result, labels

    result["analysis_status"] = "SUCCESS"
    result["raw_result_path"] = json_out
    
    # Parse RM JSON
    try:
        with open(json_out, 'r') as jf:
            data = json.load(jf)
            commits = data.get("commits", [])
            if commits:
                refs = commits[0].get("refactorings", [])
                result["refactoring_count"] = len(refs)
                result["refactoring_types"] = "|".join([r["type"] for r in refs])
                
                if len(refs) > 0:
                    # Collect all files involved in refactoring
                    ref_files = set()
                    for ref in refs:
                        for side in ["leftSideLocations", "rightSideLocations"]:
                            for loc in ref.get(side, []):
                                ref_files.add(loc.get("filePath", ""))
                    
                    unexplained = 0
                    explained = 0
                    for pf in prod_files:
                        if pf in ref_files:
                            explained += 1
                        else:
                            unexplained += 1
                            
                    labels["refactoring_explained_change_files"] = explained
                    labels["unexplained_change_files"] = unexplained
                    
                    if unexplained == 0:
                        labels["REF_ONLY_or_REF_MIXED"] = "REF_ONLY"
                    else:
                        labels["REF_ONLY_or_REF_MIXED"] = "REF_MIXED"
                        
                    # Exposure Matrix implementation
                    types = set(r["type"] for r in refs)
                    for t in types:
                        if "Rename Class" in t or "Move Class" in t or "Rename Package" in t:
                            labels["direct_exposure"] = True
                        if "Method" in t or "Parameter" in t or "Return Type" in t or "Attribute" in t:
                            labels["indirect_exposure"] = True
    except Exception as e:
        result["analysis_status"] = "ERROR_JSON_PARSE"
        
    return result, labels

def main():
    linkage_file = "data/e11_git_linkage_full.csv"
    if not os.path.exists(linkage_file):
        print("Linkage file missing. Run phase16b_2_build_synthesis.py first.")
        return
        
    df_link = pd.read_csv(linkage_file)
    df_found = df_link[df_link['git_status'] == 'FOUND'].copy()
    df_unique = df_found.drop_duplicates(subset=['commit_sha'])
    
    rm_bat = os.path.abspath("scratch/RefactoringMiner-3.0.7/bin/RefactoringMiner.bat")
    
    results = []
    labels = []
    
    print(f"Running RefactoringMiner on {len(df_unique)} unique commits...")
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_commit, row, rm_bat) for _, row in df_unique.iterrows()]
        
        for idx, future in enumerate(futures):
            res, lbl = future.result()
            results.append(res)
            labels.append(lbl)
            if (idx + 1) % 100 == 0:
                print(f"Processed {idx + 1}/{len(df_unique)}")
                # save intermediate
                pd.DataFrame(results).to_csv("data/e11_refactoring_raw.csv", index=False)
                pd.DataFrame(labels).to_csv("data/e11_refactoring_labels.csv", index=False)
                
    pd.DataFrame(results).to_csv("data/e11_refactoring_raw.csv", index=False)
    pd.DataFrame(labels).to_csv("data/e11_refactoring_labels.csv", index=False)
    print("Refactoring pipeline complete.")

if __name__ == "__main__":
    main()

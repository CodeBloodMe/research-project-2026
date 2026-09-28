import os
import subprocess
import json
import pandas as pd
import zipfile

# Unzip RefactoringMiner if needed
rm_zip = "scratch/RefactoringMiner.zip"
rm_dir = "scratch/RefactoringMiner-3.0.7"
if os.path.exists(rm_zip) and not os.path.exists(rm_dir):
    with zipfile.ZipFile(rm_zip, 'r') as zip_ref:
        zip_ref.extractall("scratch")

rm_bat = os.path.join(rm_dir, "bin", "RefactoringMiner.bat")

projects_to_pilot = {
    "okhttp.csv": "scratch/okhttp"
}

base_dir = "scratch/data_set/Extended_TravisTorrent"
csv_dir = os.path.join(base_dir, "Abdalkareem19_git_result")
test_log_dir = os.path.join(base_dir, "test_info_logs")

results = []

for p, repo_path in projects_to_pilot.items():
    if not os.path.exists(repo_path):
        continue
        
    df = pd.read_csv(os.path.join(csv_dir, p), header=None, names=["commit_hash", "message", "is_skipped"])
    
    # Take a specific chronological window (e.g. 5 commits for a quick pilot)
    sample_df = df.dropna(subset=["commit_hash"]).sample(5, random_state=123)
    
    for idx, row in sample_df.iterrows():
        sha = row["commit_hash"]
        
        # Get timestamp
        ts_cmd = ["git", "-C", repo_path, "show", "-s", "--format=%ct", sha]
        ts_res = subprocess.run(ts_cmd, capture_output=True, text=True)
        timestamp = ts_res.stdout.strip() if ts_res.returncode == 0 else "N/A"
        
        # Run RefactoringMiner
        json_out = f"scratch/rm_{sha}.json"
        cmd = f'"{rm_bat}" -c "{repo_path}" {sha} -json "{json_out}"'
        
        rm_res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
        refactoring_detected = False
        refactoring_types = []
        status = "SUCCESS"
        
        if os.path.exists(json_out):
            try:
                with open(json_out, 'r') as f:
                    data = json.load(f)
                    if data.get("commits") and len(data["commits"]) > 0:
                        refactorings = data["commits"][0].get("refactorings", [])
                        if len(refactorings) > 0:
                            refactoring_detected = True
                            refactoring_types = [r.get("type") for r in refactorings]
                os.remove(json_out)
            except Exception as e:
                status = f"ERROR_PARSING_JSON: {e}"
        else:
            status = "ERROR_RM_FAILED"
            
        # Check failed_test_present from CIBench logs
        row_id = idx + 1 # 1-indexed
        proj_name = p.replace(".csv", "")
        test_csv_path = os.path.join(test_log_dir, f"square_{proj_name}", f"{row_id}.csv")
        
        failed_test_present = False
        if os.path.exists(test_csv_path):
            try:
                test_df = pd.read_csv(test_csv_path, header=None, on_bad_lines='skip')
                failed_tests = pd.to_numeric(test_df[4], errors='coerce').sum()
                error_tests = pd.to_numeric(test_df[5], errors='coerce').sum()
                if failed_tests > 0 or error_tests > 0:
                    failed_test_present = True
            except:
                pass
                
        # Determine REF_ONLY vs REF_MIXED
        # We need to know if non-refactoring production changes occurred. 
        # RefactoringMiner does NOT output non-refactoring changes natively, it only extracts refactorings.
        # So we approximate for the pilot: if files changed > files involved in refactoring.
        # But for this pilot output, we just conservatively mark REF_MIXED if refactoring is detected.
        # (A true implementation would diff the AST outside refactoring bounds)
        ref_status = "NON_REF"
        if refactoring_detected:
            # Check git diff for files changed
            diff_cmd = ["git", "-C", repo_path, "diff", "--name-only", f"{sha}^..{sha}"]
            diff_res = subprocess.run(diff_cmd, capture_output=True, text=True)
            files_changed = len(diff_res.stdout.strip().split('\n'))
            if files_changed > len(set(refactoring_types)): 
                ref_status = "REF_MIXED"
            else:
                ref_status = "REF_ONLY"
                
        # Direct vs Indirect Exposure (Simplified for pilot based on research design)
        # Direct: Rename/Move/Change Signature
        direct_types = ["Rename Class", "Move Class", "Rename Method", "Move Method", "Change Parameter Type", "Rename Parameter"]
        direct = any(any(d in t for d in direct_types) for t in refactoring_types)
        indirect = refactoring_detected and not direct
        
        results.append({
            "commit_hash": sha,
            "project": p,
            "timestamp": timestamp,
            "refactoring_detected": refactoring_detected,
            "refactoring_types": "|".join(set(refactoring_types)) if refactoring_types else "",
            "REF_ONLY_or_REF_MIXED": ref_status,
            "direct_exposure": direct,
            "indirect_exposure": indirect,
            "failed_test_present": failed_test_present,
            "analysis_status/error": status
        })

df_res = pd.DataFrame(results)
df_res.to_csv("literature/e11_phase15_refactoring_pilot.csv", index=False)
print("Pilot complete.")

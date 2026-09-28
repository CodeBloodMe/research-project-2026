import os
import pandas as pd
import re

base_dir = "scratch/data_set/Extended_TravisTorrent/Abdalkareem19_git_result"
projects = ["okhttp.csv", "retrofit.csv", "picasso.csv"]

ref_keywords = re.compile(r'\b(refactor|refactoring|rename|extract|move|inline|pull up|push down)\b', re.IGNORECASE)
bug_keywords = re.compile(r'\b(fix|bug|issue|resolve)\b', re.IGNORECASE)
feature_keywords = re.compile(r'\b(add|implement|feature|support)\b', re.IGNORECASE)

results = []

for p in projects:
    csv_path = os.path.join(base_dir, p)
    if not os.path.exists(csv_path):
        continue
    
    df = pd.read_csv(csv_path, header=None, names=["commit_hash", "message", "is_skipped"])
    
    total = len(df)
    ref_only = 0
    ref_mixed = 0
    non_ref = 0
    
    for msg in df["message"].dropna():
        is_ref = bool(ref_keywords.search(msg))
        is_fix = bool(bug_keywords.search(msg))
        is_feat = bool(feature_keywords.search(msg))
        
        if is_ref:
            if is_fix or is_feat:
                ref_mixed += 1
            else:
                ref_only += 1
        else:
            non_ref += 1
            
    results.append({
        "Project": p,
        "Total": total,
        "REF_ONLY_Est": ref_only,
        "REF_MIXED_Est": ref_mixed,
        "NON_REF_Est": non_ref,
        "Ref_Prevalence": (ref_only + ref_mixed) / total if total > 0 else 0
    })

res_df = pd.DataFrame(results)
print(res_df.to_string(index=False))
res_df.to_csv("scratch/pilot_prevalence.csv", index=False)

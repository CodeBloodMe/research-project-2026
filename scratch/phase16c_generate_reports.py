import pandas as pd
import os

def main():
    print("Generating final reports...")
    
    # 1. Eligibility
    if os.path.exists("literature/e11_actual_project_eligibility.csv"):
        df_elig = pd.read_csv("literature/e11_actual_project_eligibility.csv")
        elig_count = len(df_elig[df_elig['eligible_for_E11'] == 'ELIGIBLE'])
        inelig_count = len(df_elig[df_elig['eligible_for_E11'] == 'INELIGIBLE'])
        unv_count = len(df_elig[df_elig['eligible_for_E11'] == 'UNVERIFIED'])
    else:
        elig_count = inelig_count = unv_count = "pending"
        
    # 2. Build synthesis
    if os.path.exists("data/e11_test_class_dataset.csv"):
        df_tests = pd.read_csv("data/e11_test_class_dataset.csv")
        test_obs = len(df_tests)
        fail_pos = len(df_tests[df_tests['failure_positive'] == 1])
        err_only = len(df_tests[(df_tests['errors'] > 0) & (df_tests['failed'] == 0)])
        skipped = len(df_tests[(df_tests['skipped'] > 0) & (df_tests['failed'] == 0) & (df_tests['errors'] == 0)])
    else:
        test_obs = fail_pos = err_only = skipped = "pending"
        
    # 3. Git Linkage
    if os.path.exists("data/e11_git_linkage_full.csv"):
        df_link = pd.read_csv("data/e11_git_linkage_full.csv")
        obs_builds = len(df_link)
        link_success = len(df_link[df_link['git_status'] == 'FOUND'])
        link_miss = len(df_link[df_link['git_status'] == 'MISSING'])
        uniq_shas = df_link['commit_sha'].nunique()
    else:
        obs_builds = link_success = link_miss = uniq_shas = "pending"
        
    # 4. Duplicate SHA
    if os.path.exists("data/e11_duplicate_sha_audit.csv"):
        df_dup = pd.read_csv("data/e11_duplicate_sha_audit.csv")
        dup_groups = len(df_dup)
    else:
        dup_groups = "pending"
        
    # 5. Parse errors
    if os.path.exists("data/e11_test_parse_errors.csv"):
        df_errs = pd.read_csv("data/e11_test_parse_errors.csv")
        parse_errs = len(df_errs)
    else:
        parse_errs = "pending"
        
    # 6. Refactoring
    if os.path.exists("data/e11_refactoring_raw.csv") and os.path.exists("data/e11_refactoring_labels.csv"):
        df_rm = pd.read_csv("data/e11_refactoring_raw.csv")
        df_lbl = pd.read_csv("data/e11_refactoring_labels.csv")
        rm_success = len(df_rm[df_rm['analysis_status'] == 'SUCCESS'])
        rm_err = len(df_rm[df_rm['analysis_status'].str.startswith('ERROR')])
        ref_only = len(df_lbl[df_lbl['REF_ONLY_or_REF_MIXED'] == 'REF_ONLY'])
        ref_mixed = len(df_lbl[df_lbl['REF_ONLY_or_REF_MIXED'] == 'REF_MIXED'])
        non_ref = len(df_lbl[df_lbl['REF_ONLY_or_REF_MIXED'] == 'NON_REF'])
        dir_exp = len(df_lbl[df_lbl['direct_exposure'] == True])
        ind_exp = len(df_lbl[df_lbl['indirect_exposure'] == True])
        
        # Merge with tests to see direct exposure failing observations
        if type(test_obs) != str:
            df_lbl_fail = pd.merge(df_lbl, df_tests, on=['project', 'commit_sha'])
            dir_fail = len(df_lbl_fail[(df_lbl_fail['direct_exposure'] == True) & (df_lbl_fail['failure_positive'] == 1)])
        else:
            dir_fail = "pending"
    else:
        rm_success = rm_err = ref_only = ref_mixed = non_ref = dir_exp = ind_exp = dir_fail = "pending"
        
    with open("literature/e11_phase16_final_dataset_quality.md", "w") as f:
        f.write("# Phase 16B: Final Dataset Quality Report\n\n")
        f.write("### Population\n")
        f.write(f"- **CIBench projects**: 100\n")
        f.write(f"- **Verified E11 projects**: {elig_count}\n")
        f.write(f"- **Ineligible projects**: {inelig_count}\n")
        f.write(f"- **Unverified projects**: {unv_count}\n\n")
        
        f.write("### Dataset Volume\n")
        f.write(f"- **CIBench rows**: ~118k\n")
        f.write(f"- **Observable builds**: {obs_builds}\n")
        f.write(f"- **Unique SHAs**: {uniq_shas}\n")
        f.write(f"- **Duplicate SHA groups**: {dup_groups}\n")
        f.write(f"- **Test-class rows**: {test_obs}\n")
        f.write(f"- **Failure-positive rows**: {fail_pos}\n")
        f.write(f"- **Error-only rows**: {err_only}\n")
        f.write(f"- **Skipped rows**: {skipped}\n\n")
        
        f.write("### Tooling and Linkage\n")
        f.write(f"- **Git linkage (SUCCESS %)**: {link_success} successful, {link_miss} missing\n")
        f.write(f"- **Parse errors**: {parse_errs}\n")
        f.write(f"- **RefactoringMiner SUCCESS**: {rm_success}\n")
        f.write(f"- **RefactoringMiner ERROR**: {rm_err}\n\n")
        
        f.write("### Refactoring Categories\n")
        f.write(f"- **REF_ONLY**: {ref_only}\n")
        f.write(f"- **REF_MIXED**: {ref_mixed}\n")
        f.write(f"- **NON_REF**: {non_ref}\n")
        f.write(f"- **Direct exposure**: {dir_exp}\n")
        f.write(f"- **Indirect exposure**: {ind_exp}\n")
        f.write(f"- **Direct-exposure failure-positive observations**: {dir_fail}\n")
        
    print("Reports generated.")

if __name__ == "__main__":
    main()

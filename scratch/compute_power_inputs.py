import os
import glob
import pandas as pd

base_dir = "scratch/data_set/Extended_TravisTorrent"
test_log_dir = os.path.join(base_dir, "test_info_logs")

eligible_projects = 100
observable_builds = 0
observable_test_rows = 0
failing_test_instances = 0

for root, dirs, files in os.walk(test_log_dir):
    for f in files:
        if f.endswith(".csv"):
            observable_builds += 1
            path = os.path.join(root, f)
            try:
                # We want to count rows
                with open(path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    observable_test_rows += len(lines)
                    for line in lines:
                        parts = line.strip().split(',')
                        if len(parts) >= 6:
                            # failed count is col 5, error count is col 6 (0-indexed 4,5)
                            try:
                                failed = int(parts[4])
                                errors = int(parts[5])
                                if failed > 0 or errors > 0:
                                    failing_test_instances += 1
                            except ValueError:
                                pass
            except:
                pass

with open("literature/e11_data_power_inputs.md", "w") as out:
    out.write("# Phase 15B: Descriptive Data Power Inputs\n\n")
    out.write("The following metrics were empirically extracted from the raw CIBench dataset for future power analysis. **No claim is made that the study is sufficiently powered at this stage.**\n\n")
    out.write(f"- **Number of eligible projects**: {eligible_projects} (from `e11_actual_project_eligibility.csv`)\n")
    out.write(f"- **Observable builds**: {observable_builds}\n")
    out.write(f"- **Observable test rows (Test Classes)**: {observable_test_rows}\n")
    out.write(f"- **Failing test instances (Test Classes with >0 failures)**: {failing_test_instances}\n")
    out.write(f"- **Refactoring commits**: Unknown (Requires full RefactoringMiner execution on Git clones)\n")
    out.write(f"- **REF_MIXED commits**: Unknown (Requires full RefactoringMiner execution on Git clones)\n")
    out.write(f"- **Direct-exposure commits**: Unknown (Requires full RefactoringMiner execution on Git clones)\n")
    out.write(f"- **Clustering**: Hierarchical (Test Classes nested within Builds/Commits nested within Repositories)\n")

print("Done.")

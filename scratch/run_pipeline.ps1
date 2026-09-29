$ErrorActionPreference = "Stop"

Write-Host "Starting Phase 16C Pipeline..."

Write-Host "`n--- 1. Historical Eligibility Verification ---"
python scratch\phase16b_1_verify_repos.py

Write-Host "`n--- 2. Build Synthesis ---"
python scratch\phase16b_2_build_synthesis.py

Write-Host "`n--- 3. RefactoringMiner Execution ---"
python scratch\phase16b_3_run_refactoring.py

Write-Host "`n--- 4. Temporal Audit ---"
python scratch\phase16c_temporal_audit.py

Write-Host "`n--- 5. Generate Reports ---"
python scratch\phase16c_generate_reports.py

Write-Host "`n--- 6. Git Commit ---"
git add data/ literature/ scratch/
git commit -m "Phase 16C complete empirical integrity gate"
git push origin main

Write-Host "`nPipeline complete."

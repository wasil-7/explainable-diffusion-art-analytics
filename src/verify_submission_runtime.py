"""Verify the clean submission dashboard using its own files and all six views."""
from common import *
from verify_dashboard import run_checks
if __name__=='__main__':
    package=ROOT/'GCR_Submission/i242551_i242532_Milestone03_DSB'
    assert not list(package.rglob('*.parquet')) and not (package/'data').exists()
    run_checks(package,ROOT/'phase3_output/ui_upgrade/compact_runtime_verification.json')

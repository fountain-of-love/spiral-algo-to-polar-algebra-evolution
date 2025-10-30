
import sys, os
BASE_DIR = '/mnt/data/gao_spiral_ref'
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
from runner import run_suite
out = os.path.join(BASE_DIR, 'results')
run_suite(out, seeds=[123], sizes=[100], two_opt_budget=500)
print('Quick run done:', os.path.join(out, 'results.csv'))

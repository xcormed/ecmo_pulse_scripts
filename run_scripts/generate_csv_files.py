import sys, os.path
dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(dir)

from disease_scripts.ARDS_ecmo import ARDS_ecmo
from disease_scripts.ARDS_nasal_cannula import ARDS_nasal_cannula
from disease_scripts.ARDS_nonrebreather import ARDS_nonrebreather
from disease_scripts.ARDS_protective_ventilator import ARDS_ventilator_protective
from disease_scripts.ARDS_traditional_ventilator import ARDS_ventilator_traditional
from disease_scripts.ARDS_untreated import ARDS_untreated
from disease_scripts.COPD_ecmo import COPD_ecmo
from disease_scripts.COPD_nasal_cannula import COPD_nasal_cannula
from disease_scripts.COPD_nonrebreather import COPD_nonrebreather
from disease_scripts.COPD_protective_ventilator import COPD_ventilator_protective
from disease_scripts.COPD_traditional_ventilator import COPD_ventilator_traditional
from disease_scripts.COPD_untreated import COPD_untreated

import multiprocessing as mp

# # Simulate across all 10 patients, giving each severities of 0.3, 0.6, and 0.9
names = ["Cynthia", "Gus", "Joel", "Nathan", "Rick", "Hassan", "Soldier", "Jeff", "Carol", "Jane"]
# List of patient's weights in lb
weights = [96.4, 215.7, 176.4, 176.4, 158.4, 206.4, 176.4, 196.4, 156.4, 80.6]
# Give each patient 6 ml/kg in VT (protective)
VTP = [w / 2.20462 * 6 for w in weights]
# Give each patient 12 ml/kg in VT (traditional)
VTT = [w / 2.20462 * 12 for w in weights]
severities = [0.3, 0.6, 0.9]
processes = []

# Add a new thread for every patient at each severity, start each thread, and join them
for name in names:
    for severity in severities:
        processes.append(mp.Process(None, ARDS_ecmo, args=(name, severity)))
        processes.append(mp.Process(None, ARDS_nasal_cannula, args=(name, severity)))
        processes.append(mp.Process(None, ARDS_nonrebreather, args=(name, severity)))
        processes.append(mp.Process(None, ARDS_untreated, args=(name, severity)))
        processes.append(mp.Process(None, COPD_ecmo, args=(name, severity)))
        processes.append(mp.Process(None, COPD_nasal_cannula, args=(name, severity)))
        processes.append(mp.Process(None, COPD_nonrebreather, args=(name, severity)))
        processes.append(mp.Process(None, COPD_untreated, args=(name, severity)))

for i, name in enumerate(names):
    for severity in severities:
        processes.append(mp.Process(None, ARDS_ventilator_protective, args=(name, severity, VTP[i])))
        processes.append(mp.Process(None, ARDS_ventilator_traditional, args=(name, severity, VTT[i])))
        processes.append(mp.Process(None, COPD_ventilator_protective, args=(name, severity, VTP[i])))
        processes.append(mp.Process(None, COPD_ventilator_traditional, args=(name, severity, VTT[i])))

for p in processes:
    p.start()

for p in processes:
    p.join()

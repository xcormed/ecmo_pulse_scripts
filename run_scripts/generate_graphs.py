import sys, os.path
dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(dir)

from analysis.analyze_CO2 import analyze_CO2
from analysis.analyze_other_properties import analyze_other_properties

analyze_CO2("COPD")
analyze_other_properties('COPD', 'OxygenSaturation')
analyze_other_properties('COPD', 'TotalPulmonaryVentilationLmin')
analyze_other_properties('COPD', 'BloodPH')

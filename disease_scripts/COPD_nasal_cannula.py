# Distributed under the Apache License, Version 2.0.
# See accompanying NOTICE file for details.

from pulse.cdm.patient_actions import SEChronicObstructivePulmonaryDiseaseExacerbation
from pulse.engine.PulseEngine import PulseEngine
from pulse.cdm.patient_actions import SESupplementalOxygen, eDevice

from pulse.cdm.scalars import FrequencyUnit, PressureUnit, \
                              VolumeUnit, VolumePerTimeUnit, MassPerVolumeUnit
from pulse.cdm.engine import SEDataRequest, SEDataRequestManager

import multiprocessing as mp

# This script gives patients COPD of varying severity and treats them with a nasal cannula


# Arguments: patient - a patient name, level_severity - a COPD severity
def COPD_nasal_cannula(patient, level_severity):
    # Initialize the pulse engine, tell pulse where to send the log file, and also show the log on the console
    pulse = PulseEngine()
    pulse.set_log_filename("./test_results/XCOR/COPD_nasal_cannula_{}_{}.log".format(patient, level_severity))
    pulse.log_to_console(True)

    # Produce a list of data requests to save to csv. All other timeseries data is calculated but not saved to disk.
    data_requests = [
        SEDataRequest.create_physiology_request("RespirationRate", unit=FrequencyUnit.Per_min),
        SEDataRequest.create_physiology_request("TidalVolume", unit=VolumeUnit.mL),
        SEDataRequest.create_physiology_request("TotalPulmonaryVentilation", unit=VolumePerTimeUnit.L_Per_min),
        SEDataRequest.create_physiology_request("OxygenSaturation"),
        SEDataRequest.create_physiology_request("BloodPH"),
        SEDataRequest.create_physiology_request("HeartRate", unit=FrequencyUnit.Per_min),
        SEDataRequest.create_physiology_request("SystolicArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("DiastolicArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("EndTidalCarbonDioxidePressure",  unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("BloodVolume",  unit=VolumeUnit.mL),
        SEDataRequest.create_physiology_request("CardiacOutput", unit=VolumePerTimeUnit.L_Per_min),
        SEDataRequest.create_substance_request("Bicarbonate", "BloodConcentration",  unit=MassPerVolumeUnit.g_Per_L),
        SEDataRequest.create_substance_request("Sodium", "BloodConcentration",  unit=MassPerVolumeUnit.g_Per_L),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "CarbonDioxide", "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "Oxygen", "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("CarbonDioxideSaturation"),
        SEDataRequest.create_substance_request("Oxygen", "AlveolarTransfer", VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_substance_request("CarbonDioxide", "AlveolarTransfer", VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_mechanical_ventilator_request("TidalVolume", unit=VolumeUnit.L)]

    # Produce a data manager object with the data request list, and tell it where to save
    data_mgr = SEDataRequestManager(data_requests)
    data_mgr.set_results_filename("./test_results/XCOR/COPD_nasal_cannula_{}_{}.csv".format(patient, level_severity))

    # Initialize the engine with our configuration. Load patient steady state.
    if not pulse.serialize_from_file("./states/{}@0s.pbb".format(patient), data_mgr):
        print("Unable to load initial state file")
        return

    # Define and process a COPD exacerbation action. Set bronchitis and emphysema severities equal.
    exacerbation = SEChronicObstructivePulmonaryDiseaseExacerbation()
    exacerbation.set_comment("Patient's COPD is exacerbated")
    exacerbation.get_bronchitis_severity().set_value(level_severity)
    exacerbation.get_emphysema_severity().set_value(level_severity)
    pulse.process_action(exacerbation)

    # Advance 2 mins to get stabilize our patient to our COPD settings
    pulse.advance_time_s(120)

    # Define and process a supplemental oxygen action. Nasal cannula with 3.5 L/min flow rate.
    oxygen = SESupplementalOxygen()
    oxygen.set_comment("Patient receives supplemental oxygen ")
    oxygen.set_device(eDevice.NasalCannula)
    oxygen.get_volume().set_value(400, VolumeUnit.L)
    oxygen.get_flow().set_value(3.5, VolumePerTimeUnit.L_Per_min)
    pulse.process_action(oxygen)

    # Advance in time 900 seconds (15 minutes). This data will be saved to the csv.
    pulse.advance_time_s(900)

    results = pulse.pull_data()
    # And write it out to the console
    data_mgr.to_console(results)

# only need to uncomment if running individual file
# if __name__ == '__main__':
#     # # Simulate across all 10 patients, giving each severities of 0.3, 0.6, and 0.9
#     names = ["Cynthia", "Gus", "Joel", "Nathan", "Rick", "Hassan", "Soldier", "Jeff", "Carol", "Jane"]
#     severities = [0.3, 0.6, 0.9]
#     processes = []
#
# # Add a new thread for every patient at each severity, start each thread, and join them
#     for name in names:
#         for severity in severities:
#             processes.append(mp.Process(None, COPD_nasal_cannula, args=(name, severity)))
#
#     for p in processes:
#         p.start()
#
#     for p in processes:
#         p.join()
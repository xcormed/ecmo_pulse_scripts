# Distributed under the Apache License, Version 2.0.
# See accompanying NOTICE file for details.

from pulse.cdm.patient_actions import SEAcuteRespiratoryDistressSyndromeExacerbation
from pulse.engine.PulseEngine import PulseEngine

from pulse.cdm.scalars import FrequencyUnit, PressureUnit, \
                              VolumeUnit, VolumePerTimeUnit, MassPerVolumeUnit
from pulse.cdm.engine import SEDataRequest, SEDataRequestManager

import multiprocessing as mp

# This script gives patients ARDS of varying severities and does not treat it


# Arguments: patient - a patient name, level_severe - level of severity ARDS
def ARDS_untreated(patient, level_severe):
    # Initialize the pulse engine, tell pulse where to send the log file, show the log on the console
    pulse = PulseEngine()
    pulse.set_log_filename("./test_results/XCOR/ARDS_untreated_{}_{}.log".format(patient, level_severe))
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
    data_mgr.set_results_filename("./test_results/XCOR/ARDS_untreated_{}_{}.csv".format(patient, level_severe))

    # Initialize the engine with our configuration. Load patient steady state.
    if not pulse.serialize_from_file("./states/{}@0s.pbb".format(patient), data_mgr):
        print("Unable to load initial state file")
        return

    # Define and process an ARDS exacerbation action. Fully affecting both lungs, with defined severity
    ards = SEAcuteRespiratoryDistressSyndromeExacerbation()
    ards.get_left_lung_affected().set_value(1.0)
    ards.get_right_lung_affected().set_value(1.0)
    ards.get_severity().set_value(level_severe)
    pulse.process_action(ards)

    # Advance in time 900 seconds (15 minutes). This data will be saved to the csv.
    pulse.advance_time_s(900)

    results = pulse.pull_data()
    # And write it out to the console
    data_mgr.to_console(results)


# if __name__ == '__main__':
#     # # Simulate across all 10 patients, giving each severities of 0.3, 0.6, and 0.9
#     names = ["Cynthia", "Gus", "Joel", "Nathan", "Rick", "Hassan", "Soldier", "Jeff", "Carol", "Jane"]
#     severities = [0.3, 0.6, 0.9]
#     processes = []
#
# # Add a new thread for every patient at each severity, start each thread, and join them
#     for name in names:
#         for severity in severities:
#             processes.append(mp.Process(None, ARDS_untreated, args=(name, severity)))
#
#     for p in processes:
#         p.start()
#
#     for p in processes:
#         p.join()

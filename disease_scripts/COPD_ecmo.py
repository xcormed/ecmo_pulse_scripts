from pulse.engine.PulseEngine import PulseEngine
from pulse.cdm.engine import SEDataRequest, SEDataRequestManager
from pulse.cdm.scalars import FrequencyUnit, MassUnit, MassPerVolumeUnit, \
                              PressureUnit, VolumeUnit, VolumePerTimeMassUnit, VolumePerTimeUnit
from pulse.cdm.patient_actions import SEChronicObstructivePulmonaryDiseaseExacerbation
from pulse.cdm.ecmo_actions import SEECMOConfiguration
from pulse.cdm.ecmo import eECMO_CannulationLocation

import multiprocessing as mp

# Arguments: patient - a patient name, level_severity - level of severity COPD
def COPD_ecmo(patient, level_severity):
    # Initialize the pulse engine, tell pulse where to send the log file, and also show the log on the console
    pulse = PulseEngine()
    pulse.set_log_filename("./test_results/XCOR/COPD_ecmo_{}_{}.log".format(patient, level_severity))
    pulse.log_to_console(True)

    # Produce a list of data requests to save to csv. All other timeseries data is calculated but not saved to disk.
    data_requests = [
        SEDataRequest.create_physiology_request("BloodPH"),
        SEDataRequest.create_physiology_request("BloodVolume", unit=VolumeUnit.mL),
        SEDataRequest.create_physiology_request("CardiacOutput", unit=VolumePerTimeUnit.L_Per_min),
        SEDataRequest.create_physiology_request("EndTidalCarbonDioxidePressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("HeartRate", unit=FrequencyUnit.Per_min),
        SEDataRequest.create_physiology_request("Hematocrit"),
        SEDataRequest.create_physiology_request("OxygenSaturation"),
        SEDataRequest.create_physiology_request("RespirationRate", unit=FrequencyUnit.Per_min),
        SEDataRequest.create_physiology_request("SystolicArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("DiastolicArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("TidalVolume", unit=VolumeUnit.mL),
        SEDataRequest.create_physiology_request("TotalPulmonaryVentilation", unit=VolumePerTimeUnit.L_Per_min),
        SEDataRequest.create_substance_request("Bicarbonate", "BloodConcentration", unit=MassPerVolumeUnit.g_Per_L),
        SEDataRequest.create_substance_request("CarbonDioxide", "AlveolarTransfer", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_substance_request("Oxygen", "AlveolarTransfer", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_substance_request("Sodium", "BloodConcentration", unit=MassPerVolumeUnit.g_Per_L),
        SEDataRequest.create_substance_request("Sodium", "Clearance-RenalClearance", unit=VolumePerTimeMassUnit.mL_Per_min_kg),
        SEDataRequest.create_substance_request("Sodium", "MassInBody", unit=MassUnit.g),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "CarbonDioxide", "PartialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "Oxygen", "PartialPressure", unit=PressureUnit.mmHg),
        # ECMO Compartments
        SEDataRequest.create_liquid_compartment_request("ECMOBloodSamplingPort", "InFlow", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_request("ECMOBloodSamplingPort", "OutFlow", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_request("ECMOOxygenator", "InFlow", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_request("ECMOOxygenator", "OutFlow", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOOxygenator", "Sodium", "Concentration", unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("VenaCava", "Sodium", "Concentration", unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "Sodium", "Concentration", unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "Oxygen", "Concentration", unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "CarbonDioxide", "Concentration", unit=MassPerVolumeUnit.g_Per_dL)
    ]

    # Produce a data manager object with the data request list, and tell it where to save
    data_mgr = SEDataRequestManager(data_requests)
    data_mgr.set_results_filename("./test_results/XCOR/COPD_ecmo_{}_{}.csv".format(patient, level_severity))

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

    # Get the values of the data you requested at this time
    results = pulse.pull_data()

    # Initialize ECMO
    cfg = SEECMOConfiguration()
    settings = cfg.get_settings()
    # Attach ECMO from jugular to left leg
    settings.set_inflow_location(eECMO_CannulationLocation.InternalJugular)
    settings.set_outflow_location(eECMO_CannulationLocation.LeftFemoralVein)

    settings.get_oxygenator_volume().set_value(500, VolumeUnit.mL)
    settings.get_transfusion_flow().set_value(16.7, VolumePerTimeUnit.mL_Per_s)

    # Calculate the amount of O2 to add to the ECMO circuit and process the action
    # O2 Added[g / min] = -0.0033 * (Blood Flow Rate[L / min]) ^ 2 + 0.1062 * (Blood Flow Rate[L / min]) - 0.0037
    # O2 Added[g / min] = -0.0033 * (1)^2 + 0.1062 * 1  - 0.0037
    # O2 Added[g / min] = -0.0033 + 0.1062 - 0.0037
    # O2 Added[g / min] = .0992
    # O2 Added[g / L] = (.0992 / 1) = .0992
    # O2 Added[g / dL] = 0.00992
    # add this value of O2 to the amount of O2 already in
    print(results[list(results)[28]][-1])
    settings.get_substance_concentration("Oxygen").get_concentration().set_value(results[list(results)[28]][-1]+0.00992
                                                                                 , MassPerVolumeUnit.g_Per_dL)
    # Calculate the amount of CO2 to remove from the ECMO circuit and process the action
    # CO2 Removed[g / min] = -0.0057 * (Blood Flow Rate[L / min]) ^ 2 + 0.1276 * (Blood Flow Rate[L / min]) + 0.0105
    # CO2 Removed[g / min] = -0.0057 * (1)^ 2 + 0.1276 * 1 + 0.0105
    # CO2 Removed[g / min] = -0.0057 + 0.1276 + 0.0105
    # CO2 Removed[g / min] = .1324
    # CO2 Removed[g / L] = .321 / 1 = .321
    # CO2 Removed[g / dL] = .321 / 1 = .0321
    settings.get_substance_concentration("CarbonDioxide").get_concentration().set_value(
        results[list(results)[29]][-1]-0.0321, MassPerVolumeUnit.g_Per_dL)

    pulse.process_action(cfg)

    results = pulse.pull_data()
    # Check that O2 saturation must not exceed 1 and pO2 must be <=300 mmHg
    # O2 added may be lower in order to fulfill this boundary condition
    while results[list(results)[7]][-1] > 1.0 or results[list(results)[20]][-1] > 300:
        current_oxygen = results[list(results)[28]][-1]
        new_oxygen = current_oxygen * .999
        settings.get_substance_concentration("Oxygen").get_concentration().set_value(new_oxygen,
                                                                                     MassPerVolumeUnit.g_Per_dL)
        pulse.process_action(cfg)
        print("Recalculated oxygen")
        results = pulse.pull_data()

    # Check that pCO2 must be >=15 mmHg
    # CO2 removed may be lower in order to fulfill this boundary condition
    while results[list(results)[19]][-1] < 15:
        current_co2 = results[list(results)[29]][-1]
        new_co2 = current_co2 * .999
        settings.get_substance_concentration("CarbonDioxide").get_concentration().set_value(new_co2,
                                                                                             MassPerVolumeUnit.g_Per_dL)
        pulse.process_action(cfg)
        print("Recalculated carbon dioxide")
        results = pulse.pull_data()

    # Advance in time 900 seconds (15 minutes). This data will be saved to the csv.
    pulse.advance_time_s(900)
    # And write it out to the console
    data_mgr.to_console(results)


if __name__ == '__main__':
    # # Simulate across all 10 patients, giving each severities of 0.3, 0.6, and 0.9
    names = ["Cynthia", "Gus", "Joel", "Nathan", "Rick", "Hassan", "Soldier", "Jeff", "Carol", "Jane"]
    severities = [0.3, 0.6, 0.9]
    processes = []

# Add a new thread for every patient at each severity, start each thread, and join them
    for name in names:
        for severity in severities:
            processes.append(mp.Process(None, COPD_ecmo, args=(name, severity)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

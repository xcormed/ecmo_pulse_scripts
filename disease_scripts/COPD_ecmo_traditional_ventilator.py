from pulse.engine.PulseEngine import PulseEngine
from pulse.cdm.engine import SEDataRequest, SEDataRequestManager
from pulse.cdm.scalars import FrequencyUnit, MassUnit, MassPerVolumeUnit, \
                              PressureUnit, VolumeUnit, VolumePerTimeMassUnit, VolumePerTimeUnit, TimeUnit
from pulse.cdm.patient_actions import SEChronicObstructivePulmonaryDiseaseExacerbation
from pulse.cdm.ecmo_actions import SEECMOConfiguration
from pulse.cdm.ecmo import eECMO_CannulationLocation
from pulse.cdm.mechanical_ventilator_actions import SEMechanicalVentilatorVolumeControl, \
                                                    eMechanicalVentilator_VolumeControlMode
from pulse.cdm.mechanical_ventilator import eSwitch
import multiprocessing as mp

# Arguments: patient - a patient name, level_severity - level of severity COPD, VoT - a tidal volume
def COPD_ecmo_traditional_ventilator(patient, level_severity, VoT):

    # Initialize the pulse engine, tell pulse where to send the log file, and also show the log on the console
    pulse = PulseEngine()
    pulse.set_log_filename("./test_results/XCOR/COPD_ecmo_traditional_ventilator_{}_{}.log".format(patient,
                                                                                                   level_severity))
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
        SEDataRequest.create_physiology_request("CarbonDioxideSaturation"),
        SEDataRequest.create_mechanical_ventilator_request("TidalVolume", unit=VolumeUnit.L),
        SEDataRequest.create_physiology_request("RespirationRate", unit=FrequencyUnit.Per_min),
        SEDataRequest.create_physiology_request("SystolicArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("DiastolicArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("TidalVolume", unit=VolumeUnit.mL),
        SEDataRequest.create_physiology_request("TotalPulmonaryVentilation", unit=VolumePerTimeUnit.L_Per_min),
        SEDataRequest.create_substance_request("Bicarbonate", "BloodConcentration", unit=MassPerVolumeUnit.g_Per_L),
        SEDataRequest.create_substance_request("CarbonDioxide", "AlveolarTransfer", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_substance_request("Oxygen", "AlveolarTransfer", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_substance_request("Sodium", "BloodConcentration", unit=MassPerVolumeUnit.g_Per_L),
        SEDataRequest.create_substance_request("Sodium", "Clearance-RenalClearance",
                                               unit=VolumePerTimeMassUnit.mL_Per_min_kg),
        SEDataRequest.create_substance_request("Sodium", "MassInBody", unit=MassUnit.g),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "CarbonDioxide", "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "Oxygen", "PartialPressure",
                                                                  unit=PressureUnit.mmHg), \
        # ECMO Compartments
        SEDataRequest.create_liquid_compartment_request("ECMOBloodSamplingPort", "InFlow",
                                                        unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_request("ECMOBloodSamplingPort", "OutFlow",
                                                        unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_request("ECMOOxygenator", "InFlow", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_request("ECMOOxygenator", "OutFlow", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOOxygenator", "Sodium", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("VenaCava", "Sodium", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "Sodium", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "CarbonDioxide",
                                                                  "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "Oxygen", "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "Oxygen", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "CarbonDioxide",
                                                                  "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL)
    ]

    # Produce a data manager object with the data request list, and tell it where to save
    data_mgr = SEDataRequestManager(data_requests)
    data_mgr.set_results_filename("./test_results/XCOR/COPD_ecmo_traditional_ventilator{}_{}.csv".format(patient,
                                                                                                         level_severity))

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

    # Initialize ECMO
    cfg = SEECMOConfiguration()
    settings = cfg.get_settings()
    # Attach ECMO from jugular to left leg
    settings.set_inflow_location(eECMO_CannulationLocation.InternalJugular)
    settings.set_outflow_location(eECMO_CannulationLocation.LeftFemoralVein)
    settings.get_oxygenator_volume().set_value(500, VolumeUnit.mL)
    settings.get_transfusion_flow().set_value(16.7, VolumePerTimeUnit.mL_Per_s)
    pulse.process_action(cfg)
    # Advance a little time to get ECMO connected and flowing
    pulse.advance_time_s(10)

    # Clear our settings, as we don't need to specify our initial values each time
    settings.clear()
    results = pulse.pull_data()
    data_mgr.to_console(results)

    # Calculate the amount of CO2 to remove from the ECMO circuit and process the action
    # CO2 Removed[g / min] = -0.0057 * (Blood Flow Rate[L / min]) ^ 2 + 0.1276 * (Blood Flow Rate[L / min]) + 0.0105
    # CO2 Removed[g / min] = -0.0057 * (1)^ 2 + 0.1276 * 1 + 0.0105
    # CO2 Removed[g / min] = -0.0057 + 0.1276 + 0.0105
    # CO2 Removed[g / min] = .1324
    # CO2 Removed[g / L] = .321 / 1 = .321
    # CO2 Removed[g / dL] = .0321
    # Check that pCO2 must be >=15 mmHg
    # We create an estimate instead before removing the CO2
    estimate = max((results[list(results)[30]][-1] - 15) * 0.0321, 0)
    estimate_co2 = min(estimate, 0.0321)
    settings.get_substance_concentration("CarbonDioxide").get_concentration().set_value(
        results[list(results)[33]][-1] - estimate_co2, MassPerVolumeUnit.g_Per_dL)

    # Get the values of the data you requested at this time
    # Calculate the amount of O2 to add to the ECMO circuit and process the action
    # O2 Added[g / min] = -0.0033 * (Blood Flow Rate[L / min]) ^ 2 + 0.1062 * (Blood Flow Rate[L / min]) - 0.0037
    # O2 Added[g / min] = -0.0033 * (1.002)^2 + 0.1062 * 1.002  - 0.0037
    # O2 Added[g / min] = -0.00331 + 0.1064 - 0.0037
    # O2 Added[g / min] = .0994
    # O2 Added[g / L] = (.0994 / 1.002) = .0992
    # O2 Added[g / dL] = 0.00992
    # add this value of O2 to the amount of O2 already in
    # Check that O2 saturation must not exceed 1 and pO2 must be <=300 mmHg
    # O2 added may be lower in order to fulfill this boundary condition
    if results[list(results)[7]][-1] < 1.0 or results[list(results)[31]][-1] <= 300:
        settings.get_substance_concentration("Oxygen").get_concentration().set_value(
            results[list(results)[32]][-1] + 0.00992, MassPerVolumeUnit.g_Per_dL)

    # Define and process a ventilator action. Assist control, FiO2=1, PEEP=5cmH2O, VT user-defined
    vc_ac = SEMechanicalVentilatorVolumeControl()
    vc_ac.set_connection(eSwitch.On)
    vc_ac.set_mode(eMechanicalVentilator_VolumeControlMode.AssistedControl)
    vc_ac.get_flow().set_value(50.0, VolumePerTimeUnit.L_Per_min)
    vc_ac.get_fraction_inspired_oxygen().set_value(1.0)
    vc_ac.get_inspiratory_period().set_value(1.0, TimeUnit.s)
    vc_ac.get_positive_end_expired_pressure().set_value(5.0, PressureUnit.cmH2O)
    vc_ac.get_respiration_rate().set_value(12.0, FrequencyUnit.Per_min)
    vc_ac.get_tidal_volume().set_value(VoT, VolumeUnit.mL)


    for i in range(900*50):

        if (i % 50 == 0):
            pulse.process_action(vc_ac)

        pulse.process_action(cfg)

        pulse.advance_time()

    data_mgr.to_console(results)

# only need to uncomment if running individual file
if __name__ == '__main__':
    # # Simulate across all 10 patients, giving each severities of 0.3, 0.6, and 0.9
    names = ["Cynthia", "Gus", "Joel", "Nathan", "Rick", "Hassan", "Soldier", "Jeff", "Carol", "Jane"]
    severities = [0.3, 0.6, 0.9]
    processes = []
    # List of patient's weights in lb
    weights = [96.4, 215.7, 176.4, 176.4, 158.4, 206.4, 176.4, 196.4, 156.4, 80.6]
    # Give each patient 12 ml/kg in VT
    VT = [w / 2.20462 * 12 for w in weights]

# Add a new thread for every patient at each severity, start each thread, and join them
    for i, name in enumerate(names):
        for severity in severities:
            processes.append(mp.Process(None, COPD_ecmo_traditional_ventilator, args=(name, severity, VT[i])))

    for p in processes:
        p.start()

    for p in processes:
        p.join()
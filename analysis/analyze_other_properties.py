import numpy as np
import matplotlib.pyplot as plt

# This script produces boxplots for generic patient properties (respiration rate, blood pH, ...)

# Arguments: case - (COPD or ARDS), property_type - what property to compare


def analyze_other_properties(case, property_type):
    # Make a list of patient names and severities
    names = ["Cynthia", "Gus", "Joel", "Nathan", "Rick", "Hassan", "Soldier", "Jeff", "Carol", "Jane"]
    severities = [0.3, 0.6, 0.9]

    # Initialize arrays to hold CO2 values for each patient and each severity. One array per treatment.
    property_untreated = np.zeros((len(names), len(severities)))
    property_ecmo = np.zeros((len(names), len(severities)))
    property_nasal_cannula = np.zeros((len(names), len(severities)))
    property_nonrebreather = np.zeros((len(names), len(severities)))
    property_ventilator = np.zeros((len(names), len(severities)))
    property_traditional_ventilator = np.zeros((len(names), len(severities)))

    for i in range(len(names)):
        for j in range(len(severities)):
            # Load in each csv file corresponding to patient name, disease severity, and treatment
            data = np.genfromtxt('./test_results/XCOR/{}_untreated_{}_{}.csv'.format(case, names[i], severities[j]),
                                 delimiter=',', names=True, dtype=None)
            # Stick the averaged final value into the array
            property_untreated[i, j] = np.mean(data[property_type][-1000:])

            data = np.genfromtxt('./test_results/XCOR/{}_ecmo_{}_{}.csv'.format(case, names[i], severities[j]),
                                 delimiter=',', names=True, dtype=None)
            property_ecmo[i, j] = np.mean(data[property_type][-1000:])

            data = np.genfromtxt('./test_results/XCOR/{}_nasal_cannula_{}_{}.csv'.format(case, names[i], severities[j]),
                                 delimiter=',', names=True, dtype=None)
            property_nasal_cannula[i, j] = np.mean(data[property_type][-1000:])

            data = np.genfromtxt('./test_results/XCOR/{}_nonrebreather_{}_{}.csv'.format(case, names[i], severities[j]),
                                 delimiter=',', names=True, dtype=None)
            property_nonrebreather[i, j] = np.mean(data[property_type][-1000:])

            data = np.genfromtxt('./test_results/XCOR/{}_ventilator_{}_{}.csv'.format(case, names[i], severities[j]),
                                 delimiter=',', names=True, dtype=None)
            property_ventilator[i, j] = np.mean(data[property_type][-1000:])

            data = np.genfromtxt('./test_results/XCOR/{}_traditional_ventilator_{}_{}.csv'.format(case, names[i],
                                                                                                  severities[j]),
                                 delimiter=',', names=True, dtype=None)
            property_traditional_ventilator[i, j] = np.mean(data[property_type][-1000:])

    print("Untreated:")
    print(property_untreated)
    print("Ecmo:")
    print(property_ecmo)
    print("Nasal cannula:")
    print(property_nasal_cannula)
    print("Nonreabreather:")
    print(property_nonrebreather)
    print("Protective ventilator:")
    print(property_ventilator)
    print("Traditional ventilator:")
    print(property_traditional_ventilator)

    w = 0.2
    X = np.array([0, 1, 2, 3, 4, 5])

    # plot the mild data
    plt.figure(figsize=[8, 4.8])
    c = 'green'
    plt.boxplot([property_untreated[:, 0], property_ecmo[:, 0], property_nasal_cannula[:, 0], property_nonrebreather[:, 0],
                 property_ventilator[:, 0], property_traditional_ventilator[:, 0]], positions=X, widths=w, notch=True,
                patch_artist=True,
                boxprops=dict(facecolor=c, color=c),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c)
                )

    # plot the moderate data
    c = 'orange'
    plt.boxplot([property_untreated[:, 1], property_ecmo[:, 1], property_nasal_cannula[:, 1], property_nonrebreather[:, 1],
                 property_ventilator[:, 1], property_traditional_ventilator[:, 1]], positions=X+w, widths=w, notch=True,
                patch_artist=True,
                boxprops=dict(facecolor=c, color=c),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c)
                )

    # plot the severe data
    c = 'red'
    plt.boxplot([property_untreated[1:8, 2], property_ecmo[1:8, 2], property_nasal_cannula[1:8, 2], property_nonrebreather[1:8, 2],
                 property_ventilator[1:8, 2], property_traditional_ventilator[1:8, 2]], positions=X+2*w, widths=w,
                notch=True, patch_artist=True,
                boxprops=dict(facecolor=c, color=c),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c)
                )
    my_xticks = ['no treatment', 'ecmo', 'nasal cannula', 'nonrebreather', 'protective vent', 'traditional vent']
    # Change the x labels
    plt.xticks(X+w, my_xticks)
    plt.xlabel('Treatment')
    plt.ylabel(property_type)
    # Save a png of the figure
    plt.savefig('{}_{}.png'.format(case, property_type))
    plt.show()

# Properties that can be tested
# - OxygenSaturation
# - BloodPH
# - TotalPulmonaryVentilationLmin
# - AortaCarbonDioxidePartialPressuremmHg
# - AortaOxygenPartialPressuremmHg


#analyze_other_properties('COPD', 'OxygenSaturation')
#analyze_other_properties('COPD', 'TotalPulmonaryVentilationLmin')
#analyze_other_properties('COPD', 'BloodPH')

import numpy as np
import matplotlib.pyplot as plt

# Produce plots of CO2 response at varying disease severity and treatment options.
# Function takes as argument "case", i.e. COPD or ARDS


def analyze_CO2(case):
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
    property_ecmo_traditional_ventilator = np.zeros((len(names), len(severities)))
    property_ecmo_protective_ventilator = np.zeros((len(names), len(severities)))


    for i in range(len(names)):
        for j in range(len(severities)):
            data = np.genfromtxt("./test_results/XCOR/{}_untreated_{}_{}.csv".format(case, names[i], severities[j]),
                                 delimiter=",", names=True, dtype=None, encoding=None)
            # Calculate total CO2 load with blood bicarb concentration and arterial CO2 partial pressure
            property_untreated[i, j] = \
                data["BicarbonateBloodConcentrationgL"][-1]*1000/61.0168 + \
                data["AortaCarbonDioxidePartialPressuremmHg"][-1]*.0308

            # Load in each csv file corresponding to patient name, disease severity, and treatment
            data = np.genfromtxt("./test_results/XCOR/{}_ecmo_{}_{}.csv".format(case, names[i], severities[j]),
                                 delimiter=",", names=True, dtype=None, encoding=None)
            # Calculate total CO2 load with blood bicarb concentration and arterial CO2 partial pressure
            property_ecmo[i, j] = \
                data["BicarbonateBloodConcentrationgL"][-1]*1000/61.0168 + \
                data["AortaCarbonDioxidePartialPressuremmHg"][-1]*.0308

            data = np.genfromtxt("./test_results/XCOR/{}_nasal_cannula_{}_{}.csv".format(case, names[i], severities[j]),
                                  delimiter=",", names=True, dtype=None, encoding=None)
            property_nasal_cannula[i, j] = data["BicarbonateBloodConcentrationgL"][-1]*1000/61.0168 + \
            data["AortaCarbonDioxidePartialPressuremmHg"][-1]*.0308

            data = np.genfromtxt("./test_results/XCOR/{}_nonrebreather_{}_{}.csv".format(case, names[i], severities[j]),
                                 delimiter=",", names=True, dtype=None, encoding=None)
            property_nonrebreather[i, j] = data["BicarbonateBloodConcentrationgL"][-1]*1000/61.0168 + \
                                 data["AortaCarbonDioxidePartialPressuremmHg"][-1]*.0308

            data = np.genfromtxt("./test_results/XCOR/{}_ventilator_{}_{}.csv".format(case, names[i], severities[j]),
                                delimiter=",", names=True, dtype=None, encoding=None)
            property_ventilator[i, j] = data["BicarbonateBloodConcentrationgL"][-1]*1000/61.0168 + \
                data["AortaCarbonDioxidePartialPressuremmHg"][-1]*.0308

            data = np.genfromtxt("./test_results/XCOR/{}_traditional_ventilator_{}_{}.csv".format(case, names[i],
                            severities[j]),delimiter=",", names=True, dtype=None, encoding=None)
            property_traditional_ventilator[i, j] = \
                data["BicarbonateBloodConcentrationgL"][-1]*1000/61.0168 + \
                data["AortaCarbonDioxidePartialPressuremmHg"][-1]*.0308

            data = np.genfromtxt("./test_results/XCOR/{}_ecmo_traditional_ventilator{}_{}.csv".format(case, names[i],
                                                                                                      severities[j]),
                                 delimiter=",", names=True, dtype=None, encoding=None)
            # Calculate total CO2 load with blood bicarb concentration and arterial CO2 partial pressure
            property_ecmo_traditional_ventilator[i, j] = \
                data["BicarbonateBloodConcentrationgL"][-1] * 1000 / 61.0168 + \
                data["AortaCarbonDioxidePartialPressuremmHg"][-1] * .0308

            data = np.genfromtxt("./test_results/XCOR/{}_ecmo_protective_ventilator{}_{}.csv".format(case, names[i],
                                                                                                      severities[j]),
                                 delimiter=",", names=True, dtype=None, encoding=None)
            # Calculate total CO2 load with blood bicarb concentration and arterial CO2 partial pressure
            property_ecmo_protective_ventilator[i, j] = \
                data["BicarbonateBloodConcentrationgL"][-1] * 1000 / 61.0168 + \
                data["AortaCarbonDioxidePartialPressuremmHg"][-1] * .0308

    print("Untreated:")
    print(property_untreated)
    print("ECMO:")
    print(property_ecmo)
    print("Nasal cannula:")
    print(property_nasal_cannula)
    print("Nonreabreather:")
    print(property_nonrebreather)
    print("Protective ventilator:")
    print(property_ventilator)
    print("Traditional ventilator:")
    print(property_traditional_ventilator)
    print("Ecmo and Traditional ventilator:")
    print(property_ecmo_traditional_ventilator)
    print("Ecmo and Protective ventilator:")
    print(property_ecmo_protective_ventilator)


    # Make a reference frame for placing the boxplots
    w = 0.2
    X = np.array([0, 1, 2, 3, 4, 5, 6, 7])

    plt.figure(figsize=[8, 4.8])

    c = "green"
    plt.boxplot([property_untreated[:, 0], property_ecmo[:, 0], property_nasal_cannula[:, 0], property_nonrebreather[:, 0],
              property_ventilator[:, 0], property_traditional_ventilator[:, 0], property_ecmo_traditional_ventilator[:, 0],
              property_ecmo_protective_ventilator[:, 0]],
                positions=X, widths=w, notch=True,
                patch_artist=True,
                boxprops=dict(facecolor=c, color=c),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c)
                )

    # plot the moderate data
    c = "orange"
    plt.boxplot([property_untreated[:, 0], property_ecmo[:, 0], property_nasal_cannula[:, 0], property_nonrebreather[:, 0],
                property_ventilator[:, 0], property_traditional_ventilator[:, 0], property_ecmo_traditional_ventilator[:, 0],
                property_ecmo_protective_ventilator[:, 0]],
                positions=X + w, widths=w,
                notch=True, patch_artist=True,
                boxprops=dict(facecolor=c, color=c),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c)
                )

    # plot the severe data
    c = "red"
    plt.boxplot([property_untreated[:, 0], property_ecmo[:, 0], property_nasal_cannula[:, 0], property_nonrebreather[:, 0],
                property_ventilator[:, 0], property_traditional_ventilator[:, 0], property_ecmo_traditional_ventilator[:, 0],
                property_ecmo_protective_ventilator[:, 0]],
                positions=X + 2 * w, widths=w,
                notch=True, patch_artist=True,
                boxprops=dict(facecolor=c, color=c),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c)
                )


    # Change the x labels
    my_xticks = ["no treatment", "ecmo", "nasal cannula", "nonrebreather", "protective vent", "traditional vent",
                 "ecmo + traditional vent", "ecmo + protective vent"]
    plt.xticks(X+w, my_xticks)
    plt.xlabel("Treatment")
    plt.ylabel("Total CO2 Load (mEq/L)")
    # Save a png of the figure
    plt.savefig("{}_{}.png".format(case, property))
    plt.show()


analyze_CO2("COPD")

#analyze_CO2("ARDS")

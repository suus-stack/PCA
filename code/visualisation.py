"""
Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405
Description: In this code functions are given that are used to make the shown
plots. The data form the plots is created by running the experiment (simulation)
an number of times. The plots show the influence of different factors on the
killing rate of the herrings.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from gamefish import *
from scipy.stats import shapiro
from scipy import stats

def influence_predator_number(max_number_predators, number_simulations):
    """
    Function that makes a violin plot of the distribution of the killed herring for
    different number of predators in an environment with and without rocks. The
    starting number of herring is set to 100. ........

    Parameters:
    -----------
    max_number_predators: Int
        The maximum number of predators that is investigated
    number_simulations: Int
        The number of simulations per experiment kind
    """
    # Make empty dataframe with three columns
    column_names = ['Nr predators', 'Killed herring', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # Loop over the number of predators
    for number_predators in range(0, max_number_predators+1):
        print('Nr predators', number_predators)

        # Do a number of simulation without rocks
        for simulation in range(number_simulations):
            experiment = Experiment(100, number_predators, 0, 30, True, True, False)
            number_killed_herring, _ = experiment.run()
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': number_killed_herring , 'Rocks':'no'}])
            df = pd.concat([df, new_row], ignore_index=True)

        # Do a number of simulations with rocks
        for simulation in range(number_simulations):
            experiment = Experiment(100, number_predators, 20, 30, True, True, False)
            number_killed_herring, _ = experiment.run()
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': number_killed_herring , 'Rocks':'yes'}])
            df = pd.concat([df, new_row], ignore_index=True)

    # Make a violin plot
    sns.violinplot(data=df, x= 'Nr predators', y= 'Killed herring', hue= 'Rocks', split=True, gap=.1, inner="quart")
    plt.ylim(bottom=0)
    plt.title('Distribution of the killed herring for different number of predators in an environment with and without rocks')
    plt.show()

def influence_rocks(number_simulations):
    """
    Function that makes a plot of the average killed herring + 1 SD errorbars
    in an environment with differnt numbers of rocks. The starting number of
    herring is set to 100 and theat of the predators to 1. ........

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind
    """
    list_rock_number =[]
    list_mean_killed =[]
    list_std_killed = []

    # Simulate the experiment with different number of rocks
    for number_rock in range(0, 60, 10):
        print('nr rock', number_rock)
        list_rock_number.append(number_rock)
        list_killed_herring = []

        # Repeat the simulation a number of times
        for simulation in range(number_simulations):
            print('simulation', simulation)
            experiment = Experiment(100, 1, number_rock, 30, False, True, False)
            number_killed_herring, _ = experiment.run()
            list_killed_herring.append(number_killed_herring)

        # Calculate the mean and the standard deviation and add it to the list
        mean_killed = np.mean(list_killed_herring)
        list_mean_killed.append(mean_killed)
        std_killed = np.std(list_killed_herring)
        list_std_killed.append(std_killed)

    # Make a plot of the average number of rilled herring vs the number of rocks
    plot = plt.errorbar(list_rock_number, list_mean_killed, yerr=list_std_killed, fmt='o', color='orange', markerfacecolor='red', label='avarage killed herring + 1 SD')
    plt.xlabel('Number or rocks')
    plt.ylabel('Average killed herring')
    plt.title('The average killed herring + 1 SD errorbars in a environment with differnt numbers of rocks')
    plt.ylim(bottom=0)
    plt.legend()
    plt.show()

def influence_alignment_distance(number_simulations):
    """
    Function that makes a plot of the average killed herring + 1 SD errorbars
    for different values of the alignment distance. The starting number of
    herring is set to 100 and theat of the predators to 1. ........

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind
    """
    list_alignment_distance = []
    list_mean_killed =[]
    list_std_killed = []

    # Simulate the experiment with different alignment distances
    for alignment_distance in range(5, 40, 5):
        print('alignment distance', alignment_distance)
        list_alignment_distance.append(alignment_distance)
        list_killed_herring = []

        # Simulate the experiment a number of times
        for simulation in range(number_simulations):
            print('simulation', simulation)
            experiment = Experiment(100, 1, 20, 20, True, True, False, alignment_distance, 20, 5)
            number_killed_herring, _ = experiment.run()
            list_killed_herring.append(number_killed_herring)

        # Calculate the mean and the standard deviation and add it to the list
        mean_killed = np.mean(list_killed_herring)
        list_mean_killed.append(mean_killed)
        std_killed = np.std(list_killed_herring)
        list_std_killed.append(std_killed)

    # Make a plot of the average number of rilled herring vs the number of rocks
    plot = plt.errorbar(list_alignment_distance, list_mean_killed, yerr=list_std_killed, fmt='o', color='purple', markerfacecolor='blue', label='avarage killed herring + 1 SD')
    plt.xlabel('Alignment distance')
    plt.ylabel('Average killed herring')
    plt.title('The average killed herring + 1 SD errorbars at different alignment distances ')
    plt.ylim(bottom=0)
    plt.legend()
    plt.show()


def influence_school_size(number_simulations):
    """
    Function that makes a violinplot of the distribution of the killed herring
    for two sizes of fish schools in an environment with and without rocks.
    The starting number of  predators to 1. ........

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind
    """

    # Make empty dataframe with three columns
    column_names = ['School size', 'Killed herring', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # Do a number of simulation without rocks and with 100 herring
    for simulation in range(number_simulations):
        print('Simulation without rocks and with 100 herring', simulation)
        experiment = Experiment(100, 1, 0, 20, True, True, False)
        number_killed_herring, _ = experiment.run()
        new_row = pd.DataFrame([{'School size': 100, 'Killed herring': number_killed_herring , 'Rocks':'no'}])
        df = pd.concat([df, new_row], ignore_index=True)

    # Do a number of simulations with rocks and with 100 herring
    for simulation in range(number_simulations):
        print('Simulation with rocks and with 100 herring', simulation)
        experiment = Experiment(100, 1, 20, 20, True, True, False)
        number_killed_herring, _ = experiment.run()
        new_row = pd.DataFrame([{'School size': 100, 'Killed herring': number_killed_herring , 'Rocks':'yes'}])
        df = pd.concat([df, new_row], ignore_index=True)

    # Do a number of simulation without rocks and with 200 herring
    for simulation in range(number_simulations):
        experiment = Experiment(200, 1, 0, 20, True, True, False)
        number_killed_herring, _ = experiment.run()
        new_row = pd.DataFrame([{'School size': 200, 'Killed herring': number_killed_herring , 'Rocks':'no'}])
        df = pd.concat([df, new_row], ignore_index=True)

    # Do a number of simulations with rocks and with 200 herring
    for simulation in range(number_simulations):
        print('Simulation with rocks and and with 200 herring', simulation)
        experiment = Experiment(200, 1, 20, 20, True, True, False)
        number_killed_herring, _ = experiment.run()
        new_row = pd.DataFrame([{ 'School size': 200, 'Killed herring': number_killed_herring , 'Rocks':'yes'}])
        df = pd.concat([df, new_row], ignore_index=True)

    # Do a statistical test
    significant_test_school_size(df)

    # Determine the colors for the plots
    colors_box = {'yes': 'peachpuff', 'no': 'lavender'}
    colors_strip = {'yes': 'red' , 'no': 'blue'}

    # Make a figure in which both the boxplot an stripplot are plotted
    plt.figure(figsize=(10, 6))
    boxplot = sns.boxplot(x='School size', y='Killed herring', hue='Rocks', data=df, palette=colors_box, width=0.8, dodge=True)
    stripplot = sns.stripplot(x='School size', y='Killed herring', hue='Rocks', data=df, dodge=True, palette=colors_strip)
    plt.title('Distribution of the killed herring in a big and small herring school in an environment with and without rocks')
    plt.ylim(bottom=0)

    # Make a legend
    handles, labels = stripplot.get_legend_handles_labels()
    plt.legend(handles[0:2], labels[0:2], title='Rocks', loc='upper right')

    plt.show()

def significant_test_school_size(df):
    """Function that determines if there is a significant difference in killed
    herring between a large and small school. It is tested in an envionment with
    and without rocks

    Parameters:
    -----------
    df: Dataframe
        Datafframe with the values obtaint from the simulated experiments
    """
    df['Killed herring'] = pd.to_numeric(df['Killed herring'], errors='coerce')

    # Extract the killing values for the small and larg school in environment with rocks
    values_small_school_rocks = df.loc[(df['School size'] == 100) & (df['Rocks'] == 'yes'), 'Killed herring']
    values_large_school_rocks = df.loc[(df['School size'] == 200) & (df['Rocks'] == 'yes'), 'Killed herring']

    # Determine if the data is normally distributed
    statistic_small_school_rocks, p_value_small_school_rocks = shapiro(values_small_school_rocks)
    statistic_large_school_rocks, p_value_large_school_rocks = shapiro(values_large_school_rocks)

    # Check if both data is normally distributed to determine the statistic test
    if  p_value_large_school_rocks >= 0.05 and  p_value_small_school_rocks >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_small_school_rocks, values_large_school_rocks)
        print(f'Small vs large school in environment with rocks. T-Statistic: {t_statistic}, p-Value: {p_value}')

    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_small_school_rocks, values_large_school_rocks)
        print(f'Small vs large school in environment with rocks. Mann-Whitney U Statistic: {mw_statistic}, p-Value: {p_value}')

    # Extract the killing values for the small and larg school in environment without rocks
    values_small_school_no_rocks = df.loc[(df['School size'] == 100) & (df['Rocks'] == 'no'), 'Killed herring']
    values_large_school_no_rocks = df.loc[(df['School size'] == 200) & (df['Rocks'] == 'no'), 'Killed herring']

    # Determine if the data is normally distributed
    statistic_small_school_no_rocks, p_value_small_school_no_rocks = shapiro(values_small_school_no_rocks)
    statistic_large_school_no_rocks, p_value_large_school_no_rocks = shapiro(values_large_school_no_rocks)

    # Check if both data is normally distributed to determine the statistic test
    if  p_value_large_school_no_rocks >= 0.05 and  p_value_small_school_no_rocks >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_small_school_no_rocks, values_large_school_no_rocks)
        print(f'Small vs large school in environment with rocks. T-Statistic: {t_statistic}, p-Value: {p_value}')

    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_small_school_no_rocks, values_large_school_no_rocks)
        print(f'Small vs large school in environment with rocks. Mann-Whitney U Statistic: {mw_statistic}, p-Value: {p_value}')

def influence_predators_close_distance(number_simulations):
    """
    Function that makes a violinplot of the distribution of the killed herring
    for two sizes of fish schools in an environment with and without rocks.
    The starting number of predators to 1. ........

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind
    """

    # Make empty dataframe with three columns
    column_names = ['Predator', 'Times within close distance']
    df = pd.DataFrame(columns=column_names)

    # Do a number of simulation without rocks and with 100 herring
    for simulation in range(number_simulations):
        print('Simulation', simulation)

        # Simulation without predators
        experiment = Experiment(100, 0, 0, 30, True, True, False)
        _, close_herring = experiment.run()
        new_row = pd.DataFrame([{'Predator': 'no', 'Times within close distance': close_herring}])
        df = pd.concat([df, new_row], ignore_index=True)

        # Simulation with predators
        experiment = Experiment(100, 1, 0, 30, True, True, False)
        _, close_herring = experiment.run()
        new_row = pd.DataFrame([{'Predator': 'yes', 'Times within close distance': close_herring}])
        df = pd.concat([df, new_row], ignore_index=True)

    # Do a statistical test
    significant_test_close(df)

    # Determine the colors for the plots
    colors_box = {'yes': 'peachpuff', 'no': 'lavender'}
    colors_strip = {'yes': 'red', 'no': 'blue'}

    # # Set Seaborn style
    # sns.set(style="whitegrid")

    # Make a figure in which both the boxplot an stripplot are plotted
    plt.figure(figsize=(10, 6))
    boxplot = sns.boxplot(x='Predator', y='Times within close distance', data=df, palette=colors_box, width=0.6)
    stripplot = sns.stripplot(x='Predator', y='Times within close distance', data=df, palette=colors_strip, jitter=0.2, dodge=True)

    plt.title('Times herring are within 0.5 of the separation distance of each other with and without a predator')
    plt.xlabel('Predator Presence')
    plt.ylabel('Times within Close Distance')
    plt.show()

def significant_test_close(df):
    """Function that determines if there is a significant difference in killed
    herring between a large and small school. It is tested in an envionment with
    and without rocks

    Parameters:
    -----------
    df: Dataframe
        Datafframe with the values obtaint from the simulated experiments
    """
    df['Times within close distance'] = pd.to_numeric(df['Times within close distance'], errors='coerce')

    # Extract the killing values for the small and larg school in environment with rocks
    values_no_predator = df.loc[(df['Predator'] == 'no'), 'Times within close distance']
    values_predator = df.loc[(df['Predator'] == 'yes'), 'Times within close distance']

    # Determine if the data is normally distributed
    statistic_no_predator, p_value_no_predator = shapiro(values_no_predator)
    statistic_predator, p_value_predator = shapiro(values_predator)

    # Check if both data is normally distributed to determine the statistic test
    if  p_value_predator >= 0.05 and  p_value_no_predator >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_no_predator, values_predator)
        print(f'Small vs large school in environment with rocks. T-Statistic: {t_statistic}, p-Value: {p_value}')

    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_no_predator, values_predator)
        print(f'Small vs large school in environment with rocks. Mann-Whitney U Statistic: {mw_statistic}, p-Value: {p_value}')


def influence_perception_length_predator(number_simulations):
    """
    Function that makes a plot of the average killed herring + 1 SD errorbars whereby
    the perception length of the predator changes over the time. In the environment are
    rocks and 1 predator.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind
    """
    data_array_killed_herring = np.empty((number_simulations, 24))

    # Simulate a number of experimens
    for simulation in range(0, number_simulations):
        print('nr simulation', simulation)
        experiment = Experiment(150, 1, 10, 240, True, True, True)
        list_killed_herring, list_predator_perception_length = experiment.run()
        data_array_killed_herring[simulation, :] = list_killed_herring

    # Calculate mean and standard deviation for each column
    mean_killed_herring_array = np.mean(data_array_killed_herring, axis=0)
    std_killed_herring_array = np.std(data_array_killed_herring, axis=0)

    # Determine the time values
    time_values = list(range(len(list_predator_perception_length)))

    # Make a plot
    fig, ax = plt.subplots()
    ax.errorbar(time_values, mean_killed_herring_array, yerr= std_killed_herring_array, fmt='o', label=' average killed herring + 1 SD', color='purple', markerfacecolor='blue')
    plt.step(x= time_values, y= list_predator_perception_length, label='perception leght', color= 'pink', where='post')
    ax.set_xticks(time_values)
    ax.set_xlabel('Time')
    ax.set_ylabel('killed herring/ perception length')
    ax.set_title('Average killed herring + 1 SD errorbars when the perception length of the predator changes')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    """
    The parameters that have to be given:
    1: The number of herring in the simulation (int). default set to one hunderd.
    2: The number of predators in the simulation (int). Default set to one.
    3: The number of rocks in the simulation (int). default set to ten.
    4: The duration of the simulation in seconds (int). Defaut set to twenty.
    5: Closeby rocks should be connected via more rocks (Bool). Default set to False.
    6: Herring start as one school instead of randomly (bool). Default set to False.
    7: Predator perception length changes over the time (bool). Default set to False.
    8: The alignment distance (float). Default set to 32.
    9: The cohestion distance (float). Default set to 32.
    10: The separation distance (float). Default set to 6.
    """
    # # Determine the influence of rocks on the predator killing rate
    # influence_rocks(3)
    # #
    # # Determin the invluence of more predators
    # influence_predator_number(6, 3)
    # #
    # # Determine the influence of the scoolsize
    # influence_school_size(3)
    #
    # # Determine the influence of the alignment distance
    # influence_alignment_distance(3)

    # Determine the influence of a change in the perception length
    influence_perception_length_predator(3)

    # Determine if predator causes panic
    influence_predators_close_distance(3)

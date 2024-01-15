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

# import packages
import pygame
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pandas as pd
from itertools import combinations
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

    # make empty dataframe with three columns
    column_names = ['Nr predators', 'Killed herring', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # loop over the number of predators
    for number_predators in range(1, max_number_predators+1):
        print('Nr predators', number_predators)

        # do a number of simulation without rocks
        for simulation in range(number_simulations):
            print('Simulation without rocks', simulation)

            # set up a experiment, run it and determin the number of killed herring
            experiment = Experiment(100, number_predators, 0, 10, True)
            number_killed_herring = experiment.run()

            # make a new row with the found values and add it to the dataframe
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': number_killed_herring , 'Rocks':'no'}])
            df = pd.concat([df, new_row], ignore_index=True)

        # do a number of simulations with rocks
        for simulation in range(number_simulations):
            print('Simulation with rocks', simulation)

            # set up a experiment, run it and determin the number of killed herring
            experiment = Experiment(100, number_predators, 20, 10, True)
            number_killed_herring = experiment.run()

            # make a new row with the found values and add it to the datafram
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': number_killed_herring , 'Rocks':'yes'}])
            df = pd.concat([df, new_row], ignore_index=True)

    # make a violin plot
    sns.violinplot(data=df, x= 'Nr predators', y= 'Killed herring', hue= 'Rocks', split=True, gap=.1, inner="quart")

    # make sure the y-axis does not go below zero because it is not possible
    # that a negative nober of herring is killed
    plt.ylim(bottom=0)

    # give the plot a title
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
    # make a list for the number of rocks
    list_rock_number =[]

    # make a list for the average killed herrings and the standard deviation
    list_mean_killed =[]
    list_std_killed = []

    # simulate the simulation with different number of rocks
    for number_rock in range(0, 10, 100):
        print('nr rock', number_rock)
        list_rock_number.append(number_rock)

        list_killed_herring = []

        # repeat the simulation a number of times
        for simulation in range(number_simulations):
            print('simulation', simulation)
            experiment = Experiment(10, number_rock, 1, 30, True, True, False, 40, 40, 15)

            # determine the nuber of killed herring and all it to a list
            number_killed_herring = experiment.run()
            list_killed_herring.append(number_killed_herring)

        # calculate the mean and the standard deviation and add it to the list
        mean_killed = np.mean(list_killed_herring)
        list_mean_killed.append(mean_killed)
        std_killed = np.std(list_killed_herring)
        list_std_killed.append(std_killed)

    # make a plot of the average number of rilled herring vs the number of rocks
    plot = plt.errorbar(list_rock_number, list_mean_killed, yerr=list_std_killed, fmt='o', color='orange', markerfacecolor='red', label='avarage killed herring + 1 SD')

    # make plot clear
    plt.xlabel('Number or rocks')
    plt.ylabel('Average killed herring')
    plt.title('The average killed herring + 1 SD errorbars in a environment with differnt numbers of rocks')

    # make sure the y-axis does not go below zero because it is not possible t
    # hat a negative nober of herring is killed
    plt.ylim(bottom=0)

    # add legend
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
    # make a list for the alignmnet distance
    list_alignment_distance = []

    # make a list for the average killed herring and for the standard deviation
    list_mean_killed =[]
    list_std_killed = []

    # simulate the simulation with different alignment distances
    for alignment_distance in range(5, 40, 5):
        print('alignment distance', alignment_distance)
        list_alignment_distance.append(alignment_distance)

        list_killed_herring = []

        # repeat the simulation a number of times
        for simulation in range(number_simulations):
            print('simulation', simulation)
            experiment = Experiment(100, 1, 20, 20, True, True, False, alignment_distance, 10, 5)

            # determine the nuber of killed herring and all it to a list
            number_killed_herring = experiment.run()
            list_killed_herring.append(number_killed_herring)

        # calculate the mean and the standard deviation and add it to the list
        mean_killed = np.mean(list_killed_herring)
        list_mean_killed.append(mean_killed)
        std_killed = np.std(list_killed_herring)
        list_std_killed.append(std_killed)

    # make a plot of the average number of rilled herring vs the number of rocks
    plot = plt.errorbar(list_alignment_distance, list_mean_killed, yerr=list_std_killed, fmt='o', color='purple', markerfacecolor='blue', label='avarage killed herring + 1 SD')

    # make plot clear
    plt.xlabel('Alignment distance')
    plt.ylabel('Average killed herring')
    plt.title('The average killed herring + 1 SD errorbars at different alignment distances ')

    # make sure the y-axis does not go below zero because it is not possible t
    # hat a negative nober of herring is killed
    plt.ylim(bottom=0)

    # add legend
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

    # make empty dataframe with three columns
    column_names = ['School size', 'Killed herring', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # do a number of simulation without rocks and with 100 herring
    for simulation in range(number_simulations):
        print('Simulation without rocks and with 100 herring', simulation)

        # set up a experiment, run it and determin the number of killed herring
        experiment = Experiment(80, 1, 0, 20, True, True, False,40, 40, 15)
        number_killed_herring = experiment.run()

        # make a new row with the found values and add it to the dataframe
        new_row = pd.DataFrame([{'School size': 80, 'Killed herring': number_killed_herring , 'Rocks':'no'}])
        df = pd.concat([df, new_row], ignore_index=True)

    # do a number of simulations with rocks and with 100 herring
    for simulation in range(number_simulations):
        print('Simulation with rocks and with 100 herring', simulation)

        # set up a experiment, run it and determin the number of killed herring
        experiment = Experiment(80, 1, 20, 20, True, True, False, 40, 40, 15)
        number_killed_herring = experiment.run()

        # make a new row with the found values and add it to the datafram
        new_row = pd.DataFrame([{'School size': 80, 'Killed herring': number_killed_herring , 'Rocks':'yes'}])
        df = pd.concat([df, new_row], ignore_index=True)

    # do a number of simulation without rocks and with 200 herring
    for simulation in range(number_simulations):
        print('Simulation without rocks and with 200 herring', simulation)

        # set up a experiment, run it and determin the number of killed herring
        experiment = Experiment(300, 1, 0, 20, True, True, False, 40, 40, 15)
        number_killed_herring = experiment.run()

        # make a new row with the found values and add it to the dataframe
        new_row = pd.DataFrame([{'School size': 500, 'Killed herring': number_killed_herring , 'Rocks':'no'}])
        df = pd.concat([df, new_row], ignore_index=True)

    # do a number of simulations with rocks and with 200 herring
    for simulation in range(number_simulations):
        print('Simulation with rocks and and with 200 herring', simulation)

        # set up a experiment, run it and determin the number of killed herring
        experiment = Experiment(300, 1, 20, 20, True, True, False, 40, 40, 15)
        number_killed_herring = experiment.run()

        # make a new row with the found values and add it to the datafram
        new_row = pd.DataFrame([{ 'School size': 500, 'Killed herring': number_killed_herring , 'Rocks':'yes'}])
        df = pd.concat([df, new_row], ignore_index=True)

    # do a statistical test
    # significant_test_school_size(df)

    # determine the colors for the
    colors_box = {'yes': 'peachpuff', 'no': 'lavender'}
    colors_strip = {'yes': 'red' , 'no': 'blue'}

    # make a figure in which both the boxplot an stripplot are plotted
    plt.figure(figsize=(10, 6))

    # Create the boxplot of all the datapoints
    boxplot = sns.boxplot(x='School size', y='Killed herring', hue='Rocks', data=df, palette=colors_box, width=0.8, dodge=True)

    # make a stripplot of all the datapoints
    stripplot = sns.stripplot(x='School size', y='Killed herring', hue='Rocks', data=df, dodge=True, palette=colors_strip)

    # make a legend
    handles, labels = stripplot.get_legend_handles_labels()
    plt.legend(handles[0:2], labels[0:2], title='Rocks', loc='upper right')

    # give title
    plt.title('Distribution of the killed herring in a big and small herring school in an environment with and without rocks')

    # make sure the y-axis does not go below zero because it is not possible t
    # hat a negative nober of herring is killed
    plt.ylim(bottom=0)

    plt.show()

    significant_test_school_size(df)


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

    # extract the killing values for the small and larg school in environment with rocks
    values_small_school_rocks = df.loc[(df['School size'] == 80) & (df['Rocks'] == 'yes'), 'Killed herring']
    values_large_school_rocks = df.loc[(df['School size'] == 500) & (df['Rocks'] == 'yes'), 'Killed herring']


    # determine if the data is normally distributed
    statistic_small_school_rocks, p_value_small_school_rocks = shapiro(values_small_school_rocks)
    statistic_large_school_rocks, p_value_large_school_rocks = shapiro(values_large_school_rocks)

    # check if both data is normally distributed to determine the statistic test
    if  p_value_large_school_rocks >= 0.05 and  p_value_small_school_rocks >= 0.05:

        # both data normally distributed: do a two-sided independet t-test
        t_statistic, p_value = stats.ttest_ind(values_small_school_rocks, values_large_school_rocks)
        print(f'Small vs large school in environment with rocks. T-Statistic: {t_statistic}, p-Value: {p_value}')

    else:
        # data not normally distributed: do a two sided Mann-whitney U test
        mw_statistic, p_value = stats.mannwhitneyu(values_small_school_rocks, values_large_school_rocks)
        print(f'Small vs large school in environment with rocks. Mann-Whitney U Statistic: {mw_statistic}, p-Value: {p_value}')

    # extract the killing values for the small and larg school in environment
    # without rocks
    values_small_school_no_rocks = df.loc[(df['School size'] == 80) & (df['Rocks'] == 'no'), 'Killed herring']
    values_large_school_no_rocks = df.loc[(df['School size'] == 500) & (df['Rocks'] == 'no'), 'Killed herring']

    # determine if the data is normally distributed
    statistic_small_school_no_rocks, p_value_small_school_no_rocks = shapiro(values_small_school_no_rocks)
    statistic_large_school_no_rocks, p_value_large_school_no_rocks = shapiro(values_large_school_no_rocks)

    # check if both data is normally distributed to determine the statistic test
    if  p_value_large_school_no_rocks >= 0.05 and  p_value_small_school_no_rocks >= 0.05:

        # both data normally distributed: do a two-sided independet t-test
        t_statistic, p_value = stats.ttest_ind(values_small_school_no_rocks, values_large_school_no_rocks)
        print(f'Small vs large school in environment with rocks. T-Statistic: {t_statistic}, p-Value: {p_value}')

    else:
        # data not normally distributed: do a two sided Mann-whitney U test
        mw_statistic, p_value = stats.mannwhitneyu(values_small_school_no_rocks, values_large_school_no_rocks)
        print(f'Small vs large school in environment with rocks. Mann-Whitney U Statistic: {mw_statistic}, p-Value: {p_value}')


def influence_perception_lenght_predator(number_simulations):
    """
    Function that makes a plot of the average killed herring + 1 SD errorbars whereby
    the perception lenght of the predator changes over the time. In the environment are
    rocks and 1 predator.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind
    """

    # make a empty data array
    data_array_killed_herring = np.empty((number_simulations, 24))

    # simulate a number of experimens
    for simulation in range(0, number_simulations):
        print('nr simulation', simulation)

        # run an experiment and add the list with killed herring to the data array
        experiment = Experiment(100, 1, 0, 192, True, False, True)
        list_killed_herring, list_predator_perception_lenght = experiment.run()
        print(list_killed_herring)
        data_array_killed_herring[simulation, :] = list_killed_herring


    # calculate mean and standard deviation for each column
    mean_killed_herring_array = np.mean(data_array_killed_herring, axis=0)
    std_killed_herring_array = np.std(data_array_killed_herring, axis=0)

    # determine the xvalues
    time_values = list(range(len(list_predator_perception_lenght)))

    # make a plot
    fig, ax = plt.subplots()

    # plot the killed herring and perception lenght over the time
    ax.errorbar(time_values, mean_killed_herring_array, yerr= std_killed_herring_array, fmt='o', label=' average killed herring + 1 SD', color='purple', markerfacecolor='blue')
    sns.lineplot(x= time_values, y= list_predator_perception_lenght, label='perception leght', color= 'pink')

    # give plot title and axis labels
    ax.set_xticks(time_values)
    ax.set_xlabel('Time')
    ax.set_ylabel('killed herring/ perception lenght')
    ax.set_title('Average killed herring + 1 SD errorbars when the perception lenght of the predator changes')

    # add a legend
    plt.legend()
    plt.show()


# Run the main function
if __name__ == "__main__":
    """
    The parameters that have to be given:
    1: The number of herring in the simulation (int). default set to one hunderd.
    2: The number of predators in the simulation (int). Default set to one.
    3: The number of rocks in the simulation (int). default set to ten.
    4: The duration of the simulation in seconds (int). Defaut set to twenty.
    5: If clossely placed rocks should be connected via more rocks (Bool). Default
    set to False.
    6: If the herring should start as one big school instead of randomly placed
    (bool). Default set to False.
    7: If the perception lenght of the predator changes over the time (bool).
    Default set to False.
    8: The alignment distance (float). Default set to 40.
    9: The cohestion distance (float). Default set to 40.
    10: The separation distance (float). Default set to 15.

    """

    # # determine the influence of rocks on the predator killing rate
    # influence_rocks(2)
    #
    # # determin the invluence of more predators
    # influence_predator_number(6, 2)
    #
    # # determine the influence of the scoolsize
    # influence_school_size(3)

    # determine the influence of the alignment distance
    influence_alignment_distance(2)

    # determine the influence of a change in the perception lenght
    influence_perception_lenght_predator(5)

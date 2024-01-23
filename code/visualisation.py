"""
Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405
Description:  In this code functions are given that are used to make the plots. The
data for the plots is created by running the experiment (simulation) from gamefish.py
a number of times. The plots show the influence of different factors on the killing
rate of the herrings.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from gamefish import *
from scipy.stats import shapiro
from scipy import stats
import matplotlib.patches as patches

def influence_predator_number(max_number_predators, number_simulations, time_simulation):
    """
    Function that makes a violin plot of the distribution of the killed herring for
    different number of predators in an environment with and without rocks. The
    starting number of herring is set to 100 and the herring start in a school.

    Parameters:
    -----------
    max_number_predators: Int
        The maximum number of predators that is investigated.
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    # Make empty dataframe with three columns
    column_names = ['Nr predators', 'Killed herring', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # Loop over the number of predators
    for number_predators in range(0, max_number_predators+1, 2):
        print('Nr predators', number_predators)

        # Do a number of simulation without rocks and with rocks
        for simulation in range(number_simulations):
            experiment = Experiment(100, number_predators, 0, time_simulation, True, True, False, False)
            values_dict = experiment.run()
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': values_dict['Killed_herring'], 'Rocks':'no'}])
            df = pd.concat([df, new_row], ignore_index=True)

            experiment = Experiment(100, number_predators, 20, time_simulation, True, True, False, False)
            values_dict  = experiment.run()
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': values_dict['Killed_herring'], 'Rocks':'yes'}])
            df = pd.concat([df, new_row], ignore_index=True)

    # Make a violin plot
    sns.violinplot(data=df, x= 'Nr predators', y= 'Killed herring', hue= 'Rocks', split=True, gap=.1, inner="quart")
    plt.xlabel('Number of predators')
    plt.ylim(bottom=0)
    plt.title('Killed herring for different numbers of predators, with and without rocks')
    plt.show()

def influence_rocks(number_simulations, time_simulation):
    """ Function that makes a plot of the average killed herring + 1 SD errorbars in
    an environment with differnt numbers of rocks. The starting number of herring is
    set to 100 and they start in 1 school. There is looked at 1 and 3 predators.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    list_rock_number =[]
    list_mean_killed_1_predator =[]
    list_std_killed_1_predator = []
    list_mean_killed_3_predators =[]
    list_std_killed_3_predators = []

    # Simulate the experiment with different number of rocks
    for number_rock in range(0, 60, 5):
        print('nr rock', number_rock)
        list_rock_number.append(number_rock)

        list_killed_herring_1_predator = []
        list_killed_herring_3_predators = []

        # Repeat the simulation with 1 predator and with 3 predators a number of times
        for simulation in range(number_simulations):
            print('simulation', simulation)
            experiment = Experiment(100, 1, number_rock, time_simulation, True, True, False, False)
            values_dict = experiment.run()
            list_killed_herring_1_predator.append(values_dict['Killed_herring'])

            experiment = Experiment(100, 3, number_rock, time_simulation, True, True, False, False)
            values_dict = experiment.run()
            list_killed_herring_3_predators.append(values_dict['Killed_herring'])

        # Calculate the mean and the standard deviation and add it to the list
        list_mean_killed_1_predator.append(np.mean(list_killed_herring_1_predator))
        list_std_killed_1_predator.append(np.std(list_killed_herring_1_predator))
        list_mean_killed_3_predators.append(np.mean(list_killed_herring_3_predators))
        list_std_killed_3_predators.append(np.std(list_killed_herring_3_predators))

    # Make a plot of the average number of killed herring vs the number of rocks
    plot = plt.errorbar(list_rock_number, list_mean_killed_1_predator, yerr=list_std_killed_1_predator, fmt='o--', color='orange', capsize=4, markerfacecolor='red', label='avarage killed herring + 1 SD, 1 predator')
    plot = plt.errorbar(list_rock_number, list_mean_killed_3_predators, yerr=list_std_killed_3_predators, fmt='o--', color='blue', capsize=4, markerfacecolor='purple', label='avarage killed herring + 1 SD, 3 predators')
    plt.xlabel('Number or rocks')
    plt.ylabel('Average killed herring')
    plt.title('Average killed herring + 1 SD errorbars in environments with different numbers of rocks')
    plt.ylim(bottom=0)
    plt.legend()
    plt.show()

def influence_alignment_distance(number_simulations, time_simulation):
    """Function that makes a plot of the average killed herring + 1 SD errorbars for
    different values of the alignment distance. The starting number of herring is set
    to 100 and that of the predators to 1. It is tested in an envionment with rocks.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    list_alignment_distance = []
    list_mean_killed =[]
    list_std_killed = []

    # Simulate the experiment with different alignment distances
    for alignment_distance in range(4, 33, 2):
        print('alignment distance', alignment_distance)
        list_alignment_distance.append(alignment_distance)
        list_killed_herring = []

        # Simulate the experiment a number of times
        for simulation in range(number_simulations):
            print('simulation', simulation)
            experiment = Experiment(100, 1, 20, time_simulation, True, True, False, False, alignment_distance)
            values_dict = experiment.run()
            list_killed_herring.append(values_dict['Killed_herring'])

        # Calculate the mean and the standard deviation and add it to the list
        list_mean_killed.append(np.mean(list_killed_herring))
        list_std_killed.append(np.std(list_killed_herring))

    # Make a plot of the average number of killed herring vs the alignment distance
    plot = plt.errorbar(list_alignment_distance, list_mean_killed, yerr=list_std_killed, fmt='o--', color='purple', markerfacecolor='blue', label='avarage killed herring + 1 SD', capsize=4)
    plt.xlabel('Alignment distance')
    plt.ylabel('Average killed herring')
    plt.title('The average killed herring + 1 SD errorbars at different alignment distances')
    plt.ylim(bottom=0)
    plt.legend()
    plt.show()


def influence_school_size(number_simulations, time_simulation):
    """Function that makes a boxplot and scatterplot of the distribution of the
    killed herring for two sizes of fish schools in an environment with and without
    rocks. The starting number of predators is 1. It also does a significance test.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    # Make empty dataframe with three columns
    column_names = ['School size', 'Killed herring', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # Do a number of simulations
    for simulation in range(number_simulations):
        print('Simulation ', simulation)
        # Do a number of simulations without rocks and with 100 herring
        experiment = Experiment(100, 1, 0, time_simulation, True, True, False, False)
        values_dict = experiment.run()
        new_row = pd.DataFrame([{'School size': 100, 'Killed herring': values_dict['Killed_herring'], 'Rocks':'no'}])
        df = pd.concat([df, new_row], ignore_index=True)

        # Do a number of simulations with rocks and with 100 herring
        experiment = Experiment(100, 1, 20, time_simulation, True, True, False, False)
        values_dict = experiment.run()
        new_row = pd.DataFrame([{'School size': 100, 'Killed herring': values_dict['Killed_herring'], 'Rocks':'yes'}])
        df = pd.concat([df, new_row], ignore_index=True)

        # Do a number of simulation without rocks and with 200 herring
        experiment = Experiment(200, 1, 0, time_simulation, True, True, False, False)
        values_dict = experiment.run()
        new_row = pd.DataFrame([{'School size': 200, 'Killed herring': values_dict['Killed_herring'], 'Rocks':'no'}])
        df = pd.concat([df, new_row], ignore_index=True)

        # Do a number of simulations with rocks and with 200 herring
        experiment = Experiment(200, 1, 20, time_simulation, True, True, False, False)
        values_dict = experiment.run()
        new_row = pd.DataFrame([{ 'School size': 200, 'Killed herring': values_dict['Killed_herring'], 'Rocks':'yes'}])
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
    plt.title('Killed herring in large and small schools in an environment with and without rocks')
    plt.xlabel('Herring school size')
    plt.ylim(bottom=0)

    # Make a legend
    handles, labels = stripplot.get_legend_handles_labels()
    plt.legend(handles[0:2], labels[0:2], title='Rocks', loc='upper right')

    plt.show()

def significant_test_school_size(df):
    """Function that determines if there is a significant difference in killed
    herring between a large and small school in environment with and without rocks.

    Parameters:
    -----------
    df: Dataframe
        Datafframe with the values obtaint from the simulated experiments.
    """
    df['Killed herring'] = pd.to_numeric(df['Killed herring'], errors='coerce')

    # Extract the killing values for the small and larg school
    values_small_school_rocks = df.loc[(df['School size'] == 100) & (df['Rocks'] == 'yes'), 'Killed herring']
    values_large_school_rocks = df.loc[(df['School size'] == 200) & (df['Rocks'] == 'yes'), 'Killed herring']
    values_small_school_no_rocks = df.loc[(df['School size'] == 100) & (df['Rocks'] == 'no'), 'Killed herring']
    values_large_school_no_rocks = df.loc[(df['School size'] == 200) & (df['Rocks'] == 'no'), 'Killed herring']

    # Determine if the data is normally distributed
    statistic_small_school_rocks, p_value_small_school_rocks = shapiro(values_small_school_rocks)
    statistic_large_school_rocks, p_value_large_school_rocks = shapiro(values_large_school_rocks)
    statistic_small_school_no_rocks, p_value_small_school_no_rocks = shapiro(values_small_school_no_rocks)
    statistic_large_school_no_rocks, p_value_large_school_no_rocks = shapiro(values_large_school_no_rocks)

    # Influence school size in environment with rocks. Check if both data is normally
    # distributed to determine the statistic test
    if  p_value_large_school_rocks >= 0.05 and  p_value_small_school_rocks >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_small_school_rocks, values_large_school_rocks)
        print(f'Small vs large school in environment with rocks. T-Statistic: {t_statistic}, p-Value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_small_school_rocks, values_large_school_rocks)
        print(f'Small vs large school in environment with rocks. Mann-Whitney U Statistic: {mw_statistic}, p-Value: {p_value}')

    # Influence school size in environment without rocks. Check if both data is normally
    # distributed to determine the statistic test
    if  p_value_large_school_no_rocks >= 0.05 and  p_value_small_school_no_rocks >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_small_school_no_rocks, values_large_school_no_rocks)
        print(f'Small vs large school in environment with rocks. T-Statistic: {t_statistic}, p-Value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_small_school_no_rocks, values_large_school_no_rocks)
        print(f'Small vs large school in environment with rocks. Mann-Whitney U Statistic: {mw_statistic}, p-Value: {p_value}')


def influences_closeness_herring(number_simulations, time_simulation):
    """Function that makes a boxplot and scatterplot of the distribution of herring
    within the seperation distance of 6 for different seperation distances and by
    introducing 2 predators. The starting number of herring is set to 100 and the
    herring start in a school. It also does a significance test.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    # Make empty dataframe with two columns
    column_names = ['Predator and separation distance', 'Times within separation distance']
    df = pd.DataFrame(columns=column_names)

    # Do a number of simulation without rocks and with 100 herring
    for simulation in range(number_simulations):
        print('Simulation', simulation)

        # Simulation with no predators, no rocks and default seperation distance (6)
        experiment = Experiment(100, 0, 0, time_simulation, True, True, False, False, 32, 32, 6)
        values_dict = experiment.run()
        new_row = pd.DataFrame([{'Predator and separation distance': 'no p + no r + s d = 6', 'Times within separation distance': values_dict['Herring_within_separation_distance']}])
        df = pd.concat([df, new_row], ignore_index=True)

        # Simulation with no predators, 20 rocks and default seperation distance (6)
        experiment = Experiment(100, 0, 20, time_simulation, True, True, False, False, 32, 32, 6)
        values_dict = experiment.run()
        new_row = pd.DataFrame([{'Predator and separation distance': 'no p + 20 r + s d = 6', 'Times within separation distance': values_dict['Herring_within_separation_distance']}])
        df = pd.concat([df, new_row], ignore_index=True)

        # Simulation with 2 predators, no rocks and default seperation distance (6)
        experiment = Experiment(100, 2, 0, time_simulation, True, True, False, False, 32, 32, 6)
        values_dict = experiment.run()
        new_row = pd.DataFrame([{'Predator and separation distance': '2 p + no r + s d = 6', 'Times within separation distance': values_dict['Herring_within_separation_distance']}])
        df = pd.concat([df, new_row], ignore_index=True)

        # simulation with no predators, no rocks and a seperation distance of 3
        experiment = Experiment(100, 0, 0, time_simulation, True, True, False, False, 32, 32, 3)
        values_dict = experiment.run()
        new_row = pd.DataFrame([{'Predator and separation distance': 'no p + no r + s d = 3', 'Times within separation distance': values_dict['Herring_within_separation_distance']}])
        df = pd.concat([df, new_row], ignore_index=True)

        # Simulation with no predators, no rocks and a seperation distance of 12
        experiment = Experiment(100, 0, 0, time_simulation, True, True, False, False, 32, 32, 12)
        values_dict = experiment.run()
        new_row = pd.DataFrame([{'Predator and separation distance': 'no p + no r + s d = 12', 'Times within separation distance': values_dict['Herring_within_separation_distance']}])
        df = pd.concat([df, new_row], ignore_index=True)

    # Do a statistical test
    significant_test_close(df)

    # Determine the colors for the plots
    colors_box = {'no p + no r + s d = 6': 'mistyrose', '2 p + no r + s d = 6': 'paleturquoise', 'no p + 20 r + s d = 6': 'wheat', 'no p + no r + s d = 3':'aquamarine', 'no p + no r + s d = 12': 'plum'}
    colors_strip = {'no p + no r + s d = 6': 'red', '2 p + no r + s d = 6': 'blue', 'no p + 20 r + s d = 6': 'darkorange', 'no p + no r + s d = 3':'green', 'no p + no r + s d = 12': 'purple'}

    # Make a figure in which both the boxplot an stripplot are plotted
    plt.figure(figsize=(10, 6))
    boxplot = sns.boxplot(x='Predator and separation distance', y='Times within separation distance', hue = 'Predator and separation distance', data=df, palette=colors_box, width=0.6, legend=False)
    stripplot = sns.stripplot(x='Predator and separation distance', y='Times within separation distance', hue = 'Predator and separation distance',  data=df, palette=colors_strip, legend=False)

    # Add legend
    ax = plt.gca()
    ax.text(0.01, 0.965, 'p = predator', transform=ax.transAxes, color='black', fontsize=10)
    ax.text(0.01, 0.93, 'r = rock', transform=ax.transAxes, color='black', fontsize=10)
    ax.text(0.01, 0.9, 's d = separation distance', transform=ax.transAxes, color='black', fontsize=10)

    # Set background color for the legend area
    background = patches.Rectangle((-0.04, 0.88), 0.3, 2, edgecolor='black', facecolor='lightcyan', transform=ax.transAxes)
    ax.add_patch(background)

    plt.title('Herring count within the original separation distance (6) across various conditions.')
    plt.xlabel('Enviromental situation')
    plt.ylabel('Times within original seperation distance (6)')
    plt.show()

def significant_test_close(df):
    """Function that determines if there is a significant difference in herring
    within the perception distance of 6 when the perception distance changes and
    when a preadator gets introduced. It is tested in an envionment without rocks.

    Parameters:
    -----------
    df: Dataframe
        Datafframe with the values obtaint from the simulated experiments.
    """
    df['Times within separation distance'] = pd.to_numeric(df['Times within separation distance'], errors='coerce')

    # Extract the killing values for the different environments
    values_no_p_6_no_r = df.loc[(df['Predator and separation distance'] == 'no p + no r + s d = 6'), 'Times within separation distance']
    values_no_p_6_r = df.loc[(df['Predator and separation distance'] == 'no p + 20 r + s d = 6'), 'Times within separation distance']
    values_p_6_no_r = df.loc[(df['Predator and separation distance'] == '2 p + no r + s d = 6'), 'Times within separation distance']
    values_no_p_3_no_r = df.loc[(df['Predator and separation distance'] == 'no p + no r + s d = 3'), 'Times within separation distance']
    values_no_p_12_no_r = df.loc[(df['Predator and separation distance'] == 'no p + no r + s d = 12'), 'Times within separation distance']

    # Determine if the data is normally distributed
    statistic_no_p_6_no_r, p_value_no_p_6_no_r = shapiro(values_no_p_6_no_r)
    statistic_no_p_6_r, p_value_no_p_6_r = shapiro(values_no_p_6_r)
    statistic_p_6_no_r, p_value_p_6_no_r = shapiro(values_p_6_no_r)
    statistic_no_p_3_no_r, p_value_no_p_3_no_r = shapiro(values_no_p_3_no_r)
    statistic_no_p_12_no_r, p_value_no_p_12_no_r = shapiro(values_no_p_12_no_r)

    # Determine if introducing predators has significant influence. Check if both data
    # is normally distributed to determine the statistic test
    if p_value_no_p_6_no_r >= 0.05 and p_value_p_6_no_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_no_p_6_no_r, values_p_6_no_r)
        print(f'Effect introduction predators. T-Statistic: {t_statistic}, p-value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_no_p_6_no_r, values_p_6_no_r)
        print(f'Effect introduction predators. Mann-Whitney U Statistic: {mw_statistic}, p-value: {p_value}')

    # Determine if introducing rocks has significant influence. Check if both data
    # is normally distributed to determine the statistic test
    if p_value_no_p_6_no_r >= 0.05 and p_value_no_p_6_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_no_p_6_no_r, values_no_p_6_r)
        print(f'Effect introduction rocks. T-Statistic: {t_statistic}, p-value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_no_p_6_no_r, values_no_p_6_r)
        print(f'Effect introduction rocks. Mann-Whitney U Statistic: {mw_statistic}, p-value: {p_value}')

    # Determine if a lower seperation distance has a significant influence. Check if
    # both data is normally distributed to determine the statistic test
    if p_value_no_p_6_no_r >= 0.05 and p_value_no_p_3_no_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_no_p_6_no_r, values_no_p_3_no_r)
        print(f'Effect smaller separation distance. T-Statistic: {t_statistic}, p-Value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_no_p_6_no_r, values_no_p_3_no_r)
        print(f'Effect smaller separation distance. Mann-Whitney U Statistic: {mw_statistic}, p-value: {p_value}')

    # Determine if a higher seperation distance has a significant influence. Check if
    # both data is normally distributed to determine the statistic test
    if p_value_no_p_6_no_r >= 0.05 and p_value_no_p_12_no_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_no_p_6_no_r, values_no_p_12_no_r)
        print(f'Effect larger separation distance. T-Statistic: {t_statistic}, p-Value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_no_p_6_no_r, values_no_p_12_no_r)
        print(f'Effect larger separation distance. Mann-Whitney U Statistic: {mw_statistic}, p-value: {p_value}')

def influence_boid_rules(number_simulations, time_simulation):
    """Function that makes a boxplot and scatterplot of the distribution of killed
    herring where differerent boid rules are most important. It also makes a stipplot
    to show the mean and standard deviation.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    data_array_killed_herring = np.empty((number_simulations + 1, 4))

    herring_nr = 150
    predator_nr = 2
    rock_nr = 10
    simulation_duration = time_simulation
    extra_rocks = True
    start_school = True
    perception_change = False

    # Make empty dataframe with two columns
    column_names = ['Boid influence', 'Killed herring']
    df = pd.DataFrame(columns=column_names)

    # Simulate a number of experiments with varying boids_influence values
    for simulation in range(number_simulations):
        print('Simulation', simulation)

        for boids_influence_value in range(0, 4):
            print('Boids Influence Value:', boids_influence_value)
            experiment = Experiment(herring_nr, predator_nr, rock_nr, simulation_duration,
                extra_rocks, start_school, perception_change, boids_influence=boids_influence_value)

            values_dict = experiment.run()
            new_row = pd.DataFrame([{'Boid influence': boids_influence_value, 'Killed herring': values_dict['Killed_herring']}])
            df = pd.concat([df, new_row], ignore_index=True)

    # Determine the colors for the plots and the x-labels
    colors_box = {0: 'mistyrose', 1: 'paleturquoise', 2: 'wheat', 3:'aquamarine'}
    colors_strip = {0: 'red', 1: 'blue', 2: 'darkorange', 3:'green'}
    custom_labels = ['no stronger', 'separation', 'alignment', 'cohesion']

    # Create a boxplot using seaborn
    plt.figure(figsize=(10, 6))
    boxplot = sns.boxplot(x='Boid influence', y='Killed herring', hue = 'Boid influence', data=df, palette=colors_box, width=0.6, legend=False)
    stripplot = sns.stripplot(x='Boid influence', y='Killed herring', hue = 'Boid influence',  data=df, palette=colors_strip, legend=False)
    plt.xticks(ticks=plt.xticks()[0], labels=custom_labels)
    plt.title('Boxplot of killed herring for different boids influence values')
    plt.show()

    # Optionally, you can also plot the mean values
    plt.figure(figsize=(10, 6))
    sns.pointplot(x='Boid influence', y='Killed herring', hue = 'Boid influence', data=df, errorbar='sd', linestyle='none', capsize=0.1, markers='o', palette= colors_strip, legend=False, err_kws={'color': 'black', 'linewidth': 1})
    plt.xticks(ticks=plt.xticks()[0], labels=custom_labels)
    plt.ylabel('Mean Killed Herring')
    plt.title('Average killed herring + 1 SD errorbars for different boid influence values')
    plt.show()

if __name__ == "__main__":
    # Determine the influence of the boid rules
    # influence_boid_rules(5, 10)
    #
    # # Determine the influence of rocks on the killing rate
    # influence_rocks(3, 2)

    # # Determin the invluence of more predators
    # influence_predator_number(10, 3, 10)

    # Determine the influence of the scoolsize
    influence_school_size(3, 5)

    # Determine the influence of the alignment distance
    # influence_alignment_distance(3, 10)

    # Determine what influence if predators are more within the separation distance
    influences_closeness_herring(5, 5)

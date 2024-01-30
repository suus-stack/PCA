"""
Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405
Description:  In this code functions are given that are used to make the plots. The
              data for the plots is created by running the experiment (simulation)
              from gamefish.py a number of times. The plots show the influence of
              different factors on the killing rate of the herring.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from herring_simulation import *
from statistic_tests import *
import matplotlib.patches as patches

def influence_predator_number(max_number_predators, number_simulations, time_simulation):
    """Function that makes a violin plot of the distribution of the killed herring
    for different number of predators in an environment with and without rocks. The
    starting number of herring is set to 200 and the herring start in one school.

    Parameters:
    -----------
    max_number_predators: Int
        The maximum number of predators that is investigated.
    number_simulations: Int
        The number of simulations per experiment type.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    # Make an empty dataframe with three columns
    column_names = ['Nr predators', 'Killed herring', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # Loop over the number of predators
    for number_predators in range(0, max_number_predators+1, 4):
        print('Nr predators:', number_predators)

        # Do a number of simulation without rocks and with rocks
        for simulation in range(number_simulations):
            print('Simulation:', simulation)
            values_dict = Experiment(200, number_predators, 0, time_simulation, True, True, False, False).run()
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': values_dict['Killed_herring'], 'Rocks':'no'}])
            df = pd.concat([df, new_row], ignore_index=True)

            values_dict = Experiment(200, number_predators, 20, time_simulation, True, True, False, False).run()
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': values_dict['Killed_herring'], 'Rocks':'yes'}])
            df = pd.concat([df, new_row], ignore_index=True)

    # Make a violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df, x= 'Nr predators', y= 'Killed herring', hue= 'Rocks', split=True, gap=.1, inner="quart")
    legend = plt.legend(loc='upper left', fontsize=10, title='Rocks')
    plt.xlabel('Number of barracudas', fontsize=11)
    plt.ylabel('Killed herring', fontsize=11)
    plt.ylim(bottom=0)
    plt.title('Killed herring for different numbers of barracudas, with and without rocks')
    plt.show()


def predator_killing_efficiency(max_number_predators, number_simulations, time_simulation):
    """Function that makes a line plot of the average number of killed herring per
    predator + 1 SD error bars when the number of predators increases in an environment
    with and without rocks. The starting number of herring is set to 200 and the herring
    start in one school.

    Parameters:
    -----------
    max_number_predators: Int
        The maximum number of predators that is investigated.
    number_simulations: Int
        The number of simulations per experiment type.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    # Make an empty dataframe with three columns
    column_names = ['Nr predators', 'Killed herring per predator', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # Loop over the number of predators
    for number_predators in range(1, max_number_predators+1, 4):
        print('Nr predators:', number_predators)

        # Do a number of simulation without rocks and with rocks
        for simulation in range(number_simulations):
            print('Simulation:', simulation)
            values_dict = Experiment(200, number_predators, 0, time_simulation, True, True, False, False).run()
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring per predator': values_dict['Killed_herring']/ number_predators , 'Rocks':'no'}])
            df = pd.concat([df, new_row], ignore_index=True)

            values_dict = Experiment(200, number_predators, 20, time_simulation, True, True, False, False).run()
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring per predator': values_dict['Killed_herring']/ number_predators, 'Rocks':'yes'}])
            df = pd.concat([df, new_row], ignore_index=True)

    # Make a violin plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot with Rocks
    rocks_data = df[df['Rocks'] == 'yes']
    rocks_avg = rocks_data.groupby('Nr predators')['Killed herring per predator'].mean()
    rocks_sd = rocks_data.groupby('Nr predators')['Killed herring per predator'].std()
    ax.errorbar(x=rocks_avg.index, y=rocks_avg, yerr=rocks_sd, label='rocks', linestyle='--', marker='o', capsize=3, color='pink', markerfacecolor='red')

    # Plot without Rocks
    no_rocks_data = df[df['Rocks'] == 'no']
    no_rocks_avg = no_rocks_data.groupby('Nr predators')['Killed herring per predator'].mean()
    no_rocks_sd = no_rocks_data.groupby('Nr predators')['Killed herring per predator'].std()
    ax.errorbar(x=no_rocks_avg.index, y=no_rocks_avg, yerr=no_rocks_sd, label='no rocks', linestyle='--', marker='o', capsize=3, color='blue', markerfacecolor='purple')

    ax.set_xlabel('Number of barracudas', fontsize =11)
    ax.set_ylabel('Killed Herring/ barracuda', fontsize =11)
    ax.set_title('Average killed herring + 1 SD error bars per barracuda, with and without rocks', fontsize =12)
    ax.legend()
    plt.show()



def influence_rocks(max_number_rocks, number_simulations, time_simulation):
    """Function that makes a plot of the average killed herring + 1 SD errorbars in
    an environment with differnt numbers of rocks. The starting number of herring is
    set to 200 and they start in one school. There is looked at 1 and 3 predators.

    Parameters:
    -----------
    max_number_rocks: Int
        The maximum number of rocks that is investigated.
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
    for number_rock in range(0, max_number_rocks+1, 10):
        print('Nr rock:', number_rock)
        list_rock_number.append(number_rock)
        list_killed_herring_1_predator = []
        list_killed_herring_3_predators = []

        # Repeat the simulation with 1 predator and 3 predators a number of times
        for simulation in range(number_simulations):
            print('Simulation:', simulation)
            values_dict = Experiment(200, 1, number_rock, time_simulation, False, True, False, False).run()
            list_killed_herring_1_predator.append(values_dict['Killed_herring'])

            values_dict = Experiment(200, 3, number_rock, time_simulation, False, True, False, False).run()
            list_killed_herring_3_predators.append(values_dict['Killed_herring'])

        # Calculate the mean and the standard deviation and add it to the list
        list_mean_killed_1_predator.append(np.mean(list_killed_herring_1_predator))
        list_std_killed_1_predator.append(np.std(list_killed_herring_1_predator))
        list_mean_killed_3_predators.append(np.mean(list_killed_herring_3_predators))
        list_std_killed_3_predators.append(np.std(list_killed_herring_3_predators))

    # Make a plot of the average number of killed herring vs the number of rocks
    plt.figure(figsize=(10, 6))
    plot = plt.errorbar(list_rock_number, list_mean_killed_1_predator, yerr=list_std_killed_1_predator, fmt='o--', color='orange', capsize=4, markerfacecolor='red', label='avarage killed herring + 1 SD, 1 barracuda')
    plot = plt.errorbar(list_rock_number, list_mean_killed_3_predators, yerr=list_std_killed_3_predators,fmt='o--', color='blue', capsize=4, markerfacecolor='purple', label='avarage killed herring + 1 SD, 3 barracudas')
    plt.xlabel('Number or rocks', fontsize=11)
    plt.ylabel('Average killed herring', fontsize=11)
    plt.title('Average killed herring + 1 SD errorbars in environments with different numbers of rocks')
    plt.ylim(bottom=0)
    plt.legend(fontsize=10)
    plt.show()

def influence_alignment_distance(number_simulations, time_simulation):
    """Function that makes a line plot of the average killed herring + 1 SD errorbars
    for different values of the alignment distance. The starting number of herring is
    set to 200 and that of the predators to 3. It is tested in an envionment with and
    without rocks.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    list_alignment_distance = []
    list_mean_killed_rocks =[]
    list_std_killed_rocks = []
    list_mean_killed_no_rocks =[]
    list_std_killed_no_rocks = []

    # Simulate the experiment with different alignment distances
    for alignment_distance in range(4, 33, 4):
        print('Alignment distance:', alignment_distance)
        list_alignment_distance.append(alignment_distance)
        list_killed_herring_rocks = []
        list_killed_herring_no_rocks = []

        # Simulate the experiments a number of times
        for simulation in range(number_simulations):
            print('Simulation:', simulation)
            values_dict = Experiment(200, 3, 20, time_simulation, True, True, False, False, alignment_distance).run()
            list_killed_herring_rocks.append(values_dict['Killed_herring'])

            values_dict = Experiment(200, 3, 0, time_simulation, True, True, False, False, alignment_distance).run()
            list_killed_herring_no_rocks.append(values_dict['Killed_herring'])

        # Calculate the mean and the standard deviation and add it to the list
        list_mean_killed_rocks.append(np.mean(list_killed_herring_rocks))
        list_std_killed_rocks.append(np.std(list_killed_herring_rocks))
        list_mean_killed_no_rocks.append(np.mean(list_killed_herring_no_rocks))
        list_std_killed_no_rocks.append(np.std(list_killed_herring_no_rocks))

    # Make a plot of the average number of killed herring vs the alignment distance
    plt.subplots(figsize=(10, 6))
    plot1 = plt.errorbar(list_alignment_distance, list_mean_killed_rocks, yerr = list_std_killed_rocks, fmt = 'o--', color = 'purple', markerfacecolor = 'blue', label = 'mean killed h + 1 SD with rocks', capsize = 4)
    plot2 = plt.errorbar(list_alignment_distance, list_mean_killed_no_rocks, yerr = list_std_killed_no_rocks, fmt = 'o--', color = 'red', markerfacecolor = 'pink', label = 'mean killed h + 1 SD without rocks', capsize = 4)
    plt.xlabel('Alignment distance')
    plt.ylabel('Average killed herring')
    plt.title('The average killed herring + 1 SD errorbars at different alignment distances')
    plt.ylim(bottom=0)
    plt.legend()
    plt.show()


def influence_school_size(number_simulations, time_simulation):
    """Function that makes a boxplot with stripplot overlap of the distribution of the
    killed herring for two sizes of fish schools in an environment with and without
    rocks. The starting number of predators is 3. It also does a significance test to
    determine if the school size significantly changes the killing proportion.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.

    Returns:
    -----------
    df_school_size: Dataframe
        The dataframe with the obtained data.
    """
    # Make an empty dataframe with three columns
    column_names = ['School size', 'Proportion killed herring', 'Rocks']
    df_school_size = pd.DataFrame(columns=column_names)

    # Do a number of simulations
    for simulation in range(number_simulations):
        print('Simulation:', simulation)

        # Without rocks and with 200 herring
        values_dict = Experiment(200, 3, 0, time_simulation, True, True, False, False).run()
        new_row = pd.DataFrame([{'School size': 200, 'Proportion killed herring': values_dict['Killed_herring']/200, 'Rocks':'no'}])
        df_school_size = pd.concat([df_school_size, new_row], ignore_index=True)

        # With rocks and with 200 herring
        values_dict = Experiment(200, 3, 20, time_simulation, True, True, False, False).run()
        new_row = pd.DataFrame([{'School size': 200, 'Proportion killed herring': values_dict['Killed_herring']/200, 'Rocks':'yes'}])
        df_school_size = pd.concat([df_school_size, new_row], ignore_index=True)

        # Without rocks and with 400 herring
        values_dict = Experiment(400, 3, 0, time_simulation, True, True, False, False).run()
        new_row = pd.DataFrame([{'School size': 400, 'Proportion killed herring': values_dict['Killed_herring']/400, 'Rocks':'no'}])
        df_school_size  = pd.concat([df_school_size , new_row], ignore_index=True)

        # With rocks and with 400 herring
        values_dict = Experiment(400, 3, 20, time_simulation, True, True, False, False).run()
        new_row = pd.DataFrame([{ 'School size': 400, 'Proportion killed herring': values_dict['Killed_herring']/400, 'Rocks':'yes'}])
        df_school_size = pd.concat([df_school_size , new_row], ignore_index=True)

    # Determine the colors for the plots
    colors_box = {'yes': 'peachpuff', 'no': 'lavender'}
    colors_strip = {'yes': 'red' , 'no': 'blue'}

    # Make a figure in which both the boxplot an stripplot are plotted
    plt.subplots(figsize=(10, 6))
    boxplot = sns.boxplot(x = 'School size', y = 'Proportion killed herring', hue = 'Rocks', data = df_school_size, palette = colors_box, width = 0.8, dodge = True)
    stripplot = sns.stripplot(x = 'School size', y = 'Proportion killed herring', hue = 'Rocks', data = df_school_size, dodge = True, palette = colors_strip)
    plt.title('Proportion killed herring in large and small schools, with and without rocks')
    plt.xlabel('Herring school size')
    plt.ylim(bottom=0)

    # Make a legend
    handles, labels = stripplot.get_legend_handles_labels()
    plt.legend(handles[0:2], labels[0:2], title='Rocks', loc='upper right')
    plt.show()

    return df_school_size

def influences_closeness_herring(number_simulations, time_simulation):
    """Function that makes a boxplot with stripplot overlap of the distribution of
    herring within the separation distance of 6 and the distribution of the herring
    killing rate for different separation distances and by introducing 3 extra
    predators or 20 rocks. The starting number of herring is set to 200 and the
    herring start in a school.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.

    Returns:
    -----------
    df_closeness: Dataframe
        The datframe with the obtained data.
    """
    # Make an empty dataframe with two columns
    column_names = ['Conditions', 'Times within separation distance', 'Killed herring']
    df_closeness = pd.DataFrame(columns=column_names)

    # Do a number of simulation without rocks and with 100 herring
    for simulation in range(number_simulations):
        print('Simulation', simulation)

        # 1 predator, no rocks and the default separation distance (6)
        values_dict = Experiment(200, 1, 0, time_simulation, True, True, False, False, 32, 32, 6).run()
        new_row = pd.DataFrame([{'Conditions': '1 p + no r + s d = 6', 'Times within separation distance': values_dict['Herring_within_separation_distance'], 'Killed herring': values_dict['Killed_herring']}])
        df_closeness = pd.concat([df_closeness, new_row], ignore_index=True)

        # 4 predators, no rocks and the default separation distance (6)
        values_dict = Experiment(200, 4, 0, time_simulation, True, True, False, False, 32, 32, 6).run()
        new_row = pd.DataFrame([{'Conditions': '4 p + no r + s d = 6', 'Times within separation distance': values_dict['Herring_within_separation_distance'], 'Killed herring': values_dict['Killed_herring']}])
        df_closeness = pd.concat([df_closeness, new_row], ignore_index=True)

        # 1 predator, 20 rocks and the default separation distance (6)
        values_dict = Experiment(200, 1, 20, time_simulation, True, True, False, False, 32, 32, 6).run()
        new_row = pd.DataFrame([{'Conditions': '1 p + 20 r + s d = 6', 'Times within separation distance': values_dict['Herring_within_separation_distance'], 'Killed herring': values_dict['Killed_herring']}])
        df_closeness = pd.concat([df_closeness, new_row], ignore_index=True)

        # 1 predator, no rocks and a separation distance of 3
        values_dict = Experiment(200, 1, 0, time_simulation, True, True, False, False, 32, 32, 3).run()
        new_row = pd.DataFrame([{'Conditions': '1 p + no r + s d = 3', 'Times within separation distance': values_dict['Herring_within_separation_distance'], 'Killed herring': values_dict['Killed_herring']}])
        df_closeness = pd.concat([df_closeness, new_row], ignore_index=True)

        # 1 predator, no rocks and a separation distance of 12
        values_dict = Experiment(200, 1, 0, time_simulation, True, True, False, False, 32, 32, 12).run()
        new_row = pd.DataFrame([{'Conditions': '1 p + no r + s d = 12', 'Times within separation distance': values_dict['Herring_within_separation_distance'], 'Killed herring': values_dict['Killed_herring']}])
        df_closeness = pd.concat([df_closeness, new_row], ignore_index=True)

    # Determine the colors for the plots
    colors_box = {'1 p + no r + s d = 6': 'mistyrose', '4 p + no r + s d = 6': 'paleturquoise', '1 p + 20 r + s d = 6': 'wheat', '1 p + no r + s d = 3':'aquamarine', '1 p + no r + s d = 12': 'plum'}
    colors_strip = {'1 p + no r + s d = 6': 'red', '4 p + no r + s d = 6': 'blue', '1 p + 20 r + s d = 6': 'darkorange', '1 p + no r + s d = 3':'green', '1 p + no r + s d = 12': 'purple'}

    fig, axes = plt.subplots(1, 2, figsize=(10, 8))

    # Plot the first plot: density
    boxplot1 = sns.boxplot(x='Conditions', y='Times within separation distance', hue='Conditions', data=df_closeness, palette=colors_box, width=0.6, ax=axes[0])
    stripplot1 = sns.stripplot(x='Conditions', y='Times within separation distance', hue='Conditions', data=df_closeness, palette=colors_strip, ax=axes[0])

    # Add legend and axis labels to the first subplot
    axes[0].text(0.01, 0.965, 'b = barracuda', transform=axes[0].transAxes, color='black', fontsize=10)
    axes[0].text(0.01, 0.93, 'r = rocks', transform=axes[0].transAxes, color='black', fontsize=10)
    axes[0].text(0.01, 0.9, 's d = separation distance', transform=axes[0].transAxes, color='black', fontsize=10)
    background_legend1 = patches.Rectangle((-0.04, 0.88), 0.45, 8, edgecolor='black', facecolor='lightcyan', transform=axes[0].transAxes)
    axes[0].add_patch(background_legend1)
    axes[0].set_xticks([0, 1, 2, 3, 4])
    axes[0].set_xticklabels(['1 b, no r,\ns d = 6', '4 b, no r,\ns d = 6', '1 b, 20 r, \ns d = 6', '1 b, no r,\ns d = 3', '1 b, no r,\ns d = 12'], fontsize=11)
    axes[0].set_title('Herring count within the original separation distance (6)', fontsize=12)
    axes[0].set_xlabel('Environmental situation', fontsize=11)
    axes[0].set_ylabel('Times within original separation distance (6)', fontsize=11)

    # Plot the second subplot: killing rate
    boxplot2 = sns.boxplot(x='Conditions', y='Killed herring', hue='Conditions', data=df_closeness, palette=colors_box, width=0.6, ax=axes[1])
    stripplot2 = sns.stripplot(x='Conditions', y='Killed herring', hue='Conditions', data=df_closeness, palette=colors_strip, ax=axes[1])

    # Add legend and axis labels to the first subplot
    axes[1].text(0.01, 0.965, 'p = predators', transform=axes[1].transAxes, color='black', fontsize=10)
    axes[1].text(0.01, 0.93, 'r = rocks', transform=axes[1].transAxes, color='black', fontsize=10)
    axes[1].text(0.01, 0.9, 's d = separation distance', transform=axes[1].transAxes, color='black', fontsize=10)
    background_legend2 = patches.Rectangle((-0.04, 0.88), 0.45, 8, edgecolor='black', facecolor='lightcyan', transform=axes[1].transAxes)
    axes[1].add_patch(background_legend2)
    axes[1].set_xticks([0, 1, 2, 3, 4])
    axes[1].set_xticklabels(['1 p, no r,\ns d = 6', '4 p, no r,\ns d = 6', '1 p, 20 r, \ns d = 6', '1 p, no r,\ns d = 3', '1 p, no r,\ns d = 12'], fontsize=11)
    axes[1].set_title('Herring killing count', fontsize=12)
    axes[1].set_xlabel('Environmental situation', fontsize=11)
    axes[1].set_ylabel('Killing count', fontsize=11)

    plt.tight_layout()
    plt.show()

    return df_closeness

def influence_boid_rules(number_simulations, time_simulation):
    """Function that makes a boxplot with stripplot overlap of the distribution of
    killed herring when different boid rules are most important. The starting number
    of herring is set to 200 and the herring start in a school.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.

    Returns:
    -----------
    boids_rules_df: Dataframe
        The dataframe with the obtained data.
    """
    data_array_killed_herring = np.empty((number_simulations, 4))

    # Keep other parameters the same for all simulations
    herring_nr = 200
    predator_nr = 3
    rock_nr = 20
    simulation_duration = time_simulation
    extra_rocks = True
    start_school = True

    # Simulate experiments with varying influence of different boids rules
    for simulation in range(number_simulations):
        print('Simulation:', simulation)
        for boids_influence_value in range(4):
            return_values = Experiment(herring_nr, predator_nr, rock_nr, simulation_duration,
                extra_rocks, start_school,boids_influence=boids_influence_value
            ).run()
            print('Boids influence rule:', boids_influence_value)

            data_array_killed_herring[simulation, boids_influence_value] = return_values['Killed_herring']

    boids_rules_df = pd.DataFrame(data_array_killed_herring, columns=['no weighted boid rules', 'weighted separation rule','weighted alignment rule', 'weighted cohesion rule'])

    # Create a boxplot of the different boid rules
    colors_box = ['mistyrose', 'paleturquoise', 'wheat', 'aquamarine']
    colors_strip = ['red', 'blue', 'darkorange', 'green']
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=boids_rules_df, palette=colors_box)
    sns.stripplot(data=boids_rules_df, palette=colors_strip, jitter=0.2, size=5)
    ax = plt.gca()
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['no weighted \n boid rules', 'weighted \n separation rule','weighted\n alignment rule', 'weighted \ncohesion rule'], fontsize=11)
    plt.xlabel('Boids influence', fontsize=15)
    plt.ylabel('Killed herring', fontsize=15)
    plt.title('Boxplot of killed herring for different boid rules', fontsize = 15)
    plt.show()

    return boids_rules_df

def sensitivity_rules_distance(number_simulations, time_simulation):
    """Function that makes a plot of the average killed herring + 1 SD errorbars for
    different alignment, cohesion and separation distances, as sensitivity analyse.
    The starting number of herring is set to 200 and the herring start in one school.
    There are no rocks present.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    list_distance_deviation = []
    list_mean_killed_alignment =[]
    list_std_killed_alignment = []
    list_mean_killed_cohesion =[]
    list_std_killed_cohesion = []
    list_mean_killed_separation =[]
    list_std_killed_separation = []

    # Simulate the experiment with different distance deviations
    for distance_deviation in range(-5, 6):
        print('Deviation of the distance:', distance_deviation)
        list_distance_deviation.append(distance_deviation)
        list_killed_herring_alignment = []
        list_killed_herring_cohesion = []
        list_killed_herring_separation = []

        # Simulate the experiments a number of times
        for simulation in range(number_simulations):
            print('Simulation:', simulation)
            values_dict = Experiment(200, 3, 0, time_simulation, True, True, False, False, 32+distance_deviation, 32, 6).run()
            list_killed_herring_alignment.append(values_dict['Killed_herring'])

            values_dict = Experiment(200, 3, 0, time_simulation, True, True, False, False, 32, 32+distance_deviation, 6).run()
            list_killed_herring_cohesion.append(values_dict['Killed_herring'])

            values_dict = Experiment(200, 3, 0, time_simulation, True, True, False, False, 32, 32, 6+distance_deviation).run()
            list_killed_herring_separation.append(values_dict['Killed_herring'])

        # Calculate the mean and the standard deviation and add it to the list
        list_mean_killed_alignment.append(np.mean(list_killed_herring_alignment))
        list_std_killed_alignment.append(np.std(list_killed_herring_alignment))
        list_mean_killed_cohesion.append(np.mean(list_killed_herring_cohesion))
        list_std_killed_cohesion.append(np.std(list_killed_herring_cohesion))
        list_mean_killed_separation.append(np.mean(list_killed_herring_separation))
        list_std_killed_separation.append(np.std(list_killed_herring_separation))

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Alignment distance
    plot1 = axes[0].errorbar(list_distance_deviation, list_mean_killed_alignment, yerr = list_std_killed_alignment, fmt = 'o--', color = 'blue', markerfacecolor = 'blue', capsize = 4, label = 'average killed h + 1 SD')
    axes[0].set_title('Alignment distance')
    axes[0].set_xlabel('Alignment distance')
    axes[0].set_xticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    axes[0].set_xticklabels(['27', '28','29', '30', '31', '32','33', '34', '35', '36','37'], fontsize=11)

    # Cohesion distance
    plot2 = axes[1].errorbar(list_distance_deviation, list_mean_killed_cohesion, yerr = list_std_killed_cohesion, fmt = 'o--', color = 'red', markerfacecolor = 'red', capsize = 4, label = 'average killed h + 1 SD')
    axes[1].set_title('Cohesion distance')
    axes[1].set_xlabel('Cohesion distance')
    axes[1].set_xticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    axes[1].set_xticklabels(['27', '28','29', '30', '31', '32','33', '34', '35', '36','37'], fontsize=11)

    # Separation distance
    plot3 = axes[2].errorbar(list_distance_deviation, list_mean_killed_separation, yerr = list_std_killed_separation, fmt = 'o--', color = 'green', markerfacecolor = 'green', capsize = 4, label = 'average killed h + 1 SD')
    axes[2].set_title('Separation distance')
    axes[2].set_xlabel('Separation distance')
    axes[2].set_xticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    axes[2].set_xticklabels(['1', '2','3', '4', '5', '6','7', '8', '9', '10','11'], fontsize=11)

    for ax in axes:
        ax.set_ylabel('Average killed herring')
        ax.legend()

    plt.show()

def visualizing_perception_change(number_simulations, time_simulation, number_herring):
    """Function that makes four line plots that show the differences between the
    number of killed herring per time interval (20 sec) for different perception lengths.
    The 4 simulated cases are:
    - Both perception lengths do not change over time and remain their default setting.
    - Solely the herring perception length changes over time.
    - Solely the predator perception length changes over time.
    - Both perception lengths are changed over time, but with a different adaption.
    (2 for herring and 3 for predator) change over time.

    Parameters:
    -----------
    time_simulation: Int
        The number of seconds the simulation runs.
    number_simulations: Int
        The number of simulations per experiment kind.
    number_herring: Int
        The number of herring in the beginning of the simulation
    """
    # Create an empty dataframes
    df_no_change = pd.DataFrame()
    df_predator_change = pd.DataFrame()
    df_herring_change = pd.DataFrame()
    df_both_change = pd.DataFrame()

    for simulation in range(number_simulations):
        print('Simulation:', simulation)
        # No herring and predator perception change
        return_values_dict1 = Experiment(number_herring, 4, 20, time_simulation, True, True, False, False, 32, 32, 6).run()
        new_row_df = pd.DataFrame([np.diff(return_values_dict1['Killed_herring_over_time'])])
        df_no_change = pd.concat([df_no_change, new_row_df], ignore_index=True)
        print('hi')
        # Predator perception change
        return_values_dict2 = Experiment(number_herring, 4, 20, time_simulation, True, True, True, False, 32, 32, 6).run()
        new_row_df = pd.DataFrame([np.diff(return_values_dict2['Killed_herring_count_predator_perception_change'])])
        df_predator_change = pd.concat([df_predator_change, new_row_df], ignore_index=True)
        print('hi')
        # Herring perception change
        return_values_dict3 = Experiment(number_herring, 4, 20, time_simulation, True, True, False, True, 32, 32, 6).run()
        new_row_df = pd.DataFrame([np.diff(return_values_dict3['Killed_herring_count_herring_perception_change'])])
        df_herring_change = pd.concat([df_herring_change, new_row_df], ignore_index=True)
        print('hi')
        # Herring and predator perception change
        return_values_dict4 = Experiment(number_herring, 4, 20, time_simulation, True, True, True, True, 32, 32, 6).run()
        new_row_df = pd.DataFrame([np.diff(return_values_dict4['Killed_herring_count_herring_perception_change'])])
        df_both_change = pd.concat([df_both_change, new_row_df], ignore_index=True)

    # Calculate mean values and 95% CI
    mean_values_no_change = df_no_change.mean(axis=0)
    sem_values_no_change = df_no_change.sem(axis=0)
    ci_values_no_change = 1.96 * sem_values_no_change
    summary_df_no_change = pd.DataFrame({'Mean': mean_values_no_change, 'CI_low': mean_values_no_change - ci_values_no_change, 'CI_high': mean_values_no_change + ci_values_no_change})

    mean_values_predator_change = df_predator_change.mean(axis=0)
    sem_values_predator_change = df_predator_change.sem(axis=0)
    ci_values_predator_change = 1.96 * sem_values_predator_change
    summary_df_predator_change = pd.DataFrame({'Mean': mean_values_predator_change, 'CI_low': mean_values_predator_change - ci_values_predator_change, 'CI_high': mean_values_predator_change + ci_values_predator_change})

    mean_values_herring_change = df_herring_change.mean(axis=0)
    sem_values_herring_change = df_herring_change.sem(axis=0)
    ci_values_herring_change = 1.96 * sem_values_herring_change
    summary_df_herring_change = pd.DataFrame({'Mean': mean_values_herring_change, 'CI_low': mean_values_herring_change - ci_values_herring_change, 'CI_high': mean_values_herring_change + ci_values_herring_change})

    mean_values_both_change = df_both_change.mean(axis=0)
    sem_values_both_change = df_both_change.sem(axis=0)
    ci_values_both_change = 1.96 * sem_values_both_change
    summary_df_both_change = pd.DataFrame({'Mean': mean_values_both_change, 'CI_low': mean_values_both_change - ci_values_both_change, 'CI_high': mean_values_both_change + ci_values_both_change})

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # No perception change
    axs[0, 0].plot(return_values_dict1['Elapsed_time'], summary_df_no_change['Mean'], label = 'Average killed herring')
    axs[0, 0].fill_between(return_values_dict1['Elapsed_time'], summary_df_no_change['CI_low'], summary_df_no_change['CI_high'], alpha=0.3, label='95% CI')
    axs[0, 0].axhline(y=32, color='tab:green', linestyle='--',  label='Perception length herring')
    axs[0, 0].axhline(y=100, color='tab:orange', linestyle='--',  label='Perception length barracuda')
    axs[0, 0].set_title('No perception change', fontsize=12)

    # Predator perception change
    axs[0, 1].plot(return_values_dict2['Elapsed_time'], summary_df_predator_change['Mean'])
    axs[0, 1].fill_between(return_values_dict2['Elapsed_time'], summary_df_predator_change['CI_low'], summary_df_predator_change['CI_high'], alpha=0.3 )
    axs[0, 1].axhline(y=32, color='tab:green', linestyle='--')
    axs[0, 1].plot(return_values_dict2['Elapsed_time'], return_values_dict2['Perception_lenghts_predator'], 'tab:orange', linestyle='--', alpha=0.5)
    axs[0, 1].set_title('Barracuda perception change', fontsize=12)

    # Herring perception change
    axs[1, 0].plot(return_values_dict3['Elapsed_time'], summary_df_herring_change['Mean'])
    axs[1, 0].fill_between(return_values_dict3['Elapsed_time'], summary_df_herring_change['CI_low'], summary_df_herring_change['CI_high'], alpha=0.3)
    axs[1, 0].axhline(y=100, color='tab:orange', linestyle='--')
    axs[1, 0].plot(return_values_dict3['Elapsed_time'], return_values_dict3['Perception_lenghts_herring'], 'tab:green', linestyle='--', alpha=0.5)
    axs[1, 0].set_title('Herring perception change', fontsize=12)
    axs[1, 0].set_xlabel('Elapsed time (sec)', fontsize=11)

    # Both herring and predator perception change (herring count lists should be the same so does not matter which one you choose)
    axs[1, 1].plot(return_values_dict4['Elapsed_time'], summary_df_both_change['Mean'])
    axs[1, 1].fill_between(return_values_dict4['Elapsed_time'], summary_df_both_change['CI_low'], summary_df_both_change['CI_high'], alpha=0.3)
    axs[1, 1].plot(return_values_dict4['Elapsed_time'], return_values_dict4['Perception_lenghts_herring'], 'tab:green', linestyle='--', alpha=0.5)
    axs[1, 1].plot(return_values_dict4['Elapsed_time'], return_values_dict4['Perception_lenghts_predator'], 'tab:orange', linestyle='--', alpha=0.5)
    axs[1, 1].set_title('Barracuda and herring perception change', fontsize=12)
    axs[1, 1].set_xlabel('Elapsed time (sec)', fontsize=11)

    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize='medium', framealpha=1)

    for ax in axs.flat:
        ax.set_ylabel('Number of killed herring', fontsize=11)
        ax.tick_params(axis='y', which='both', labelleft=True, labelsize=11)
        ax.tick_params(axis='y', which='both', labelleft=True, labelsize=11)
        ax.grid(True)

    plt.show()


    def sensitivity_weighted_x(number_simulation, time_simulation, min_range, max_range):
    """The function makes two plots of the mean number of killed herrings
        under different combinations of Boids Influence and Weighted X values.

    Parameters:
    -----------
    number_simulation: int
        The number of simulations to be executed.
    time_simulation: int
        The duration of each simulation.
    min_range: int
        The lower bound of the range of weighted_x values to be tested.
    max_range: int
        The upper bound of the range of weighted_x values to be tested.
    Returns:
    --------
    boids_influence_df: DataFrame
        DataFrame containing the results of all simulations, including
        the simulation number, Boids Influence value, Weighted X value,
        and the number of killed herrings.
    mean_values: Series
        Series containing the mean number of killed herrings for each
        combination of Boids Influence and Weighted X values.
    """

    # Keep other parameters the same for all simulations
    herring_nr = 200
    predator_nr = 3
    rock_nr = 20
    simulation_duration = time_simulation
    extra_rocks = True
    start_school = True

    all_simulation_values = []
    for simulation in range(number_simulation):
        print('simulation', simulation)
        for boids_influence_value in range(4):
            print('boids influence',boids_influence_value)
            for weighted_x in range(min_range, max_range):
                print(weighted_x)
                return_values = Experiment(herring_nr, predator_nr, rock_nr, simulation_duration,
                        extra_rocks, start_school,boids_influence=boids_influence_value, weighted_x = weighted_x
                    ).run()
                all_simulation_values.append({
                    'Simulation': simulation,
                    'Boids_Influence': boids_influence_value,
                    'Weighted_X': weighted_x,
                    'Killed_Herring': return_values['Killed_herring']
                })

    # Maak een DataFrame van de opgeslagen waarden
    boids_influence_df = pd.DataFrame(all_simulation_values)
    print(boids_influence_df)
    titles = ['No Weighted Boid Rules', 'Weighted Separation Rule', 'Weighted Alignment Rule', 'Weighted Cohesion Rule']
    # Bereken de gemiddelde waarden voor elke combinatie van Boids Influence en Weighted X
    mean_values = boids_influence_df.groupby(['Boids_Influence', 'Weighted_X'])['Killed_Herring'].mean()
    std_values = boids_influence_df.groupby(['Boids_Influence', 'Weighted_X'])['Killed_Herring'].std()

    fig, axs = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)

    for ax, (boids_influence, data), title in zip(axs.flat, mean_values.groupby('Boids_Influence'), titles):
        std_data = data.reset_index(level=0, drop=True)
        mean_data = data.reset_index(level=0, drop=True)

        x_values = mean_data.index
        scaled_std_data = std_data.reindex(x_values).interpolate()

        ax.plot(x_values, mean_data, marker='o', label='Mean')
        ax.fill_between(x_values, mean_data - std_data, mean_data + std_data, alpha=0.3)
        ax.set_title(title)
        ax.set_xlabel('Weighted X')
        ax.set_ylabel('Mean Killed Herring')
        ax.set_xticks(range(min_range, max_range+1))

        # Toon aswaarden op alle subplots
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.show()

    fig, axs = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)

    for ax, (boids_influence, data), title in zip(axs.flat, mean_values.groupby('Boids_Influence'), titles):
        mean_data = data.reset_index(level=0, drop=True)
        x_values = mean_data.index

        ax.plot(x_values, mean_data, marker='o', label='Mean')
        ax.set_title(title)
        ax.set_xlabel('Weighted X')
        ax.set_ylabel('Mean Killed Herring')
        ax.set_xticks(range(min_range, max_range+1))

        # Toon aswaarden op alle subplots
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.show()

    return boids_influence_df, mean_values

if __name__ == "__main__":
    # Determine the influence of the boid rules
    df_boid_killed = influence_boid_rules(40, 60)
    significant_test_boidsrules(df_boid_killed)

    # Determine the influence of rocks on the killing rate
    influence_rocks(80, 30, 30)

    #Determine the invluence of more predators
    influence_predator_number(20, 30, 30)

    # # Determine the influence of the scoolsize
    df_school_size = influence_school_size(40, 30)
    significant_test_school_size(df_school_size)

    # Determine the influence of the alignment distance
    influence_alignment_distance(30, 30)

    # Determine what influence if predators are more within the separation distance
    df_closeness_herring = influences_closeness_herring(40, 30)
    significant_test_close(df_closeness_herring)
    significant_test_killed(df_closeness_herring)

    # Determine the influence of changes in the perception length
    visualizing_perception_change(6, 600, 250)

    # Determine the influence of changes when there are only a few herring
    visualizing_perception_change(5, 600, 250)

    # Do a sensitivity analyse for the alignment, separation and cohesion distance
    sensitivity_rules_distance(30, 30)

    # Determine the killing efficiency per predator if the number of predators increases
    predator_killing_efficiency(30, 30, 30)

    # Determine the difference in killed herring when boid rules get different weights
     #Determine  the weighted_x best influence'
    sensitivity_weighted_x(40, 30, -5, 5)

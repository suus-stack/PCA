"""
Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405
Description:  In this code functions are given that are used to make the plots. The
              data for the plots is created by running the experiment (simulation)
              from gamefish.py a number of times. The plots show the influence of
              different factors on the killing rate of the herrings.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from gamefish import *
from statistic_tests import *
import matplotlib.patches as patches

def influence_predator_number(max_number_predators, number_simulations, time_simulation):
    """ Function that makes a violin plot of the distribution of the killed herring
    for different number of predators in an environment with and without rocks. The
    starting number of herring is set to 200 and the herring start in a school.

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
    for number_predators in range(0, max_number_predators+1, 4):
        print('Nr predators', number_predators)

        # Do a number of simulation without rocks and with rocks
        for simulation in range(number_simulations):
            print('simulation', simulation)
            values_dict = Experiment(200, number_predators, 0, time_simulation, True, True, False, False).run()
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': values_dict['Killed_herring'], 'Rocks':'no'}])
            df = pd.concat([df, new_row], ignore_index=True)

            values_dict = Experiment(200, number_predators, 20, time_simulation, True, True, False, False).run()
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': values_dict['Killed_herring'], 'Rocks':'yes'}])
            df = pd.concat([df, new_row], ignore_index=True)

    # Make a violin plot
    sns.violinplot(data=df, x= 'Nr predators', y= 'Killed herring', hue= 'Rocks', split=True, gap=.1, inner="quart")
    legend = plt.legend(loc='upper left', fontsize=10, title='Rocks')
    plt.xlabel('Number of predators', fontsize=11)
    plt.ylabel('Killed herring', fontsize=11)
    plt.ylim(bottom=0)
    plt.title('Killed herring for different numbers of predators, with and without rocks')
    plt.show()

def influence_rocks(max_number_rocks, number_simulations, time_simulation):
    """ Function that makes a plot of the average killed herring + 1 SD errorbars in
    an environment with differnt numbers of rocks. The starting number of herring is
    set to 200 and they start in 1 school. There is looked at 1 and 3 predators.

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
        print('nr rock', number_rock)
        list_rock_number.append(number_rock)

        list_killed_herring_1_predator = []
        list_killed_herring_3_predators = []

        # Repeat the simulation with 1 predator and 3 predators a number of times
        for simulation in range(number_simulations):
            print('simulation', simulation)
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
    plot = plt.errorbar(list_rock_number, list_mean_killed_1_predator, yerr=list_std_killed_1_predator, fmt='o--', color='orange', capsize=4, markerfacecolor='red', label='avarage killed herring + 1 SD, 1 predator')
    plot = plt.errorbar(list_rock_number, list_mean_killed_3_predators, yerr=list_std_killed_3_predators,fmt='o--', color='blue', capsize=4, markerfacecolor='purple', label='avarage killed herring + 1 SD, 3 predators')
    plt.xlabel('Number or rocks', fontsize=11)
    plt.ylabel('Average killed herring', fontsize=11)
    plt.title('Average killed herring + 1 SD errorbars in environments with different numbers of rocks')
    plt.ylim(bottom=0)
    plt.legend(fontsize=10)
    plt.show()

def influence_alignment_distance(number_simulations, time_simulation):
    """Function that makes a plot of the average killed herring + 1 SD errorbars for
    different values of the alignment distance. The starting number of herring is set
    to 200 and that of the predators to 3. It is tested in an envionment with rocks.

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
        print('alignment distance', alignment_distance)
        list_alignment_distance.append(alignment_distance)
        list_killed_herring_rocks = []
        list_killed_herring_no_rocks = []

        # Simulate the experiment a number of times
        for simulation in range(number_simulations):
            print('simulation', simulation)
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
    plot1 = plt.errorbar(list_alignment_distance, list_mean_killed_rocks, yerr=list_std_killed_rocks, fmt='o--', color='purple', markerfacecolor='blue', label='mean killed h + 1 SD with rocks', capsize=4)
    plot2 = plt.errorbar(list_alignment_distance, list_mean_killed_no_rocks, yerr=list_std_killed_no_rocks, fmt='o--', color='red', markerfacecolor='pink', label='mean killed h + 1 SD without rocks', capsize=4)
    plt.xlabel('Alignment distance')
    plt.ylabel('Average killed herring')
    plt.title('The average killed herring + 1 SD errorbars at different alignment distances')
    plt.ylim(bottom=0)
    plt.legend()
    plt.show()


def influence_school_size(number_simulations, time_simulation):
    """Function that makes a boxplot and scatterplot of the distribution of the
    killed herring for two sizes of fish schools in an environment with and without
    rocks. The starting number of predators is 3. It also does a significance test.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    # Make empty dataframe with three columns
    column_names = ['School size', 'Proportion killed herring', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # Do a number of simulations
    for simulation in range(number_simulations):
        print('School size simulation:', simulation)

        # Without rocks and with 200 herring
        values_dict = Experiment(200, 3, 0, time_simulation, True, True, False, False).run()
        new_row = pd.DataFrame([{'School size': 200, 'Proportion killed herring': values_dict['Killed_herring']/200, 'Rocks':'no'}])
        df = pd.concat([df, new_row], ignore_index=True)

        # With rocks and with 200 herring
        values_dict = Experiment(200, 3, 20, time_simulation, True, True, False, False).run()
        new_row = pd.DataFrame([{'School size': 200, 'Proportion killed herring': values_dict['Killed_herring']/200, 'Rocks':'yes'}])
        df = pd.concat([df, new_row], ignore_index=True)

        # Without rocks and with 400 herring
        values_dict = Experiment(400, 3, 0, time_simulation, True, True, False, False).run()
        new_row = pd.DataFrame([{'School size': 400, 'Proportion killed herring': values_dict['Killed_herring']/400, 'Rocks':'no'}])
        df = pd.concat([df, new_row], ignore_index=True)

        # With rocks and with 400 herring
        values_dict = Experiment(400, 3, 20, time_simulation, True, True, False, False).run()
        new_row = pd.DataFrame([{ 'School size': 400, 'Proportion killed herring': values_dict['Killed_herring']/400, 'Rocks':'yes'}])
        df = pd.concat([df, new_row], ignore_index=True)

    # Do a statistical test
    significant_test_school_size(df)

    # Determine the colors for the plots
    colors_box = {'yes': 'peachpuff', 'no': 'lavender'}
    colors_strip = {'yes': 'red' , 'no': 'blue'}

    # Make a figure in which both the boxplot an stripplot are plotted
    plt.figure(figsize=(10, 6))
    boxplot = sns.boxplot(x='School size', y='Proportion killed herring', hue='Rocks', data=df, palette=colors_box, width=0.8, dodge=True)
    stripplot = sns.stripplot(x='School size', y='Proportion killed herring', hue='Rocks', data=df, dodge=True, palette=colors_strip)
    plt.title('Proportion killed herring in large and small schools, with and without rocks')
    plt.xlabel('Herring school size')
    plt.ylim(bottom=0)

    # Make a legend
    handles, labels = stripplot.get_legend_handles_labels()
    plt.legend(handles[0:2], labels[0:2], title='Rocks', loc='upper right')
    plt.show()


def influences_closeness_herring(number_simulations, time_simulation):
    """Function that makes a boxplot and scatterplot of the distribution of herring
    within the seperation distance of 6 for different seperation distances and by
    introducing 2 predators. The starting number of herring is set to 200 and the
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

        # No predators, no rocks and default seperation distance (6)
        values_dict = Experiment(200, 0, 0, time_simulation, True, True, False, False, 32, 32, 6).run()
        new_row = pd.DataFrame([{'Predator and separation distance': 'no p + no r + s d = 6', 'Times within separation distance': values_dict['Herring_within_separation_distance']}])
        df = pd.concat([df, new_row], ignore_index=True)

        # No predators, 20 rocks and default seperation distance (6)
        values_dict = Experiment(200, 0, 20, time_simulation, True, True, False, False, 32, 32, 6).run()
        new_row = pd.DataFrame([{'Predator and separation distance': 'no p + 20 r + s d = 6', 'Times within separation distance': values_dict['Herring_within_separation_distance']}])
        df = pd.concat([df, new_row], ignore_index=True)

        # 2 predators, no rocks and default seperation distance (6)
        values_dict = Experiment(200, 2, 0, time_simulation, True, True, False, False, 32, 32, 6).run()
        new_row = pd.DataFrame([{'Predator and separation distance': '2 p + no r + s d = 6', 'Times within separation distance': values_dict['Herring_within_separation_distance']}])
        df = pd.concat([df, new_row], ignore_index=True)

        # No predators, no rocks and a seperation distance of 3
        values_dict = Experiment(200, 0, 0, time_simulation, True, True, False, False, 32, 32, 3).run()
        new_row = pd.DataFrame([{'Predator and separation distance': 'no p + no r + s d = 3', 'Times within separation distance': values_dict['Herring_within_separation_distance']}])
        df = pd.concat([df, new_row], ignore_index=True)

        # No predators, no rocks and a seperation distance of 12
        values_dict = Experiment(200, 0, 0, time_simulation, True, True, False, False, 32, 32, 12).run()
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
    background_legend = patches.Rectangle((-0.04, 0.88), 0.3, 2.5, edgecolor='black', facecolor='lightcyan', transform=ax.transAxes)
    ax.add_patch(background_legend)

    plt.title('Herring count within the original separation distance (6) across various conditions.')
    plt.xlabel('Enviromental situation', fontsize=11)
    plt.ylabel('Times within original seperation distance (6)', fontsize=11)
    plt.show()

def influence_boid_rules(number_simulations, time_simulation):
    """Function that makes a boxplot the distribution of killed herring when different
    boid rules are most important.

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind.
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    data_array_killed_herring = np.empty((number_simulations, 4))

    # Keep other parameters the same for all simulations
    herring_nr = 150
    predator_nr = 2
    rock_nr = 10
    simulation_duration = time_simulation
    extra_rocks = True
    start_school = True

    # Simulate a number of experiments with varying boids_influence values
    for simulation in range(number_simulations):
        print('simulation:', simulation)
        for boids_influence_value in range(4):
            return_values = Experiment(herring_nr, predator_nr, rock_nr, simulation_duration,
                extra_rocks, start_school,boids_influence=boids_influence_value
            ).run()
            print('Boids Influence rule:', boids_influence_value)

            data_array_killed_herring[simulation, boids_influence_value] = return_values['Killed_herring']

    # Calculate mean and standard deviation for each column
    mean_killed_herring_array = np.mean(data_array_killed_herring, axis=0)
    std_killed_herring_array = np.std(data_array_killed_herring, axis=0)
    print(data_array_killed_herring)
    df = pd.DataFrame(data_array_killed_herring, columns=['no weigted boid rules', 'weighted seperation rule','weighted alignment rule', 'weighted cohesion rule'])
    print(df)

    # Create a boxplot of the different boid rules
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df)
    plt.xlabel('Boids influence')
    plt.ylabel('Killed herring')
    plt.title('Boxplot of killed herring for different Boid rules')
    plt.show()

    # Plot bar graf of mean values ->*** Kan dit weg ?? ***
    plt.figure(figsize=(10, 6))
    sns.barplot(x=df.columns, y=df.mean())
    plt.xlabel('Boids influence')
    plt.ylabel('Mean killed herring')
    plt.title('Mean killed herring for different boid rules')
    plt.show()

def visualizing_perception_change(time_simulation):
    """Function that makes four line plots that show the differences between the number of killed herring per
    time interval (10 sec) for different perception lengths. The 4 simulated cases are:
    - Both perception lengths do not change over time and remain their default setting. 
    - Solely the herring perception length changes over time. 
    - Solely the predator perception length changes over time.
    - Both perception lengths are changed over time, but with a different adaption. (3 for herring and 5 for predator) 
    change over time.

    Parameters:
    -----------
    time_simulation: Int
        The number of seconds the simulation runs.
    """
    # no perception change
    return_values_dict1 = Experiment(200, 5, 20, time_simulation, True, True, False, False, 32, 32, 6).run()
    # predator perception change
    return_values_dict2 = Experiment(200, 5, 20, time_simulation, True, True, True, False, 32, 32, 6).run()
    # herring perception change
    return_values_dict3 = Experiment(200, 5, 20, time_simulation, True, True, False, True, 32, 32, 6).run()
    # herring and predator perception change
    return_values_dict4 = Experiment(200, 5, 20, time_simulation, True, True, True, True, 32, 32, 6).run()

    plt.style.use('seaborn')
    fig, axs = plt.subplots(2, 2)


    # no perception change
    axs[0, 0].plot(return_values_dict1['Elapsed_time'], np.diff(return_values_dict1['Killed_herring_over_time']))
    axs[0, 0].set_title('No perception change', fontsize=10)
    # predator perception change
    axs[0, 1].plot(return_values_dict2['Elapsed_time'], np.diff(return_values_dict2['Killed_herring_count_predator_perception_change']), 'tab:orange')
    axs[0, 1].plot(return_values_dict2['Elapsed_time'], return_values_dict2['Perception_lenghts_predator'])
    axs[0, 1].set_title('Predator perception change', fontsize=10)
    # herring perception change (x-as:time, y-as: killed herring)
    axs[1, 0].plot(return_values_dict3['Elapsed_time'], np.diff(return_values_dict3['Killed_herring_count_herring_perception_change']), 'tab:green')
    axs[1, 0].plot(return_values_dict3['Elapsed_time'], return_values_dict3['Perception_lenghts_herring'])
    axs[1, 0].set_title('Herring perception change', fontsize=10)
    # both herring and predator perception change (herring count lists should be the same so does not matter which one you choose)
    axs[1, 1].plot(return_values_dict4['Elapsed_time'], np.diff(return_values_dict4['Killed_herring_count_herring_perception_change']), 'tab:red')
    axs[1, 1].plot(return_values_dict4['Elapsed_time'], return_values_dict4['Perception_lenghts_herring'])
    axs[1, 1].plot(return_values_dict4['Elapsed_time'], return_values_dict4['Perception_lenghts_predator'])
    axs[1, 1].set_title('Predator and herring perception change', fontsize=10)

    for ax in axs.flat:
        ax.set(xlabel= 'Elapsed time', ylabel= 'Number of killed herring')
        ax.tick_params(axis='y', which='both', labelleft=True, labelsize=6)
        ax.tick_params(axis='x', which='both', labelsize=6)
        ax.grid(True)

    for ax in axs.flat:
        ax.label_outer()

    fig.savefig("..\\data_visualisation\\4-perception_change_plot.png")


if __name__ == "__main__":
    # Determine the influence of the boid rules
    # influence_boid_rules(20, 30)

    # # Determine the influence of rocks on the killing rate
    # influence_rocks(80, 20, 30)

    # Determin the invluence of more predators
    # influence_predator_number(20, 20, 30)

    # Determine the influence of the scoolsize
    # influence_school_size(20, 30)

    # # Determine the influence of the alignment distance
    # influence_alignment_distance(20, 30)

    # Determine what influence if predators are more within the separation distance
    # influences_closeness_herring(20, 30)

    # Determine the influence of changes in the perception length
    visualizing_perception_change(30)


    # """Faster run???????"""
    # # Determine the influence of the boid rules
    # influence_boid_rules(3, 5)
    #
    # # Determine the influence of rocks on the killing rate
    # influence_rocks(30, 5, 5)
    #
    # # Determin the invluence of more predators
    # influence_predator_number(3, 10, 5)
    #
    # # Determine the influence of the scoolsize
    # influence_school_size(3, 5)
    #
    # # # Determine the influence of the alignment distance
    # influence_alignment_distance(3, 5)
    #
    # # Determine what influence if predators are more within the separation distance
    # influences_closeness_herring(3, 5)
    #
    # # Determine the influence of changes in the perception length
    # visualizing_perception_change(30)

"""
Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project Computational Science
Student ID's: 14773279 , 15159337, 13717405
Description:  In this code the functions are given to do statistical tests in
              visualisation.py with the data from the runned simulations.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import shapiro
from scipy import stats
import matplotlib.patches as patches
from scipy.stats import shapiro, ttest_rel
import numpy as np
from scipy.stats import mannwhitneyu

def significant_test_school_size(df):
    """Function that determines if there is a significant difference in killed
    herring between a large and small school in environments with and without rocks.

    Parameters:
    -----------
    df: Dataframe
        Datafframe with the values obtained from the simulated experiments.
    """
    df['Proportion killed herring'] = pd.to_numeric(df['Proportion killed herring'], errors='coerce')

    # Extract the killing values for the small and large school with and without rocks
    values_small_school_rocks = df.loc[(df['School size'] == 200) & (df['Rocks'] == 'yes'), 'Proportion killed herring']
    values_large_school_rocks = df.loc[(df['School size'] == 400) & (df['Rocks'] == 'yes'), 'Proportion killed herring']
    values_small_school_no_rocks = df.loc[(df['School size'] == 200) & (df['Rocks'] == 'no'), 'Proportion killed herring']
    values_large_school_no_rocks = df.loc[(df['School size'] == 400) & (df['Rocks'] == 'no'), 'Proportion killed herring']

    # Determine if the data is normally distributed
    statistic_small_school_rocks, p_value_small_school_rocks = shapiro(values_small_school_rocks)
    statistic_large_school_rocks, p_value_large_school_rocks = shapiro(values_large_school_rocks)
    statistic_small_school_no_rocks, p_value_small_school_no_rocks = shapiro(values_small_school_no_rocks)
    statistic_large_school_no_rocks, p_value_large_school_no_rocks = shapiro(values_large_school_no_rocks)

    # Influence of school size in an environment with rocks.
    if  p_value_large_school_rocks >= 0.05 and p_value_small_school_rocks >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_small_school_rocks, values_large_school_rocks)
        print(f'Small vs large school in an environment with rocks; t-statistic: {t_statistic}, p-Value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_small_school_rocks, values_large_school_rocks)
        print(f'Small vs large school in an environment with rocks; Mann-Whitney U statistic: {mw_statistic}, p-Value: {p_value}')

    # Influence of school size in an environment without rocks.
    if  p_value_large_school_no_rocks >= 0.05 and p_value_small_school_no_rocks >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_small_school_no_rocks, values_large_school_no_rocks)
        print(f'Small vs large school in an environment without rocks; t-statistic: {t_statistic}, p-Value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_small_school_no_rocks, values_large_school_no_rocks)
        print(f'Small vs large school in an environment without rocks; Mann-Whitney U statistic: {mw_statistic}, p-Value: {p_value}')


def significant_test_close(df):
    """Function that determines if there is a significant difference in herring within
    the original perception distance of 6 when the perception distance changes, when
    more preadators gets introduced or when rocks get introduced.

    Parameters:
    -----------
    df: Dataframe
        Dataframe with the values obtaint from the simulated experiments.
    """
    df['Times within separation distance'] = pd.to_numeric(df['Times within separation distance'], errors='coerce')

    # Extract the killing values for the different conditions
    values_1_p_6_no_r = df.loc[(df['Conditions'] == '1 p + no r + s d = 6'), 'Times within separation distance']
    values_1_p_6_r = df.loc[(df['Conditions'] == '1 p + 20 r + s d = 6'), 'Times within separation distance']
    values_4_p_6_no_r = df.loc[(df['Conditions'] == '4 p + no r + s d = 6'), 'Times within separation distance']
    values_1_p_3_no_r = df.loc[(df['Conditions'] == '1 p + no r + s d = 3'), 'Times within separation distance']
    values_1_p_12_no_r = df.loc[(df['Conditions'] == '1 p + no r + s d = 12'), 'Times within separation distance']

    # Determine if the data is normally distributed
    statistic_1_p_6_no_r, p_value_1_p_6_no_r = shapiro(values_1_p_6_no_r)
    statistic_1_p_6_r, p_value_1_p_6_r = shapiro(values_1_p_6_r)
    statistic_4_p_6_no_r, p_value_4_p_6_no_r = shapiro(values_4_p_6_no_r)
    statistic_1_p_3_no_r, p_value_1_p_3_no_r = shapiro(values_1_p_3_no_r)
    statistic_1_p_12_no_r, p_value_1_p_12_no_r = shapiro(values_1_p_12_no_r)

    print('values_1_p_6_no_r', values_1_p_6_no_r)
    print('values_1_p_6_r', values_1_p_6_r)
    print('values_4_p_6_no_r', values_4_p_6_no_r)
    print('values_1_p_3_no_r', values_1_p_3_no_r)
    print('values_1_p_12_no_r', values_1_p_12_no_r)

    # Determine if introducing predators has a significant influence on the density
    if p_value_1_p_6_no_r >= 0.05 and p_value_4_p_6_no_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_1_p_6_no_r, values_4_p_6_no_r)
        print(f'Effect introduction predators on density; t-statistic: {t_statistic}, p-value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_1_p_6_no_r, values_p_6_no_r)
        print(f'Effect introduction predators on density; Mann-Whitney U Statistic: {mw_statistic}, p-value: {p_value}')

    # Determine if introducing rocks has significant influence on the density
    if p_value_1_p_6_no_r >= 0.05 and p_value_1_p_6_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_1_p_6_no_r, values_1_p_6_r)
        print(f'Effect introduction rocks on density; t-statistic: {t_statistic}, p-value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_1_p_6_no_r, values_1_p_6_r)
        print(f'Effect introduction rocks on density; Mann-Whitney U statistic: {mw_statistic}, p-value: {p_value}')

    # Determine if a lower seperation distance has a significant influence on the density
    if p_value_1_p_6_no_r >= 0.05 and p_value_1_p_3_no_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_1_p_6_no_r, values_1_p_3_no_r)
        print(f'Effect smaller separation distance on density; t-statistic: {t_statistic}, p-Value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_1_p_6_no_r, values_1_p_3_no_r)
        print(f'Effect smaller separation distance on density; Mann-Whitney U statistic: {mw_statistic}, p-value: {p_value}')

    # Determine if a higher seperation distance has a significant influence on the density
    if p_value_1_p_6_no_r >= 0.05 and p_value_1_p_12_no_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_1_p_6_no_r, values_1_p_12_no_r)
        print(f'Effect larger separation distance on density; t-statistic: {t_statistic}, p-Value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_1_p_6_no_r, values_1_p_12_no_r)
        print(f'Effect larger separation distance on density; Mann-Whitney U statistic: {mw_statistic}, p-value: {p_value}')


def significant_test_killed(df):
    """Function that determines if there is a significant difference in the number
    of killed herring killed when the perception distance changes, when more preadators
    gets introduced or when rocks get introduced.

    Parameters:
    -----------
    df: Dataframe
        Datafframe with the values obtaint from the simulated experiments.
    """
    df['Killed herring'] = pd.to_numeric(df['Killed herring'], errors='coerce')

    # Extract the killing values for the different conditions
    values_1_p_6_no_r = df.loc[(df['Conditions'] == '1 p + no r + s d = 6'), 'Killed herring']
    values_1_p_6_r = df.loc[(df['Conditions'] == '1 p + 20 r + s d = 6'), 'Killed herring']
    values_4_p_6_no_r = df.loc[(df['Conditions'] == '4 p + no r + s d = 6'), 'Killed herring']
    values_1_p_3_no_r = df.loc[(df['Conditions'] == '1 p + no r + s d = 3'), 'Killed herring']
    values_1_p_12_no_r = df.loc[(df['Conditions'] == '1 p + no r + s d = 12'), 'Killed herring']

    # Determine if the data is normally distributed
    statistic_1_p_6_no_r, p_value_1_p_6_no_r = shapiro(values_1_p_6_no_r)
    statistic_1_p_6_r, p_value_1_p_6_r = shapiro(values_1_p_6_r)
    statistic_4_p_6_no_r, p_value_4_p_6_no_r = shapiro(values_4_p_6_no_r)
    statistic_1_p_3_no_r, p_value_1_p_3_no_r = shapiro(values_1_p_3_no_r)
    statistic_1_p_12_no_r, p_value_1_p_12_no_r = shapiro(values_1_p_12_no_r)

    # Determine if introducing predators has significant influence on the killing rate
    if p_value_1_p_6_no_r >= 0.05 and p_value_4_p_6_no_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_1_p_6_no_r, values_4_p_6_no_r)
        print(f'Effect introduction predators on killing rate; t-statistic: {t_statistic}, p-value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_1_p_6_no_r, values_4_p_6_no_r)
        print(f'Effect introduction predators on killing rate; Mann-Whitney U Statistic: {mw_statistic}, p-value: {p_value}')

    # Determine if introducing rocks has significant influence on the killing rate
    if p_value_1_p_6_no_r >= 0.05 and p_value_1_p_6_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_1_p_6_no_r, values_1_p_6_r)
        print(f'Effect introduction rocks on killing rate; t-statistic: {t_statistic}, p-value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_1_p_6_no_r, values_1_p_6_r)
        print(f'Effect introduction rocks on killing rate; Mann-Whitney U statistic: {mw_statistic}, p-value: {p_value}')

    # Determine if a lower seperation distance has a significant influence on the killing rate
    if p_value_1_p_6_no_r >= 0.05 and p_value_1_p_3_no_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_1_p_6_no_r, values_1_p_3_no_r)
        print(f'Effect smaller separation distance on killing rate; t-statistic: {t_statistic}, p-value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_1_p_6_no_r, values_1_p_3_no_r)
        print(f'Effect smaller separation distance on killing rate; Mann-Whitney U statistic: {mw_statistic}, p-value: {p_value}')

    # Determine if a higher seperation distance has a significant influence on the killing rate
    if p_value_1_p_6_no_r >= 0.05 and p_value_1_p_12_no_r >= 0.05:
        t_statistic, p_value = stats.ttest_ind(values_1_p_6_no_r, values_1_p_12_no_r)
        print(f'Effect larger separation distance on killing rate; t-statistic: {t_statistic}, p-value: {p_value}')
    else:
        mw_statistic, p_value = stats.mannwhitneyu(values_1_p_6_no_r, values_1_p_12_no_r)
        print(f'Effect larger separation distance on killing rate; Mann-Whitney U statistic: {mw_statistic}, p-value: {p_value}')


def significant_test_boidsrules(data):
    """Function that determines if there is a significant difference in herring
    killing rate when one of the boid rules is emphasised.

    Parameters:
    -----------
    data: Dataframe
        Datafframe with the values obtaint from the simulated experiments.
    """
    # Perform tests for each pair
    comparison_pairs = [('no weighted boid rules', 'weighted separation rule'),
                        ('no weighted boid rules', 'weighted alignment rule'),
                        ('no weighted boid rules', 'weighted cohesion rule')]

    for group1_name, group2_name in comparison_pairs:
        group1_data = data[group1_name]
        group2_data = data[group2_name]

        # Check normality for group2_data
        normality_group2 = shapiro(group2_data).pvalue >= 0.05

        if any(group1_data) and any(group2_data) and normality_group2:
            # Perform paired t-tests
            t_stat, p_value = ttest_rel(group1_data, group2_data)

            # Print results
            print(f'Paired t-test between "{group1_name}" and "{group2_name}": t-statistic = {t_stat}, p-value = {p_value}')

        else:
            # Perform Mann-Whitney U test
            u_stat, p_value_mannwhitney = mannwhitneyu(group1_data, group2_data, alternative='two-sided')

            # Print results for Mann-Whitney U test
            print(f'Mann-Whitney U test between "{group1_name}" and "{group2_name}": U-statistic = {u_stat}, p-value = {p_value_mannwhitney}')

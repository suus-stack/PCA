from  matplotlib import pyplot as plt
import numpy as np

def visualizing_perception_change(return_values_dict1, return_values_dict2, return_values_dict3, return_values_dict4):
    """Plots the difference.!!!"""
    plt.style.use('seaborn')
    fig, axs = plt.subplots(2, 2)
    # no perception change 
    axs[0, 0].plot(return_values_dict1['Elapsed_time'], np.diff(return_values_dict1['Killed_herring_over_time']))
    axs[0, 0].set_title('No perception change', fontsize=10)
    # predator perception change 
    axs[0, 1].plot(return_values_dict2['Elapsed_time'], np.diff(return_values_dict2['Killed_herring_count_predator_perception_change']), 'tab:orange')
    axs[0, 1].set_title('Predator perception change', fontsize=10)
    # herring perception change (x-as:time, y-as: killed herring)
    axs[1, 0].plot(return_values_dict3['Elapsed_time'], np.diff(return_values_dict3['Killed_herring_count_herring_perception_change']), 'tab:green')
    axs[1, 0].set_title('Herring perception change', fontsize=10)
    # both herring and predator perception change (herring count lists should be the same so does not matter which one you choose)
    axs[1, 1].plot(return_values_dict4['Elapsed_time'], np.diff(return_values_dict4['Killed_herring_count_herring_perception_change']), 'tab:red')
    axs[1, 1].set_title('Predator and herring perception change', fontsize=10)
    
    for ax in axs.flat:
        ax.set(xlabel= 'Elapsed time', ylabel= 'Number of killed herring')
        ax.tick_params(axis='y', which='both', labelleft=True, labelsize=6) 
        ax.tick_params(axis='x', which='both', labelsize=6)
        ax.grid(True) 


    for ax in axs.flat:
        ax.label_outer()
  
    # fig.savefig('4-plot perception length change')
    fig.savefig("..\\visualisations\\4-perception_change_plot.png")

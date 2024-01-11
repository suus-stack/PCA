import numpy as np
from  matplotlib import pyplot as plt


def initialize_flock(nr_herring, lower_lim, upper_lim):
    """ if you want the x-axis to vary between 100 and 200 and the y-axis to be betweeb
    900 and 1100, you use: lower_lim = np.array([100, 900]) and upper_lim = np.array([200, 1100])"""
    width = upper_lim - lower_lim
    flock = lower_lim[:, np.newaxis] + np.random.rand(2, nr_herring) * width[:, np.newaxis]
    return flock

def initialize_velocities(nr_herring, lower_lim, upper_lim):
    """Random initializatio of velocitie for each herring."""
    width = upper_lim - lower_lim
    velocities = lower_lim[:, np.newaxis] + np.random.rand(2, nr_herring) * width[:, np.newaxis]
    return velocities 


def update(positions, velocities):
    min_distance = 70
    # Initial movement being to the middle
    attraction_to_center = 0.01
    center = np.mean(positions, 1) # 1 because along the horizontal axis
    # Calculating direction vectors from each position to the center
    # By adding a new axis the shape of center changes from (2,) to (2,1)
    direction_to_center = positions - center[:, np.newaxis]
    velocities -= direction_to_center * attraction_to_center
    
    # Avoiding collision
    # Creating a 2 x N x N matrix of the distances between each herring
    # distances_eucl = np.linalg.norm(positions[:, np.newaxis, :] - positions[:, :, np.newaxis], axis=0)
    # print('eucladian distances', distances_eucl)
    distances = positions[:, np.newaxis, :] - positions[:, :, np.newaxis] #?!
    # print('distances', distances)
    squared_distances = np.sum(distances**2, 0)
    # print('squared_distances', squared_distances)
    # # # Herring that are too close
    # far_away = distances_eucl >= min_distance
    # print('far away', far_away)
    # # far_away = np.logical_not(close_herrings)
    # # print(far_away.shape)
    # # # Need to find the herrings that are too close and then swim away from them
    # close_herrings = np.copy(distances_eucl)
    # # close_herrings[0, :, :][far_away] = 0
    # # close_herrings[1, :, :][far_away] = 0
    # close_herrings[far_away] = 0
    # print('close herrings', close_herrings)
    # print(velocities.shape)
    # print('sum', np.sum(close_herrings))
    # velocities += np.sum(close_herrings, 1)
    # print('velocities after change', velocities)
    
    separations = positions[:, np.newaxis, :] - positions[:, :, np.newaxis]
    squared_displacements = separations * separations
    square_distances = np.sum(squared_displacements, 0)
    alert_distance = 100
    far_away = square_distances > alert_distance
    separations_if_close = np.copy(separations)
    separations_if_close[0, :, :][far_away] = 0
    separations_if_close[1, :, :][far_away] = 0
    velocities += np.sum(separations_if_close, 1)
    
    
    velocity_differences = velocities[:, np.newaxis, :] - velocities[:, :, np.newaxis]
    formation_flying_distance = 10000
    formation_flying_strength = 0.125
    very_far = squared_distances > formation_flying_distance
    velocity_differences_if_close = np.copy(velocity_differences)
    velocity_differences_if_close[0, :, :][very_far] = 0
    velocity_differences_if_close[1, :, :][very_far] = 0
    velocities -= np.mean(velocity_differences_if_close, 1) * formation_flying_strength

    
    
    # Update all individual positions
    positions += velocities
    positions %= 900

def visualize(positions, ax1):
    
    ax1.axis([0, 2000, 0, 2000])
    ax1.scatter(positions[0, :], positions[1, :], c='blue', alpha=0.5, marker='o', s=10)

    plt.draw()
    plt.pause(0.01)
    ax1.cla()


def setup_plot():
    fig, ax1 = plt.subplots(1)
    ax1.set_aspect('equal')
    ax1.set_facecolor((0.7, 0.8, 1.0))
    ax1.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)

    return ax1

def run(iterations, positions, velocities):
    ax1 = setup_plot()
    for _ in range(iterations):
        update(positions, velocities)
        visualize(positions, ax1)


# USAGE 
positions = initialize_flock(100, np.array([100, 900]), np.array([200, 1100]))
velocities = initialize_velocities(100, np.array([0, -20]), np.array([10, 20]))

run(1000, positions, velocities)

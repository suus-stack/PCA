import numpy as np
from  matplotlib import pyplot as plt


def initialize_flock(nr_herring, lower_lim, upper_lim):
    """ If you want the x-values to vary between 100 and 200 and the y-values to be between
    900 and 1100, you use: lower_lim = np.array([100, 900]) and upper_lim = np.array([200, 1100])"""
    width = upper_lim - lower_lim
    flock = lower_lim[:, np.newaxis] + np.random.rand(2, nr_herring) * width[:, np.newaxis]

    return flock

def initialize_predator(nr_predators, lower_lim, upper_lim):
    width = upper_lim - lower_lim
    predator_positions = lower_lim[:, np.newaxis] + np.random.rand(2, nr_predators) * width[:, np.newaxis]

    return predator_positions 

def initialize_velocities(nr_herring, lower_lim, upper_lim):
    """Random initialization of velocitie for each herring."""
    width = upper_lim - lower_lim
    velocities = lower_lim[:, np.newaxis] + np.random.rand(2, nr_herring) * width[:, np.newaxis]

    return velocities 

def center_movement(positions, velocities):
    """Center of the mass attraction, like the need to get to the group"""
    
    # negative=repulsion, positive is attraction 
    attraction_to_center = 0.006
    center = np.mean(positions, 1) # 1 because along the horizontal axis
    # Calculating direction vectors from each position to the center
    # By adding a new axis the shape of center changes from (2,) to (2,1)
    direction_to_center = positions - center[:, np.newaxis] 
    
    velocities -= direction_to_center * attraction_to_center 
    positions += velocities
    positions[0] %= 2000
    positions[1] %= 2000
    
   

def cohesion(positions, velocities):
    """Align positions."""

    min_distance = 2000
    alignment_distance = 3000

    distances = normalize(positions[:, np.newaxis, :] - positions[:, :, np.newaxis]) # all pairwise distances in x and y direction
    
    squared_distances = np.sum(distances**2, 0) # distance from 1 to 2 equals 2 to 1 (eucladian distances)
    too_close = squared_distances < min_distance
    too_far = squared_distances > alignment_distance
    # Creating an alignment matrix with the herring that are import for the direction 
    alignment_herring = np.copy(distances)
    alignment_herring[0, :, :][too_close] = 0
    alignment_herring[1, :, :][too_close] = 0
    alignment_herring[0, :, :][too_far] = 0
    alignment_herring[1, :, :][too_far] = 0
    
    velocities -= (np.sum(alignment_herring, 1) / nr_herring)
    positions += velocities
    positions[0] %= 2000
    positions[1] %= 2000

def alignment(positions, velocities):

    distances = normalize(positions[:, np.newaxis, :] - positions[:, :, np.newaxis]) # all pairwise distances in x and y direction
    
    squared_distances = np.sum(distances**2, 0) # distance from 1 to 2 equals 2 to 1 (eucladian distances)
    velocity_differences = velocities[:, np.newaxis, :] - velocities[:, :, np.newaxis]
    formation_flying_distance = 10
    formation_flying_strength = 0.5
    very_far = squared_distances > formation_flying_distance
    velocity_differences_if_close = np.copy(velocity_differences)
    velocity_differences_if_close[0, :, :][very_far] = 0
    velocity_differences_if_close[1, :, :][very_far] = 0
    velocities -= np.mean(velocity_differences_if_close, 1) * formation_flying_strength 


def collision_avoidance(positions, velocities):
    min_distance = 2000
    # Creating a 2 x N x N matrix of the distances between each herring
    # distances = normalize(positions[:, np.newaxis, :] - positions[:, :, np.newaxis]) # all pairwise distances in x and y direction
    distances = positions[:, np.newaxis, :] - positions[:, :, np.newaxis]# all pairwise distances in x and y direction
    squared_distances = np.sum(distances**2, 0) # distance from 1 to 2 equals 2 to 1 (eucladian distances)
    
    # making sure that the impact of herring far away is not taken into account 
    far_away = squared_distances >= min_distance
    close_herring = np.copy(distances)
    # X-direction
    close_herring[0, :, :][far_away] = 0
    # Y-direction
    close_herring[1, :, :][far_away] = 0
   
    # Swimming away from the close herring
    velocities -= np.sum(close_herring, 1) 
    
    # Update all individual positions
    positions += velocities
    positions[0] %= 2000
    positions[1] %= 2000

def normalize(vector):
    magnitude = np.linalg.norm(vector)
    
    if magnitude > 0:
        # Scale the vector to have a unit magnitude
        return vector / magnitude
    else:
        # If the magnitude is 0, return the original vector
        return vector

    

def visualize(positions, ax1):
    # nu nog gehardcode, nog dynamisch maken
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

def run(iterations, positions, velocities, positions2=None, velocities2=None):
    
    ax1 = setup_plot()
    for i in range(iterations):
        collision_avoidance(positions, velocities)
        alignment(positions, velocities)
        center_movement(positions, velocities)
        cohesion(positions, velocities)
        visualize(positions, ax1)
            
        if not positions2 == None:
            collision_avoidance(positions2, velocities2)
            center_movement(positions2, velocities2)
            alignment(positions2, velocities2)
            cohesion(positions2, velocities2)



# USAGE
nr_herring = 20
iterations = 150
upper_lim = np.array([0, 100])
positions  = initialize_flock(nr_herring, np.array([0, 100]), np.array([0, 100]))
velocities = initialize_velocities(nr_herring, np.array([0, -20]), np.array([10, 20]))

# second flock
positions2  = initialize_flock(nr_herring, np.array([0, 50]), np.array([0, 50]))
velocities2 = initialize_velocities(nr_herring, np.array([0, -20]), np.array([10, 20]))

# predator 
predator_positions = initialize_predator(2, np.array([0, 100]), np.array([0, 100]))

# run(iterations, positions, velocities, positions2, velocities2, predator_positions)
run(iterations, positions, velocities)


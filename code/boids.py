"""
Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405
Description:  Agent-based model to simulate herring school movement dynamics.
"""

import numpy as np
from  matplotlib import pyplot as plt
import doctest
import unittest

class Experiment():
    def __init__(self, lower_lim_flock, upper_lim_flock, lower_lim_veloc, upper_lim_veloc, nr_herring, nr_predators,  lower_lim_predator, upper_lim_predator, perception_predator):
        self.width_flock = upper_lim_flock - lower_lim_flock
        self.width_veloc = upper_lim_veloc - lower_lim_veloc
        self.width_predator = upper_lim_predator - lower_lim_predator
        self.lower_lim_flock = lower_lim_flock
        self.upper_lim_flock = upper_lim_flock
        self.lower_lim_veloc = lower_lim_veloc
        self.upper_lim_veloc = upper_lim_veloc

        self.lower_lim_predator = lower_lim_predator
        self.upper_lim_predator = upper_lim_predator
        self.perception_predator = perception_predator

        self.nr_herring = nr_herring
        self.nr_predators = nr_predators
        self.attraction_to_center = 0.0008 # negative=repulsion, positive is attraction
        # self.alignment_distance = 3000
        self.min_distance = 100
        self.formation_flying_distance = 10 #alignment
        self.formation_flying_strength = 0.5 #alignment
        self.iterations = 100
        self.second_flock = True
        self.perception_length = 0.002
        self.velocity_predator = 80

    def initialize_flock(self):
        """ Function makes an array with the random start positions of the herring.
        If you want the x-values to vary between 100 and 200 and the y-values to be
        between 900 and 1100, you use: lower_lim = np.array([100, 900]) and upper_lim
        = np.array([200, 1100]). The function returns an array of size (2, N), where N is
        the number of herring, with the initialized positions of the flock."""

        flock = self.lower_lim_flock[:, np.newaxis] + np.random.rand(2, self.nr_herring) * self.width_flock[:, np.newaxis]

        return flock

    def initialize_predator(self):
        """Function returns an array with the random start positions of the predator."""

        predator = self.lower_lim_predator[:, np.newaxis] + np.random.rand(2, self.nr_predators) * self.width_predator[:, np.newaxis]

        return predator

    def initialize_velocities(self):
        """ Function returns an array of size (2, N), where N is the number of herring,
        with the random initialized velocities of the herring."""

        velocities = self.lower_lim_veloc[:, np.newaxis] + np.random.rand(2, self.nr_herring) * self.width_veloc[:, np.newaxis]

        return velocities

    def center_movement(self, positions, velocities):
        """ This function applies the center of the mass attraction, the need to get
        to the group. The function adapts the velocities of the herring accordingly."""

        center = np.mean(positions, 1) # 1 because along the horizontal axis
        # Calculating direction vectors from each position to the center
        # By adding a new axis the shape of center changes from (2,) to (2,1)
        direction_to_center = positions - center[:, np.newaxis]

        velocities -= direction_to_center * self.attraction_to_center
        positions += velocities
        positions[0] %= 500
        positions[1] %= 500

    def normalize(self, vector):
        """Function that normalizes a vector."""

        magnitude = np.linalg.norm(vector)

        if magnitude > 0:
            # Scale the vector to have a unit magnitude
            return vector / magnitude
        else:
            # If the magnitude is 0, return the original vector
            return vector

    def cohesion(self, positions, velocities):
        """Function that aligns the positions of the herring and adapts the velocities accordingly,
        whereafter they are added to the positions."""

        # eigenlijk is de perception length het verschil tussen min_distance en alignment_distance
        distances = self.normalize(positions[:, np.newaxis, :] - positions[:, :, np.newaxis]) # all pairwise distances in x and y direction
        squared_distances = np.sum(distances**2, 0) # distance from 1 to 2 equals 2 to 1 (eucladian distances)
        # perceived = squared_distances <= self.perception_length
        # fish does not see these surrounding fish because outside of perception length
        not_perceived = squared_distances > self.perception_length
        # print('squared dist', squared_distances)
        # Creating an alignment matrix with the herring that are import for the direction
        alignment_herring = np.copy(distances)
        alignment_herring[0, :, :][not_perceived] = 0
        alignment_herring[1, :, :][not_perceived] = 0
        # alignment_herring[0, :, :][too_far] = 0
        # alignment_herring[1, :, :][too_far] = 0
        # print('alignment', alignment_herring)

        velocities -= np.sum(alignment_herring, 1)
        positions += velocities
        positions[0] %= 500
        positions[1] %= 500

    def alignment(self, positions, velocities):
        """ Function that aligns the velocities of the herring."""

        distances = self.normalize(positions[:, np.newaxis, :] - positions[:, :, np.newaxis]) # all pairwise distances in x and y direction
        squared_distances = np.sum(distances**2, 0) # distance from 1 to 2 equals 2 to 1 (eucladian distances)
        velocity_differences = velocities[:, np.newaxis, :] - velocities[:, :, np.newaxis]

        very_far = squared_distances > self.formation_flying_distance
        velocity_differences_if_close = np.copy(velocity_differences)
        velocity_differences_if_close[0, :, :][very_far] = 0
        velocity_differences_if_close[1, :, :][very_far] = 0
        velocities -= np.mean(velocity_differences_if_close, 1) * self.formation_flying_strength


    def collision_avoidance(self, positions, velocities):
        """ Function that makes sure the herring do not collide."""

        #Creating a 2 x N x N matrix of the distances between each herring
        distances = positions[:, np.newaxis, :] - positions[:, :, np.newaxis] # all pairwise distances in x and y direction
        squared_distances = np.sum(distances**2, 0) # distance from 1 to 2 equals 2 to 1 (eucladian distances)

        # making sure that the impact of herring far away is not taken into account
        far_away = squared_distances > self.min_distance

        close_herring = np.copy(distances)
        # X-direction
        close_herring[0, :, :][far_away] = 0
        # Y-direction
        close_herring[1, :, :][far_away] = 0

        adjustment = np.copy(close_herring)
        non_zero_mask = close_herring != 0
        adjustment[non_zero_mask] -= self.min_distance / self.min_distance

        # Update all individual positions
        positions += np.sum(adjustment, 1)
        positions[0] %= 500
        positions[1] %= 500

    def velocitie_predator(self, predator_pos, positions):
        """ Function that changes the position of the predators, possibly based
        on nearby herring."""

        distances = self.normalize(positions[:, np.newaxis, :] - predator_pos[:, :, np.newaxis]) # all pairwise distances in x and y direction
        squared_distances = np.sum(distances**2, 0)
        closest = np.argmin(squared_distances)

        # Copy the distances matrix
        close_herring = np.copy(distances)
        if closest < self.perception_predator:
            # Obtain the x and y coordinates of the closest fish
            x_coord_closest = close_herring[0, :, :][:, closest]
            y_coord_closest = close_herring[1, :, :][:, closest]

            predator_pos += np.array([x_coord_closest, y_coord_closest]) * self.velocity_predator
            #Changing velocity if fish is closer.

        return predator_pos


    def visualize(self, positions, predator_pos, ax1):
        """ Function to vizualize the herring and predators on the plot."""

        # nu nog gehardcode, nog dynamisch maken
        ax1.axis([0, 500, 0, 500])
        ax1.scatter(positions[0, :], positions[1, :], c='blue', alpha=0.5, marker='o', s=20)
        ax1.scatter(predator_pos[0], predator_pos[1], c='red', alpha=0.5, marker='o', s=20)
        plt.draw()
        plt.pause(0.01)
        ax1.cla()


    def setup_plot(self):
        """ Function that sets up the plot."""
        fig, ax1 = plt.subplots(1)
        ax1.set_aspect('equal')
        ax1.set_facecolor((0.7, 0.8, 1.0))
        ax1.axes.get_xaxis().set_visible(False)
        ax1.axes.get_yaxis().set_visible(False)

        return ax1

    def run(self):
        """ Function that runs an experiment."""

        ax1 = self.setup_plot()

        # Initializing flock and positions
        positions = self.initialize_flock()
        velocities = self.initialize_velocities()
        positions2 = self.initialize_flock()
        velocities2 = self.initialize_velocities()
        predator_pos = self.initialize_predator()

        for _ in range(self.iterations):
            self.collision_avoidance(positions, velocities)
            self.alignment(positions, velocities)
            self.center_movement(positions, velocities)
            self.cohesion(positions, velocities)
            self.visualize(positions, predator_pos, ax1)
            self.velocitie_predator(predator_pos, positions)

            if self.second_flock:
                self.collision_avoidance(positions2, velocities2)
                self.alignment(positions2, velocities2)
                self.center_movement(positions2, velocities2)
                self.cohesion(positions2, velocities2)
                self.visualize(positions,predator_pos, ax1)

# USAGE
upper_lim_flock = np.array([0, 100])
lower_lim_flock = np.array([0, 100])
upper_lim_veloc = np.array([10, 20])
lower_lim_veloc = np.array([0, -20])
upper_lim_predator = np.array([50, 100])
lower_lim_predator = np.array([50, 100])
nr_herring = 20
nr_predators = 1
perception_predator = 5

if __name__ == '__main__':
    doctest.testmod()
    simulation = Experiment(lower_lim_flock, upper_lim_flock, lower_lim_veloc, upper_lim_veloc, nr_herring, nr_predators, lower_lim_predator, upper_lim_predator, perception_predator)
    simulation.run()

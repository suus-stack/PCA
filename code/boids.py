"""
Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405
Description:  Agent-based model to simulate herring school movement dynamics using
              matrices. This code is not complete.
"""

import numpy as np
from  matplotlib import pyplot as plt
import random
import doctest

class Experiment():
    def __init__(self, lower_lim_flock, upper_lim_flock, lower_lim_veloc, upper_lim_veloc,
                                nr_herring, nr_predators, nr_rocks):

        # All initializing methods
        self.width_flock = upper_lim_flock - lower_lim_flock
        self.width_veloc = upper_lim_veloc - lower_lim_veloc
        self.lower_lim_flock = lower_lim_flock
        self.upper_lim_flock = upper_lim_flock
        self.lower_lim_veloc = lower_lim_veloc
        self.upper_lim_veloc = upper_lim_veloc

        # Predator parameters
        self.perception_predator = 50
        self.velocity_predator = 2

        # Experiment setting
        self.nr_herring = nr_herring
        self.nr_predators = nr_predators
        self.nr_rocks = nr_rocks
        self.iterations = 100
        self.second_flock = False

        # Centre movement method, negative=repulsion, positive is attraction
        self.attraction_to_center = 0.0008

        # Collision avoidance method
        self.min_distance = 20

        # Alignment method
        self.formation_flying_distance = 10
        self.formation_flying_strength = 0.8

        # Cohesion method
        self.perception_length_herring = 0.002

    def initialize_flock(self):
        """Function makes an array with the random start positions of the herring.
        If the x-values should vary between 100 and 200 and the y-values to be
        between 900 and 1100, use: lower_lim = np.array([100, 900]) and upper_lim
        = np.array([200, 1100]).

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        flock: Numpy array
            An array of size (2, N), with the initialized positions of all herring,
            where N is the number of herring.
        """
        flock = self.lower_lim_flock[:, np.newaxis] + np.random.rand(2, self.nr_herring) \
                * self.width_flock[:, np.newaxis]
        return flock

    def initialize_predator(self):
        """Function returns an array with the random start positions of the predator.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        flock: Numpy array
            An array with the initialized positions of all preators.
        """
        predator = np.random.rand(2, self.nr_predators) * 500
        return predator

    def rock_initialization(self):
        """ Function makes an array with the random positions of the rocks.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        flock: Numpy array
            An array with the initialized positions of all rocks.
        """
        rock_positions = np.random.rand(2, self.nr_rocks) * 500
        return rock_positions

    def initialize_velocities(self):
        """ Function returns an array of size (2, N), where N is the number of herring,
        with the random initialized velocities of the herring.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        velocities: Numpy array
            An array with the initialized velocities of all herring.
        """
        velocities = self.lower_lim_veloc[:, np.newaxis] + np.random.rand(2, \
                    self.nr_herring) * self.width_veloc[:, np.newaxis]
        return velocities

    def initialize_velocities_predator(self):
        """ Function returns an array of size (2, N) with the random initialized
        velocities of the predator, where N is the number of predators.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        velocities: Numpy array
            An array with the initialized velocities of all predators.
        """
        velocities_predator = self.lower_lim_veloc[:, np.newaxis] + np.random.rand(2, \
                        self.nr_predators) * self.width_veloc[:, np.newaxis]
        return velocities_predator

    def center_movement(self, positions, velocities):
        """ This function applies the center of the mass attraction, the need to get
        to the group. The function adapts the velocities of the herring accordingly.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        positions: Numpy array
            An array with the positions of the herring.
        velocities: Numpy array
            An array with the velocities of the herring.
        """
        # Determine the center of the positions along the horizontal axes
        center = np.mean(positions, 1)

        # Calculating direction vectors from each position to the center and using
        # these vectors to change the velocities
        direction_to_center = positions - center[:, np.newaxis]
        velocities -= direction_to_center * self.attraction_to_center
        positions += velocities

        # Periodic boundaries
        positions[0] %= 500
        positions[1] %= 500

    def normalize(self, vector):
        """Function that normalizes a vector. This ensures we are left with solely
        direction without considering its scale/length.

         Parameters:
         -----------
         self: Experiment
             The experiment being simulated.
         vector: Vector
             The vector that has to be normalized.

         Example:
         --------
         >>> vector = Experiment(0, 1, 0, 1, 10, 5, 1)
         >>> vector.normalize(np.array([3, 4]))
         array([0.6, 0.8])
         >>> vector.normalize(np.array([0.5, 0.2]))
         array([0.92847669, 0.37139068])
         """
        magnitude = np.linalg.norm(vector)

        if magnitude > 0:
            # Scale the vector to have a unit magnitude
            return vector / magnitude
        else:
            # If magnitude is 0, return the original vector
            return vector

    def cohesion(self, positions, velocities):
        """This function finds the surrounding herring for each individual herring
        based on perception length, and aligns the position of the individual herring
        based on its surroundings.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        positions: Numpy array
            An array with the positions of the herring.
        velocities: Numpy array
            An array with the velocities of the herring.
        """
        # Creating a (2, N, N) matrix of pairwise distances between each herring
        distances = self.normalize(positions[:, np.newaxis, :] - positions[:, :, \
                                                                        np.newaxis])
        squared_distances = np.sum(distances**2, 0)

        # Only considering the herring that are perceived by an individual herring
        not_perceived = squared_distances > self.perception_length_herring

        # Creating a matrix containing only the distances of relevant herring
        alignment_herring = np.copy(distances)
        # X-direction
        alignment_herring[0, :, :][not_perceived] = 0
        # Y-direction
        alignment_herring[1, :, :][not_perceived] = 0

        # Taking the columnwise sum for each herring its alignment matrix
        velocities -= np.sum(alignment_herring, 1)
        positions += velocities
        positions = self.add_randomness(positions)

        # Periodic boundaries
        positions[0] %= 500
        positions[1] %= 500

    def alignment(self, positions, velocities):
        """Function that finds the surrounding herring within the radius of the formation
        size, for each individual herring, and aligns the velocity of the individual
        herring based on this. Here the formation_flying_distance determines the radius
        in which herring are considered to be included in the formation size, forming of
        the school.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        positions: Numpy array
            An array with the positions of the herring.
        velocities: Numpy array
            An array with the velocities of the herring.
        """
        # Creating a (2, N, N) matrix of pairwise distances between each herring
        distances = self.normalize(positions[:, np.newaxis, :] - positions[:, :, \
                                                                        np.newaxis])
        squared_distances = np.sum(distances**2, 0) #

        # Determine the velocity differences between all herrings
        velocity_differences = velocities[:, np.newaxis, :] - velocities[:, :, np.newaxis]

        # Only included herring that are considered to be relevant for the flock formation
        excluded_from_formation = squared_distances > self.formation_flying_distance
        velocity_differences_if_close = np.copy(velocity_differences)
        velocity_differences_if_close[0, :, :][excluded_from_formation] = 0
        velocity_differences_if_close[1, :, :][excluded_from_formation] = 0

        velocities -= np.mean(velocity_differences_if_close, 1) * \
                                                self.formation_flying_strength

    def collision_avoidance(self, positions, velocities):
        """ Function that makes sure the herring do not collide.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        positions: Numpy array
            An array with the positions of the herring.
        velocities: Numpy array
            An array with the velocities of the herring.
        """
        # Creating a 2 x N x N matrix of the distances between each herring
        distances = positions[:, np.newaxis, :] - positions[:, :, np.newaxis]
        squared_distances = np.sum(distances**2, 0)

        # Find the herring that are far away
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
        velocities += np.sum(adjustment, 1)
        positions += velocities

        # Periodic boundaries
        positions[0] %= 500
        positions[1] %= 500

    def herring_rock_avoidance(self, positions, rock_positions):
        """Function to adapt the herring velocity to avoid swimming through a rock.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        positions: Numpy array
            An array with the positions of the herring.
        rock_positions: Numpy array
            An array with the positions of the rocks.
        """
        # Calculate distances for all pairs of herring and rocks [i, j]
        all_distances = np.linalg.norm(positions[:, :, np.newaxis] - \
                rock_positions[:, np.newaxis, :], axis=0)

        # Find herring that are too close to rocks
        too_close_mask = all_distances < 25

        # Determine the direction from each rock to herring
        direction_rock_herring = positions[:, :, np.newaxis] - rock_positions[:,\
                                                                    np.newaxis, :]
        direction_rock_herring_normal = direction_rock_herring/ all_distances

        # Adjust the positions of the herring close to a rock
        avoidance_directions = np.where(too_close_mask, direction_rock_herring_normal, 0)
        positions += np.sum(avoidance_directions * (25 - all_distances), axis=2)

        # Periodic boundaries
        positions[0] %= 500
        positions[1] %= 500

    def herring_predator_avoidance(self, positions, predator_pos):
        """Function to adapt the herring velocity to avoid a predator

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        positions: Numpy array
            An (2, N) array with the positions of the herring.
        predator_pos: Numpy array
            An (2, N) array with the positions of the predators.
        """
        # Calculate distances for all pairs of herring and predators [i, j]
        all_distances = np.linalg.norm(positions[:, :, np.newaxis] - \
                predator_pos[:, np.newaxis, :], axis=0)

        # Find herring that are too close to the predators
        too_close_mask = all_distances < 25

        # Determine the direction from each preadator to herring
        direction_predator_herring = positions[:, :, np.newaxis] - predator_pos[:,\
                                                                    np.newaxis, :]
        direction_predator_herring_normal = direction_predator_herring/ all_distances

        # Adjust the positions of the herring away from the predators
        avoidance_directions = np.where(too_close_mask, direction_predator_herring_normal, 0)
        positions += np.sum(avoidance_directions * (25 - all_distances), axis=2)

        # Periodic boundaries
        positions[0] %= 500
        positions[1] %= 500


    def predator_rock_avoidance(self, predator_pos, rock_positions):
        """Function to adapt the predator velocity to avoid the rocks.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        predator_pos: Numpy array
            An array with the positions of the predators.
        rock_positions: Numpy array
            An array with the positions of the rocks.
        """
        # Calculate distances for all pairs of predators and rocks [i, j]
        all_distances = np.linalg.norm(predator_pos[:, :, np.newaxis] - \
                rock_positions[:, np.newaxis, :], axis=0)

        # Find predators that are too close to rocks
        too_close_mask = all_distances < 25

        # Determine the direction from each rock to the predator
        direction_rock_predator = predator_pos[:, :, np.newaxis] - rock_positions[:, \
                                                                        np.newaxis, :]
        direction_rock_predator_normal = direction_rock_predator/ all_distances

        # Adjust the positions of the predator close to a rock
        avoidance_directions = np.where(too_close_mask, direction_rock_predator_normal, 0)
        predator_pos += np.sum(avoidance_directions * (25 - all_distances), axis=2)

        # Periodic boundaries
        predator_pos[0] %= 500
        predator_pos[1] %= 500

    def add_randomness(self, positions):
        """ Function to add randomness to the movement of the herring. The function
        adds a random number to both x and y positions of k randomly chosen fish.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        positions: Numpy array
            An array with the positions of the herring.
        """
        # Number of herring to add randomness to (k) and strength of the randomness
        k=3
        randomness_factor = 10
        selected_columns = random.choices(np.arange(positions.shape[1]), k=k)
        positions[:, selected_columns] = positions[:, selected_columns] + random.random() \
                                        * randomness_factor

        return positions

    def velocitie_predator(self, predator_pos, positions, velocities_predator):
        """ Function that changes the position of the predators, possibly based
        on nearby herring.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        positions: Numpy array
            An array with the positions of the herring.
        predator_pos: Numpy array
            An array with the positions of the predators.
        """
        all_distances = np.linalg.norm(predator_pos[:, :, np.newaxis] - \
                    positions[:, np.newaxis, :], axis=0)

        # find the minimal distance between herring and predator
        min_distance = np.min(all_distances)

        # Find if the closest herring is close enough
        if min_distance < self.perception_predator:

            # Find closeby predators
            close_predators_mask = all_distances < self.perception_predator

            # Determine the direction from each predator to the herring
            direction_predator_herring = positions[:, np.newaxis, :] - predator_pos[:, \
                                                                            :, np.newaxis]
            direction_predator_herring_normal = direction_predator_herring / all_distances

            # Adjust the positions of the predator close to the herring
            attraction_directions = np.where(close_predators_mask,
                                                    direction_predator_herring_normal, 0)
            predator_pos += np.sum(attraction_directions * (self.perception_predator - \
                                all_distances), axis=2)

        # If no herring is close the predator will move in its current direction
        else:
            predator_pos += velocities_predator * self.velocity_predator

        # Periodic boundaries
        predator_pos[0] %= 500
        predator_pos[1] %= 500

    def visualize(self, positions, predator_pos, rock_positions, ax1):
        """ Function to vizualize the herring and predators on the plot.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        positions: Numpy array
            An array with the positions of the herring.
        predator_pos: Numpy array
            An array with the positions of the predators.
        ax1: Plot
            The plot on which the objects have to be visualized.
        """
        ax1.axis([0, 500, 0, 500])
        ax1.scatter(positions[0, :], positions[1, :], c='blue', alpha=0.6, marker='o', s=20)
        ax1.scatter(predator_pos[0], predator_pos[1], c='red', alpha=0.6, marker='o', s=20)
        ax1.scatter(rock_positions[0], rock_positions[1], c= 'grey',  marker = 's', s=20)
        plt.draw()
        plt.pause(0.08)
        ax1.cla()

    def setup_plot(self):
        """ Function that sets up the plot.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        """
        fig, ax1 = plt.subplots(1)
        ax1.set_aspect('equal')
        ax1.set_facecolor((0.7, 0.8, 1.0))
        ax1.axes.get_xaxis().set_visible(False)
        ax1.axes.get_yaxis().set_visible(False)

        return ax1

    def run(self):
        """ Function that runs the experiment.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        """
        ax1 = self.setup_plot()

        # Initializing flock(s) and positions
        positions = self.initialize_flock()
        velocities = self.initialize_velocities()

        # Second flock
        positions2 = self.initialize_flock()
        velocities2 = self.initialize_velocities()

        # External factor initialization
        predator_pos = self.initialize_predator()
        velocities_predator = self.initialize_velocities_predator()
        rock_positions = self.rock_initialization()

        # Update the positions of the predators and herring
        for _ in range(self.iterations):
            self.alignment(positions, velocities)
            self.collision_avoidance(positions, velocities)
            self.center_movement(positions, velocities)
            self.herring_rock_avoidance( positions, rock_positions)
            self.herring_predator_avoidance(positions, predator_pos)
            self.cohesion(positions, velocities)
            self.velocitie_predator(predator_pos, positions, velocities_predator)
            self.predator_rock_avoidance(predator_pos, rock_positions)
            self.visualize(positions, predator_pos, rock_positions, ax1)

            # If needed update the positions of the second flocks
            if self.second_flock:
                self.alignment(positions2, velocities2)
                self.collision_avoidance(positions2, velocities2)
                self.center_movement(positions2, velocities2)
                self.herring_rock_avoidance( positions, rock_positions)
                self.herring_predator_avoidance(positions, predator_pos)
                self.cohesion(positions2, velocities2)
                self.visualize(positions,  predator_pos, rock_positions, ax1)

if __name__ == '__main__':
    # The upper and lower limits for the herring positions and velocities
    upper_lim_flock = np.array([0, 100])
    lower_lim_flock = np.array([0, 100])
    upper_lim_veloc = np.array([10, 20])
    lower_lim_veloc = np.array([0, -20])

    # The number of herring, predators and rocks
    nr_herring = 20
    nr_predators = 2
    nr_rocks = 10

    # Do doc test and run simulation
    doctest.testmod()
    simulation = Experiment(lower_lim_flock, upper_lim_flock, lower_lim_veloc,
            upper_lim_veloc, nr_herring, nr_predators, nr_rocks)
    simulation.run()

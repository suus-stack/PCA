import numpy as np
from  matplotlib import pyplot as plt

class Experiment():
    def __init__(self, lower_lim_flock, upper_lim_flock, lower_lim_veloc, upper_lim_veloc, nr_herring):
        self.width_flock = upper_lim_flock - lower_lim_flock
        self.width_veloc = upper_lim_veloc - lower_lim_veloc
        self.lower_lim_flock = lower_lim_flock
        self.upper_lim_flock = upper_lim_flock
        self.lower_lim_veloc = lower_lim_veloc
        self.upper_lim_veloc = upper_lim_veloc
        self.nr_herring = nr_herring
        self.attraction_to_center = 0.006 # negative=repulsion, positive is attraction 
        self.alignment_distance = 3000 
        self.min_distance = 50
        self.formation_flying_distance = 10 #alignment
        self.formation_flying_strength = 0.5 #alignment
        self.iterations = 100
        self.second_flock = True
        self.perception_length = 0.02

    def initialize_flock(self):
        """ If you want the x-values to vary between 100 and 200 and the y-values to be between
        900 and 1100, you use: lower_lim = np.array([100, 900]) and upper_lim = np.array([200, 1100])"""
        # self.width = upper_lim - lower_lim
        flock = self.lower_lim_flock[:, np.newaxis] + np.random.rand(2, self.nr_herring) * self.width_flock[:, np.newaxis]
        return flock

    def initialize_predator(self):
        pass

    def initialize_velocities(self):
        """Random initialization of velocitie for each herring."""
        # width = upper_lim - lower_lim
        velocities = self.lower_lim_veloc[:, np.newaxis] + np.random.rand(2, self.nr_herring) * self.width_veloc[:, np.newaxis]

        return velocities 

    def center_movement(self, positions, velocities):
        """Center of the mass attraction, like the need to get to the group."""

        center = np.mean(positions, 1) # 1 because along the horizontal axis
        # Calculating direction vectors from each position to the center
        # By adding a new axis the shape of center changes from (2,) to (2,1)
        direction_to_center = positions - center[:, np.newaxis] 

        velocities -= direction_to_center * self.attraction_to_center 
        positions += velocities
        positions[0] %= 500
        positions[1] %= 500
        
    
    def normalize(self, vector):
        magnitude = np.linalg.norm(vector)
        
        if magnitude > 0:
            # Scale the vector to have a unit magnitude
            return vector / magnitude
        else:
            # If the magnitude is 0, return the original vector
            return vector

    def cohesion(self, positions, velocities):
        """Align positions."""
        # eigenlijk is de perception length het verschil tussen min_distance en alignment_distance
        distances = self.normalize(positions[:, np.newaxis, :] - positions[:, :, np.newaxis]) # all pairwise distances in x and y direction
        squared_distances = np.sum(distances**2, 0) # distance from 1 to 2 equals 2 to 1 (eucladian distances)
        # print('squared distances', squared_distances)
        # print('avg squared distance', np.mean(squared_distances))
        too_close = squared_distances < self.min_distance
        too_far = squared_distances > self.alignment_distance

        # Creating an alignment matrix with the herring that are import for the direction 
        alignment_herring = np.copy(distances)
        alignment_herring[0, :, :][too_close] = 0
        alignment_herring[1, :, :][too_close] = 0
        alignment_herring[0, :, :][too_far] = 0
        alignment_herring[1, :, :][too_far] = 0

        velocities -= np.sum(alignment_herring, 1) 
        positions += velocities
        positions[0] %= 500
        positions[1] %= 500

    def alignment(self, positions, velocities):
        """aligning velocities"""

        distances = self.normalize(positions[:, np.newaxis, :] - positions[:, :, np.newaxis]) # all pairwise distances in x and y direction
        squared_distances = np.sum(distances**2, 0) # distance from 1 to 2 equals 2 to 1 (eucladian distances)
        velocity_differences = velocities[:, np.newaxis, :] - velocities[:, :, np.newaxis]
       
        very_far = squared_distances > self.formation_flying_distance
        velocity_differences_if_close = np.copy(velocity_differences)
        velocity_differences_if_close[0, :, :][very_far] = 0
        velocity_differences_if_close[1, :, :][very_far] = 0
        velocities -= np.mean(velocity_differences_if_close, 1) * self.formation_flying_strength 


    def collision_avoidance(self, positions, velocities):
        """..."""

        #Creating a 2 x N x N matrix of the distances between each herring
        distances = positions[:, np.newaxis, :] - positions[:, :, np.newaxis] # all pairwise distances in x and y direction
        squared_distances = np.sum(distances**2, 0) # distance from 1 to 2 equals 2 to 1 (eucladian distances)
        # print('squared_distances', squared_distances)

        # making sure that the impact of herring far away is not taken into account 
        # far_away = squared_distances > self.min_distance
        far_away = squared_distances > self.min_distance
        # print('far away', far_away)

        close_herring = np.copy(distances)
        # X-direction
        close_herring[0, :, :][far_away] = 0
        # Y-direction
        close_herring[1, :, :][far_away] = 0

        # print('close_herring', close_herring)
        adjustment = np.copy(close_herring)
        non_zero_mask = close_herring != 0
        adjustment[non_zero_mask] -= self.min_distance * 0.1
        # print('adjustment', adjustment)
        # adjustment = self.min_distance - close_herring
        # adjustment = positions - self.min_distance
        # print('adjustment', adjustment) 
        
        # Update all individual positions
        positions += np.sum(adjustment, 1) 
        positions[0] %= 500
        positions[1] %= 500


    def visualize(self, positions, ax1):
        # nu nog gehardcode, nog dynamisch maken
        ax1.axis([0, 500, 0, 500])
        ax1.scatter(positions[0, :], positions[1, :], c='blue', alpha=0.5, marker='o', s=20)
        plt.draw()
        plt.pause(0.01)
        ax1.cla()


    def setup_plot(self):
        fig, ax1 = plt.subplots(1)
        ax1.set_aspect('equal')
        ax1.set_facecolor((0.7, 0.8, 1.0))
        ax1.axes.get_xaxis().set_visible(False)
        ax1.axes.get_yaxis().set_visible(False)

        return ax1

    def run(self):

        ax1 = self.setup_plot()

        # Initializing flock and positions
        positions = self.initialize_flock()
        velocities = self.initialize_velocities()
        positions2 = self.initialize_flock()
        velocities2 = self.initialize_velocities()

        for _ in range(self.iterations):
            self.collision_avoidance(positions, velocities)
            self.alignment(positions, velocities)
            self.center_movement(positions, velocities)
            self.cohesion(positions, velocities)
            self.visualize(positions, ax1)
                
            if self.second_flock:
                self.collision_avoidance(positions2, velocities2)
                self.alignment(positions2, velocities2)
                self.center_movement(positions2, velocities2)
                self.cohesion(positions2, velocities2)
                self.visualize(positions, ax1)

# USAGE
upper_lim_flock = np.array([0, 100])
lower_lim_flock = np.array([0, 100])
upper_lim_veloc = np.array([10, 20])
lower_lim_veloc = np.array([0, -20])
nr_herring = 20

if __name__ == '__main__':
    simulation = Experiment(lower_lim_flock, upper_lim_flock, lower_lim_veloc, upper_lim_veloc, nr_herring)
    simulation.run()
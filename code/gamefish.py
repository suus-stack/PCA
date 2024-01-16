"""
Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405
Description:  Agent-based model to simulate herring school movement dynamics. It
determine the killing rate in different kinds of environments, with and without
rocks and/or predators.
"""

import pygame
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from itertools import combinations

class Config:
    """ Class that stores the values of all the constants in the experiment"""

    WIDTH = 600
    HEIGHT = 600
    FRAMES_PER_SECOND = 30

    """herring parameters"""
    HERRING_RADIUS = 4
    SEPARATION_DISTANCE = 10
    ALIGNMENT_DISTANCE =20
    COHESION_DISTANCE = 20
    HERRING_SPEED = 3
    HERRING_SPEED_MAX = 6
    PERCEPTION_LENGHT_HERRING = 20
    KILL_DISTANCE = 5

    """predator parameter"""
    PREDATOR_RADIUS = 7
    PREDATOR_SPEED = 4
    PREDATOR_SPEED_MAX = 8
    PERCEPTION_LENGHT_PREDATOR = 40

    """rock parameters"""
    ROCK_LENGHT = 10

class Herring(pygame.sprite.Sprite):

    # Keeping track of the number of killed herring
    killed_herring = 0

    def __init__(self, x_pos, y_pos):
        """Function that initialize a herring.

        Parameters:
        -----------
        self: Herring
            The herring being initialized.
        x_pos: Float
            The x-coordinate of the herring position.
        y_pos: Float
            The y-coordinate of the herring position.
        """
        super().__init__()
        # Creating the visualization of the herring and adding to the display
        self.image = pygame.Surface((Config.HERRING_RADIUS * 2, Config.HERRING_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255), (Config.HERRING_RADIUS, Config.HERRING_RADIUS), Config.HERRING_RADIUS)
        self.rect = self.image.get_rect(center=( x_pos, y_pos))

        # Add the position of the herrring to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

        # Pick velocity and multiply it with the correct speed
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        self.velocity = pygame.Vector2(dx, dy).normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

    def separation_herring(self, all_herring):
        """ Function that implements the separation rule, stating that a herring
        does not get closer to an other herring than some minimum distance. The
        closer the neighbour the stronger its influence.

        Parameters:
        -----------
        self: Herring
            The herring for which the separation vector is determined.
        all_herring: Pygame.sprite.Group
            Group containing all herring entities.

        Returns:
        --------
        average_separation_vector: Vector
            The average separation vector indicating the direction to keep a distance
            from neighbour herring.
        """
        total_separation_vector = pygame.Vector2(0, 0)
        average_separation_vector = pygame.Vector2(0, 0)
        neighbour_herring_separation = 0

        # Finding the herring within the seperation distance
        for herring in all_herring:
            distance_two_herring = self.position.distance_to(herring.position)

            if herring != self and distance_two_herring != 0 and distance_two_herring < Config.SEPARATION_DISTANCE:
                    # Determine separation vector and add it to the total vector
                    verctor_keep_separation = (self.position - herring.position)/ distance_two_herring
                    total_separation_vector += verctor_keep_separation
                    neighbour_herring_separation += 1

        # Calculate average separation vector
        if neighbour_herring_separation > 0:
            average_separation_vector = total_separation_vector / neighbour_herring_separation

        return(average_separation_vector)

    def alignment_herring(self, all_herring):
        """ Function that implements the alignment rule, stating that the herring
        heads in the direction of the neighbours within the alignment distance.

        Parameters:
        -----------
        self: Herring
            The herring for which the alignment vector is determined.
        all_herring: pygame.sprite.Group
            Group containing all herring entities.

        Returns:
        --------
        average_alignment_vector: Vector
            The average alignment vector indicating the direction of its closest neighbours.
        """
        total_alignment_vector = pygame.Vector2(0, 0)
        average_alignment_vector = pygame.Vector2(0, 0)
        neighbour_herring_alignment = 0

        # Finding the herring within the alignment distance
        for herring in all_herring:
            distance_two_herring = self.position.distance_to(herring.position)

            if herring != self and distance_two_herring != 0 and distance_two_herring < Config.ALIGNMENT_DISTANCE:
                    # Add direction of the neighbour to the total alignment vector
                    total_alignment_vector += herring.velocity
                    neighbour_herring_alignment += 1

        # Calculate the avreage alignment vector
        if neighbour_herring_alignment > 0:
            average_alignment_vector = total_alignment_vector / neighbour_herring_alignment

        return average_alignment_vector

    def cohesion_herring(self, all_herring):
        """ Function that implements the cohesion rule, stating that the herring
        moves to the position of the neighbours within the cohesion distance. The
        closer the neighbour the stronger its influence.

        Parameters:
        -----------
        self: Herring
            The herring for which the cohesion vector is determined.
        all_herring: pygame.sprite.Group
            Group containing all herring entities.

        Returns:
        --------
        average_cohesion_vector: Vector
            The average cohesion vector indicating the position of its closest neighbours.
        """
        total_cohesion_vector = pygame.Vector2(0, 0)
        average_cohesion_vector = pygame.Vector2(0, 0)
        neighbour_herring_cohesion = 0

        # Finding the herring within the cohesion distance
        for herring in all_herring:
            distance_two_herring = self.position.distance_to(herring.position)

            if herring != self and distance_two_herring != 0 and distance_two_herring < Config.COHESION_DISTANCE:
                    # Determine the cohesion vector and add it to the total vector
                    verctor_close_cohesion = (herring.position - self.position) / distance_two_herring
                    total_cohesion_vector += verctor_close_cohesion
                    neighbour_herring_cohesion += 1

        # Calculate the avreage cohesion vector
        if neighbour_herring_cohesion > 0:
            average_cohesion_vector = total_cohesion_vector / neighbour_herring_cohesion

        return(average_cohesion_vector)

    def rules_updatey(self, all_herring):
        """ Function that calculates the total vector of the separation, alignment
        and cohesion behavoiurs with neighbour herring and updates the velocity using
        this vector

        Parameters:
        -----------
        self: Herring
            The herring for which the vector is determined.
        all_herring: pygame.sprite.Group
            Group containing all herring entities.
        """
        # Determine the total effect of the three rules
        alignment_vector = self.alignment_herring(all_herring)
        cohesion_vector = self.cohesion_herring(all_herring)
        separation_vector = self.separation_herring(all_herring)
        total_vector_rules = separation_vector + alignment_vector + cohesion_vectors

        # Normalize velocity and multiply by speed to which some variation is added
        self.velocity += total_vector_rules
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

    def avoid_predator(self, all_predators):
        """ Function that ensures that a herring avoids the predator if the predator
        is within the perception lenght of the herring. The closer the predator the
        more it will influence the direction of the herring

        Parameters:
        -----------
        self: Herring
            The herring currently updated.
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        """
        total_predator_avoidance_vector = pygame.Vector2(0, 0)
        average_predator_avoidance_vector = pygame.Vector2(0, 0)
        neighbour_predator = 0

        # Finding the predators within the perception distance
        for predator in all_predators:
            distance_to_predator = self.position.distance_to(predator.position)

            if distance_to_predator < Config.PERCEPTION_LENGHT_HERRING and distance_to_predator != 0:
                # Determine the avoidance vector and add it to total vector
                total_predator_avoidance_vector += (self.position - predator.position) / distance_to_predator
                neighbour_predator +=1

        # Calculate the avreage predator avoidance vector
        if neighbour_predator > 0:
            average_predator_avoidance_vector = total_predator_avoidance_vector / neighbour_predator

            # Multiply by 2.5 to make moving away from predator extra important
            self.velocity += average_predator_avoidance_vector *2.5

        # Normalizing velocity and multiply by speed to which some variation is added
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

    def avoid_rock(self, all_rocks):
        """ Function that ensures the herring does not swim through a rock but will
        swim around or away from a rock

        Parameters:
        -----------
        self: Herring
            The herring currently updated.
        all_rocks: pygame.sprite.Group
            Group containing all rock entities.
        """
        total_rock_avoidance_vector = pygame.Vector2(0, 0)
        average_rock_avoidance_vector = pygame.Vector2(0, 0)
        neighbour_rock = 0

        # Finding the closeby rocks
        for rock in all_rocks:
            distance_to_rock = self.position.distance_to(rock.position)

            if distance_to_rock < 12 and distance_to_rock != 0 :
                # Determine the avoidance vector and add it to total vector
                total_rock_avoidance_vector += (self.position - rock.position)/ distance_to_rock
                neighbour_rock +=1

        # Determine the average rock avoidance vector
        if neighbour_rock > 0:
            average_rock_avoidance_vector = total_rock_avoidance_vector / neighbour_rock

            # multiply by three to ensure moving away from rock is extra important
            self.velocity += average_rock_avoidance_vector * 3

        # normalize velocity and multiply by speed to which some variation is added
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

    def accelerate_to_avoid_perdator(self, all_predators):
        """Function that ensures the herring will accelerate when a predator is within
        its perception lenght. The closer the predator is the faster the herrig will move

        Parameters:
        -----------
        self: Herring
            The herring currently updated.
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        """
        # Determine if the closest predator is within the perception distance
        if all_predators:
            closest_predator_distance = min(self.position.distance_to(predator.position) for predator in all_predators)

            if closest_predator_distance < Config.PERCEPTION_LENGHT_HERRING:
                speed_h = Config.HERRING_SPEED

                # Normalize velocity and multiply by the changed speed to which some variation is added.
                self.velocity = self.velocity.normalize() * (speed_h + (Config.HERRING_SPEED_MAX -Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING))

    def kill_herring(self, all_herring, all_predators):
        """ Function that ensures the herring gets killed when within the killing
        distance of the predator

        Parameters:
        -----------
        self: Herring
            The herring currently updated.
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        all_herring: pygame.sprite.Group
            Group containing all herring entities.
        """
        # Determine if a predator is within the kill distance
        for predator in all_predators:
            distance_to_herring = self.position.distance_to(predator.position)

            if distance_to_herring < Config.KILL_DISTANCE:
                all_herring.remove(self)
                Herring.killed_herring += 1

    def update(self, all_herring, all_predators, all_rocks):
        """Function to update the position of a herring. The new position is dependent
         on the old position, the cohesion, separation and alignment rules, the rock
         positions and the positions of the predator(s).

        Parameters:
        -----------
        self: Herring
            The herring currently updated.
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        all_herring: pygame.sprite.Group
            Group containing all herring entities.
        all_rocks: pygame.sprite.Group
            Group containing all rock entities.
        """
        # Appy three boids rules
        self.rules_update(all_herring)

        # Determine influence of the environment
        self.kill_herring(all_herring, all_predators)
        self.avoid_predator(all_predators)
        self.avoid_rock(all_rocks)
        self.accelerate_to_avoid_perdator(all_predators)

        # Change the position
        self.position += self.velocity

        # Periodic boundaries
        self.position.x = self.position.x % Config.WIDTH
        self.position.y = self.position.y % Config.HEIGHT

        # Update the center of the herring form
        self.rect.center = self.position


class Predator(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        """Function that initialize a predator.

        Parameters:
        -----------
        self: Predator
            The predator being initialized.
        x_pos: Float
            The x-coordinate of the predator position.
        y_pos: Float
            The y-coordinate of the predator position.
        """
        super().__init__()
        # Creating the visualization of the predator and adding to the display
        self.image = pygame.Surface((Config.PREDATOR_RADIUS * 2, Config.PREDATOR_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,0, 0), (Config.PREDATOR_RADIUS, Config.PREDATOR_RADIUS), Config.PREDATOR_RADIUS)
        self.rect = self.image.get_rect(center=( x_pos, y_pos))

        # Add the position of the predator to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

        # Pick velocity and multiply it with the correct speed
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        self.velocity = pygame.Vector2(dx, dy).normalize() * (Config.PREDATOR_SPEED + random.uniform(-0.4, 0.4))

    def collision_avoidance(self, all_predators):
        """ Function that makes sure predators donnot fully collide

        Parameters:
        -----------
        self: Predator
            The predator currently updated.
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        """
        total_collision_avoidance_vector = pygame.Vector2(0, 0)
        average_collision_avoidance_vector = pygame.Vector2(0, 0)
        close_predator = 0

        # Finding the predators within the perception lenght
        for predator in all_predators:
            distance_between_predator = self.position.distance_to(predator.position)

            if predator != self and distance_between_predator !=0 and distance_between_predator < Config.PERCEPTION_LENGHT_PREDATOR:

                    # Make a collision avoidance vector and dd it to total vector
                    collision_avoidance_vector = (self.position - predator.position) / distance_between_predator
                    total_collision_avoidance_vector += collision_avoidance_vector
                    close_predator += 1

        # Calculate the average collision avoidance vector
        if close_predator > 0:
            average_collision_avoidance_vector = total_collision_avoidance_vector / close_predator
            self.velocity += average_collision_avoidance_vector

        # Normalize velocity and multiply by speed to which some variation is added
        self.velocity = self.velocity.normalize() * (Config.PREDATOR_SPEED + random.uniform(-2, 2))

    def attack_herring(self, all_herring):
        """ Function that ensures a predator will attack a herring when the herring
        is within its perception lenght. The closer the herring the more influence
        it has on the direction of the predator

        Parameters:
        -----------
        self: Predator
            The predator currently updated.
        all_herring: pygame.sprite.Group
            Group containing all herring entities.
        """
        total_herring_attack_vector = pygame.Vector2(0, 0)
        average_herring_attack_vector = pygame.Vector2(0, 0)
        neighbour_herring = 0

        # Finding the herrings within the perception lenght
        for herring in all_herring:
            distance_to_herring = self.position.distance_to(herring.position)

            if distance_to_herring < Config.PERCEPTION_LENGHT_PREDATOR and distance_to_herring != 0:

                # Determine the attack vector and add it to the total vector
                direction_to_herring = ( herring.position - self.position ) / distance_to_herring
                total_herring_attack_vector += direction_to_herring
                neighbour_herring +=1

        # Determine the average attack vector
        if neighbour_herring > 0:
            average_herring_attack_vector = total_herring_attack_vector  / neighbour_herring
            self.velocity +=  average_herring_attack_vector* 2

        # Normalize velocity and multiply by speed to which some variation is added
        self.velocity = self.velocity.normalize() * (Config.PREDATOR_SPEED + random.uniform(-0.4, 0.4))

    def avoid_rock(self, all_rocks):
        """ Function that ensures the predator will swim around or away from a rock

        Parameters:
        -----------
        self: Predator
            The predator currently updated.
        all_rocks: pygame.sprite.Group
            Group containing all rock entities.
        """
        total_rock_avoidance_vector = pygame.Vector2(0, 0)
        average_rock_avoidance_vector = pygame.Vector2(0, 0)
        neighbour_rock = 0

        # Finding closeby rocks
        for rock in all_rocks:
            distance_to_rock = self.position.distance_to(rock.position)

            if distance_to_rock < 15 and distance_to_rock != 0 :

                # Make an avoidance vector and add it to total vector
                rock_avoidance_vector = (self.position - rock.position)/ distance_to_rock
                total_rock_avoidance_vector += rock_avoidance_vector
                neighbour_rock +=1

        # Determine the average avoidance vector
        if neighbour_rock > 0:
            average_rock_avoidance_vector = total_rock_avoidance_vector / neighbour_rock

            # Multiply by three to ensure moving away from rock is extra important
            self.velocity += average_rock_avoidance_vector * 3

        # Normalize velocity and multiply by speed to which some variation is added
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

    def accelerate_to_attack_herrig(self, all_herring):
        """Function that ensures the predator will accelerate when a herring is within
        its perception lenght. The closer the herring is the faster the predator
        will move.

        Parameters:
        -----------
        self: Predator
            The predator currently updated.
        all_herring: Pygame.sprite.Group
            Group containing all herring entities.
        """

        # check if the closest herring is within the perception distance
        if all_herring:
            closest_herring_distance = min(self.position.distance_to(herring.position) for herring in all_herring)

            if closest_herring_distance < Config.PERCEPTION_LENGHT_PREDATOR:
                speed_p = Config.PREDATOR_SPEED

                # Normalize velocity and multiply by changed speed to which some variation is added
                self.velocity = self.velocity.normalize() * (speed_p + (Config.PREDATOR_SPEED_MAX - Config.PREDATOR_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_PREDATOR-closest_herring_distance) / Config.PERCEPTION_LENGHT_PREDATOR))

    def update(self, all_herring, all_predators, all_rocks):
        """ Function to update the position of a predator. The new position is
        dependent on the the rock positions, old position and the positions of
        the herring.

        Parameters:
        -----------
        self: Predators
            The predator currently updated.
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        all_herring: pygame.sprite.Group
            Group containing all herring entities.
        all_rocks: pygame.sprite.Group
            Group containing all rock entities.
        """
        # Determine influence of the environment
        self.attack_herring(all_herring)
        self.avoid_rock(all_rocks)
        self.collision_avoidance(all_predators)
        self.accelerate_to_attack_herrig(all_herring)

        # Change the position
        self.position += self.velocity

        # Periodic boundaries
        self.position.x = self.position.x % Config.WIDTH
        self.position.y = self.position.y % Config.HEIGHT

        # Update the center of the predator form
        self.rect.center = self.position


class Rock(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        """Function that initialize a rock.

        Parameters:
        -----------
        self: Rock
            The rock being initialized.
        x_pos: float
            The x-coordinate of the rock position.
        y_pos: float
            The y-coordinate of the rock position.
        """
        super().__init__()
        # Creating the visualization of the rock and adding to the display
        self.image = pygame.Surface((Config.ROCK_LENGHT * 2, Config.ROCK_LENGHT * 2), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (125, 125, 125), (0, 0, Config.ROCK_LENGHT, Config.ROCK_LENGHT))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        # Add the position of the rock to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

    def distance_to(self, other_position):
        """ Function that calculates the ecludian distance between two rocks

        Parameters:
        -----------
        self: Rock
            The rock being observed.
        other_position: List
            The position of the other rock.

        Returns:
        -----------
        distance_rocks: float
            The ecludian distance between two rocks.
        """
        distance_rocks = np.sqrt((self.position[0] - other_position[0])**2 + (self.position[1] - other_position[1])**2)
        return distance_rocks


class Experiment(pygame.sprite.Sprite):
    def __init__(self, herring_nr = 100, predator_nr = 1, rock_nr = 10, simulation_duration = 20, extra_rocks = False, start_school = False, perception_change = False, alignment_distance = 40, cohesion_distance = 40, separation_distance = 20):
        """Initialize an experiment (simulation) with specified parameters.

        Parameters:
        -----------
        self: Experiment
            The experiment being initialized.
        herring_nr: Int
            The number of herring in the experiment.
        predator_nr: Int
            The number of predators in the experiment.
        rock_nr: Int
            The number of rocks in the experiment.
        simulation_duration: Int
            The number of seconds the experiment is simulated.
        extra_rocks: Bool
            If true areas between close rocks ar filled with more rocks.
        start_school: Bool
            If true the herring ar not randomly placed but in a school
        perception_change: Bool
            If true perception lenght of predator changes over the time
        alignment_distance: Float
            The distance that determines which neighbour herring are used for the
            alignment rule
        cohesion_distance: Float
            The distance that determines which neighbour herring are used for the
            cohesion rule
        separation_distance: Float
            The distance that determines which neighbour herring are used for the
            separation rule
        """
        # set the experiment parameters to the specified values
        self.herring_nr = herring_nr
        self.predator_nr = predator_nr
        self.rock_nr = rock_nr
        self.simulation_duration = simulation_duration
        self.extra_rocks = extra_rocks
        self.start_school = start_school
        self.perception_change = perception_change
        Config.ALIGNMENT_DISTANCE = alignment_distance
        Config.COHESION_DISTANCE = cohesion_distance
        Config.SEPARATION_DISTANCE = separation_distance

    def distance_two_positions(self, position_1, position_2):
        """ Function that calculates the ecludian distance between two positions

        Parameters:
        -----------
        position_1: List
            The position of onject 1
        position_2: List
            The position of onject 2

        Returns:
        -----------
        distance_objects: float
            The ecludian distance between two objects.
        """
        distance_objects = np.sqrt((position_1[0] - position_2[0])**2 + (position_1[1] - position_2[1])**2)
        return distance_objects

    def extra_rocks_experiment(self, all_rocks):
        """ Function tha adds extra rocks to the rock population to connect rocks
        that lay close to one another

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        all_predators: Pygame.sprite.Group
            Group containing all predator entities.
        """
        distances = []

        # Pairwise loop
        for rockA in all_rocks:
            for rockB in all_rocks:
                if rockA != rockB:

                    # Calculate Euclidean distances between rocks
                    distance_rock = rockB.distance_to(rockA.position)

                    # Make clusters
                    if distance_rock < 60:
                        num_extra_rocks = int((60 - distance_rock) / 10)

                        # Fill the distance
                        for i in range(1, num_extra_rocks + 1):
                            ratio = i / (num_extra_rocks + 1)
                            new_x = int(rockA.position[0] + ratio * (rockB.position[0] - rockA.position[0]))
                            new_y = int(rockA.position[1] + ratio * (rockB.position[1] - rockA.position[1]))
                            distances.append((new_x, new_y))

                            # Add the rock to the rock population
                            new_rock = Rock(new_x, new_y)
                            all_rocks.add(new_rock)

                        # Make 'clusters'
                        for n in range(num_extra_rocks):
                            random_ratio = random.uniform(0, 1)
                            if rockA.position[1] == rockB.position[1]:
                                new_x = int(rockB.position[0] + random_ratio * (rockB.position[0] - rockA.position[0]))
                                new_y = int(rockA.position[1] + random_ratio * (rockB.position[1] - rockA.position[1]))
                                new_rock = Rock(new_x, new_y)
                                all_rocks.add(new_rock)

                            else:
                                new_x = int(rockA.position[0] + random_ratio * (rockB.position[0] - rockA.position[0]))
                                new_y = int(rockB.position[1] + random_ratio * (rockB.position[1] - rockA.position[1]))
                                new_rock = Rock(new_x, new_y)
                                all_rocks.add(new_rock)

    def add_rocks_experiment(self):
        """ Function thad adds rocks to the experiment

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        """
        all_rocks = pygame.sprite.Group()

        # Give all the rocks a position and add them to the group
        for _ in range(self.rock_nr):
            rock_i = Rock(random.randint(0, Config.WIDTH), random.randint(0, Config.HEIGHT))
            all_rocks.add(rock_i)

        # add ectra rocks if needed
        if self.extra_rocks == True:
            self.extra_rocks_experiment(all_rocks)

        return all_rocks

    def add_herring_experiment(self, all_rocks):
        """ Function that adds herring to the experiment

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        all_herring: pygame.sprite.Group
            Group containing all herring entities.
        """
        all_herring = pygame.sprite.Group()

        # Give all the herring a position and add them to the group
        for _ in range(self.herring_nr):

            # Determine if the herring schould start in a school
            if self.start_school == True:
                # Give the herring its own position not under a rock
                pos_x = random.randint(0, Config.WIDTH)
                pos_y = random.randint(0, Config.HEIGHT)
                position_herring = [pos_x, pos_y]

                while any(self.distance_two_positions(rock.position, position_herring) < 10 for rock in all_rocks) or any(herring.position == position_herring for herring in all_herring) or any(self.distance_two_positions(herring.position, position_herring) > 100 for herring in all_herring):
                    pos_x = random.randint(0, Config.WIDTH)
                    pos_y = random.randint(0, Config.HEIGHT)
                    position_herring = [pos_x, pos_y]

                # Add the herring to the herring population
                herring_i = Herring(pos_x, pos_y)
                all_herring.add(herring_i)

            else:
                # Give the herring its own position not under a rock
                pos_x = random.randint(0, Config.WIDTH)
                pos_y = random.randint(0, Config.HEIGHT)
                position_herring = [pos_x, pos_y]

                while any(self.distance_two_positions(rock.position, position_herring) < 10 for rock in all_rocks) or any(herring.position == position_herring for herring in all_herring):
                    pos_x = random.randint(0, Config.WIDTH)
                    pos_y = random.randint(0, Config.HEIGHT)
                    position_herring = [pos_x, pos_y]

                # Add the herring to the herring population
                herring_i = Herring(pos_x, pos_y)
                all_herring.add(herring_i)

        return all_herring

    def add_predator_experiment(self, all_rocks, all_herring):
        """ Function that adds predators to the experiment

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        """
        all_predators = pygame.sprite.Group()

        # Give all the predators a position and add them to the group
        for _ in range(self.predator_nr):

            # Give the predator its own position not under a rock and not near a herring
            pos_x = random.randint(0, Config.WIDTH)
            pos_y = random.randint(0, Config.HEIGHT)
            position_predator = [pos_x, pos_y]

            while any(self.distance_two_positions(rock.position, position_predator) < 10 for rock in all_rocks) or any(self.distance_two_positions(herring.position, position_predator) < Config.PERCEPTION_LENGHT_PREDATOR for herring in all_herring) or any(predator.position == position_predator for predator in all_predators):
                pos_x = random.randint(0, Config.WIDTH)
                pos_y = random.randint(0, Config.HEIGHT)
                position_predator  = [pos_x, pos_y]

            # Add the predator to thepredator population
            predator_i = Predator(pos_x, pos_y)
            all_predators.add(predator_i)

        return all_predators

    def make_legend(self, font_style, screen):
        """Function that adds a legend to the simulation screen

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        font: Font
            The font used to style the text in the legend.
        screen: Screen
            The screen on which the legend is shown.
        """
        # Make a white background for the legend
        legend_background_rect = pygame.Rect(2, Config.HEIGHT-495, 80, 50)
        pygame.draw.rect(screen, 'white', legend_background_rect)

        # Add text to write herring in blue
        herring_legend_text = font_style.render("Herring", True, 'blue')
        herring_legend_rect = herring_legend_text.get_rect()
        herring_legend_rect.topleft = (5, Config.HEIGHT - 490)
        screen.blit(herring_legend_text, herring_legend_rect)

        # Add text to write predator in red
        predator_legend_text = font_style.render("Predator", True, 'red')
        predator_legend_rect = predator_legend_text.get_rect()
        predator_legend_rect.topleft = (5, Config.HEIGHT - 475)
        screen.blit(predator_legend_text, predator_legend_rect)

        # Add text to write rock in gray
        rock_legend_text = font_style.render("Rock", True, 'gray')
        rock_legend_rect = rock_legend_text.get_rect()
        rock_legend_rect.topleft = (5, Config.HEIGHT - 460)
        screen.blit(rock_legend_text, rock_legend_rect)

        return screen

    def predator_perception_change(self, showed_frames, list_predator_perception_lenght, list_killed_herring_count):
        """ Function that changes the predator perception lenghtbover the time.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        showed_frames: Int
            The number of frames that is shown.
        list_predator_perception_lenght: List
            List with the perception lenght of the predator on every measure
            timepoint.
        list_killed_herring: List
            List with the number of killed herring between every timepoint.

        Returns:
        -----------
        list_predator_perception_lenght: List
            List with the perception lenght of the predator on every measure
            timepoint.
        list_killed_herring: List
            List with the number of killed herring between every timepoint.
        """
        # Convert the number of frame to seconds and determine the elapsed time
        frame_to_seconds = showed_frames / Config.FRAMES_PER_SECOND
        elapsed_time = frame_to_seconds % 240

        # Check if the perception lenght of predator should decrease
        if elapsed_time <= 120 and round(elapsed_time, 4) % 10 == 0:
            list_predator_perception_lenght.append(Config.PERCEPTION_LENGHT_PREDATOR)
            Config.PERCEPTION_LENGHT_PREDATOR -= 2

            # Determine th number of killed herring
            killed_herring_count = Herring.killed_herring
            list_killed_herring_count.append(killed_herring_count)
            Herring.killed_herring = 0

        # Check if the perception lenght of predator should increase
        if elapsed_time > 120 and round(elapsed_time, 4) % 10 == 0:
            list_predator_perception_lenght.append(Config.PERCEPTION_LENGHT_PREDATOR)
            Config.PERCEPTION_LENGHT_PREDATOR += 2

            # Determine the number of killed herring
            killed_herring_count = Herring.killed_herring
            list_killed_herring_count.append(killed_herring_count)
            Herring.killed_herring = 0
            print(elapsed_time, 'hi')

        return(list_predator_perception_lenght, list_killed_herring_count)

    def run(self):
        """ Function that runs an experiment

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        """
        pygame.font.init()
        pygame.init()

        # Set the number of killed herring to zero
        Herring.killed_herring = 0

        # If needed make extra lists and a parameter
        if self.perception_change == True:
            list_killed_herring_count = []
            list_predator_perception_lenght = []

        # Make the rocks, herring and predator group
        all_rocks = self.add_rocks_experiment()
        all_herring = self.add_herring_experiment(all_rocks)
        all_predators = self.add_predator_experiment(all_rocks, all_herring)

        # make a screen
        screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption(f'Simulation of herring school with {self.herring_nr} herring and {self.predator_nr} predator(s)')
        font_style = pygame.font.Font(None, 23)
        clock = pygame.time.Clock()

        # Set running of simulation as TRUE
        simulation_run = True

        # Determine the number of total frames that have to be shown
        total_frames = Config.FRAMES_PER_SECOND * self.simulation_duration
        showed_frames = 0

        # Run the simulation as long as simulation running = TRUE
        while simulation_run:
            showed_frames += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    simulation_run = False

            # Update the position of the herring and predators
            all_herring.update(all_herring, all_predators, all_rocks)
            all_predators.update(all_herring, all_predators, all_rocks)

            # Draw the herring, rocks and predators on the screen
            screen.fill((173, 216, 230))
            all_herring.draw(screen)
            all_predators.draw(screen)
            all_rocks.draw(screen)
            screen = self.make_legend(font_style, screen)

            # Update display
            pygame.display.flip()

            # keep track of the number of killed herring
            killed_herring_count = Herring.killed_herring

            # Determine if perception lenght should maybe change
            if self.perception_change == True:
                list_predator_perception_lenght, list_killed_herring_count = self.predator_perception_change(showed_frames, list_predator_perception_lenght, list_killed_herring_count)

            # Stop the simultion after the specified time
            if showed_frames >= total_frames:
                simulation_run = False

            clock.tick(Config.FRAMES_PER_SECOND)

        # If the while loop is stoped quite the game
        pygame.quit()

        # return killed herring and if needed the perception lenght of the predator
        if self.perception_change == True:
            return list_killed_herring_count, list_predator_perception_lenght
        else:
            return killed_herring_count

if __name__ == "__main__":
    """
    The parameters that have to be given:
    1: The number of herring in the simulation (int). default set to one hunderd.
    2: The number of predators in the simulation (int). Default set to one.
    3: The number of rocks in the simulation (int). default set to ten.
    4: The duration of the simulation in seconds (int). Defaut set to twenty.
    5: Closeby rocks should be connected via more rocks (Bool). Default set to False.
    6: Herring start as one school instead of randomly (bool). Default set to False.
    7: Predator perception lenght changes over the time (bool). Default set to False.
    8: The alignment distance (float). Default set to 40.
    9: The cohestion distance (float). Default set to 40.
    10: The separation distance (float). Default set to 15.
    """
    experiment_example = Experiment(40, 5, 20, 48, True, False, True)
    list_killed_herring, list_predator_perception_lenght = experiment_example.run()

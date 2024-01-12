
# make a parameter not constant (maybe change over the day nightitme they see less)
# small amount of randomness into perception length (random fluctuation =)
# oval body, circle shape, connecting two ponds
# agents cannot move out agent based models support boundaries (opzoeken en onderbouwen)
# is strategy still valid in different sizes of pools

import pygame
import sys
import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt

"""
Authors:      Suze Frikke, Luca Pouw, Eva Nieuwenhuis
University:   Universiteit van Amsterdam (UvA)
Course:       Project computational science
Student id's:
Description: Agent-based moddel to simulate herring school movement dynamics when
confronted with predators.
"""

class Config:
    """ Class that stores the values of all the constants in the experiment. Makes it easy to adapt
    parameter values to change experimental outcomes."""

    WIDTH = 500
    HEIGHT = 500
    FRAMES_PER_SECOND = 30
    HERRING_RADIUS = 4

    # Distance in which neighbours have to be to influenced by the direction of a herring
    SEPARATION_DISTANCE = 20
    ALIGNMENT_DISTANCE = 40
    COHESION_DISTANCE = 40

    HERRING_SPEED = 3
    HERRING_SPEED_MAX = 6

    # Length at which a herring can sense a predator
    PERCEPTION_LENGHT_HERRING = 40

    # Distance at wich a predator can kill a herring
    KILL_DISTANCE = 5
    PREDATOR_RADIUS = 6
    PREDATOR_SPEED = 2
    PREDATOR_SPEED_MAX = 6
    PERCEPTION_LENGHT_PREDATOR = 100
    ROCK_LENGHT = 10

class Herring(pygame.sprite.Sprite):

    # Keeping track of killed herring
    total_herring = 50


    def __init__(self, x_pos, y_pos):
        """Function that initializes a herring with its own image, specified position and
        random determined velocity. The velocity is a vector that also indicates the direction
        of the herring movement.
        """

        super().__init__()

        # Create the surface of the herring and add it to the display
        self.image = pygame.Surface((Config.HERRING_RADIUS * 2, Config.HERRING_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255), (Config.HERRING_RADIUS, Config.HERRING_RADIUS), Config.HERRING_RADIUS)

        # Rectangle for predator
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        # Add the position of the predator to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

        # determine dx and dy
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)

        # make sure the velocity will be in the correct direction and add randomness
        self.velocity = pygame.Vector2(dx, dy).normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

    def rules_update_velocity(self, neighbour_herring_separation, total_separation_vector, neighbour_herring_alignment, total_alignment_vector, neighbour_herring_cohesion, total_cohesion_vector):
        """ Function that calculates the total vector of the seperation, alignment
        and cohesion behavoiurs with neighbour herring and updates the velocity using
        this vector

        Parameters:
        -----------
        self: Herring
            The herring for which the vector is determined.
        neighbour_herring_separation: Int
            Number of herring within the seperation distance.
        total_separation_vector: Vector
            The tottal separation vector indicating the direction to keep a distance
            from neighbour herring.
        neighbour_herring_alignment: Int
            Number of herring within the alignment distance.
        total_alignment_vector: Vector
            The total alignment vector indicating the direction of its closest neighbours.
        neighbour_herring_cohesion: Int
            Number of herring within the cohesion distance.
        total_cohesion_vector: Vector
            The total cohesion vector indicating the position of its closest neighbours.
        """

        # check if the seperation rule needs to be used
        if neighbour_herring_separation > 0:

            # normalize the vector
            total_separation_vector = total_separation_vector  / neighbour_herring_separation

        # check if the alignment rule needs to be used
        if neighbour_herring_alignment > 0:

            # normalize the vector / determine the mean direction of the neighboor herring
            total_alignment_vector = total_alignment_vector / neighbour_herring_alignment

        # check if the cohesion rule needs to be used
        if neighbour_herring_cohesion > 0:

            # normalise the vector/ determine the mean position of the neighboor herring
            total_cohesion_vector = total_cohesion_vector / neighbour_herring_cohesion

        # calculate total_vector
        total_vector_rules = total_separation_vector + total_alignment_vector + total_cohesion_vector

        self.velocity += total_vector_rules

        # normalize velocity and multiply bt speed
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))


    def separation_herring(self, distance_two_herring, total_separation_vector, neighbour_herring_separation, other_herring_position):
        """ Function that implements the seperation rule, stating that a herring
        does not get closer to an other herring than some minimum distance. The
        closer the neighbour the stronger its influence.

        Parameters:
        -----------
        self: Herring
            The herring for which the seperation vector is determined.
        neighbour_herring_separation: Int
            Number of herring within the seperation distance.
        total_separation_vector: Vector
            The tottal separation vector indicating the direction to keep a distance
            from neighbour herring.
        other_herring_position: Vector
            The position of the neighbour herring.

        Returns:
        --------
        neighbour_herring_separation: Int
            Number of herring within the seperation distance.
        total_separation_vector: Vector
            The tottal separation vector indicating the direction to keep a distance
            from neighbour herring.

        """

        # determine if the distance lays within the seperation distance
        if distance_two_herring < Config.SEPARATION_DISTANCE:

            # determine vector that represents the direction in which the herring
            # should move to keep seperated form the other herring
            verctor_keep_seperation = (self.position - other_herring_position) / distance_two_herring

            # add vector to the total seperation vector
            total_separation_vector += verctor_keep_seperation

            # add 1 to the number of herring in the seperation distance
            neighbour_herring_separation += 1

        return total_separation_vector, neighbour_herring_separation

    def alignment_herring(self, distance_two_herring, total_alignment_vector, neighbour_herring_alignment, other_herring_velocity):
        """ Function that implements the alignment rule, stating that the herring
        heads in the direction of the neighbours within the alignment distance.

        Parameters:
        -----------
        self: Herring
            The herring for which the alignment vector is determined.
        neighbour_herring_alignment: Int
            Number of herring within the alignment distance.
        total_alignment_vector: Vector
            The total alignment vector indicating the direction of its closest neighbours.
        other_herring_position: Vector
            The position of the neighbour herring.

        Returns:
        --------
        neighbour_herring_alignment: Int
            Number of herring within the alignment distance.
        total_alignment_vector: Vector
            The total alignment vector indicating the direction of its closest neighbours.
        """

        # determine if the distance lays within the alignment distance
        if distance_two_herring < Config.ALIGNMENT_DISTANCE:

            # add direction of the neighbour to the alignment vector
            total_alignment_vector += other_herring_velocity

            # add 1 to the number of herring in the alignment distance
            neighbour_herring_alignment += 1

        return total_alignment_vector, neighbour_herring_alignment


    def cohesion_herring(self, distance_two_herring, total_cohesion_vector, neighbour_herring_cohesion, other_herring_position):
        """ Function that implements the cohesion rule, stating that the herring
        moves to the position of the neighbours within the cohesion distance. The
        closer the neighbour the stronger its influence.

        Parameters:
        -----------
        self: Herring
            The herring for which the cohesion vector is determined.
        neighbour_herring_cohesion: Int
            Number of herring within the cohesion distance.
        total_cohesion_vector: Vector
            The total cohesion vector indicating the position of its closest neighbours.
        other_herring_position: Vector
            The position of the neighbour herring.

        Returns:
        --------
        neighbour_herring_cohesion: Int
            Number of herring within the cohesion distance.
        total_cohesion_vector: Vector
            The total cohesion vector indicating the position of its closest neighbours.
        """

        # determine if the distance lays within the cohesion distance
        if distance_two_herring < Config.COHESION_DISTANCE:

            # determine vector that represents the direction in which the herring
            # should move to come closer to the other herring
            verctor_close_seperation =(other_herring_position - self.position) / distance_two_herring

            # add vector to the totalcohestion vector
            total_cohesion_vector += verctor_close_seperation

            # add 1 to the number of herring in the cohesion distance
            neighbour_herring_cohesion += 1

        return(total_cohesion_vector, neighbour_herring_cohesion)


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

        # make avoidance vector
        total_predator_avoidance_vector = pygame.Vector2(0, 0)

        # predators within the perception distance
        neighbour_predator = 0

        for predator in all_predators:

            # determine the distance to the predator
            distance_to_predator = self.position.distance_to(predator.position)

            # determine if the predetor is close ehough to sense it and avoid deviding by zero
            if distance_to_predator < Config.PERCEPTION_LENGHT_HERRING and distance_to_predator != 0:

                # make vector tha gives the direction to move away from predator
                direction_away_from_predator = (self.position - predator.position) / distance_to_predator
                total_predator_avoidance_vector += direction_away_from_predator

                neighbour_predator +=1

        # determine if there was a predator close enough that it will influence the
        # direction of the herring
        if neighbour_predator > 0:

            # normalize the vector
            total_predator_avoidance_vector = total_predator_avoidance_vector / neighbour_predator

            # multiply by two to ensure moving away from predator is more important the the
            # three swimming rules
            self.velocity += total_predator_avoidance_vector * 2.0

        # normalize velocity and add randomness
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

    def avoid_rock(self, all_rocks):
        """ Function that ensures the herring will swim around or away from a rock

        Parameters:
        -----------
        self: Herring
            The herring currently updated.
        all_rocks: pygame.sprite.Group
            Group containing all rock entities.
        """
        # make rock avoidance vector
        total_rock_avoidance_vector = pygame.Vector2(0, 0)

        # value representing the number of close by rocks
        neighbour_rock = 0

        # loop over the rocks
        for rock in all_rocks:

            # determine distance between rock and herring
            distance_to_rock = self.position.distance_to(rock.position)

            # determine if there is a rock so close that it will influence the direction
            # of the herring. also avoid deviding by zero
            if distance_to_rock < 15 and distance_to_rock != 0 :

                # make a avoidance vector and add it to total vector
                rock_avoidance_vector = (self.position - rock.position)/ distance_to_rock
                total_rock_avoidance_vector += rock_avoidance_vector

                neighbour_rock +=1

        # determine if there was a rock close enough that it will influence the
        # direction of the herring
        if neighbour_rock > 0:

            # normalize the vector
            total_rock_avoidance_vector = total_rock_avoidance_vector / neighbour_rock

            # multiply by two point five to ensure moving away from rock is extra important
            self.velocity += total_rock_avoidance_vector * 2.5

        # normalize velocity and add randomness
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

        # check if there are predators
        if all_predators:
            # determine the distance to the clostest predator
            closest_predator_distance = min(self.position.distance_to(predator.position) for predator in all_predators)

            # chance velocity if closest predtor is inside perception distance
            if closest_predator_distance < Config.PERCEPTION_LENGHT_HERRING:

                speed_h = Config.HERRING_SPEED

                # if the predator is closer the velocity is increased more and add randomness
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

        # loop over al the  herring
        for predator in all_predators:

            # determine the distance to the herring
            distance_to_herring = self.position.distance_to(predator.position)

            # if the predator is close enough kill the herring
            if distance_to_herring < Config.KILL_DISTANCE:
                all_herring.remove(self)
                Herring.killed_herring += 1
                Herring.total_herring -= 1


    def update(self, all_herring, all_predators, all_rocks):
        """Function to update the position of a herring. The new position is dependent
         on the old position, cohesion, seperation and alignment rules, the rock
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

        # check if herring gets killed
        self.kill_herring(all_herring, all_predators)

        # make vector for the three rules
        total_separation_vector = pygame.Vector2(0, 0)
        total_alignment_vector = pygame.Vector2(0, 0)
        total_cohesion_vector = pygame.Vector2(0, 0)

        # herring withing the spereation radius
        neighbour_herring_separation = 0

        # herring withing the alignment radius
        neighbour_herring_alignment = 0

        # herring withing the cohesion radius
        neighbour_herring_cohesion = 0

        # loop over all the herring to determine which are in the spereation radius,
        # alignment radius and cohesion radius
        for herring in all_herring:

            # determine the distance between two herring
            distance_two_herring = self.position.distance_to(herring.position)

            # make sure a herring is not compared to itself and avoid devision by zero
            if herring != self and distance_two_herring != 0:

                    # implement seperation rule
                    total_separation_vector, neighbour_herring_separation = self.separation_herring(distance_two_herring, total_separation_vector, neighbour_herring_separation, herring.position)

                    # implement alignment rule
                    total_alignment_vector, neighbour_herring_alignment = self. alignment_herring( distance_two_herring, total_alignment_vector, neighbour_herring_alignment, herring.velocity)

                    # implement cohension rule
                    total_cohesion_vector, neighbour_herring_cohesion = self.cohesion_herring(distance_two_herring, total_cohesion_vector, neighbour_herring_cohesion, herring.position)

        # Update velocity
        self.rules_update_velocity(neighbour_herring_separation, total_separation_vector, neighbour_herring_alignment, total_alignment_vector, neighbour_herring_cohesion, total_cohesion_vector)

        # avoid the predators
        self.avoid_predator(all_predators)

        # swim around the rock
        self.avoid_rock(all_rocks)

        # accelerate if predator is close
        self.accelerate_to_avoid_perdator(all_predators)

        # change the position
        self.position += self.velocity

        # use periodic boundaries
        self.position.x = self.position.x % Config.WIDTH
        self.position.y = self.position.y % Config.HEIGHT

        # update the center of the predator form
        self.rect.center = self.position


class Predator(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        """Function that initialize a predator with its own image, specified position and
        random determined velocity. The velocity is a vector that also indicated the direction
        of the predator movement

        Parameters:
        -----------
        self: Predator
            The predator being initialized.
        x_pos: float
            The x-coordinate of the predator position.
        y_pos: float
            The y-coordinate of the predator position.
        """
        super().__init__()

        # create the surface of the predator and add it to the display
        self.image = pygame.Surface((Config.PREDATOR_RADIUS * 2, Config.PREDATOR_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,0, 0), (Config.PREDATOR_RADIUS, Config.PREDATOR_RADIUS), Config.PREDATOR_RADIUS)

        # make the form of the predator
        self.rect = self.image.get_rect(center=( x_pos, y_pos))

        # add the position of the predator to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

        # determine dx and dy
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)

        # make sure the velocity will be in the correct direction
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
        # makecollision avoidance vector
        total_collision_avoidance_vector = pygame.Vector2(0, 0)

        # herring so close that collision should be avoided
        close_predator = 0

        # loop over all the predators
        for predator in all_predators:

            # determine distance between the predators
            distance_between_predator = self.position.distance_to(predator.position)

            # make sure the predator is not compared to itself and avoid deviding by zero
            if predator != self and distance_between_predator !=0:

                # check if the two predators are too close to each other
                if distance_between_predator < 30:

                    # make a collision avoidance vector and dd it to total vector
                    collision_avoidance_vector = (self.position - predator.position) / distance_between_predator
                    total_collision_avoidance_vector += collision_avoidance_vector

                    close_predator += 1

        # determine if there was an other predator  is close ehough that collision
        # avoidance influences the position
        if close_predator > 0:

            # normalize the vector
            total_collision_avoidance_vector = total_collision_avoidance_vector / close_predator

            # adjust the velocity
            self.velocity += total_collision_avoidance_vector

        # normalise velocity and add randomness
        self.velocity = self.velocity.normalize() * (Config.PREDATOR_SPEED + random.uniform(-0.4, 0.4))



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
        # make attack vector
        total_herring_attack_vector = pygame.Vector2(0, 0)

        # herring within the perception distance
        neighbour_herring = 0

        # loop over al the  herring
        for herring in all_herring:

            # determine the distance to the herring
            distance_to_herring = self.position.distance_to(herring.position)

            # determine if the predetor is close enough to sense it and avoid deving by zero
            if distance_to_herring < Config.PERCEPTION_LENGHT_PREDATOR and distance_to_herring != 0:

                # make vector that gives the direction to move to the herring
                direction_to_herring = ( herring.position - self.position ) / distance_to_herring
                total_herring_attack_vector += direction_to_herring

                neighbour_herring +=1

        # determine if there is a herring
        if neighbour_herring > 0:

            # normalize the vector
            total_herring_attack_vector = total_herring_attack_vector  / neighbour_herring

            # multiply by one point five to ensure moving to the herring is most important
            self.velocity +=  total_herring_attack_vector* 2

        # normalise velocity and add randomness
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

        # make rock avoidance vector
        total_rock_avoidance_vector = pygame.Vector2(0, 0)

        # value representing the number of close by rocks
        neighbour_rock = 0

        # loop over the rocks
        for rock in all_rocks:

            # determine distance between rock and predator
            distance_to_rock = self.position.distance_to(rock.position)

            # determine if there is a rock so close that it will influence the direction
            # of the predator and avoid deviding by zero
            if distance_to_rock < 20 and distance_to_rock != 0 :

                # make a avoidance vector and add it to total vector
                rock_avoidance_vector = (self.position - rock.position)/ distance_to_rock
                total_rock_avoidance_vector += rock_avoidance_vector

                neighbour_rock +=1

        # determine if there was a rock close enough that it will influence the
        # direction of the predator
        if neighbour_rock > 0:

            # normalize the vector
            total_rock_avoidance_vector = total_rock_avoidance_vector / neighbour_rock

            # multiply by two point five to ensure moving away from rock is extra important
            self.velocity += total_rock_avoidance_vector * 2.5

        # normalize velocity and add randomness
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))


    def accelerate_to_attack_herrig(self, all_herring):
        """Function that ensures the predator will accelerate when a herring is within
        its perception lenght. The closer the herring is the faster the predator
        will move.

        Parameters:
        -----------
        self: Predator
            The predator currently updated.
        all_herring: pygame.sprite.Group
            Group containing all herring entities.
        """

        # check if there are herring
        if all_herring:
            # determine the distance to the clostest herring
            closest_herring_distance = min(self.position.distance_to(herring.position) for herring in all_herring)

            # chance velocity if closest herring is inside perception distance
            if closest_herring_distance < Config.PERCEPTION_LENGHT_PREDATOR:
                speed_p = Config.PREDATOR_SPEED

                # the closer the herring is the faster the predator will move and adds# randomness
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

        # determine if predator will attack herring
        self.attack_herring(all_herring)

        # ensure the predator will swim around the rock
        self.avoid_rock(all_rocks)

        # accelerate if a herring is close
        self.accelerate_to_attack_herrig(all_herring)

        # avoid coilision of the predators
        self.collision_avoidance(all_predators)

        # change the position
        self.position += self.velocity

        # use periodic boundaries
        self.position.x = self.position.x % Config.WIDTH
        self.position.y = self.position.y % Config.HEIGHT

        # update the center of the predator form
        self.rect.center = self.position


class Rock(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        """Function that initialize a rock with its own image and specified position

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

        # create the surface of the rock and add it to the display
        self.image = pygame.Surface((Config.ROCK_LENGHT * 2, Config.ROCK_LENGHT * 2), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (125, 125, 125), (0, 0, Config.ROCK_LENGHT, Config.ROCK_LENGHT))

        # make form rock for collision
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        # add the position of the rock to a vector
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
        distance_rocks =math.sqrt((self.position[0] - other_position[0])**2 + (self.position[1] - other_position[1])**2)

        return distance_rocks


class Experiment(pygame.sprite.Sprite):
    def __init__(self, herring_nr, predator_nr, rock_nr, simulation_duration, extra_rocks = True):
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
        extra_rocks: bool
            If true areas between close rocks ar filled with more rocks.
        """
        self.herring_nr = herring_nr
        self.predator_nr = predator_nr
        self.rock_nr = rock_nr
        self.simulation_duration = simulation_duration
        self.extra_rocks = extra_rocks

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
        distance_objects = math.sqrt((position_1[0] - position_2[0])**2 + (position_1[1] - position_2[1])**2)

        return distance_objects

    def extra_rocks_experiment(self, all_rocks):
        """ Function tha adds extra rocks to the rock population to connect rocks
        that lay close to one another

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        all_rocks: pygame.sprite.Group
            Group containing all rock positions.

        enable_clusetering: bool, optional
            Whether to use the clustering of rocks. -> Default is True.

        Returns:
        ----------
        all_rocks: pygame.sprite.Group
            Updated group containing all rock entities.
        """

        #make a lsit to add the distance to
        distances = []

        # loop over all the rocks to compare them
        for rockA in all_rocks:
            for rockB in all_rocks:

                # ensure the distance to itself is not calculated
                if rockA != rockB:

                    # calculate Euclidean distances between rocks
                    distance_rock = rockB.distance_to(rockA.position)
                    distances.append(distance_rock)

                    #TOBEDONE onderzoekje distancerocks
                    # if rock lay really close make a group of rocks conection thes rocks
                    if distance_rock < 60:

                        # determine the number of extra rocks that has to be added
                        num_extra_rocks = int((60 - distance_rock) / 10) #ten is size rocks

                        # give every rock a position
                        for i in range(1, num_extra_rocks + 1):
                            ratio = i / (num_extra_rocks + 1)
                            new_x = int(rockA.position[0] + ratio * (rockB.position[0] - rockA.position[0]))
                            new_y = int(rockA.position[1] + ratio * (rockB.position[1] - rockA.position[1]))
                            distances.append((new_x, new_y))

                            # add the rock to the rock population
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

        # make the rocks group
        all_rocks = pygame.sprite.Group()

        # give all the rocks a position and add them to the group
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

        # make the herring group
        all_herring = pygame.sprite.Group()

        # give all the herring a position and add them to the group
        for _ in range(self.herring_nr):

            # give the herring a position
            pos_x = random.randint(0, Config.WIDTH)
            pos_y = random.randint(0, Config.HEIGHT)
            position_herring = [pos_x, pos_y]

            # make sure the position of a herring is not (partialy) under a rock or the
            # same as that of an other herring
            # Value is 10 because that is the lenght of a rock
            while any(self.distance_two_positions(rock.position, position_herring) < 5 for rock in all_rocks) and any(herring.position == position_herring for herring in all_herring):
                pos_x = random.randint(0, Config.WIDTH)
                pos_y = random.randint(0, Config.HEIGHT)
                position_herring = [pos_x, pos_y]

            # add herring to the herring population
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

        # make the predators group
        all_predators = pygame.sprite.Group()

        # give all the predators a position and add them to the group
        for _ in range(self.predator_nr):

            # give the predator a position
            pos_x = random.randint(0, Config.WIDTH)
            pos_y = random.randint(0, Config.HEIGHT)
            position_predator = [pos_x, pos_y]

            # make sure the position of a predator is not (partialy) under a rock or the
            # same as that of a herring or other paredator
            # Value is 10 because that is the lenght of a rock
            while any(self.distance_two_positions(rock.position, position_predator) < 10 for rock in all_rocks) and any(predator.position == position_predator for predator in all_predators) and any(herring.position == position_predator for herring in all_herring):
                pos_x = random.randint(0, Config.WIDTH)
                pos_y = random.randint(0, Config.HEIGHT)
                position_predator  = [pos_x, pos_y]

            # add predator to thepredator population
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

        # make a white background for the legend
        legend_background_rect = pygame.Rect(2, Config.HEIGHT-495, 80, 50)
        pygame.draw.rect(screen, 'white', legend_background_rect)

        # make text to write herring in blue
        herring_legend_text = font_style.render("Herring", True, 'blue')

        # make text rectangle
        herring_legend_rect = herring_legend_text.get_rect()

        # determine top left position text and add text to herring screen
        herring_legend_rect.topleft = (5, Config.HEIGHT - 490)
        screen.blit(herring_legend_text, herring_legend_rect)

        # make text to write predator in red
        predator_legend_text = font_style.render("Predator", True, 'red')

        # make text rectangle
        predator_legend_rect = predator_legend_text.get_rect()

        # determine top left position text and add predator text to screen
        predator_legend_rect.topleft = (5, Config.HEIGHT - 475)
        screen.blit(predator_legend_text, predator_legend_rect)

        # make text to write rock in gray
        rock_legend_text = font_style.render("Rock", True, 'gray')

        # make text rectangle
        rock_legend_rect = rock_legend_text.get_rect()

        # determine top left position text and add rock text to screen
        rock_legend_rect.topleft = (5, Config.HEIGHT - 460)
        screen.blit(rock_legend_text, rock_legend_rect)

        return screen

    def run(self):
        """ Function that runs an experiment

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        """

        pygame.font.init()
        pygame.init()

        # set the number of killedherring to zero
        Herring.killed_herring = 0

        # make the rocks group
        all_rocks = self.add_rocks_experiment()

        # make the herring group
        all_herring = self.add_herring_experiment(all_rocks)

        # make the predators groep
        all_predators = self.add_predator_experiment(all_rocks, all_herring)

        # variable that keeps trackon the number of killed herring
        killed_herring_count = 0

        # make a screen
        screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption(f'Simulation of herring school with {self.herring_nr} herring and {self.predator_nr} predator(s)')

        # set up font style for legend
        font_style = pygame.font.Font(None, 23)

        # add a clock
        clock = pygame.time.Clock()

        # capture the start time
        start_time = time.time()

        # set running of simulation as TRUE
        simulation_run = True

        # loop in which the simulation is runned as long as simulation running = TRUE
        while simulation_run:
            for event in pygame.event.get():

                # make sure the simulation stops if the window is closed, by setting
                # simulation run as FALSE
                if event.type == pygame.QUIT:
                    simulation_run = False


            # update the position of the herring
            all_herring.update(all_herring, all_predators, all_rocks)

            # update the position of the predators
            all_predators.update(all_herring, all_predators, all_rocks)

            # fill the screen with ligh blue color
            screen.fill((173, 216, 230))

            # draw the herring, rocks and predators on the screen
            all_herring.draw(screen)
            all_predators.draw(screen)
            all_rocks.draw(screen)

            screen =self.make_legend(font_style, screen)

            # update display
            pygame.display.flip()

            # # keep track of the number of killed herring
            # killed_herring_count = Herring.killed_herring
            # print(f"Number of killed herring: {killed_herring_count}")
            # total_herring_count = Herring.total_herring
            # print(f"Number of total herring: {total_herring_count}")

            # determine the time that has elapsed
            time_elapsed = time.time() - start_time


            # stop the simultion after the specified time
            if time_elapsed >= self.simulation_duration:
                simulation_run = False

            # set the number of frames per secod
            clock.tick(Config.FRAMES_PER_SECOND)

        # if the while loop is stoped quite the game
        pygame.quit()

        # return the number of killed herring
        return killed_herring_count


# Run the main function
if __name__ == "__main__":
    #Experiment(Nfish, Npredators, Nrocks, rockclustering)
    experiment_1 = Experiment(40, 20, 10, 20, True)
    number_killed_herring = experiment_1.run()

    # # determine the influence of the number of rock on killing of fish
    # list_mean_killed = []
    # list_std_killed = []
    # list_rock_number = []
    #
    # # simulate the simulation with different number of rocks
    # for number_rock in range(0, 101, 10):
    #     print('nr rock', number_rock)
    #     list_rock_number.append(number_rock)
    #
    #     list_killed_herring = []
    #
    #     # repeat the simulation a number of times
    #     for simulation in range(10):
    #         print('simulation', simulation)
    #         experiment = Experiment(100, 1, number_rock, 10, False)
    #         number_killed_herring = experiment.run()
    #         list_killed_herring.append(number_killed_herring)
    #
    #     # calculate the mean and the standard deviation and add it to the list
    #     mean_killed = np.mean(list_killed_herring)
    #     list_mean_killed.append(mean_killed)
    #     std_killed = np.std(list_killed_herring)
    #     list_std_killed.append(std_killed)
    #
    # # make a plot of the average number of rilled herring vs the number of rocks
    # plt.errorbar(list_rock_number, list_mean_killed, yerr=list_std_killed, fmt='o', color='orange', markerfacecolor='red', label='avarage killed herring + 1 SD')
    #
    # # make plot clear
    # plt.xlabel('Number or rocks')
    # plt.ylabel('Average killed herring')
    # plt.title('The average killed herring + 1 SD errorbars at differnt numbers of rocks')
    #
    # # add legend
    # plt.legend()
    #
    # plt.show()

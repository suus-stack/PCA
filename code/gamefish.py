
# Eerste simulatie is random laten bewegen
# implement the two basic principles of escape of and attraction

# stap 1: eerst dat de visjes binnen een bepaalde afstand van elkaar blijven
# niet meer dan

# aanpak 1: via coordinaten systeem en dan verschillende snelheid
# aanpak 2: moore neighbourhood

# data:
# geo
# percepetion length
# find realistic values for these parameters
# make a parameter not constant (maybe change over the day nightitme they see less)
# small amount of randomness into perception length (random fluctuation =)
# oval body, circle shape, connecting two ponds
# agents cannot move out agent based models support boundaries (opzoeken en onderbouwen)
# is strategy still valid in different sizes of pools


# 1. zorgen dat de vissen een bepaalde afstand tot elkaar bewaren
# 2. gedragsregels voor vissen implementeren
# ze kunnen dezelfde positie op het grid hebben (transparency hoog)

# import packages
import pygame
import sys
import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""
Authors:      Suze Frikke, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's:
Description: Agent-based moddel to simulate herring school movement dynamics when
confronted with predators.
"""

class Config:
    """ Class that stores the values of all the constants in the experiment.
    Random ness is added later in the Predator and Herring class"""

    # determine the size of the surfase investigated
    WIDTH = 500
    HEIGHT = 500

    # determine the number of frames per second
    FRAMES_PER_SECOND = 30

    # herring values
    HERRING_RADIUS = 4

    # distance in which neighbours have to be to influence the direction of a herring
    SEPARATION_DISTANCE = 10
    ALIGNMENT_DISTANCE = 50
    COHESION_DISTANCE = 50

    # normal average speed of a herring
    HERRING_SPEED = 3

    # maximal speed of a herring
    HERRING_SPEED_MAX = 6

    # lenght at which a herring can sense a predator
    PERCEPTION_LENGHT_HERRING = 40

    # distance from wich a predator can kill a fish
    KILL_DISTANCE = 5

    # predator values
    PREDATOR_RADIUS = 6

    # normal average speed predator
    PREDATOR_SPEED = 2

    # maximum speed predator
    PREDATOR_SPEED_MAX = 6

    # the lenght at wich a predator can sense a herring
    PERCEPTION_LENGHT_PREDATOR = 100

    # rock values
    ROCK_LENGHT = 10

class Herring(pygame.sprite.Sprite):

    # make variable that keeps track on the number of killed herring
    total_herring = 50


    def __init__(self, x_pos, y_pos):
        """Function that initialize a herring with its own image, specified position and
        random determined velocity. The velocity is a vector that also indicated the direction
        of the herring movement

        Parameters:
        -----------
        self: Herring
            The herring being initialized.
        x_pos: float
            The x-coordinate of the herring position
        y_pos: float
            The y-coordinate of the herring position
        """

        super().__init__()

        # create the surface of the herring and add it to the display
        self.image = pygame.Surface((Config.HERRING_RADIUS * 2, Config.HERRING_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0,0, 255), (Config.HERRING_RADIUS, Config.HERRING_RADIUS), Config.HERRING_RADIUS)

        # make a form of the predator
        self.rect = self.image.get_rect(center=( x_pos, y_pos))

        # add the position of the predator to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

        # determine dx and dy
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)

        # make sure the velocity will be in the correct direction and add randomness
        self.velocity = pygame.Vector2(dx, dy).normalize() * (Config.HERRING_SPEED + random.uniform(-0.2, 0.2))

    def rule_vector(self, neighbour_herring_separation, total_separation_vector, neighbour_herring_alignment, total_alignment_vector, neighbour_herring_cohesion, total_cohesion_vector):
        """ Function that calculates the total vector of the seperation, alignment
        and cohesion behavoiurs with neighbour herring

        Parameters:
        -----------
        self: Herring
            The herring for which the vector is determined.
        neighbour_herring_separation: # IDEA: nt
            Number of herring within the seperation distance.
        total_separation_vector: Vector
            The tottal separation vector indicating the direction to keep a distance
            from neighbour herring.
        neighbour_herring_alignment: Int
            Number of herring within the alignment distance
        total_alignment_vector: Vector
            The total alignment vector indicating the direction of its closest neighbours.
        neighbour_herring_cohesion: Int
            Number of herring within the cohesion distance
        total_cohesion_vector: Vector
            The total cohesion vector indicating the position of its closest neighbours.

        Returns:
        --------
        total_vector: Vector
            Vector that indicates the direction based on separation, alignment,
            and cohesion rules.
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
        total_vector = total_separation_vector + total_alignment_vector + total_cohesion_vector

        return total_vector

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
            The position of the neighbour herring

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

            # determine vector that represents the direction in which the herrring
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
            Number of herring within the alignment distance
        total_alignment_vector: Vector
            The total alignment vector indicating the direction of its closest neighbours.
        other_herring_position: Vector
            The position of the neighbour herring

        Returns:
        --------
        neighbour_herring_alignment: Int
            Number of herring within the alignment distance
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
            Number of herring within the cohesion distance
        total_cohesion_vector: Vector
            The total cohesion vector indicating the position of its closest neighbours.
        other_herring_position: Vector
            The position of the neighbour herring

        Returns:
        --------
        neighbour_herring_cohesion: Int
            Number of herring within the cohesion distance
        total_cohesion_vector: Vector
            The total cohesion vector indicating the position of its closest neighbours.
        """

        # determine if the distance lays within the cohesion distance
        if distance_two_herring < Config.COHESION_DISTANCE:

            # determine vector that represents the direction in which the herrring
            # should move to come closer to the other herring
            verctor_close_seperation =(other_herring_position - self.position) / distance_two_herring

            # add vector to the totalcohestion vector
            total_cohesion_vector += verctor_close_seperation

            # add 1 to the number of herring in the cohesion distance
            neighbour_herring_cohesion += 1

        return(total_cohesion_vector, neighbour_herring_cohesion)

    def collision_avoidance(self, all_herring):
        """ Function that make sure herring donnot fully collide.

        Parameters:
        -----------
        self: Herring
            The herring currently updated
        all_herring: pygame.sprite.Group
            Group containing all herring entities
        """
        # loop over all the herring
        for herring in all_herring:

            # avoid comparing the herring to itself
            if herring != self:

                # determine distance between the herring
                distance_between_herring = self.position.distance_to(herring.position)

                # check if the two herring are too close to each other
                if distance_between_herring < 10:

                    # make a collision avoidance vector
                    collision_avoidance_vector = (self.position - herring.position)/ distance_between_herring

                    # adjust the position
                    self.position += collision_avoidance_vector


    def avoid_predator(self, all_predators):
        """ Function that ensures that a herring avoids the predator if the predator
        is within the perception lenght of the herring. The closer the predator the
        more it will influence the direction of the herring

        Parameters:
        -----------
        self: Herring
            The herring currently updated
        all_predators: pygame.sprite.Group
            Group containing all predator entities
        """

        # make avoidance vector
        total_predator_avoidance_vector = pygame.Vector2(0, 0)

        # predators within the perception distance
        neighbour_predator = 0

        for predator in all_predators:
            # determine the distance to the predator
            distance_to_predator = self.position.distance_to(predator.position)


            # determine if the predetor is close ehough to sense it
            if distance_to_predator < Config.PERCEPTION_LENGHT_HERRING:

                # make vector tha gives the direction to move away from predator
                direction_away_from_predator = (self.position - predator.position) / distance_to_predator
                total_predator_avoidance_vector += direction_away_from_predator

                neighbour_predator +=1

        # determine if there was a predator close enough that it will influence the
        # direction of the herring
        if neighbour_predator > 0:

            # normalize the vector
            total_predator_avoidance_vector = total_predator_avoidance_vector / neighbour_predator

            # multiply by three to ensure moving away from predator is more important the the
            # three swimming rules
            self.velocity +=  total_predator_avoidance_vector * 2.0

        # normalize velocity and add randomness
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.2, 0.2))

    def avoid_rock(self, all_rocks):
        """ Function that ensures the herring will swim around or away from a rock

        Parameters:
        -----------
        self: Herring
            The herring currently updated
        all_rocks: pygame.sprite.Group
            Group containing all rock entities
        """

        # loop over the rocks
        for rock in all_rocks:

            # determine distance between rock and herring
            distance_to_rock = self.position.distance_to(rock.position)

            # determine if there is a rock so close that it will influence the direction
            # of the herring
            if distance_to_rock < 20:
                # make a avoidance vector
                rock_avoidance_vector = (self.position - rock.position).normalize()

                # multiply by two to give priority to avoiding the rocks
                self.velocity += rock_avoidance_vector * 2

        # normalize velocity and add randomness
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.2, 0.2))

    def accelerate_to_avoid_perdator(self, all_predators):
        """Function that ensures the herring will accelerate when a predator is within
        its perception lenght. The closer the predator is the faster the herrig will move

        Parameters:
        -----------
        self: Herring
            The herring currently updated
        all_predators: pygame.sprite.Group
            Group containing all predator entities
        """

        # check if there are predators
        if all_predators:
            # determine the distance to the clostest predator
            closest_predator_distance = min(self.position.distance_to(predator.position) for predator in all_predators)

            # chance velocity if closest predtor is inside perception distance
            if closest_predator_distance < Config.PERCEPTION_LENGHT_HERRING:
                speed_h = Config.HERRING_SPEED

                # if the predator is closer the velocity is increased more and add randomness
                self.velocity = self.velocity.normalize() * (speed_h + (Config.HERRING_SPEED_MAX -Config.HERRING_SPEED + random.uniform(-0.2, 0.2)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING))

    def kill_herring(self, all_herring, all_predators):
        """ Function that ensures the herring gets killed when within the killing
        distance of the predator

        Parameters:
        -----------
        self: Herring
            The herring currently updated
        all_predators: pygame.sprite.Group
            Group containing all predator entities
        all_herring: pygame.sprite.Group
            Group containing all herring entities
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
            The herring currently updated
        all_predators: pygame.sprite.Group
            Group containing all predator entities
        all_herring: pygame.sprite.Group
            Group containing all herring entities
        all_rocks: pygame.sprite.Group
            Group containing all rock entities
        """

        # check is herring gets killed
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

            # make sure a herring is not compared to itself
            if herring != self:

                # determine the distance between two herring
                distance_two_herring = self.position.distance_to(herring.position)

                if distance_two_herring != 0:
                    # implement seperation rule
                    total_separation_vector, neighbour_herring_separation = self.separation_herring(distance_two_herring, total_separation_vector, neighbour_herring_separation, herring.position)

                    # implement alignment rule
                    total_alignment_vector, neighbour_herring_alignment = self. alignment_herring( distance_two_herring, total_alignment_vector, neighbour_herring_alignment, herring.velocity)

                    # implement cohension rule
                    total_cohesion_vector, neighbour_herring_cohesion = self.cohesion_herring(distance_two_herring, total_cohesion_vector, neighbour_herring_cohesion, herring.position)

        # Update velocity
        total_vector_rules = self.rule_vector(neighbour_herring_separation, total_separation_vector, neighbour_herring_alignment, total_alignment_vector, neighbour_herring_cohesion, total_cohesion_vector)
        self.velocity += total_vector_rules

        # avoid the predators
        self.avoid_predator(all_predators)

        # swim around the rock
        self.avoid_rock(all_rocks)

        # accelerate if predator is close
        self.accelerate_to_avoid_perdator(all_predators)

        # avoid collision
        self.collision_avoidance(all_herring)

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
            The x-coordinate of the predator position
        y_pos: float
            The y-coordinate of the predator position
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
        self.velocity = pygame.Vector2(dx, dy).normalize() * (Config.PREDATOR_SPEED + random.uniform(-0.2, 0.2))

    def collision_avoidance(self, all_predators):
        """ Function that makes sure predators donnot fully collide

        Parameters:
        -----------
        self: Predator
            The predator currently updated
        all_predators: pygame.sprite.Group
            Group containing all predator entities
        """

        # loop over all the predators
        for predator in all_predators:

            # make sure the predator is not compared to itself
            if predator != self:

                # determine distance between the predators
                distance_between_predator = self.position.distance_to(predator.position)

                # check if the two predators are too close to each other
                if distance_between_predator < 30:
                    print('yes')

                    # make a collision avoidance vector
                    collision_avoidance_vector = (self.position - predator.position) / distance_between_herring

                    # adjuest the  position
                    self.position += collision_avoidance_vector *2


    def attack_herring(self, all_herring):
        """ Function that ensures a predator will attack a herring when the herring
        is within its perception lenght. The closer the herring the more influence
        it has on the direction of the predator

        Parameters:
        -----------
        self: Predator
            The predator currently updated
        all_herring: pygame.sprite.Group
            Group containing all herring entities
        """
        # make attack vector
        total_herring_attack_vector = pygame.Vector2(0, 0)

        # herring within the perception distance
        neighbour_herring = 0

        # loop over al the  herring
        for herring in all_herring:

            # determine the distance to the herring
            distance_to_herring = self.position.distance_to(herring.position)

            # determine if the predetor is close ehough to sense it
            if distance_to_herring < Config.PERCEPTION_LENGHT_PREDATOR:

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

        # normalise velocity
        self.velocity = self.velocity.normalize() * (Config.PREDATOR_SPEED + random.uniform(-0.2, 0.2))

    def avoid_rock(self, all_rocks):
        """ Function that ensures the predator will swim around or away from a rock

        Parameters:
        -----------
        self: Predator
            The predator currently updated
        all_rocks: pygame.sprite.Group
            Group containing all rock entities
        """

        # loop over the rocks
        for rock in all_rocks:

            # determine distance between rock and predator
            distance_to_rock = self.position.distance_to(rock.position)

            # determine if there is a rock so close that it will influence the direction
            # of the predator
            if distance_to_rock < 15:

                # make a avoidance vector
                rock_avoidance_vector = (self.position - rock.position).normalize()

                # multiply by two to give priority to avoiding the rocks
                self.velocity += rock_avoidance_vector * 1.5

        # normalize velocity
        self.velocity = self.velocity.normalize() * (Config.PREDATOR_SPEED + random.uniform(-0.2, 0.2))

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
            closest_herrring_distance = min(self.position.distance_to(herring.position) for herring in all_herring)

            # chance velocity if closest herring is inside perception distance
            if closest_herrring_distance < Config.PERCEPTION_LENGHT_PREDATOR:
                speed_p = Config.PREDATOR_SPEED

                # the closer the herring is the faster the predator will move and adds# randomness
                self.velocity = self.velocity.normalize() * (speed_p + (Config.PREDATOR_SPEED_MAX - Config.PREDATOR_SPEED + random.uniform(-0.2, 0.2)) * ((Config.PERCEPTION_LENGHT_PREDATOR-closest_herrring_distance) / Config.PERCEPTION_LENGHT_PREDATOR))

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
        return math.sqrt((self.position[0] - other_position[0])**2 + (self.position[1] - other_position[1])**2)


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
            If true areas between close rocks ar filled with more rocks
        """
        self.herring_nr = herring_nr
        self.predator_nr = predator_nr
        self.rock_nr = rock_nr
        self.simulation_duration = simulation_duration
        self.extra_rocks = extra_rocks


    def add_herring_experiment(self):
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
            herring_i = Herring(random.randint(0, Config.WIDTH), random.randint(0, Config.HEIGHT))
            all_herring.add(herring_i)

        return all_herring

    def add_predator_experiment(self):
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
            predator_i = Predator(random.randint(0, Config.WIDTH), random.randint(0, Config.HEIGHT))
            all_predators.add(predator_i)

        return all_predators

    def extra_rocks(self, all_rocks):
        """ Function tha adds extra rocks to the rock population to connect rocks
        that lay close to one another

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        """

        #make a lsit to add the distance to
        distances = []

        # loop over all the rocks to compare them
        for rockA in all_rocks:
            for rockB in all_rocks:

                # ensure the distance to itself is not calculated
                if rockA != rockB:

                    #Calculate Euclidean distances between rocks
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

        return all_rocks


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
            all_rocks = self.extra_rocks(all_rocks)

        return all_rocks

    def make_legend(self, font_style, screen):
        """Function that adds a legend to the simulation screen

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        font: Font
            The font used to style the text in the legend.
        screen: Screen
            The screen on which the legend is shown
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

        # make the herring group
        all_herring = self.add_herring_experiment()

        # make the predators groep
        all_predators = self.add_predator_experiment()

        # make the rocks group
        all_rocks = self.add_rocks_experiment()

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

            # keep track of the number of killed herring
            killed_herring_count = Herring.killed_herring
            print(f"Number of killed herring: {killed_herring_count}")
            killed_herring_count = Herring.total_herring
            print(f"Number of total herring: {killed_herring_count}")

            # determine the time that has elapsed
            time_elapsed = time.time() - start_time
            print(time_elapsed)

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
    # experiment_1 = Experiment(100, 1, 20, 10, False)
    # number_killed_herring = experiment_1.run()

    # determine the influence of the number of rock on killing of fish
    list_mean_killed = []
    list_std_killed = []
    list_rock_number = []

    # simulate the simulation with different number of rocks
    for number_rock in range(0, 101, 10):
        print('nr', number_rock)
        list_rock_number.append(number_rock)

        list_killed_herring = []

        # repeat the simulation a number of times
        for simulation in range(10):
            experiment = Experiment(100, 1, number_rock, 10, False)
            number_killed_herring = experiment.run()
            list_killed_herring.append(number_killed_herring)

        # calculate the mean and the standard deviation and add it to the list
        mean_killed = np.mean(list_killed_herring)
        list_mean_killed.append(mean_killed)
        std_killed = np.std(list_killed_herring)
        list_std_killed.append(std_killed)

    # make a plot of the average number of rilled herring vs the number of rocks
    plt.errorbar(list_rock_number, list_mean_killed, yerr=list_std_killed, fmt='o', color='orange', markerfacecolor='red', label='avarage killed herring + 1 SD')

    # make plot clear
    plt.xlabel('Number or rocks')
    plt.ylabel('Average killed herrring')
    plt.title('The average killed herring + 1 SD errorbars at differnt numbers of rocks')

    # add legend
    plt.legend()

    plt.show()

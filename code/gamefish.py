#make a parameter not constant (maybe change over the day nightitme they see less)
# small amount of randomness into perception length (random fluctuation =)
# oval body, circle shape, connecting two ponds
# agents cannot move out agent based models support boundaries (opzoeken en onderbouwen)
# is strategy still valid in different sizes of pools
"""
Authors:      Suze Frikke, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: .... , ....., 13717405
Description: Agent-based model to simulate herring school movement dynamics. The
plain movement of a herring (boid) is based on the three rules:
- Separation: Herring do not get closer than some minimum distance
- Alignment: Herring heads in the direction of the neighbours within close distance.
- Cohesion: Herring moves to the position of the neighbours within close distance.

It is possible to introduce rocks and predators in the experiment, which both
influencethe movement of a herring. The herring will always move away from the
predator and will also accelerate when a predator is near. The herring cannot move
through a rock and has to go around it or away from it. To the speed of a herring
is some value between 1 SD away from the average speed added, to create variation.

The plain movement of a predator is random unless it comes too close to another
predator then it will move away. When rocks and herring are introduced they influence
the movement of a predator. The predator will always move to the herring and will also
accelerate when a herring is near. The predator cannot move through a rock an has
to go around it or away from it. To the speed of the predators is some value between
1 SD away from the average speed added, to create variation.

In the default function first the rocks get a random position, ten the herring get a
random position that is not (partially) under a rock or the same as a position of an
other herring and lastly the predators get ar random position that is not (partially)
under a rock or the same as a position of an other predator or within perception distance.
Thepredator is placed not within the perxeption distance of herring so the ful attack
can be studied. The simulation is runned for the specified number of seconds. It is
possible to connect nearby rocks by introducing more rocks and to place the herring not
random but in one big school. The alignment distance, cohesion distance and separation
distance can also be change in order to determine their influence.
 - Experiment(nr herring, nr predator, nr rocks, duraction, connect rocks, start as
 school, alignment distance, cohesion distance, separation distance)

"""

# import needed packages
import pygame
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pandas as pd
from scipy.stats import shapiro
from scipy import stats
from itertools import combinations

class Config:
    """ Class that stores the values of all the constants in the experiment.
    Randomness is added later in the Predator and Herring class"""

    """ symulation parameters"""
    # the size of the surface investigated
    WIDTH = 600
    HEIGHT = 600

    # the number of frames per second
    FRAMES_PER_SECOND = 10

    """herring parameters"""
    # radius of the circle indicationg a herring in a simulation
    HERRING_RADIUS = 4

    # distance in which neighbours influence the direction of a herring
    SEPARATION_DISTANCE = 10
    ALIGNMENT_DISTANCE =20
    COHESION_DISTANCE = 20

    # normal average speed of a herring
    HERRING_SPEED = 3

    # maximal speed of a herring
    HERRING_SPEED_MAX = 6

    # lenght at which a herring can sense a predator
    PERCEPTION_LENGHT_HERRING = 20

    # distance from wich a predator can kill a herring
    KILL_DISTANCE = 5

    # the time a herring can swim at a high speed
    HERRING_HIGH_SPEED_TIME = 60

    """predator parameter"""
    # radius of the circle indicationg a predator in a simulation
    PREDATOR_RADIUS = 7

    # normal average speed predator
    PREDATOR_SPEED = 4

    # maximum speed predator
    PREDATOR_SPEED_MAX = 8

    # the lenght at wich a predator can sense a herring
    PERCEPTION_LENGHT_PREDATOR = 40

    # the time a predator can swim at a high speed
    PREDATOR_HIGH_SPEED_TIME = 60

    """rock parameters"""
    # lenght of the square indicationg a rock in a simulation
    ROCK_LENGHT = 10


class Herring(pygame.sprite.Sprite):

    # make variable that keeps track of the number of killed herring
    killed_herring = 0

    def __init__(self, x_pos, y_pos):
        """Function that initialize a herring with its own image, specified position
        and velocity.

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

        # create the surface of the herring and add it to the display
        self.image = pygame.Surface((Config.HERRING_RADIUS * 2, Config.HERRING_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255), (Config.HERRING_RADIUS, Config.HERRING_RADIUS), Config.HERRING_RADIUS)

        # make a form for the herring
        self.rect = self.image.get_rect(center=( x_pos, y_pos))

        # add the position of the herrring to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

        # determine dx and dy
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)

        # make sure the velocity will be with the correct speed and add variation
        self.velocity = pygame.Vector2(dx, dy).normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

        # The number of frames a high speed
        self.high_speed_frames = 0


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
        # make a vector indicating the total effct of a neighbour herrings
        total_separation_vector = pygame.Vector2(0, 0)

        # make a vector indicating the average effct of a neighbour herrings
        average_separation_vector = pygame.Vector2(0, 0)

        # herring withing the separation distance
        neighbour_herring_separation = 0

        # loop over all the herring to determine which are in the spereation distance,
        # alignment radius and cohesion radius
        for herring in all_herring:

            # determine the distance between two herring
            distance_two_herring = self.position.distance_to(herring.position)

            # make sure a herring is not compared to itself and avoid devision by zero
            if herring != self and distance_two_herring != 0:

                # determine if the distance between the herring lays within the separation distance
                if distance_two_herring < Config.SEPARATION_DISTANCE:

                    # determine vector that represents the direction in which the herring
                    # should move to keep seperated form the other herring
                    verctor_keep_separation = (self.position - herring.position)/ distance_two_herring

                    # add vector to the total separation vector
                    total_separation_vector += verctor_keep_separation

                    # add 1 to the number of herring in the separation distance
                    neighbour_herring_separation += 1

        # check if the separation rule needs to be used
        if neighbour_herring_separation > 0:

            # determine the average vector
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

        # make a vector indicating the total effct of a neighbour herrings
        total_alignment_vector = pygame.Vector2(0, 0)

        # make a vector indicating the average effct of a neighbour herrings
        average_alignment_vector = pygame.Vector2(0, 0)

        # herring withing the alignment radius
        neighbour_herring_alignment = 0

        # loop over all the herring to determine which are in the spereation radius,
        # alignment radius and cohesion radius
        for herring in all_herring:

            # determine the distance between two herring
            distance_two_herring = self.position.distance_to(herring.position)

            # make sure a herring is not compared to itself and avoid devision by zero
            if herring != self and distance_two_herring != 0:

                # determine if the distance between the herring lays within the alignment distance
                if distance_two_herring < Config.ALIGNMENT_DISTANCE:

                    # add direction of the neighbour to the alignment vector
                    """ bij de andere twee regels deel je dooor de distance om het effect van haringen die dichtbij zijn meer te laten wegen.
                    Hier ook doen???. In eerste instantie niet gedaan omdat alignment niet naar positie kijkt"""
                    # average_alignment_vector += (herring.velocity / distance_two_herring)
                    total_alignment_vector += herring.velocity

                    # add 1 to the number of herring in the alignment distance
                    neighbour_herring_alignment += 1

        # check if the alignment rule needs to be used
        if neighbour_herring_alignment > 0:

            # determine the average alignment vector
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
        # make a vector indicating the total effct of a neighbour herrings
        total_cohesion_vector = pygame.Vector2(0, 0)

        # make a vector indicating the average effct of a neighbour herrings
        average_cohesion_vector = pygame.Vector2(0, 0)

        # herring withing the cohesion radius
        neighbour_herring_cohesion = 0

        # loop over all the herring to determine which are in the spereation radius,
        # alignment radius and cohesion radius
        for herring in all_herring:

            # determine the distance between two herring
            distance_two_herring = self.position.distance_to(herring.position)

            # make sure a herring is not compared to itself and avoid devision by zero
            if herring != self and distance_two_herring != 0:

                # determine if the distance between the herring lays within the cohesion distance
                if distance_two_herring < Config.COHESION_DISTANCE:

                    # determine vector that represents the direction in which the herring
                    # should move to come closer to the other herring
                    verctor_close_separation = (herring.position - self.position) / distance_two_herring

                    # add vector to the total cohestion vector
                    total_cohesion_vector += verctor_close_separation

                    # add 1 to the number of herring in the cohesion distance
                    neighbour_herring_cohesion += 1

        # check if the cohesion rule needs to be used
        if neighbour_herring_cohesion > 0:

            # determine the average cohesion vector
            average_cohesion_vector = total_cohesion_vector / neighbour_herring_cohesion

        return(average_cohesion_vector)


    def rules_update_velocity(self, all_herring):
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

        # determine the alignment vector
        alignment_vector = self.alignment_herring(all_herring)

        # determine the cohesion vector
        cohesion_vector = self.cohesion_herring(all_herring)

        # determine the separation vector
        separation_vector = self.separation_herring(all_herring)

        # calculate total_vector
        total_vector_rules = separation_vector + alignment_vector + cohesion_vector

        # add vector to the velocity
        self.velocity += total_vector_rules

        # normalize velocity and multiply by speed to which some variation is added
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

        # make total predator avoidance vector
        total_predator_avoidance_vector = pygame.Vector2(0, 0)

        # make average predator avoidance vector
        average_predator_avoidance_vector = pygame.Vector2(0, 0)

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

            # determine the average predator avoidance vector
            average_predator_avoidance_vector = total_predator_avoidance_vector / neighbour_predator

            # multiply by two point five to ensure moving away from predator is more
            # important the the three shooling rules
            self.velocity += average_predator_avoidance_vector *2.5

        # normalize velocity and multiply by speed to which some variation is added
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
        # make total rock avoidance vector
        total_rock_avoidance_vector = pygame.Vector2(0, 0)

        # make average rock avoidance vector
        average_rock_avoidance_vector = pygame.Vector2(0, 0)

        # value representing the number of close by rocks
        neighbour_rock = 0

        # loop over the rocks
        for rock in all_rocks:

            # determine distance between rock and herring
            distance_to_rock = self.position.distance_to(rock.position)

            # determine if there is a rock so close that it will influence the direction
            # of the herring.also avoid deviding by zero
            if distance_to_rock < 12 and distance_to_rock != 0 :

                # make a avoidance vector and add it to total vector
                rock_avoidance_vector = (self.position - rock.position)/ distance_to_rock
                total_rock_avoidance_vector += rock_avoidance_vector

                neighbour_rock +=1

        # determine if there was a rock close enough that it will influence the
        # direction of the herring
        if neighbour_rock > 0:

            # determine the average rock avoidance vector
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
        speed_h = Config.HERRING_SPEED

        # check if there are predators
        if all_predators:

            # determine the distance to the clostest predator
            closest_predator_distance = min(self.position.distance_to(predator.position) for predator in all_predators)

            # chance velocity if closest predator is inside perception distance
            if closest_predator_distance < Config.PERCEPTION_LENGHT_HERRING:

                # deermine if the herring wants to swim faster than the maximum
                # speed it can have for long time
                if (speed_h + (Config.HERRING_SPEED_MAX -Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING)) < (Config.HERRING_SPEED_MAX - 1.5):

                    # deterine how long the herring is swimming fast and if it can
                    # swim fast for longer
                    if self.high_speed_frames <= Config.HERRING_HIGH_SPEED_TIME:

                        # normalize velocity and multiply by speed to which some variation is
                        # added. If the predator is closer the speed higer
                        self.velocity = self.velocity.normalize() * (speed_h + (Config.HERRING_SPEED_MAX -Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING))

                        # add one to number of frames at high speed
                        self.high_speed_frames += 1

                    else:
                        # multiply velocity with maximum speed that herring can have for long time
                        self.velocity = self.velocity.normalize() * (speed_h + ((Config.HERRING_SPEED_MAX-1.5) -Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING))

                else:
                    # normalize velocity and multiply by speed to which some variation is
                    # added. If the predator is closer the speed higer
                    self.velocity = self.velocity.normalize() * (speed_h + (Config.HERRING_SPEED_MAX -Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING))

                    # set the teller of high speed frames to zero
                    self.high_speed_frames = 0

            else:
                # set the teller of high speed frames to zero
                self.high_speed_frames = 0

    """ Dezelfde functie maar dan dat een herring voor oneindig lang heel snel kan zwemmen. In de
    functie hierboven kan de herring maar voor een bepaalde tijd (Config.HERRING_HIGH_SPEED_TIME)
    heel hard zwemmen. Voordeel van die hieronder is dat de code korter is en dus ook sneller.
    Voordeel van die hierboven is dat realistischer is. Wat is beter/handiger ???"""
    # def accelerate_to_avoid_perdator(self, all_predators):
    #     """Function that ensures the herring will accelerate when a predator is within
    #     its perception lenght. The closer the predator is the faster the herrig will move
    #
    #     Parameters:
    #     -----------
    #     self: Herring
    #         The herring currently updated.
    #     all_predators: pygame.sprite.Group
    #         Group containing all predator entities.
    #     """
    #
    #     # check if there are predators
    #     if all_predators:
    #         # determine the distance to the clostest predator
    #         closest_predator_distance = min(self.position.distance_to(predator.position) for predator in all_predators)
    #
    #         # chance velocity if closest predtor is inside perception distance
    #         if closest_predator_distance < Config.PERCEPTION_LENGHT_HERRING:
    #
    #             speed_h = Config.HERRING_SPEED
    #
    #             # normalize velocity and multiply by speed to which some variation is
    #             # added. If the predator is closer the speed higer
    #             self.velocity = self.velocity.normalize() * (speed_h + (Config.HERRING_SPEED_MAX -Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING))


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

        # determine if predator will kill herring
        self.kill_herring(all_herring, all_predators)

        # appy three boids rules
        self.rules_update_velocity(all_herring)

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

        # update the center of the herring form
        self.rect.center = self.position


class Predator(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        """Function that initialize a predator with its own image, specified position
        and velocity.

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

        # normalize velocity and multiply by speed to which some variation is added
        self.velocity = pygame.Vector2(dx, dy).normalize() * (Config.PREDATOR_SPEED + random.uniform(-0.4, 0.4))

        self.high_speed_frames = 0

    def collision_avoidance(self, all_predators):
        """ Function that makes sure predators donnot fully collide

        Parameters:
        -----------
        self: Predator
            The predator currently updated.
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        """
        # make a vector indicating the total of the collision avoidance vectors
        total_collision_avoidance_vector = pygame.Vector2(0, 0)

        # make a vector indicating the average of the collision avoidance vectors
        average_collision_avoidance_vector = pygame.Vector2(0, 0)

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

            # determine the average collision avoidance vector
            average_collision_avoidance_vector = total_collision_avoidance_vector / close_predator

            # adjust the velocity
            self.velocity += average_collision_avoidance_vector

        # normalize velocity and multiply by speed to which some variation is added
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
        # makea total attack vector
        total_herring_attack_vector = pygame.Vector2(0, 0)

        # make an average  attack vector
        average_herring_attack_vector = pygame.Vector2(0, 0)

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

            # determine the average herring attack vector
            average_herring_attack_vector = total_herring_attack_vector  / neighbour_herring

            # multiply by one point five to ensure moving to the herring is most important
            self.velocity +=  average_herring_attack_vector* 2

        # normalize velocity and multiply by speed to which some variation is added
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

        # make a total rock avoidance vector
        total_rock_avoidance_vector = pygame.Vector2(0, 0)

        # make an average rock avoidance vector
        average_rock_avoidance_vector = pygame.Vector2(0, 0)

        # value representing the number of close by rocks
        neighbour_rock = 0

        # loop over the rocks
        for rock in all_rocks:

            # determine distance between rock and predator
            distance_to_rock = self.position.distance_to(rock.position)

            # determine if there is a rock so close that it will influence the direction
            # of the predator and avoid deviding by zero
            if distance_to_rock < 15 and distance_to_rock != 0 :

                # make a avoidance vector and add it to total vector
                rock_avoidance_vector = (self.position - rock.position)/ distance_to_rock
                total_rock_avoidance_vector += rock_avoidance_vector

                neighbour_rock +=1

        # determine if there was a rock close enough that it will influence the
        # direction of the predator
        if neighbour_rock > 0:

            # normalize the vector
            average_rock_avoidance_vector = total_rock_avoidance_vector / neighbour_rock

            # multiply by two point five to ensure moving away from rock is extra important
            self.velocity += average_rock_avoidance_vector * 3

        # normalize velocity and multiply by speed to which some variation is added
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
        speed_p = Config.PREDATOR_SPEED

        # check if there are herring
        if all_herring:
            # determine the distance to the clostest herring
            closest_herring_distance = min(self.position.distance_to(herring.position) for herring in all_herring)

            # change velocity if closest herring is inside the perception distance
            if closest_herring_distance < Config.PERCEPTION_LENGHT_PREDATOR:

                # determine if the predator wants to swim faster than the maximum speed
                #it can have for long time
                if (speed_p + (Config.PREDATOR_SPEED_MAX -Config.PREDATOR_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_PREDATOR-closest_herring_distance) / Config.PERCEPTION_LENGHT_PREDATOR)) < (Config.PREDATOR_SPEED_MAX - 1.5):

                    # deterine how long the predator is swimming fast and if it can swim
                    # fast any longer
                    if self.high_speed_frames <= Config.PREDATOR_HIGH_SPEED_TIME:

                        # normalize velocity and multiply by speed to which some variation is
                        # added. If the herring is closer the speed higer
                        self.velocity = self.velocity.normalize() * (speed_p + (Config.PREDATOR_SPEED_MAX -Config.PREDATOR_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_PREDATOR-closest_herring_distance) / Config.PERCEPTION_LENGHT_PREDATOR))

                        # add one to number of frames at high speed
                        self.high_speed_frames += 1

                    else:
                        # multiply velocity with maximum speed that predator can have for long time
                        self.velocity = self.velocity.normalize() * (speed_p + ((Config.PREDATOR_SPEED_MAX-1.5)-Config.PREDATOR_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_PREDATOR-closest_herring_distance) / Config.PERCEPTION_LENGHT_PREDATOR))
                else:
                    # normalize velocity and multiply by speed to which some variation is
                    # added. If the herring is closer the speed higer
                    self.velocity = self.velocity.normalize() * (speed_p + (Config.PREDATOR_SPEED_MAX -Config.PREDATOR_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_PREDATOR-closest_herring_distance) / Config.PERCEPTION_LENGHT_PREDATOR))

                    # set the teller of high speed frames to zero
                    self.high_speed_frames = 0

            else:
                # set the teller of high speed frames to zero
                self.high_speed_frames = 0

    """ Dezelfde functie maar dan dat een predator voor oneindig lang heel snel kan zwemmen. In de
    functie hierboven kan de predator maar voor een bepaalde tijd (Config.PREDATOR_HIGH_SPEED_TIME)
    heel hard zwemmen.Voordeel van die hieronder is dat de code korter is en dus ook sneller.
    Voordeel van die hierboven is dat realistischer is. Wat is beter/handiger ???"""
    # def accelerate_to_attack_herrig(self, all_herring):
    #     """Function that ensures the predator will accelerate when a herring is within
    #     its perception lenght. The closer the herring is the faster the predator
    #     will move.
    #
    #     Parameters:
    #     -----------
    #     self: Predator
    #         The predator currently updated.
    #     all_herring: Pygame.sprite.Group
    #         Group containing all herring entities.
    #     """
    #
    #     # check if there are herring
    #     if all_herring:
    #         # determine the distance to the clostest herring
    #         closest_herring_distance = min(self.position.distance_to(herring.position) for herring in all_herring)
    #
    #         # chance velocity if closest herring is inside perception distance
    #         if closest_herring_distance < Config.PERCEPTION_LENGHT_PREDATOR:
    #             speed_p = Config.PREDATOR_SPEED
    #
    #             # the closer the herring is the faster the predator will move and adds# variation
    #             self.velocity = self.velocity.normalize() * (speed_p + (Config.PREDATOR_SPEED_MAX - Config.PREDATOR_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_PREDATOR-closest_herring_distance) / Config.PERCEPTION_LENGHT_PREDATOR))


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

        # avoid coilision of the predators
        self.collision_avoidance(all_predators)

        # accelerate if a herring is close
        self.accelerate_to_attack_herrig(all_herring)

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
        distance_rocks = np.sqrt((self.position[0] - other_position[0])**2 + (self.position[1] - other_position[1])**2)

        return distance_rocks


class Experiment(pygame.sprite.Sprite):
    def __init__(self, herring_nr = 100, predator_nr = 1, rock_nr = 10, simulation_duration = 20, extra_rocks = False, start_school = False, alignment_distance = 40, cohesion_distance = 40, separation_distance = 20):
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

        # change the rule constant to the specified value
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

        #make a lsit to add the distance to
        distances = []

        distances = []
        rock_combinations = combinations(all_rocks, 2)

        for rockA, rockB in rock_combinations:
            # Calculate Euclidean distances between rocks
            distance_rock = rockB.distance_to(rockA.position)

            # Make clusters for rocks that are too close
            if distance_rock < 60:
                
                # Determine the number of extra rocks needed to fill the gap
                num_extra_rocks = int((60 - distance_rock) / 10)

                # Fill the distance with extra rocks
                for i in range(1, num_extra_rocks + 1):
                    ratio = i / (num_extra_rocks + 1)
                    new_x = int(rockA.position[0] + ratio * (rockB.position[0] - rockA.position[0]))
                    new_y = int(rockA.position[1] + ratio * (rockB.position[1] - rockA.position[1]))
                    distances.append((new_x, new_y))

                    # Add the rock to the rock population
                    new_rock = Rock(new_x, new_y)
                    all_rocks.add(new_rock)

                # Create 'clusters' of rocks
                for n in range(num_extra_rocks):
                    random_ratio = random.uniform(0, 1)

                    # Determine new positions based on the orientation of rocks
                    if rockA.position[1] == rockB.position[1]:
                        new_x = int(rockA.position[0] + random_ratio * (rockB.position[0] - rockA.position[0]))
                        new_y = int(rockB.position[1] + random_ratio * (rockB.position[1] - rockA.position[1]))
                    else:
                        new_x = int(rockB.position[0] + random_ratio * (rockB.position[0] - rockA.position[0]))
                        new_y = int(rockA.position[1] + random_ratio * (rockB.position[1] - rockA.position[1]))

                    # Add the rock to the rock population with a specific color (RED)
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

            # determine if the herring schould start in a school
            if self.start_school == True:

                # give the herring a position
                pos_x = random.randint(0, Config.WIDTH)
                pos_y = random.randint(0, Config.HEIGHT)
                position_herring = [pos_x, pos_y]


                # make sure the position of a herring is not (partialy) under a rock, the
                # same as that of an other herring or to far drom the other herring
                # Value is 10 because that is the lenght of a rock
                while any(self.distance_two_positions(rock.position, position_herring) < 10 for rock in all_rocks) or any(herring.position == position_herring for herring in all_herring) or any(self.distance_two_positions(herring.position, position_herring) > 100 for herring in all_herring):
                    pos_x = random.randint(0, Config.WIDTH)
                    pos_y = random.randint(0, Config.HEIGHT)
                    position_herring = [pos_x, pos_y]


                # add herring to the herring population
                herring_i = Herring(pos_x, pos_y)
                all_herring.add(herring_i)

            else:
                # give the herring a position
                pos_x = random.randint(0, Config.WIDTH)
                pos_y = random.randint(0, Config.HEIGHT)
                position_herring = [pos_x, pos_y]


                # make sure the position of a herring is not (partialy) under a rock or the
                # same as that of an other herring
                # Value is 10 because that is the lenght of a rock
                while any(self.distance_two_positions(rock.position, position_herring) < 10 for rock in all_rocks) or any(herring.position == position_herring for herring in all_herring):
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

            # make sure the position of a predator is not (partialy) under a rock,
            # in perception distance of a herring or the same ast that of an other paredator
            # Value is 10 because that is the lenght of a rock
            while any(self.distance_two_positions(rock.position, position_predator) < 10 for rock in all_rocks) or any(self.distance_two_positions(herring.position, position_predator) < Config.PERCEPTION_LENGHT_PREDATOR for herring in all_herring) or any(predator.position == position_predator for predator in all_predators):
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
            # print(f"Number of killed herring: {killed_herring_count}")

            # determine the time that has elapsed
            time_elapsed = time.time() - start_time


            # stop the simultion after the specified time
            if time_elapsed >= self.simulation_duration:
                simulation_run = False

            # set the number of frames per secod
            clock.tick(Config.FRAMES_PER_SECOND)

        # if the while loop is stoped quite the game
        pygame.quit()



if __name__ == "__main__":
    experiment_1 = Experiment(40, 5, 20, 8, True)
    number_killed_herring = experiment_1.run()
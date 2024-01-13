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
plain movement of a herring is based on the three Boids rules:
- Separation rule: Herring do not get closer than some minimum distance
- Alignment rule: Herring heads in the direction of the neighbours within close distance.
- Cohesion rule: Herring moves to the position of the neighbours within close distance.

It is possible to introduce rocks and predators in the experiment, which both influence
the movement of a herring. The herring will always move away from the predator and will
also accelerate when a predator is near. The herring cannot move through a rock and has
to go around it or away from it. To the speed of the herring is some value between
1 SD away from the average added to create variation.

The plain movement of a predator is random unless it comes too close to another predator
then it will move away. When rocks and herring are introduced they influence the
movement of a predator. The predator will always move to the herring and will also
accelerate when a predator is near. The predator cannot move through a rock an has
to go around it or away from it. To the speed of the predators is some value between
1 SD away from the average added to create variation.

In the default function the herring, predators and rocks get a random position in
yhe beginnging. The simulation is runned for the specified number of seconds. It is
possible to connect nearby rocks by introducing more and to place the herring not
random but in one big school. The alignment distance, cohesion distance and seperation
distance can also be change in order to determine their influence.
 - Experiment(nr herring, nr predator, nr rocks, duraction, connect rocks, start as
 school, alignment distance, cohesion distance, seperation distance)

"""

#import packages
import pygame
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Config:
    """ Class that stores the values of all the constants in the experiment.
    Random ness is added later in the Predator and Herring class"""

    # determine the size of the surfase investigated
    WIDTH = 500
    HEIGHT = 500

    # determine the number of frames per second
    FRAMES_PER_SECOND = 30

    """herring parameters"""
    HERRING_RADIUS = 4

    # distance in which neighbours have to be to influence the direction of a herring
    SEPARATION_DISTANCE = 10
    ALIGNMENT_DISTANCE =20
    COHESION_DISTANCE = 20

    # normal average speed of a herring
    HERRING_SPEED = 3

    # maximal speed of a herring
    HERRING_SPEED_MAX = 6

    # lenght at which a herring can sense a predator
    PERCEPTION_LENGHT_HERRING = 10

    # distance from wich a predator can kill a herring
    KILL_DISTANCE = 5

    """predator parameter"""
    PREDATOR_RADIUS = 7

    # normal average speed predator
    PREDATOR_SPEED = 4

    # maximum speed predator
    PREDATOR_SPEED_MAX = 8

    # the lenght at wich a predator can sense a herring
    PERCEPTION_LENGHT_PREDATOR = 40

    """rock parameters"""
    ROCK_LENGHT = 10


class Herring(pygame.sprite.Sprite):

    # make variable that keeps track on the number of killed herring
    killed_herring = 0


    def __init__(self, x_pos, y_pos):
        """Function that initialize a herring with its own image, specified position and
        random determined velocity. The velocity is a vector that also indicated the direction
        of the herring movement

        Parameters:
        -----------
        self: Herring
            The herring being initialized.
        x_pos: float
            The x-coordinate of the herring position.
        y_pos: float
            The y-coordinate of the herring position.
        """

        super().__init__()

        # create the surface of the herring and add it to the display
        self.image = pygame.Surface((Config.HERRING_RADIUS * 2, Config.HERRING_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255, 200), (Config.HERRING_RADIUS, Config.HERRING_RADIUS), Config.HERRING_RADIUS)

        # make a form for the herring
        self.rect = self.image.get_rect(center=( x_pos, y_pos))

        # add the position of the herrring to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

        # determine dx and dy
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)

        # make sure the velocity will be in the correct direction and add variation
        self.velocity = pygame.Vector2(dx, dy).normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))


    def separation_herring(self, all_herring):
        """ Function that implements the seperation rule, stating that a herring
        does not get closer to an other herring than some minimum distance. The
        closer the neighbour the stronger its influence.

        Parameters:
        -----------
        self: Herring
            The herring for which the seperation vector is determined.
        all_herring: pygame.sprite.Group
            Group containing all herring entities.

        Returns:
        --------
        average_separation_vector: Vector
            The average separation vector indicating the direction to keep a distance
            from neighbour herring.

        """
        # make vector for the seperation rule
        average_separation_vector = pygame.Vector2(0, 0)

        # herring withing the spereation distance
        neighbour_herring_separation = 0

        # loop over all the herring to determine which are in the spereation distance,
        # alignment radius and cohesion radius
        for herring in all_herring:

            # determine the distance between two herring
            distance_two_herring = self.position.distance_to(herring.position)

            # make sure a herring is not compared to itself and avoid devision by zero
            if herring != self and distance_two_herring != 0:

                # determine if the distance lays within the seperation distance
                if distance_two_herring < Config.SEPARATION_DISTANCE:

                    # determine vector that represents the direction in which the herring
                    # should move to keep seperated form the other herring
                    verctor_keep_seperation = (self.position - herring.position)/ distance_two_herring

                    # add vector to the total seperation vector
                    average_separation_vector += verctor_keep_seperation

                    # add 1 to the number of herring in the seperation distance
                    neighbour_herring_separation += 1

        # check if the seperation rule needs to be used
        if neighbour_herring_separation > 0:

            # normalize the vector
            average_separation_vector = average_separation_vector  / neighbour_herring_separation

        return(average_separation_vector)

    def alignment_herring(self, all_herring):
        """ Function that implements the alignment rule, stating that the herring
        heads in the direction of the neighbours within the alignment distance. The
        closer the neighbour the stronger its influence.

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

        # make a vector for the alignment rule
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

                # determine if the distance lays within the alignment distance
                if distance_two_herring < Config.ALIGNMENT_DISTANCE:

                    # add direction of the neighbour to the alignment vector
                    # average_alignment_vector += (herring.velocity / distance_two_herring)
                    average_alignment_vector += herring.velocity

                    # add 1 to the number of herring in the alignment distance
                    neighbour_herring_alignment += 1

        # check if the alignment rule needs to be used
        if neighbour_herring_alignment > 0:

            # normalize the vector / determine the average velocity of the neighbours
            average_alignment_vector = average_alignment_vector / neighbour_herring_alignment

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
        # make vector for the cohesion rule
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

                # determine if the distance lays within the cohesion distance
                if distance_two_herring < Config.COHESION_DISTANCE:

                    # determine vector that represents the direction in which the herring
                    # should move to come closer to the other herring
                    verctor_close_seperation = (herring.position - self.position) / distance_two_herring

                    # add vector to the totalcohestion vector
                    average_cohesion_vector += verctor_close_seperation

                    # add 1 to the number of herring in the cohesion distance
                    neighbour_herring_cohesion += 1

        # check if the cohesion rule needs to be used
        if neighbour_herring_cohesion > 0:

            # normalize the vector/ determine the mean position of the neighboor herring
            average_cohesion_vector = average_cohesion_vector / neighbour_herring_cohesion

        return(average_cohesion_vector)


    def rules_update_velocity(self, all_herring):
        """ Function that calculates the total vector of the seperation, alignment
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

        # determine the seperation vector
        separation_vector = self.separation_herring(all_herring)

        # calculate total_vector
        total_vector_rules = separation_vector  + alignment_vector + cohesion_vector

        # add vector to the velocity
        self.velocity += total_vector_rules

        # normalize velocity and multiply by speed
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
            self.velocity += total_predator_avoidance_vector * 4

        # normalize velocity and add variation
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
            if distance_to_rock < 12 and distance_to_rock != 0 :

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
            self.velocity += total_rock_avoidance_vector * 3

        # normalize velocity and add variation
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

                # if the predator is closer the velocity is increased more and add variation
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
        pygame.draw.circle(self.image, (255,0, 0, 200), (Config.PREDATOR_RADIUS, Config.PREDATOR_RADIUS), Config.PREDATOR_RADIUS)

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

        # normalize velocity and add variation
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

        # normalize velocity and add variation
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
            if distance_to_rock < 15 and distance_to_rock != 0 :

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
            self.velocity += total_rock_avoidance_vector * 3

        # normalize velocity and add variation
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

                # the closer the herring is the faster the predator will move and adds# variation
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
        distance_rocks = np.sqrt((self.position[0] - other_position[0])**2 + (self.position[1] - other_position[1])**2)

        return distance_rocks


class Experiment(pygame.sprite.Sprite):
    def __init__(self, herring_nr = 100, predator_nr = 1, rock_nr = 10, simulation_duration = 20, extra_rocks = False, start_school = False, alignment_distance = 40, cohesion_distance = 40, seperation_distance = 20):
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
        seperation_distance: Float
            The distance that determines which neighbour herring are used for the
            seperation rule

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
        Config.SEPARATION_DISTANCE = seperation_distance


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
            # in kil distance of a herring or the same ast that of an other paredator
            # Value is 10 because that is the lenght of a rock
            while any(self.distance_two_positions(rock.position, position_predator) < 10 for rock in all_rocks) or any(self.distance_two_positions(herring.position, position_predator) < Config.KILL_DISTANCE for herring in all_herring) or any(predator.position == position_predator for predator in all_predators):
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

        # return the number of killed herring
        return killed_herring_count

def influence_predator_number(max_number_predators, number_simulations):
    """
    Function that makes a violin plot of the distribution of the killed herring for
    different number of predators in an environment with and without rocks. The
    starting number of herring is set to 100. ........

    Parameters:
    -----------
    max_number_predators: Int
        The maximum number of predators that is investigated
    number_simulations: Int
        The number of simulations per experiment kind
    """

    # make empty dataframe with three columns
    column_names = ['Nr predators', 'Killed herring', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # loop over the number of predators
    for number_predators in range(1, max_number_predators+1):
        print('Nr predators', number_predators)

        # do a number of simulation without rocks
        for simulation in range(number_simulations):
            print('Simulation without rocks', simulation)

            # set up a experiment, run it and determin the number of killed herring
            experiment = Experiment(100, number_predators, 0, 10, True)
            number_killed_herring = experiment.run()

            # make a new row with the found values and add it to the dataframe
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': number_killed_herring , 'Rocks':'no'}])
            df = pd.concat([df, new_row], ignore_index=True)

        # do a number of simulations with rocks
        for simulation in range(number_simulations):
            print('Simulation with rocks', simulation)

            # set up a experiment, run it and determin the number of killed herring
            experiment = Experiment(100, number_predators, 20, 10, True)
            number_killed_herring = experiment.run()

            # make a new row with the found values and add it to the datafram
            new_row = pd.DataFrame([{'Nr predators': number_predators, 'Killed herring': number_killed_herring , 'Rocks':'yes'}])
            df = pd.concat([df, new_row], ignore_index=True)

    # make a violin plot
    sns.violinplot(data=df, x= 'Nr predators', y= 'Killed herring', hue= 'Rocks', split=True, gap=.1, inner="quart")

    # make sure the y-axis does not go below zero because it is not possible
    # that a negative nober of herring is killed
    plt.ylim(bottom=0)

    # give the plot a title
    plt.title('Distribution of the killed herring for different number of predators in an environment with and without rocks')

    plt.show()


def influence_rocks(number_simulations):
    """
    Function that makes a plot of the average killed herring + 1 SD errorbars
    in an environment with differnt numbers of rocks. The starting number of
    herring is set to 100 and theat of the predators to 1. ........

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind
    """

    # simulate the simulation with different number of rocks
    for number_rock in range(0, 1, 5):
        print('nr rock', number_rock)
        list_rock_number.append(number_rock)

        list_killed_herring = []

        # repeat the simulation a number of times
        for simulation in range(number_simulations):
            print('simulation', simulation)
            killed_rabbits = Experiment(10, rocks_or_not, number_hunter)
            number_killed_herring = experiment.run()
            list_killed_herring.append(number_killed_herring)

        # calculate the mean and the standard deviation and add it to the list
        mean_killed = np.mean(list_killed_herring)
        list_mean_killed.append(mean_killed)
        std_killed = np.std(list_killed_herring)
        list_std_killed.append(std_killed)

    # make a plot of the average number of rilled herring vs the number of rocks
    plot = plt.errorbar(list_rock_number, list_mean_killed, yerr=list_std_killed, fmt='o', color='orange', markerfacecolor='red', label='avarage killed herring + 1 SD')

    # make plot clear
    plt.xlabel('Number or rocks')
    plt.ylabel('Average killed herring')
    plt.title('The average killed herring + 1 SD errorbars in a environment with differnt numbers of rocks')

    # make sure the y-axis does not go below zero because it is not possible t
    # hat a negative nober of herring is killed
    plt.ylim(bottom=0)

    # add legend
    plt.legend()

    plt.show()


def influence_schooling(number_simulations):
    """
    Function that makes a violinplot of the distribution of the killed herring
    for schooling and lonely herring in an environment with and without rocks.
    The starting number of herring is set to 100 and theat of the predators to
    1. ........

    Parameters:
    -----------
    number_simulations: Int
        The number of simulations per experiment kind
    """

    # make empty dataframe with three columns
    column_names = ['Schooling', 'Killed herring', 'Rocks']
    df = pd.DataFrame(columns=column_names)

    # do a number of simulation without rocks and schooling
    # for simulation in range(number_simulations):
    #     print('Simulation without rocks and scholling', simulation)
    #
    #     # set up a experiment, run it and determin the number of killed herring
    #     experiment = Experiment(100, 1, 10, 10, True, True)
    #     number_killed_herring = experiment.run()
    #
    #     # make a new row with the found values and add it to the dataframe
    #     new_row = pd.DataFrame([{'Schooling': 'no', 'Killed herring': number_killed_herring , 'Rocks':'no'}])
    #     df = pd.concat([df, new_row], ignore_index=True)

    # do a number of simulations with rocks and without schooling
    for simulation in range(number_simulations):
        print('Simulation with rocks and without schoolimg', simulation)

        # set up a experiment, run it and determin the number of killed herring
        experiment = Experiment(100, 1, 20, 30, True, False, 0, 0, 5)
        number_killed_herring = experiment.run()

        # make a new row with the found values and add it to the datafram
        new_row = pd.DataFrame([{'Schooling': 'no', 'Killed herring': number_killed_herring , 'Rocks':'yes'}])
        df = pd.concat([df, new_row], ignore_index=True)
    #
    # # do a number of simulation without rocks
    # for simulation in range(number_simulations):
    #     print('Simulation without rocks and with schooling', simulation)
    #
    #     # set up a experiment, run it and determin the number of killed herring
    #     experiment = Experiment(100, 1, 10, 10, True, True)
    #     number_killed_herring = experiment.run()
    #
    #     # make a new row with the found values and add it to the dataframe
    #     new_row = pd.DataFrame([{'Schooling': 'yes', 'Killed herring': number_killed_herring , 'Rocks':'no'}])
    #     df = pd.concat([df, new_row], ignore_index=True)

    # do a number of simulations with rocks
    for simulation in range(number_simulations):
        print('Simulation with rocks and schooling', simulation)

        # set up a experiment, run it and determin the number of killed herring
        experiment = Experiment(100, 1, 20, 30, True, False, 0, 0, 5)
        number_killed_herring = experiment.run()

        # make a new row with the found values and add it to the datafram
        new_row = pd.DataFrame([{'Schooling': 'yes', 'Killed herring': number_killed_herring , 'Rocks':'yes'}])
        df = pd.concat([df, new_row], ignore_index=True)

    # make a violin plot
    sns.violinplot(data=df, x= 'Schooling', y= 'Killed herring', hue= 'Rocks', split=True, gap=.1, inner="quart")

    # give title
    plt.title('Distribution of the killed herring for schooling and lonely herring in an environment with and without rocks')

    # make sure the y-axis does not go below zero because it is not possible t
    # hat a negative nober of herring is killed
    plt.ylim(bottom=0)

    plt.show()

# Run the main function
if __name__ == "__main__":
    """
    The parameters that have to be given:
    1: The number of herring in the simulation (int). default set to one hunderd.
    2: The number of predators in the simulation (int). Default set to one.
    3: The number of rocks in the simulation (int). default set to ten.
    4: The duration of the simulation in seconds (int). Defaut set to twenty.
    5: If clossely placed rocks should be connected via more rocks (Bool). Default
    set to False.
    6: If the herring should start as one big school instead of randomly placed
    (bool). Defaut set to False.
    7: The alignment distance (float). Default set to 40.
    8: The cohestion distance (float). Default set to 40.
    9: The seperation distance (float). Default set to 15.

    """
    # this experiment is to show how the simulation looks like
    experiment_example = Experiment(100, 2, 1, 60, True, False)
    experiment_example.run()


    # determine the influence of rocks on the predator killing rate
    influence_rocks(10)

    # determin the invluence of more predators
    influence_predator_number(6, 10)

    #determine the influence of schooling
    influence_schooling(40)

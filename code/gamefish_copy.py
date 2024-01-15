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

class Config:
    """ Class that stores the values of all the constants in the experiment."""

    WIDTH = 600
    HEIGHT = 600
    FRAMES_PER_SECOND = 10
    HERRING_SIZE = 4
    SEPARATION_DISTANCE = 10
    ALIGNMENT_DISTANCE =20
    COHESION_DISTANCE = 20

    HERRING_SPEED = 3
    HERRING_SPEED_MAX = 6
    PERCEPTION_LENGHT_HERRING = 20
    # Time a herring can swim at a full speed
    HERRING_HIGH_SPEED_TIME = 60

    KILL_DISTANCE = 5
    PREDATOR_SIZE = 7
    PREDATOR_SPEED = 4
    PREDATOR_SPEED_MAX = 8
    PERCEPTION_LENGHT_PREDATOR = 40
    # Time a predator can swim at a high speed
    PREDATOR_HIGH_SPEED_TIME = 60

    ROCK_LENGTH = 10


class Herring(pygame.sprite.Sprite):

    # Keeping track of the number of killed herring
    killed_herring = 0

    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
    
        # Creating the visualization of the herring and adding to the display
        self.image = pygame.Surface((Config.HERRING_SIZE * 2, Config.HERRING_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255), (Config.HERRING_SIZE, Config.HERRING_SIZE), Config.HERRING_SIZE)
        self.rect = self.image.get_rect(center=( self.x_pos, self.y_pos))

        # Add the position of the herrring to a vector
        self.position = pygame.Vector2(self.x_pos, self.y_pos)
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)

        # Velocity with the correct speed and added variation
        self.velocity = pygame.Vector2(dx, dy).normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

        # The number of frames at high speed
        self.high_speed_frames = 0


    def seperation_herring(self, all_herring):
        """ Function that implements the separation rule, stating that a herring
        does not get closer to an other herring than the minimum distance. The
        closer the neighbour the stronger its influence. The function returns the average 
        seperation vector, indicating what distance to keep from neighbouring herring.
        """
        
        total_separation_vector = pygame.Vector2(0, 0)
        average_separation_vector = pygame.Vector2(0, 0)
        neighbouring_herring = 0

        # Finding the herring within the seperation distance, alignment- and cohesion radius
        for herring in all_herring:
            distance = self.position.distance_to(herring.position)

            if herring != self and distance != 0:
                if distance < Config.SEPARATION_DISTANCE:
                    # Determine direction vector to keep seperated from the other herring
                    seperation_vector = (self.position - herring.position) / distance
                    # Add vector to the total separation vector
                    total_separation_vector += seperation_vector
                    neighbouring_herring += 1

        if neighbouring_herring > 0:
            average_separation_vector = total_separation_vector / neighbouring_herring

        return(average_separation_vector)

    def alignment_herring(self, all_herring):
        """ Function that implements the alignment rule, stating that the herring
        heads in the direction of its neighbours within the alignment distance.
        The function returns the average alignment vector indicating the direction
        to its closest neighbours.
        """

        # Vector indicating the total effect of neighbouring herring
        total_alignment_vector = pygame.Vector2(0, 0)
        average_alignment_vector = pygame.Vector2(0, 0)
        neighbour_herring_alignment = 0

        for herring in all_herring:
            distance = self.position.distance_to(herring.position)
            if herring != self and distance != 0:
                if distance < Config.ALIGNMENT_DISTANCE:
                    total_alignment_vector += herring.velocity
                    neighbour_herring_alignment += 1

        if neighbour_herring_alignment > 0:
            average_alignment_vector = total_alignment_vector / neighbour_herring_alignment

        return average_alignment_vector


    def cohesion_herring(self, all_herring):
        """ Function that implements the cohesion rule, stating that the herring
        moves to the position of the neighbours within the cohesion distance. The
        closer the neighbour the stronger its influence.
        """
        total_cohesion_vector = pygame.Vector2(0, 0)
        average_cohesion_vector = pygame.Vector2(0, 0)
        neighbour_herring_cohesion = 0


        for herring in all_herring:
            distance = self.position.distance_to(herring.position)
            if herring != self and distance != 0:
                if distance < Config.COHESION_DISTANCE:
                    verctor_close_separation = (herring.position - self.position) / distance
                    total_cohesion_vector += verctor_close_separation
                    neighbour_herring_cohesion += 1

        if neighbour_herring_cohesion > 0:
            average_cohesion_vector = total_cohesion_vector / neighbour_herring_cohesion

        return(average_cohesion_vector)


    def update(self, all_herring):
        """ Function that calculates the total vector of the separation, alignment
        and cohesion behaviour with neighbouring herring and updates the velocity using
        this vector.
        """

        alignment_vector = self.alignment_herring(all_herring)
        cohesion_vector = self.cohesion_herring(all_herring)
        separation_vector = self.seperation_herring(all_herring)
        total_vector_rules = separation_vector + alignment_vector + cohesion_vector
        self.velocity += total_vector_rules

        # Normalize velocity and multiply by speed to which some variation is added
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))


    def avoid_predator(self, all_predators):
        """ Function that ensures that a herring avoids the predator if the predator
        is within the perception lenght of the herring. The closer the predator, the higher its
        influence on the direction of the herring.
        """

        total_predator_avoidance_vector = pygame.Vector2(0, 0)
        average_predator_avoidance_vector = pygame.Vector2(0, 0)
        neighbour_predator = 0

        for predator in all_predators:
            distance_to_predator = self.position.distance_to(predator.position)
            if distance_to_predator < Config.PERCEPTION_LENGHT_HERRING and distance_to_predator != 0:
                direction_away_from_predator = (self.position - predator.position) / distance_to_predator
                total_predator_avoidance_vector += direction_away_from_predator
                neighbour_predator +=1

        # Check if there is a predator close enough
        if neighbour_predator > 0:
            average_predator_avoidance_vector = total_predator_avoidance_vector / neighbour_predator

            # Multiplying by two point five to ensure moving away from predator is more
            # important than the three shooling rules
            self.velocity += average_predator_avoidance_vector *2.5

        # Normalizing velocity and multiply by speed to which some variation is added
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

    def rock_avoidance(self, all_rocks):
        """ Function that ensures the herring does not swim through a rock but will
        swim around or away from a rock.
        """
        total_rock_avoidance_vector = pygame.Vector2(0, 0)
        average_rock_avoidance_vector = pygame.Vector2(0, 0)
        neighbouring_rocks = 0

        for rock in all_rocks:
            distance_to_rock = self.position.distance_to(rock.position)

            if distance_to_rock < 12 and distance_to_rock != 0 :
                rock_avoidance_vector = (self.position - rock.position)/ distance_to_rock
                total_rock_avoidance_vector += rock_avoidance_vector
                neighbouring_rocks +=1

        if neighbouring_rocks > 0:
            average_rock_avoidance_vector = total_rock_avoidance_vector / neighbouring_rocks

            # Multiply by three to ensure moving away from rock is extra important
            self.velocity += average_rock_avoidance_vector * 3

        # Normalize velocity and multiply by speed to which some variation is added
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.4, 0.4))

    def accelerate_to_avoid_perdator(self, all_predators):
        """Function that ensures the herring will accelerate when a predator is within
        its perception length. The closer the predator is the faster the herring will swim.
        """

        if all_predators:
            closest_predator_distance = min(self.position.distance_to(predator.position) for predator in all_predators)

            # Chance velocity if closest predator is inside perception distance
            if closest_predator_distance < Config.PERCEPTION_LENGHT_HERRING:

                # Determine if the herring wants to swim harder than its duration speed 
                if (Config.HERRING_SPEED + (Config.HERRING_SPEED_MAX - Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING - closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING)) < (Config.HERRING_SPEED_MAX - 1.5):

                    # Determine if the herring can swim at high speed for longer
                    if self.high_speed_frames <= Config.HERRING_HIGH_SPEED_TIME:
                        # If the predator is closer the speed higer
                        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + (Config.HERRING_SPEED_MAX -Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING))
                        self.high_speed_frames += 1
                    else:
                        # Multiplying velocity with maximum speed that herring can have for long time
                        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + ((Config.HERRING_SPEED_MAX-1.5) -Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING))
                else:
                    self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + (Config.HERRING_SPEED_MAX -Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING))
                    self.high_speed_frames = 0
            else:
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
    #             Config.HERRING_SPEED = Config.HERRING_SPEED
    #
    #             # normalize velocity and multiply by speed to which some variation is
    #             # added. If the predator is closer the speed higer
    #             self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + (Config.HERRING_SPEED_MAX -Config.HERRING_SPEED + random.uniform(-0.4, 0.4)) * ((Config.PERCEPTION_LENGHT_HERRING-closest_predator_distance) / Config.PERCEPTION_LENGHT_HERRING))


    def kill_herring(self, all_herring, all_predators):
        """ Function that ensures the herring gets killed when within the killing
        distance of the predator.
        """
  
        for predator in all_predators:
            distance_to_herring = self.position.distance_to(predator.position)
            if distance_to_herring < Config.KILL_DISTANCE:
                all_herring.remove(self)
                Herring.killed_herring += 1

    def update(self, all_herring, all_predators, all_rocks):
        """Function to update the position of a herring. The new position is dependent
         on the old position, the cohesion, separation and alignment rules, the rock
         positions and the positions of the predator(s).
        """

        self.kill_herring(all_herring, all_predators)
        # Apply three boids rules
        self.update(all_herring)
        self.avoid_predator(all_predators)
        self.rock_avoidance(all_rocks)
        self.accelerate_to_avoid_perdator(all_predators)
        self.position += self.velocity

        # Periodic boundaries
        self.position.x = self.position.x % Config.WIDTH
        self.position.y = self.position.y % Config.HEIGHT

        # Update the center of the herring form
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
        self.image = pygame.Surface((Config.PREDATOR_SIZE * 2, Config.PREDATOR_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,0, 0), (Config.PREDATOR_SIZE, Config.PREDATOR_SIZE), Config.PREDATOR_SIZE)

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

    def rock_avoidance(self, all_rocks):
        """ Function that ensures the predator will swim around or away from a rock.
        """

        # make a total rock avoidance vector
        total_rock_avoidance_vector = pygame.Vector2(0, 0)

        # make an average rock avoidance vector
        average_rock_avoidance_vector = pygame.Vector2(0, 0)

        # value representing the number of close by rocks
        neighbouring_rocks = 0

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

                neighbouring_rocks +=1

        # determine if there was a rock close enough that it will influence the
        # direction of the predator
        if neighbouring_rocks > 0:

            # normalize the vector
            average_rock_avoidance_vector = total_rock_avoidance_vector / neighbouring_rocks

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
        self.rock_avoidance(all_rocks)

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
        self.image = pygame.Surface((Config.ROCK_LENGTH * 2, Config.ROCK_LENGTH * 2), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (125, 125, 125), (0, 0, Config.ROCK_LENGTH, Config.ROCK_LENGTH))

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

        # return the number of killed herring
        return killed_herring_count


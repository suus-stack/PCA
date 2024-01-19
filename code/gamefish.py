"""
Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project Computational Science
Student ID's: 14773279 , 15159337, 13717405
Description:  Agent-based model to simulate the movement dynamics of a school of herring.
            The dynamics are also studied in the presence of rocks and predators. This enables us to keep track
            of the amount of surviving herring and which strategy of movement results in the highest surviving rate.
"""

import pygame
import random
import numpy as np
import doctest
import math
import itertools

class Config():
    """ Class that stores the values of all the parameter constants in the experiment."""

    # Experimental setting
    WIDTH = 600
    HEIGHT = 600
    FRAMES_PER_SECOND = 20

    # Parameters herring
    HERRING_SIZE = 3
    SEPARATION_DISTANCE = 5
    ALIGNMENT_DISTANCE = 20
    COHESION_DISTANCE = 20
    HERRING_SPEED = 1.24
    HERRING_SPEED_MAX = 18.44
    PERCEPTION_LENGTH_HERRING = 32
    KILL_DISTANCE = 3.6

    # Parameters predator
    PREDATOR_SIZE = 4
    PREDATOR_SPEED = 3.6
    PREDATOR_SPEED_MAX = 24.4
    PERCEPTION_LENGTH_PREDATOR = 100

    # Parameters rock
    ROCK_LENGTH = 10
    ROCK_AVOIDANCE_DIST = 15

class Herring(pygame.sprite.Sprite):

    killed_herring = 0

    def __init__(self, x_pos, y_pos):

        # Pygame 
        super().__init__()

        # Creating the visualization of the herring and adding it to the display
        self.image = pygame.Surface((Config.HERRING_SIZE * 2, Config.HERRING_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255, 140), (Config.HERRING_SIZE, Config.HERRING_SIZE), Config.HERRING_SIZE)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        # Add the position of the herring to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

        # Pick velocity and multiply it with the correct speed and add randomness
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * (Config.HERRING_SPEED + random.uniform(-0.05, 0.05))

    def boids_rules_herring(self, all_herring):
        """ Function to adapt the herring velocity to implement the flocking rules:
        - The separation rule: herring maintain a certain minimum distance with respect to its surrounding herring.
        - The alignment rule: herring will head in the same direction of the neighbours within its alignment distance.
        - The cohesion rule: herring moves to the position of the neighbours within cohesion distance.

        Parameters:
        -----------
        self: Herring
            The herring for which the separation vector is determined.
        all_herring: Pygame.sprite.Group
            Group containing all herring entities.
        """
        # Make needed vectors and counters
        separation_vector = pygame.Vector2(0, 0)
        neighbour_herring_separation = 0
        alignment_vector = pygame.Vector2(0, 0)
        neighbour_herring_alignment = 0
        cohesion_vector = pygame.Vector2(0, 0)
        neighbour_herring_cohesion = 0

        # Finding the herring within separation distance
        for herring in all_herring:
            distance_two_herring = self.position.distance_to(herring.position)

            if herring != self and distance_two_herring != 0 and distance_two_herring < Config.SEPARATION_DISTANCE:
                    # Determine separation vector and add it to the total vector
                    separation_vector += ((self.position - herring.position) / distance_two_herring)
                    neighbour_herring_separation += 1

            if herring != self and distance_two_herring != 0 and distance_two_herring < Config.ALIGNMENT_DISTANCE:
                    # Add direction of the neighbour to the total alignment vector
                    alignment_vector += herring.velocity
                    neighbour_herring_alignment += 1

            if herring != self and distance_two_herring != 0 and distance_two_herring < Config.COHESION_DISTANCE:
                    # Determine the cohesion vector and add it to the total vector
                    cohesion_vector += ((herring.position - self.position) / distance_two_herring)
                    neighbour_herring_cohesion += 1

        # Calculate average separation-, alignment-, and cohesion vector
        if neighbour_herring_separation > 0:
            separation_vector = separation_vector / neighbour_herring_separation
            self.position += separation_vector

        if neighbour_herring_alignment > 0:
            alignment_vector = alignment_vector / neighbour_herring_alignment

        if neighbour_herring_cohesion > 0:
            cohesion_vector = cohesion_vector / neighbour_herring_cohesion

        # Determine total vector of all the rules and add it to the velocity
        self.velocity += (separation_vector + alignment_vector + cohesion_vector)

        # Normalize velocity and multiply by speed to which some variation is added
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.05, 0.05))

    def avoid_predator(self, all_predators, all_herring):
        """This function adapts the velocity of a herring to avoid the predators within the
        perception length of the herring. The closer the predator the higher its impact on 
        the direction of the herring. If the herring is within killing distance, it will be killed.

        Parameters:
        -----------
        self: Herring
            The herring currently being updated.
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        all_herring: pygame.sprite.Group
            Group containing all herring entities.
        """
        predator_avoidance_vector = pygame.Vector2(0, 0)
        neighbour_predator = 0

        # Finding the predators within the perception distance
        for predator in all_predators:
            distance_to_predator = self.position.distance_to(predator.position)

            if distance_to_predator < Config.PERCEPTION_LENGTH_HERRING and distance_to_predator != 0:
                # Determine the avoidance vector and add it to total vector
                predator_avoidance_vector += (self.position - predator.position) / distance_to_predator
                neighbour_predator +=1

            # Kill herring if a predator is within the killing distance
            if distance_to_predator < Config.KILL_DISTANCE:
                all_herring.remove(self)
                Herring.killed_herring += 1

        # Calculate the average predator avoidance vector
        if neighbour_predator > 0:
            self.velocity += (predator_avoidance_vector / neighbour_predator)

        # Normalizing velocity and multiply by speed to which some randomness is added
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.05, 0.05))

    def avoid_rock(self, all_rocks)  :
        """Function to adapt the herring velocity to avoid nearby rocks.

        Parameters:
        -----------
        self: Herring
            The herring currently being updated.
        all_rocks: pygame.sprite.Group
            Group containing all rock entities.
        """

        rock_avoidance_vector = pygame.Vector2(0, 0)
        neighbour_rock = 0

        # Finding the closeby rocks
        for rock in all_rocks:
            distance_to_rock = self.position.distance_to(rock.position)

            if distance_to_rock < Config.ROCK_AVOIDANCE_DIST and distance_to_rock != 0:
                # Determine the avoidance vector and add it to total vector
                rock_avoidance_vector += (self.position - rock.position)/ distance_to_rock
                neighbour_rock +=1

        # Determine the average rock avoidance vector
        if neighbour_rock > 0:
            rock_avoidance_vector = rock_avoidance_vector / neighbour_rock

            # Multiply by five to ensure moving away from rock is prioritized 
            self.velocity += rock_avoidance_vector * 5

        # Normalize velocity and multiply by speed to which some randomness is added
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.05, 0.05))

    def accelerate_to_avoid_perdator(self, all_predators):
        """This function ensures that herring will accelerate in speed when a predator is within
        the herrings' perception length. The closer the predator is the faster the herring will swim.

        Parameters:
        -----------
        self: Herring
            The herring currently being updated.
        all_predators: pygame.sprite.Group
            Group containing all predator entities.
        """
        # Determine if the closest predator is within the perception distance
        if all_predators:
            closest_predator_distance = min(self.position.distance_to(predator.position) for predator in all_predators)

            if closest_predator_distance < Config.PERCEPTION_LENGTH_HERRING:
                # Closeness of the herring to the nearest predator within its perception range
                closeness = (Config.PERCEPTION_LENGTH_HERRING - closest_predator_distance) / Config.PERCEPTION_LENGTH_HERRING
                # Normalize velocity and multiply by the changed speed to which some variation is added.
                self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + (Config.HERRING_SPEED_MAX - Config.HERRING_SPEED + random.uniform(-0.05, 0.05)) * closeness)

    def update(self, all_herring, all_predators, all_rocks):
        """This function updates the position of a herring. The new position is dependent
         on the old position, the cohesion-, separation- and alignment rule, the rock
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
        # Appy the three boids rules
        self.boids_rules_herring(all_herring)

        # Determine influence of the environment
        self.avoid_predator(all_predators, all_herring)
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
        
        # Pygame
        super().__init__()

        # Creating the visualization of the predator and adding it to the display
        self.image = pygame.Surface((Config.PREDATOR_SIZE * 2, Config.PREDATOR_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (Config.PREDATOR_SIZE, Config.PREDATOR_SIZE), Config.PREDATOR_SIZE)
        self.rect = self.image.get_rect(center=( x_pos, y_pos))

        # Add the position of the predator to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

        # Pick velocity and multiply it with the correct speed
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * (Config.PREDATOR_SPEED + random.uniform(-0.8, 0.8))

    def collision_avoidance(self, all_predators):
        """Function to adapt the predator's velocity to avoid collision.

        Parameters:
        -----------
        self: Predator
            The predator currently updated.
        all_predators: Pygame.sprite.Group
            Group containing all predator entities.
        """
        collision_avoidance_vector = pygame.Vector2(0, 0)
        close_predator = 0

        # Finding the predators within 0.5 * the perception length
        for predator in all_predators:
            distance_between_predator = self.position.distance_to(predator.position)

            if predator != self and distance_between_predator !=0 and distance_between_predator < (Config.PERCEPTION_LENGTH_PREDATOR/ 2):

                    # Make a collision avoidance vector and add it to total vector
                    collision_avoidance_vector += (self.position - predator.position) / distance_between_predator
                    close_predator += 1

        # Calculate the average collision avoidance vector
        if close_predator > 0:
            self.velocity += (collision_avoidance_vector / close_predator)

        # Normalize velocity and multiply by speed to which some randomness is added
        self.velocity = self.velocity.normalize() * (Config.PREDATOR_SPEED + random.uniform(-0.8, 0.8))

    def attack_herring(self, all_herring):
        """Function to adapt the predator's velocity to attack the closest herring.

        Parameters:
        -----------
        self: Predator
            The predator currently updated.
        all_herring: Pygame.sprite.Group
            Group containing all herring entities.
        """
        closest_herring = None
        closest_distance = math.inf

        # Determine the closest herring within the perception length
        for herring in all_herring:
            distance_to_herring = self.position.distance_to(herring.position)

            if 0 < distance_to_herring < Config.PERCEPTION_LENGTH_PREDATOR and distance_to_herring < closest_distance:
                closest_herring = herring
                closest_distance = distance_to_herring

                # Determine the attack vector and add it to the total vector
                attack_vector = (herring.position - self.position) / distance_to_herring

        if closest_herring != None:
            self.velocity +=  attack_vector

        # Normalize velocity and multiply by speed to which some randomness is added
        self.velocity = self.velocity.normalize() * (Config.PREDATOR_SPEED + random.uniform(-0.8, 0.8))


    def avoid_rock(self, all_rocks):
        """Function to adapt the herring's velocity to avoid nearby rocks.

        Parameters:
        -----------
        self: Predator
            The predator currently updated.
        all_rocks: Pygame.sprite.Group
            Group containing all rock entities.
        """
        rock_avoidance_vector = pygame.Vector2(0, 0)
        neighbour_rock = 0

        # Finding nearby rocks
        for rock in all_rocks:
            distance_to_rock = self.position.distance_to(rock.position)

            if distance_to_rock < 15 and distance_to_rock != 0 :

                # Make an avoidance vector and add it to total vector
                rock_avoidance_vector += (self.position - rock.position)/ distance_to_rock
                neighbour_rock +=1

        # Determine the average avoidance vector
        if neighbour_rock > 0:
            rock_avoidance_vector = rock_avoidance_vector / neighbour_rock

            # Multiply by five to ensure moving away from rock is prioritized
            self.velocity += rock_avoidance_vector * 5

        # Normalize velocity and multiply by speed to which some randomness is added
        self.velocity = self.velocity.normalize() * (Config.HERRING_SPEED + random.uniform(-0.05, 0.05))

    def accelerate_to_attack_herrig(self, all_herring):
        """Function that ensures the predator will accelerate its speed when a herring is within
        the predator's perception length. The closer the herring is the faster the predator
        will swim.

        Parameters:
        -----------
        self: Predator
            The predator currently updated.
        all_herring: Pygame.sprite.Group
            Group containing all herring entities.
        """

        # Check if the closest herring is within the perception distance
        if all_herring:
            closest_herring_distance = min(self.position.distance_to(herring.position) for herring in all_herring)

            if closest_herring_distance < Config.PERCEPTION_LENGTH_PREDATOR:
                # Closeness of the predator to the nearest herring within its perception range
                closeness = (Config.PERCEPTION_LENGTH_PREDATOR - closest_herring_distance) / Config.PERCEPTION_LENGTH_PREDATOR
                # Normalize velocity and multiply by changed speed to which some variation is added
                self.velocity = self.velocity.normalize() * (Config.PREDATOR_SPEED + (Config.PREDATOR_SPEED_MAX - Config.PREDATOR_SPEED + random.uniform(-0.8, 0.8)) * closeness)

    def update(self, all_herring, all_predators, all_rocks):
        """Function to update the position of a predator. The new position is
        dependent on the the rock-, old- and herring positions.

        Parameters:
        -----------
        self: Predators
            The predator currently updated.
        all_predators: Pygame.sprite.Group
            Group containing all predator entities.
        all_herring: Pygame.sprite.Group
            Group containing all herring entities.
        all_rocks: Pygame.sprite.Group
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
       
        # Pygame
        super().__init__()

        # Creating the visualization of the rock and adding to the display
        self.image = pygame.Surface((Config.ROCK_LENGTH * 2, Config.ROCK_LENGTH * 2), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (125, 125, 125), (0, 0, Config.ROCK_LENGTH, Config.ROCK_LENGTH))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        # Add the position of the rock to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

    def rock_distance(self, other_position):
        """ Function that calculates the Eucladian distance between two rocks.

        Parameters:
        -----------
        self: Rock
            The rock being observed.
        other_position: List
            The position of the other rock.

        Returns:
        -----------
        distance_rocks: float
            The Eucladian distance between two rocks.

        Examples:
        --------
        >>> rock = Rock(0, 0)
        >>> rock.rock_distance((3, 4))
        5.0
        >>> rock = Rock(1, 2)
        >>> rock.rock_distance((1, 2))
        0.0
        """
        return np.sqrt((self.position[0] - other_position[0])**2 + (self.position[1] - other_position[1])**2)

class Experiment(pygame.sprite.Sprite):
    def __init__(self, herring_nr=100, predator_nr=1, rock_nr=10, simulation_duration=20, extra_rocks=False, start_school=False, perception_change=False, alignment_distance=20, cohesion_distance=20, separation_distance=5):
        """
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
            If true; areas between close rocks ar filled with more rocks.
        start_school: Bool
            If true; the herring are not randomly placed but in a school.
        perception_change: Bool
            If true; the perception length of predator changes over the time.
        alignment_distance: Float
            The distance that determines which neighbouring herring are used for the
            alignment rule.
        cohesion_distance: Float
            The distance that determines which neighbouring herring are used for the
            cohesion rule.
        separation_distance: Float
            The distance that determines which neighbouring herring are used for the
            separation rule.
        """
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
        """Function that calculates the Eucladian distance between two positions.

        Parameters:
        -----------
        position_1: List
            The position of onject 1
        position_2: List
            The position of onject 2

        Returns:
        -----------
        distance_objects: float
            The Eucladian distance between two objects.

        Examples:
        >>> obj = Experiment()
        >>> obj.distance_two_positions((0, 0), (3, 4))
        5.0

        >>> obj.distance_two_positions((0, 0), (0, 0))
        0.0
        """
        return np.sqrt((position_1[0] - position_2[0])**2 + (position_1[1] - position_2[1])**2)

    def add_rocks_experiment(self):
        """ Function thad adds rocks to the experiment.

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

        # add extra rocks if needed
        if self.extra_rocks == True:
            self.extra_rocks_experiment(all_rocks)

        return all_rocks
    def extra_rocks_experiment(self, all_rocks):
        """ Function that adds extra rocks to connect rocks that already lay close to one another, to form rock clusters.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.

        Returns:
        -----------
        all_rocks: Pygame.sprite.Group
            Group containing all rock entities.
        """

        distances = []

        # Generate all unique pairs of rocks
        rock_pairs = itertools.combinations(all_rocks, 2)

        for rockA, rockB in rock_pairs:
            # Calculate Euclidean distances between rocks
            distance_rock = rockB.rock_distance(rockA.position)

            # Make clusters
            if distance_rock < 60:
                num_extra_rocks = int((60 - distance_rock) / 10)

                # Finding possible rock positions and filling those positions
                for i in range(1, num_extra_rocks + 1):
                    ratio = i / (num_extra_rocks + 1)
                    new_x = rockA.position[0] + ratio * (rockB.position[0] - rockA.position[0])
                    new_y = rockA.position[1] + ratio * (rockB.position[1] - rockA.position[1])
                    distances.append((new_x, new_y))

                    # Add the rock to the rock population 
                    all_rocks.add(Rock(new_x, new_y))

                # Adding additional rocks >> introduce variability in the placement of rocks for a more natural look
                for _ in range(num_extra_rocks):
                    random_ratio = random.uniform(0, 1)
                    new_x = rockA.position[0] + random_ratio * (rockB.position[0] - rockA.position[0])
                    new_y = rockA.position[1] + random_ratio * (rockB.position[1] - rockA.position[1])

                    # Add the rock to the rock population
                    all_rocks.add(Rock(new_x, new_y))

        return all_rocks


    def add_herring_experiment(self, all_rocks):
        """ Function that adds herring to the experiment.

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
            pos_x, pos_y = random.randint(0, Config.WIDTH), random.randint(0, Config.HEIGHT)
            position_herring = [pos_x, pos_y]

            # This function checks all conditions for a position to be valid
            def invalid_position():
                return any(self.distance_two_positions(rock.position, position_herring) < 10 for rock in all_rocks) or any(herring.position == position_herring for herring in all_herring)

            # Check if herring should start in a school
            if self.start_school:
                while invalid_position() or any(self.distance_two_positions(herring.position, position_herring) > 100 for herring in all_herring):
                    pos_x, pos_y = random.randint(0, Config.WIDTH), random.randint(0, Config.HEIGHT)
                    position_herring = [pos_x, pos_y]
            else:
                while invalid_position():
                    pos_x, pos_y = random.randint(0, Config.WIDTH), random.randint(0, Config.HEIGHT)
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

            while any(self.distance_two_positions(rock.position, position_predator) < 10 for rock in all_rocks) or any(self.distance_two_positions(herring.position, position_predator) < Config.PERCEPTION_LENGTH_PREDATOR for herring in all_herring) or any(predator.position == position_predator for predator in all_predators):
                pos_x = random.randint(0, Config.WIDTH)
                pos_y = random.randint(0, Config.HEIGHT)
                position_predator  = [pos_x, pos_y]

            # Add the predator to the predator population
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
        legend_background_rect = pygame.Rect(2, Config.HEIGHT-595, 80, 50)
        pygame.draw.rect(screen, 'white', legend_background_rect)

        # Add text to write herring in blue
        herring_legend_text = font_style.render("Herring", True, 'blue')
        herring_legend_rect = herring_legend_text.get_rect()
        herring_legend_rect.topleft = (5, Config.HEIGHT - 590)
        screen.blit(herring_legend_text, herring_legend_rect)

        # Add text to write predator in red
        predator_legend_text = font_style.render("Predator", True, 'red')
        predator_legend_rect = predator_legend_text.get_rect()
        predator_legend_rect.topleft = (5, Config.HEIGHT - 575)
        screen.blit(predator_legend_text, predator_legend_rect)

        # Add text to write rock in gray
        rock_legend_text = font_style.render("Rock", True, 'gray')
        rock_legend_rect = rock_legend_text.get_rect()
        rock_legend_rect.topleft = (5, Config.HEIGHT - 560)
        screen.blit(rock_legend_text, rock_legend_rect)

        return screen

    def predator_perception_change(self, showed_frames):
        """ Function that changes the predator perception lengthbover the time.

        Parameters:
        -----------
        self: Experiment
            The experiment being simulated.
        showed_frames: Int
            The number of frames that is shown.
        perception_lenghts_predator: List
            List with the perception length of the predator on each measured
            timepoint.
        list_killed_herring: List
            List with the number of killed herring between each timepoint.

        Returns:
        -----------
        perception_lenghts_predator: List
            List with the perception length of the predator on each measured
            timepoint.
        list_killed_herring: List
            List with the number of killed herring between each timepoint.
        """
        
        killed_herring_count = []
        perception_lenghts_predator = []
        
        # Convert the number of frame to seconds and determine the elapsed time
        frame_to_seconds = showed_frames / Config.FRAMES_PER_SECOND
        elapsed_time = frame_to_seconds % 240

        # Check if the perception length of predator should decrease
        if elapsed_time < 120 and round(elapsed_time, 4) % 10 == 0:
            perception_lenghts_predator.append(Config.PERCEPTION_LENGTH_PREDATOR)
            Config.PERCEPTION_LENGTH_PREDATOR -= 2

            # Determine th number of killed herring
            killed_herring_count.append(Herring.killed_herring)
            Herring.killed_herring = 0

        # Check if the perception length of predator should increase
        if elapsed_time >= 120 and round(elapsed_time, 4) % 10 == 0:
            perception_lenghts_predator.append(Config.PERCEPTION_LENGTH_PREDATOR)
            Config.PERCEPTION_LENGTH_PREDATOR += 2

            # Determine the number of killed herring
            killed_herring_count.append(Herring.killed_herring)
            Herring.killed_herring = 0

        return(perception_lenghts_predator, killed_herring_count)

    def run(self):
        """ Function that runs an experiment."""

        pygame.font.init()
        pygame.init()

        # Set the number of killed herring and perception length to the begin value
        Herring.killed_herring = 0
        Config.PERCEPTION_LENGTH_PREDATOR = 100

        # Make the rocks, herring and predator group
        all_rocks = self.add_rocks_experiment()
        all_herring = self.add_herring_experiment(all_rocks)
        all_predators = self.add_predator_experiment(all_rocks, all_herring)

        # make a screen
        screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption(f'Simulation of herring school with {self.herring_nr} herring and {self.predator_nr} predator(s)')
        font_style = pygame.font.Font(None, 23)
        clock = pygame.time.Clock()

        # Determine the number of total frames that have to be shown
        total_frames = Config.FRAMES_PER_SECOND * self.simulation_duration
        showed_frames = 0
        simulation_run = True

        # Run the simulation as long as simulation running = True
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

            # Determine if perception length should maybe change
            if self.perception_change == True:
                perception_lenghts_predator, Herring.killed_herring = self.predator_perception_change(showed_frames)

            # Stop the simultion after the specified time
            if showed_frames >= total_frames:
                simulation_run = False

            clock.tick(Config.FRAMES_PER_SECOND)

        # If the while loop has stopped quit the game
        pygame.quit()

        # Return killed herring and if needed the perception length of the predator
        if self.perception_change == True:
            return Herring.killed_herring, perception_lenghts_predator
        else:
            return Herring.killed_herring

if __name__ == "__main__":
    """
    The parameters that have to be given:
    1: The number of herring in the simulation (int). default set to one hunderd.
    2: The number of predators in the simulation (int). Default set to one.
    3: The number of rocks in the simulation (int). default set to ten.
    4: The duration of the simulation in seconds (int). Defaut set to twenty.
    5: Closeby rocks should be connected via more rocks (Bool). Default set to False.
    6: Herring start as one school instead of randomly (bool). Default set to False.
    7: Predator perception length changes over the time (bool). Default set to False.
    8: The alignment distance (float). Default set to 40.
    9: The cohestion distance (float). Default set to 40.
    10: The separation distance (float). Default set to 15.
    """
    doctest.testmod()
    experiment_example = Experiment(150, 1, 20, 200, True, True, False, 20, 20, 5)
    killed_herring = experiment_example.run()

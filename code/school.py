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

"""
Authors:      Suze Frikke, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's:
Description: Agent-based moddel to simulate herring school movement dynamics when
confronted with predators.
"""

# import packages
import matplotlib
import matplotlib.pyplot as plt
import math
import random
import numpy as np

class Creature():

    # lists to add the positions of the rocks
    all_rock_positions = []

    def __init__(self, pos_x, pos_y, angle):
        """Function that initialize a creature with a specified position and angle.

        Parameters:
        -----------
        self: Creature
            The creature instance being initialized.
        pos_x: float
            The x-coordinate of the creature's initial position
        pos_y: float
            The y-coordinate of the creature's initial position.
        angle: float
            The initial angle of the direction of the creature
        """

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = angle

        # determine the avreage speed
        self.speed_p = 0.4
        self.speed_h = 0.4


    def distance(self, other):
        """ Function that calculates the Euclidean distance between two creatures

        Parameters:
        -----------
        self: Creature
            The creature that is currently observed
        other: Creature
            Another creature

        Returns:
        --------
        eucl_distance: float
            The Euclidean distance between two creatures.
        """

        distance = (self.pos_x - other.pos_x)**2 + (self.pos_y - other.pos_y)**2
        eucl_distance = np.sqrt(distance)
        return eucl_distance

    def is_within_radius(self, object_1, object_2, radius):
        """Function that determines if two objects are within a specified radius
         of one another.

        Parameters:
        -----------
        object_1: list
            a list representing the coordinates of object 1
        onject_2: list
            A tuple representing the coordinates of object 2
        radius: float
            The radius within to points are considerd (too) close

        Returns:
        --------
        bool
            True if object 1 is within the specified radius of object 2
        """

        object_1 = np.array(object_1)
        object_2 = np.array(object_2)
        distance = np.linalg.norm(object_1 - object_2)

        return abs(distance) <= radius

    @classmethod
    def make_list_rock_position(cls, rock_position):
        """Function that makes a list of all the rock positions

        Parameters:
        -----------
        cls: type
            The class.

        rock_position: list
            A list representing the coordinates of a rock
        """
        cls.all_rock_positions.append(rock_position)

    def find_closest_herring(self, list_position_herring):
        """ Function determines which herring is closest to the observed creature

        Parameters:
        -----------
        self: Creature
            The creature that is currently observed

        list_position_herring: list
            List with the position of all the herring

        Returns:
        --------
        closest_herring: Herring
            The herring that is closest to the observed creature
        """

        closest_herring = min(list_position_herring, key=lambda herring: np.linalg.norm(np.array([self.pos_x, self.pos_y]) - np.array(herring)))
        return closest_herring

    def find_closest_predator(self, list_position_predator):
        """ Function determines which predator is closest to the observed creature

        Parameters:
        -----------
        self: Creature
            The creature that is currently observed

        list_position_predator: list
            List with the position of all the predators

        Returns:
        --------
        closest_herring: Predator
            The predator that is closest to the observed creature
        """

        closest_predator = min(list_position_predator, key=lambda predator: np.linalg.norm(np.array([self.pos_x, self.pos_y]) - np.array(predator)))
        return closest_predator

    def make_list_positions(self, position_creature):
        """ Function that makes a list with all the creature positions

        Parameters:
        -----------
        position_creature: list
            List with all the information about the creature

        Returns:
        --------
        closest_herring: list
            List whith only the position of every creature
        """
        list_position_creature =[]

        # loop over all the creatures and add their positions to the list
        for c in position_creature:
            list_position_creature.append([c.pos_x, c.pos_y])

        return list_position_creature

    def step(self, information_predator, information_herring, other=None):
        """
        The step function updates the coordinates of a creature, ensuring the
        movement of creatures in the simulation. It ensures that creatures go
        in a different direction when they come close to a rock. The speed of
        the herring and predators will also chance when they come near eachother.

        Parameters:
        -----------
        self: Creature
            The creature currently observed

        information_predator: list
            List with the information of every predator

        information_herring: list
            List with the information of every herring

        other: Creature or None
            An potential other creature the currenly observed creature interacts with
        """

        # The location of the predator does not depend on another creature (yet)
        if other == None:

            # make list with the current positions of the herring
            list_position_herring = self.make_list_positions(information_herring)

            # determine which herring is closest to the predator
            closest_herring = self.find_closest_herring(list_position_herring)

            # if the a herring is within the perception length of the predator the speed will change
            if self.is_within_radius([self.pos_x, self.pos_y], closest_herring, self.perception_length):

                # the closer the predator is to the herring the fasterit will move
                distance_to_herring = np.linalg.norm(np.array([self.pos_x, self.pos_y]) - np.array(closest_herring))
                predator_speed = self.speed_p + ((self.perception_length/3) / abs(distance_to_herring)) + random.uniform(-0.05, 0.05)

            # ff there is no herring within the perception lenght the speed stays normal
            else:
                predator_speed = self.speed_p + random.uniform(-0.05, 0.05)


            # determine the movement in the x and y direction
            dx = math.cos(self.angle) * predator_speed
            dy = math.sin(self.angle) * predator_speed

            # determine the old positions
            old_position_x = self.pos_x
            old_position_y = self.pos_y

            # determine the possible new positions
            new_position_x = old_position_x + dx
            new_position_y = old_position_y + dy

            # while the new position is within a specific radius of a rock change the
            # angle create a new position
            while any(self.is_within_radius([new_position_x, new_position_y], position_single_rock, 4) for position_single_rock in self.all_rock_positions):

                # change angle
                self.angle = random.uniform(0,100) * math.pi

                # determine new position
                dx = math.cos(self.angle) * predator_speed
                dy = math.sin(self.angle) * predator_speed
                new_position_x = old_position_x + dy
                new_position_y = old_position_y + dy

            # change the position of the creature to the new position
            self.pos_x = new_position_x
            self.pos_y = new_position_y

        # The location of the herring depends on its closest neighbour
        else:

            # make list with the current positions of the predator
            list_position_predator = self.make_list_positions(information_predator)

            # determine which preadator is closest to the herring
            closest_predator = self.find_closest_predator(list_position_predator)

            # if the predator is within the perception length of a herring the speed will change
            if self.is_within_radius([self.pos_x, self.pos_y], closest_predator, self.perception_length):

                # the closer the herring is to the predator the faster it will move
                distance_to_predator = np.linalg.norm(np.array([self.pos_x, self.pos_y]) - np.array(closest_predator))
                herring_speed = self.speed_h + ((self.perception_length/3) / abs(distance_to_predator)) + random.uniform(-0.05, 0.05)

            # if there is no predator is within the perception lenght the speeds stays normal
            else:
                herring_speed = self.speed_h + random.uniform(-0.05, 0.05)


            # determine the movement in the x and y direction
            dx = math.cos(self.angle) * herring_speed
            dy = math.sin(self.angle) * herring_speed

            # determine the old positions
            old_position_x = self.pos_x
            old_position_y = self.pos_y

            # determine the possible new positions
            new_position_x = other.pos_x + dx
            new_position_y = other.pos_y + dy

            # while the new position is within a specific radius of a rock change the
            # angle create a new position
            while any(self.is_within_radius([new_position_x, new_position_y], position_single_rock, 4) for position_single_rock in self.all_rock_positions):

                # change angle
                self.angle = random.uniform(0,100) * math.pi

                # determine new position
                dx = math.cos(self.angle) * herring_speed
                dy = math.sin(self.angle) * herring_speed
                new_position_x = other.pos_x + dx
                new_position_y = other.pos_y + dy

            # change the position of the creature to the new position
            self.pos_x = new_position_x
            self.pos_y = new_position_y

        # ensures a periodic boundary condition (torus)
        self.pos_x %= 100
        self.pos_y %= 100

    def interact(self):
        pass

    def escape(self):
        pass

class Herring(Creature):
    def __init__(self, pos_x, pos_y, angle, perception_length):
        """Function that initialize a herring with a specified position, angle
        and perception lenght.

        Parameters:
        -----------
        self: Herring
            The herring being initialized.
        pos_x: float
            The x-coordinate of the herring's position
        pos_y: float
            The y-coordinate of the herring's position
        angle: float
            The angle of the direction of the herring
        """

        super().__init__(pos_x, pos_y, angle)
        self.perception_length = perception_length
        self.position = [pos_x, pos_y]

        # determine the marker and color to indicate the herring during the visualisation
        self.color = 'blue'
        self.marker = 'o'

    def step(self, information_predator, information_herring, other):
        """Function that ensures the herring moves

        Parameters:
        -----------
        self: Herring
            The herring currently observed

        information_predator: list
            List with the information of every predator

        information_herring: list
            List with the information of every herring

        other: Creature
            Another creature the herring potentially interacts with
        """
        super().step(information_predator, information_herring, other)

    def __repr__(self):
        """Function that gives a string representation of a herring

        Parameters:
        -----------
        self: Herring
            The herring currently observed

        Returns:
        --------
        str
            A string representation of the herring
        """

        return f'Herring: {self.pos_x}, {self.pos_y}'

class Predator(Creature):

    def __init__(self, pos_x, pos_y, angle, perception_length):
        """Function that initialize a predator with a specified position, angle
        and perception lenght.

        Parameters:
        -----------
        self: Predator
            The predator being initialized.
        pos_x: float
            The x-coordinate of the predator's position
        pos_y: float
            The y-coordinate of the predator's position
        angle: float
            The angle of the direction of the predator
        """
        super().__init__(pos_x, pos_y, angle)
        self.perception_length = perception_length
        self.position = [pos_x, pos_y]

        # determine the marker and color to indicate the predator during the visualisation
        self.color = 'red'
        self.marker = 'D'


    def step(self, information_predator, information_herring):
        """Function that ensures the predator moves

        Parameters:
        -----------
        self: Predator
            The predator currently observed

        information_predator: list
            List with the information of every predator

        information_herring: list
            List with the information of every herring

        """
        super().step(information_predator, information_herring)

    def __repr__(self):
        """Function that gives a string representation of a predator

        Parameters:
        -----------
        self: Predator
            The predator currently observed

        Returns:
        --------
        str
            A string representation of the predator
        """
        return f'Predator: {self.pos_x}, {self.pos_y}'


class Rock(Creature):
    def __init__(self, pos_x, pos_y, angle):
        """Function that initialize a rock with a specified position.

        Parameters:
        -----------
        self: Rock
            The Rock being initialized.
        pos_x: float
            The x-coordinate of the rock's position
        pos_y: float
            The y-coordinate of the rock's position
        angle: float
            The angle of the direcion of the rock. Is always zero because the rock
            does not move.
        """
        super().__init__(pos_x, pos_y, angle)
        self.position = [pos_x, pos_y]

        # determine the marker and color to indicate the rock during the visualisation
        self.color = 'gray'
        self.marker = 's'

        # ensure that in the creature class a list with the postions of the
        # rocks is made
        Creature.make_list_rock_position(self.position)

    def __repr__(self):
        """Function that gives a string representation of a rock

        Parameters:
        -----------
        self: Rock
            The rock currently observed

        Returns:
        --------
        str
            A string representation of the rock
        """
        return f'Rock: {self.pos_x}, {self.pos_y}'

class Experiment(Creature):


    def __init__(self, iterations, nr_herring, nr_predators, nr_rocks, visualize=True):
        """Initialize an experiment (simulation) with specified parameters.

        Parameters:
        -----------
        self: Experiment
            The experiment being initialized.
        iterations: int
            The number of iterations the experiment will run
        nr_herring: int
            The number of herring in the experiment
        nr_predators: int
            The number of predators in the experiment
        nr_rocks: int
            The number of rocks in the experiment
        visualize: bool
            Whether to visualize the experiment simulation. The default value is True.
        """

        self.iterations = iterations
        self.nr_herring = nr_herring
        self.nr_predators = nr_predators
        self.nr_rocks = nr_rocks

        # make list for the herrings, predators and rocks in the exoperiment
        self.herring = []
        self.predators = []
        self.rock = []
        self.visualize = True

        # add The rocks, herrings and predators to the simulation
        self.add_rock(nr_rocks)
        self.add_predators(nr_predators)
        self.add_herring(nr_herring)


        # visualize the experiment simulation if the statement is True
        if self.visualize == True:
            self.setup_plot()

    def is_within_radius(self, object_1, object_2, radius):
        """Function that determines if two objects are within a specified radius
         of one another.

        Parameters:
        -----------
        object_1: list
            a list representing the coordinates of object 1
        onject_2: list
            A tuple representing the coordinates of object 2
        radius: float
            The radius within to points are considerd (too) close

        Returns:
        --------
        bool
            True if point1 is within the specified radius of point2, False otherwise.
        """
        object_1 = np.array(object_1)
        object_2 = np.array(object_2)
        distance = np.linalg.norm(object_1 - object_2)

        return abs(distance) <= radius

    def add_rock(self, nr_rocks):
        """Function that adds rocks to the experiment. Every rock gets a unique
        position.

       Parameters:
       -----------
       self: Experiment
           The experiment currently simulated
       nr_rocks: int
           The number of rocks to add
       """
        # make a specified number of rocks
        for _ in range(self.nr_rocks):

            # choose a random position
            pos_x_r = random.uniform(0,100)
            pos_y_r = random.uniform(0,100)

            # rocks don't move so the angle is always zero
            angle_r = 0

            # if there is already a rock present on the position choose a new position
            while any([pos_x_r, pos_y_r] == rock.position for rock in self.rock):
                pos_x_r = random.uniform(0,100)
                pos_y_r = random.uniform(0,100)
                angle_r = 0

            # add make a rock and add it to the list with present rocks
            rock = Rock(pos_x_r, pos_y_r, angle_r)
            self.rock.append(rock)


    def add_herring(self, nr_herring):
        """Function that adds herring to the experiment. Every herring gets a unique
        position that is add a specidied radius of the rocks.

       Parameters:
       -----------
       self: Experiment
           The experiment currently simulated
       nr_herring: int
           The number of herring to add
       """

        # make a specified number of herrings
        for _ in range(self.nr_herring):

            # determine the perception lenght (average + sd)
            perception_lenghth_h = 10 + random.uniform(-1, 1)

            # choose a random position and angle
            pos_x_h = random.uniform(0,100)
            pos_y_h = random.uniform(0,100)
            angle_h = random.uniform(0,100) * math.pi

            # if the position is too close to a rock or a predator choose a new position.
            while any(self.is_within_radius([pos_x_h, pos_y_h], rock.position, 2) for rock in self.rock)and any(self.is_within_radius([pos_x_h, pos_y_h], predator.position, 5) for predator in self.predators):
                pos_x_h = random.uniform(0,100)
                pos_y_h = random.uniform(0,100)
                angle_h = random.uniform(0,100) * math.pi

            # add make a herring and add it to the list with present herrings
            herring = Herring(pos_x_h, pos_y_h, angle_h, perception_length=perception_lenghth_h)
            self.herring.append(herring)

    def add_predators(self, nr_predators):
        """Function that adds predators to the experiment. Every predator gets a
        unique position that is add a specified radius of the rocks and the herring.

       Parameters:
       -----------
       self: Experiment
           The experiment currently simulated
       nr_predators: int
           The number of predators to add
       """

        # make a specified number of predators
        for _ in range(self.nr_predators):

            # determine the perception lenght (average + sd)
            perception_lenghth_p = 10 + random.uniform(-1, 1)

            # choose a random position and angle
            pos_x_p = random.uniform(0,100)
            pos_y_p = random.uniform(0,100)
            angle_p = random.uniform(0,100) * math.pi

            # if the position is too close to a rock choose a new position.
            while any(self.is_within_radius([pos_x_p, pos_y_p], rock.position, 2) for rock in self.rock):
                pos_x_p = random.uniform(0,100)
                pos_y_p = random.uniform(0,100)
                angle_p = random.uniform(0,100) * math.pi

             # add make a herring and add it to the list with present herrings
            predator = Predator(pos_x_p, pos_y_p, angle_p, perception_length=perception_lenghth_p)
            self.predators.append(predator)


    def step(self):
        """Advance the simulation by one time step. It ensures the herring and
        predators will move. The direction can be based on the interaction with
        other animals or rocks.

       Parameters:
       -----------
       self: Experiment
           The experiment currently simulated

       """
        # collect the information over the herrings and predators that are present
        information_herring = self.herring
        information_predator = self.predators

        # move every herring based on the position of other herring
        for herring1 in self.herring:

            # set the minimum distance to infinity
            min_distance = math.inf

            # loop over all the herrings
            for herring2 in self.herring:

                # ensure the herring is not compared with itselfe
                if herring1 != herring2:

                    # determine the distance between the two herrings
                    distance = herring1.distance(herring2)

                    # Finding the closest herring
                    if distance < min_distance:
                        min_distance = distance
                        closest_neighbour = herring2

            # the herring moves in the direction of the closest herring
            herring1.step(information_predator, information_herring, closest_neighbour)

        # move the every predator
        for predator in self.predators:
            predator.step(information_predator, information_herring)

    def draw(self):
        """
        This function creates the axes along which the creatures move and with
        that the simulation frame, the creatures are plotted making use of
        a scatterplot.

        Parameters:
        -----------
        self: Experiment
            The experiment currently simulated
        """

        # plot range is from 0 to 100 for both x and y axis
        self.ax1.axis([0, 100, 0, 100])

        # add a background color
        self.ax1.set_facecolor((0.7, 0.8, 1.0))

        # make list for the x and y cordinates of the herring, predators and rocks
        coordinates_x_h = []
        coordinates_y_h = []
        coordinates_x_p = []
        coordinates_y_p = []
        coordinates_x_r = []
        coordinates_y_r = []

        # loop over all the herring
        for herring in self.herring:
            # add the x and y coordinates of the herring to the lists
            coordinates_x_h.append(herring.pos_x)
            coordinates_y_h.append(herring.pos_y)

            # determine the color and marker used for the herring visualisation
            marker_herring = herring.marker
            color_herring = herring.color

        # loop over all the predators
        for predator in self.predators:
            # add the x and y coordinates of the predators to the lists
            coordinates_x_p.append(predator.pos_x)
            coordinates_y_p.append(predator.pos_y)

            # determine the color and marker used for the predator visualisation
            marker_predator = predator.marker
            color_predator = predator.color

        # loop over all the rocks
        for rock in self.rock:
            # add the x and y coordinates of the rocks to the lists
            coordinates_x_r.append(rock.pos_x)
            coordinates_y_r.append(rock.pos_y)

            # determine the color and marker used for the predator visualisation
            marker_rocks = rock.marker
            color_rocks = rock.color


        # Achteraf nog aparte creature lijsten maken zodat je aparte markers en groottes kan kiezen

        # add the herring, predators and rocks to the plot
        self.ax1.scatter(coordinates_x_h, coordinates_y_h, c=color_herring, alpha=0.5, marker=marker_herring, s=10)
        self.ax1.scatter(coordinates_x_p, coordinates_y_p, c=color_predator, alpha=0.5, marker=marker_predator, s=150)
        self.ax1.scatter(coordinates_x_r, coordinates_y_r, c=color_rocks, alpha=0.5, marker=marker_rocks, s=50)

        # add a title
        plt.title(f'Simulation of herring school with {self.nr_herring} herring and {self.nr_predators} predator(s)')

        # draw the current siuation
        plt.draw()
        plt.pause(0.01)
        self.ax1.cla()

    def run(self):
        """
        Function that runs the simulation.

        Parameters:
        -----------
        self: Experiment
            The experiment simulation that is runnend.
        """

        # loop over the number of time steps
        for i in range(self.iterations):
            # move one step in time
            self.step()

            # visualise the situation
            if self.visualize == True:
                self.draw()

    def setup_plot(self):
        """Function that makes a plot in which the experiment is simulated

        Parameters:
        -----------
        self: Experiment
            The experiment that will be simulated in the plot
        """
        self.fig, self.ax1 = plt.subplots(1)
        self.ax1.set_aspect('equal')
        self.ax1.axes.get_xaxis().set_visible(False)
        self.ax1.axes.get_yaxis().set_visible(False)

if __name__ == "__main__":

    # make an experiment and run it
    my_experiment = Experiment(200, 20, 1, 10)
    my_experiment.run()

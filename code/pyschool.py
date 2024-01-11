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


import pygame
import sys
import random
import math
import time

# make a pygame
pygame.init()

# determine the size of the game
WIDTH, HEIGHT = 500, 500

# determine the number of frames per second
FRAMES_PER_SECOND = 30

# herring values
HERRING_SPEED = 2
HERRING_SPEED_MAX = 4
HERRING_SIZE = 5
HERRING_RADIUS = 5
SEPARATION_DISTANCE = 30
ALIGNMENT_DISTANCE = 80
COHESION_DISTANCE = 80
PERCEPTION_LENGHT_HERRING = 40

# predator values
PREDATOR_RADIUS = 8
PREDATOR_SPEED = 2
PREDATOR_SPEED_MAX = 4
PERCEPTION_LENGHT_PREDATOR = 100

# rock values
ROCK_LENGHT = 10


# Classes
class Herring(pygame.sprite.Sprite):


    def __init__(self, x_pos, y_pos):
        super().__init__()

        # create the surface of the herring and add it to the display
        self.image = pygame.Surface((HERRING_RADIUS * 2, HERRING_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0,0, 255), (HERRING_RADIUS, HERRING_RADIUS), HERRING_RADIUS)

        # make a form of the predator
        self.rect = self.image.get_rect(center=( x_pos, y_pos))

        # add the position of the predator to a vector
        self.position = pygame.Vector2(x_pos, y_pos)


        # determine dx and dy
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)

        # make sure the speed will be in the correct direction
        self.speed = pygame.Vector2(dx, dy).normalize() * HERRING_SPEED

    def rule_vector(self, neighbour_herring_separation, total_separation_vector, neighbour_herring_alignment, total_alignment_vector, neighbour_herring_cohesion, total_cohesion_vector):
        """ Function that calculates the total vector of the seperation, alignment
        and cohesion rule """

        # check if the seperation rule needs to be used
        if neighbour_herring_separation > 0:

            # normalize the vector
            total_separation_vector = total_separation_vector  / neighbour_herring_separation

        # check if the alignment rule needs to be used
        if neighbour_herring_alignment > 0:

            # normalize the vector
            total_alignment_vector = total_alignment_vector / neighbour_herring_alignment

        # check if the cohesion rule needs to be used
        if neighbour_herring_cohesion > 0:

            # normalise the vector
            total_cohesion_vector = total_cohesion_vector / neighbour_herring_cohesion

        # calculate total_vector
        total_vector = total_separation_vector + total_alignment_vector + total_cohesion_vector

        return total_vector

    def separation_herring(self, distance_two_herring, total_separation_vector, neighbour_herring_separation, other_herring_position, self_position):
        """ Function that implements the seperation rule """

        # determine if the distance lays within the seperation distance
        if distance_two_herring < SEPARATION_DISTANCE:

            # determine vector that represents the direction in which the herrring
            # should move to keep seperated form the other herring
            verctor_keep_seperation = (self_position - other_herring_position) / distance_two_herring

            # add vector to the total seperation vector
            total_separation_vector += verctor_keep_seperation

            # add 1 to the number of herrings in the seperation distance
            neighbour_herring_separation += 1

        return total_separation_vector, neighbour_herring_separation

    def alignment_herring(self, distance_two_herring, total_alignment_vector, neighbour_herring_alignment, other_herring_speed):
        """ Function that implements the alignment rule """

        # determine if the distance lays within the alignment distance
        if distance_two_herring < ALIGNMENT_DISTANCE:

            # add direction of the neighbour to the alignment vector
            total_alignment_vector += other_herring_speed

            # add 1 to the number of herrings in the alignment distance
            neighbour_herring_alignment += 1

        return total_alignment_vector, neighbour_herring_alignment

    def cohesion_herring(self, distance_two_herring, total_cohesion_vector, neighbour_herring_cohesion, other_herring_position, self_position):
        """ Function that implements the cohesion rule """

        # determine if the distance lays within the cohesion distance
        if distance_two_herring < COHESION_DISTANCE:

            # determine vector that represents the direction in which the herrring
            # should move to come closer to the other herring
            verctor_close_seperation =(other_herring_position - self_position) / distance_two_herring

            # add vector to the totalcohestion vector
            total_cohesion_vector += verctor_close_seperation

            # add 1 to the number of herrings in the cohesion distance
            neighbour_herring_cohesion += 1

        return(total_cohesion_vector, neighbour_herring_cohesion)

    def avoid_predator(self, all_predators):
        """ Function that ensures that a herring avoids the predator"""

        # make avoidance vector
        total_predator_avoidance_vector = pygame.Vector2(0, 0)

        # predators within the perception distance
        neighbour_predator = 0

        for predator in all_predators:
            # determine the distance to the predator
            distance_to_predator = self.position.distance_to(predator.position)


            # determine if the predetor is close ehough to sense it
            if distance_to_predator < PERCEPTION_LENGHT_HERRING:

                # make vector tha gives the direction to move away from predator
                direction_away_from_predator = (self.position - predator.position) / distance_to_predator
                total_predator_avoidance_vector += direction_away_from_predator

                neighbour_predator +=1

        # determine if there was a predator close enough that it will influence the
        # direction of the herring
        if neighbour_predator > 0:

            # normalize the vector
            total_predator_avoidance_vector = total_predator_avoidance_vector  / neighbour_predator

            # multiply by three to ensure moving away from predator is more important the the
            # three swimming rules
            self.speed +=  total_predator_avoidance_vector * 3.0

        # normalize speed
        self.speed = self.speed.normalize() * HERRING_SPEED

    def avoid_rock(self, all_rocks):
        """ Function that ensures the herring will swim around a rock """

        # loop over the rocks
        for rock in all_rocks:

            # determine distance between rock and herring
            distance_to_rock = self.position.distance_to(rock.position)

            # determine if there is a rock so close that it will influence the direction
            # of the herring
            if distance_to_rock < 30:
                # make a avoidance vector
                rock_avoidance_vector = (self.position - rock.position).normalize()
                self.speed += rock_avoidance_vector

                # adjsut the position to move from the rock
                self.position += rock_avoidance_vector

        # normalize speed
        self.speed = self.speed.normalize() * HERRING_SPEED

    def accelerate_to_avoid_perdator(self, all_predators):
        """Function that ensures the herring will accelerate when a predator is within
        its perception lenght. The closer the predator is the faster the herrig will move"""

        # check if there are predators
        if all_predators:
            # determine the distance to the clostest predator
            closest_predator_distance = min(self.position.distance_to(predator.position) for predator in all_predators)

            # chance speed if closest predtor is inside perception distance
            if closest_predator_distance < PERCEPTION_LENGHT_HERRING:
                speed_h = HERRING_SPEED
                self.speed.normalize()

                self.speed = self.speed * (speed_h + (HERRING_SPEED_MAX -HERRING_SPEED) * ((PERCEPTION_LENGHT_HERRING-closest_predator_distance) / PERCEPTION_LENGHT_HERRING))


    def update(self,all_herring, all_predators, all_rocks):
        """Function to update the position of a herring"""

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

        # loop over all the herrings to determine which are in the spereation radius,
        # alignment radius and cohesion radius
        for herring in all_herring:

            # make sure a herring is not compared to itself
            if herring != self:

                # determine the distance between two herring
                distance_two_herring = self.position.distance_to(herring.position)

                # implement seperation rule
                total_separation_vector, neighbour_herring_separation = self.separation_herring(distance_two_herring, total_separation_vector, neighbour_herring_separation, herring.position, self.position)

                # implement alignment rule
                total_alignment_vector, neighbour_herring_alignment = self. alignment_herring( distance_two_herring, total_alignment_vector, neighbour_herring_alignment, herring.speed)

                # implement cohension rule
                total_cohesion_vector, neighbour_herring_cohesion = self.cohesion_herring(distance_two_herring, total_cohesion_vector, neighbour_herring_cohesion, herring.position , self.position)

        # Update velocity
        total_vector_rules = self.rule_vector(neighbour_herring_separation, total_separation_vector, neighbour_herring_alignment, total_alignment_vector, neighbour_herring_cohesion, total_cohesion_vector)
        self.speed += total_vector_rules

        # avoid the predators
        self.avoid_predator(all_predators)

        # swim around the rock
        self.avoid_rock(all_rocks)

        # accelerate if predator is close
        self.accelerate_to_avoid_perdator(all_predators)

        # change the position
        self.position += self.speed

        # use periodic boundaries
        self.position.x = self.position.x % WIDTH
        self.position.y = self.position.y % HEIGHT

        # update the center of the predator form
        self.rect.center = self.position


class Predator(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()

        # create the surface of the predator and add it to the display
        self.image = pygame.Surface((PREDATOR_RADIUS * 2, PREDATOR_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,0, 0), (PREDATOR_RADIUS, PREDATOR_RADIUS), PREDATOR_RADIUS)

        # make the form of the predator
        self.rect = self.image.get_rect(center=( x_pos, y_pos))

        # add the position of the predator to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

        # determine dx and dy
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)

        # make sure the speed will be in the correct direction
        self.speed = pygame.Vector2(dx, dy).normalize() * PREDATOR_SPEED

    def attack_herring(self, all_herring):
        """ Function that ensures a predator will attack a herring when the herring
        is within its perception lenght"""

        # make attack vector
        total_herring_attack_vector = pygame.Vector2(0, 0)

        # herring within the perception distance
        neighbour_herring = 0

        # loop over al the  herrings
        for herring in all_herring:

            # determine the distance to the herring
            distance_to_herring = self.position.distance_to(herring.position)

            # determine if the predetor is close ehough to sense it
            if distance_to_herring < PERCEPTION_LENGHT_PREDATOR:

                # make vector that gives the direction to move to the herring
                direction_to_herring = ( herring.position - self.position ) / distance_to_herring
                total_herring_attack_vector += direction_to_herring

                neighbour_herring +=1

        # determine if there is a herring
        if neighbour_herring > 0:

            # normalize the vector
            total_herring_attack_vector = total_herring_attack_vector  / neighbour_herring

            # multiply by five to ensure moving  to the herring is most important
            self.speed +=  total_herring_attack_vector

        # normalise speed
        self.speed = self.speed.normalize() * PREDATOR_SPEED

    def avoid_rock(self, all_rocks):
        """ Function that ensures the predator will swim around a rock """

        # loop over the rocks
        for rock in all_rocks:

            # determine distance between rock and predator
            distance_to_rock = self.position.distance_to(rock.position)

            # determine if there is a rock so close that it will influence the direction
            # of the predator
            if distance_to_rock < 30:

                # make a avoidance vector
                rock_avoidance_vector = (self.position - rock.position).normalize()
                self.speed += rock_avoidance_vector

                # adjsut the position to move from the rock
                self.position += rock_avoidance_vector

        # normalize speed
        self.speed = self.speed.normalize() * PREDATOR_SPEED

    def accelerate_to_attack_herrig(self, all_herring):
        """Function that ensures the predator will accelerate when a herring is within
        its perception lenght. The closer the herring is the faster the predator will move"""

        # check if there are herring
        if all_herring:
            # determine the distance to the clostest herring
            closest_herrring_distance = min(self.position.distance_to(herring.position) for herring in all_herring)

            # chance speed if closest herring is inside perception distance
            if closest_herrring_distance < PERCEPTION_LENGHT_PREDATOR:
                speed_p = PREDATOR_SPEED
                self.speed.normalize()

                self.speed = self.speed * (speed_p + (PREDATOR_SPEED_MAX -PREDATOR_SPEED) * ((PERCEPTION_LENGHT_PREDATOR-closest_herrring_distance) / PERCEPTION_LENGHT_PREDATOR))

    def update(self, all_herring, all_predators, all_rocks):
        """ Function to update the position of a predator"""

        # determine if predator will attack herring
        self.attack_herring(all_herring)

        # ensure the predator will swim around the rock
        self.avoid_rock(all_rocks)

        # accelerate if a herring is close
        self.accelerate_to_attack_herrig(all_herring)

        # change the position
        self.position += self.speed

        # use periodic boundaries
        self.position.x = self.position.x % WIDTH
        self.position.y = self.position.y % HEIGHT

        # update the center of the predator form
        self.rect.center = self.position

class Rock(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()

        # create the surface of the rock and add it to the display
        self.image = pygame.Surface((ROCK_LENGHT * 2, ROCK_LENGHT * 2), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (125, 125, 125), (0, 0, ROCK_LENGHT, ROCK_LENGHT))

        # make form rock for collision
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        # add the position of the rock to a vector
        self.position = pygame.Vector2(x_pos, y_pos)

    def distance_to(self, other_position):
        return math.sqrt((self.position[0] - other_position[0])**2 + (self.position[1] - other_position[1])**2)


class Experiment(pygame.sprite.Sprite):
    def __init__(self, herring_nr, predator_nr, rock_nr, simulation_duration):
        self.herring_nr = herring_nr
        self.predator_nr = predator_nr
        self.rock_nr = rock_nr
        self.simulation_duration = simulation_duration

    def add_herring_experiment(self):
        """ Function thad adds herring to the experiment"""

        # make the herring group
        all_herring = pygame.sprite.Group()

        # give all the herring a position and add them to the group
        for _ in range(self.herring_nr):
            herring_i = Herring(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            all_herring.add(herring_i)

        return all_herring

    def add_predator_experiment(self):
        """ Function thad adds predators to the experiment"""

        # make the predators group
        all_predators = pygame.sprite.Group()

        # give all the predators a position and add them to the group
        for _ in range(self.predator_nr):
            predator_i = Predator(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            all_predators.add(predator_i)

        return all_predators
    
    def add_rocks_experiment(self):
        """ Function thad adds rocks to the experiment"""

        # make the rocks group
        all_rocks = pygame.sprite.Group()

        # give all the rocks a position and add them to the group
        for _ in range(self.rock_nr):
            rock_i = Rock(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            all_rocks.add(rock_i)
        
        #Calculate Euclidean distances between rocks
        distances = []
        for rockA in all_rocks:
            for rockB in all_rocks:
                if rockA != rockB:  # Ensure we're not calculating distance to itself
                    distance_rock = rockB.distance_to(rockA.position)
                    #print(f"Distance between {rockA.position} and {rockB.position}: {distance_rock}")
                    distances.append(distance_rock)

                    #TOBEDONE onderzoekje distancerocks
                    if distance_rock < 60:
                        num_extra_rocks = int((60 - distance_rock) / 10) #ten is size rocks
                        for i in range(1, num_extra_rocks + 1):
                            ratio = i / (num_extra_rocks + 1)
                            new_x = int(rockA.position[0] + ratio * (rockB.position[0] - rockA.position[0]))
                            new_y = int(rockA.position[1] + ratio * (rockB.position[1] - rockA.position[1]))
                            new_rock = Rock(new_x, new_y)
                            all_rocks.add(new_rock)
                            distances.append((new_x, new_y))

        return all_rocks                   



    def run(self):
        """ Function that runs an experiment"""
        # make the herring group
        all_herring = self.add_herring_experiment()

        # make the predators groep
        all_predators = self.add_predator_experiment()

        # make the rocks group
        all_rocks = self.add_rocks_experiment()

        # make a screen
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f'Simulation of herring school with {self.herring_nr} herring and {self.predator_nr} predator(s)')

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

            # update display
            pygame.display.flip()

            # determine the time that has elapsed
            time_elapsed = time.time() - start_time

            # stop the simultion after the specified time
            if time_elapsed >= self.simulation_duration:
                simulation_run = False

            # set the number of frames per secod
            clock.tick(FRAMES_PER_SECOND)

        # if the while loop is stoped quite the game
        pygame.quit()


# Run the main function
if __name__ == "__main__":
    experiment_1 = Experiment(10, 1, 10, 10)
    experiment_1.run()

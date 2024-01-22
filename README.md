Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405

THE GOAL
The main goal of this project is to make an 2D Agent-based model that simulates the behaviour of a herring school. 
The aim is to assess the influence of three movement rules, as well as the impact of environmental changes, 
the presence of rocks, and the number of predators (barracuda), on the herring killing rate.


THE MODEL: gamefish
Gamefish contains the code to run an agent-based model in which the herring, rocks
and predators are represented as agents with each their own positions and velocity's.

The movement of a herring (boid) is based on three rules:
- Separation: Herring don't want to get closer than some minimum distance.
- Alignment: Herrings align their direction with that of their close neighbors
- Cohesion: Herring moves towards the position of their close neighbours.

Herring features
The speed of the herring is the average speed in which some value between -1 and +1 (the stadard deviation) 
is added.This variation is introduced to create diversity within the herring population.
The presence of rocks and predators in the enviroment influences the herrings behaviour. 
Rocks can alter the direction of a herring, as herrings avoid collisions with rocks.
Predators can affect both the speed and direction of a herring. 
If a predator is within the perception range ofa herring, the herring's speed increases, 
and the herring moves away from the predator. The closer the predator, the greater the speed increase.

Baracuda features
The movement of a baracuda is primarily random unless it comes too close to another baracuda
in wich case it will move away. The speed of the baracuda is the average speed in which some 
value between -1 and +1 (the stadard deviation) is added.This variation is introduced to 
create diversity within the baracuda population. The presence of rocks and herring in the 
environment influences the movement of a baracuda. Rocks can alter the direction of a predator, 
as baracuda's also tend to avoid collisions. Herrings can change the speed and direction of a 
predator. If a herring is within the perception range of the baracuda, the baracuda's speed 
increases and the predator will move towards the herring. The closer the herring the greater 
the speed increase.

Rock features
The stones are randomly distributed across the plot. No creature can traverse these obstacles. 
When the parameter 'extra_rocks' is set to true, the stones will cluster. This is achieved by 
identifying stones within a Euclidean distance of less than 60 units and placing additional 
rocks along this distance line. For each extra rock, another rock is added, and its position 
is determined by multiplying a random number between 0 and 1.

Default experiment

THE FUNCION
Experiment(nr herring, nr predator, nr rocks, duration, connect_rocks, start as
        school, change perception predator, alignment distance, cohesion distance,
        separation distance)

In the default function the rocks get a random position, and connect_rocks is set to true. 
The herrings get different positions close to each other to form a school. The baracuda's 
get a random position that is not within the baracuda's perception with a herring. 
This is done so the full attack can be studied. The simulation is runned for the specified 
number of seconds. 

Specifications in model (finetuning)
When the 'start_school' parameter is set to False, herrings will not be placed in a school 
but rather randomly. For longer simulation durations, the perception length of barracuda 
can dynamically change over time using the 'perception_change' parameter. Additionally, 
the alignment distance, cohesion distance, and separation distance can be modified to 
assess their respective influences. This is done to investigate whether these rule 
adjustments have an impact on the killing rate of herrings.

The model returns the number of killed herrings and the times a barracuda came close to a herring. It also provides a list with the number of killed herrings over time and a list with the perception lengths of the predators over time

FIXED PARAMETERS ###the the number?
* HERRING_SIZE (float) = the radius of the circle representing a herring in the simulation.
* HERRING_SPEED (float) = the average speed of a herring.
* HERRING_SPEED_MAX (float) = the maximum speed of a herring.
* PERCEPTION_LENGHT_HERRING (float) = the length a herring can sense.
* KILL_DISTANCE (float) = the distance between herring predator that the predator will kill
                  the herring.
* PREDATOR_SIZE (float) = radius of the circle representing a herring in the simulation.
* PREDATOR_SPEED (float) = the normal average speed of a barracuda.
* PREDATOR_SPEED_MAX (float) = the highest speed a barracuda can have.
* PERCEPTION_LENGHT_PREDATOR (float)= the length a barracuda can sense.
* ROCK_LENGHT (float) = the length of the square representing a rock in the simulation.

OTHER PARAMETERS
* herring_nr (int) = intial number of herrings added to the simulation.
* predator_nr (int) = intial number of predators added to the simulation.
* rock_nr (int) = initial number of rocks added to the simulation.
* simulation_duration (int) = duration of a simulation is seconds.
* extra_rocks (bool) = added rocks for the clustering/connecting of rocks. ###
* start_school (bool) = herring start as one school instead of randomly.
* perception_change (bool) = change of the perception length by baracuda over the time.
* SEPARATION_DISTANCE (float) = if another herring is within this distance, it will be included
                        in the separation rule. ###
                        for the separation rule
* ALIGNMENT_DISTANCE (float) = if another herring is within this distance, it will be included
                       in the alignment rule.
* COHESION_DISTANCE (float) = if another herring is within this distance, it will be included in
                      the cohesion rule.


THE VISUALISATION
Visualization contains the code to make plots that show the influence of environmental
changes on the herring killing rate. It uses the gamefish code to run an experiment.

HOW TO RUN:

Command to run a simulation in the model with these values: 
Experiment(herring_nr = 100, predator_nr = 1, rock_nr = 10, simulation_duration = 20, 
extra_rocks = False, start_school = True, perception_change = False, alignment_distance = 32, 
cohesion_distance = 32 and separation_distance = 6)

- python gamefish.py



MODEL: matrixes
Boids contains code to run a agent-based simulation of herring schools and possibly
rocks and/or predators. This code works with matrices.
Implementing the three Boid flocking rules (separation, alignment and cohesion) was
possible. However, by introducing rocks and predators, working with the matrices became
too difficult. So for that reason the code is not complete and we did not use it for
analyse. But it shows that we tried it this way.   


THE FUNCTION
Experiment(lower_lim_flock, upper_lim_flock, lower_lim_veloc, upper_lim_veloc, nr_herring, 
           nr_predators, nr_rocks)

FIXED PARAMETERS
* perception_predator (float) = perception rate of predator set to 50.
* velocity_predator (float) = velocity of predator set to 2.
* attraction_to_center (float) = the strength of the center movement method, 
        where a negative value implies repulsion and a positive value implies attraction.
        set to 0.00008
* width_flock (float) = Calculated as the difference between the upper limit and the lower limit.
                        It determines the range or spread of the flocking behavior in the simulation.
* width_veloc (float) = Calculated as the difference between the upper limit and the lower limit. 
                        It determines the range or spread of possible velocities for entities in the simulation.
* lower_lim_flock (float)= Minimum value where a herring of a flock can be placed.
                           Between 0 and 100.
* upper_lim_flock (float)= Maximum value where a herring of a flock can be placed.
                           Between 0 and 100.
* lower_lim_veloc (float)= Minimum range of the velocity of a herring.
                           Between -20 and 0.
* lower_lim_veloc (float)= Maximum range of the velocity of a herring.
                           Between 0 and 20.
* perception_length_herring (float)= the length a herring can sense.
                           Set to 0.002

PARAMETERS
* nr_herring (int) = intial number of herrings added to the simulation.
* nr_predators (int) = intial number of predators added to the simulation.
* nr_rocks (int) = initial number of rocks added to the simulation.
* iterations (int) = number of times experement will be repeated.
* second_flock (bool) = enables/ disables a second flock of nr_herrings.
* min_distance (float) = minimum distance entities must maintain to avoid collisions in the simulation. 
                        Set to 20.
* formation_flying_distance (float)= determines the distance at which entities align with each other.
                        Set to 10.
* formation_flying_distance (float)= controls the strength of the alignment. A higher value increases 
                                     the influence of alignment on entity direction within the specified distance.
                        Set to 0.8

HOW TO RUN:
Command to run a simulation in the incomplete model with the values: 
Experiment(lower_lim_flock, upper_lim_flock, lower_lim_veloc, 
           upper_lim_veloc, nr_herring = 20, nr_predators = 2, nr_rocks = 10)

- python boids.py

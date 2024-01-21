Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405

THE GOAL
The main goal of this project is to make an 2D Agent-based model that simulates the behaviour of a herring school. 
The aim is to assess the influence of three movement rules, as well as the impact of environmental changes, 
the presence of rocks, and the number of predators (barracuda), on the herring killing rate.

#to uitleg 
killing rate it taken as measurement because the most important function of schooling
is protection against predators. So by changing the schooling, the protection
and thus herring killing rate also changes.


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

Default experiment

THE FUNCION
Experiment(nr herring, nr predator, nr rocks, duration, connect rocks, start as
        school, change perception predator, alignment distance, cohesion distance,
        separation distance)

In the default function the rocks get a random position, then the herrings get different
positions close to each other to form a school. The baracuda's get a random position that 
is not within the baracuda's perception with a herring. This is done so the full attack can 
be studied. 
The simulation is runned for the specified number of seconds. 

It is possible to connect nearby rocks by introducing more rocks and to place the herring not
in one big school but random. If the simulation is runned for a long time it is possible
that the perception length of the predator gets changed over the time. The alignment
distance, cohesion distance and separation distance can also be change in order to determine
their influence.

The model returns the number of herring killed and the times a baracuda came close to a. 

###herring or it
returns a list with the number of killed herring over the time and a list with the
perception lengths of the predators over the time.

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

THE PARAMETERS IN THE MODEL
Parameters that can be changed by the user:
* herring_nr = number of herrings added to the simulation (int).
* predator_nr = number of predators added to the simulation (int).
* rock_nr = number of rocks added to the simulation (int).
* simulation_duration = the duration of a simulation is seconds (int).
* extra_rocks: closeby rocks should be connected via more rocks (Bool).
* start_school: herring start as one school instead of randomly (bool).
* perception_change: predator perception length changes over the time (bool).
* SEPARATION_DISTANCE = if another herring is within this distance, it will be included
                        in the separation rule (float).
* ALIGNMENT_DISTANCE = if another herring is within this distance, it will be included
                       in the alignment rule (float).
* COHESION_DISTANCE = if another herring is within this distance, it will be included in
                      the cohesion rule (float).


THE VISUALISATION
Visualization contains the code to make plots that show the influence of environmental
changes on the herring killing rate. It uses the gamefish code to run an experiment.

HOW TO RUN:

Command to run a simulation in the model with these values: herring_nr = 100, predator_nr = 1,
rock_nr = 10, simulation_duration = 20, extra_rocks = False, start_school = True, perception_
change = False, alignment_distance = 32, cohesion_distance = 32 and separation_distance = 6
- python gamefish.py






MODEL MAKING WITH MATRICES (incomplete model)
Boids contains code to run a agent-based simulation of herring schools and possibly
rocks and/or predators. This code works with matrices and is therefore extremely fast.
Implementing the three Boid flocking rules (separation, alignment and cohesion) was
possible. However, by introducing rocks and predators, working with the matrices became
too difficult. So for that reason the code is not complete and we did not use it for
analyse. But it shows that we tried it this way.   



Possibly:
Command to run a simulation in the incomplete model with the values: herring_nr = 20,
predator_nr = 1, rock_nr = 10.
- python boids.py

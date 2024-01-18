Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405

THE GOAL
The main goal of this project is to make an 2D Agent-based model that simulates
the herring schooling behaviour and to determine the influence of environmental
changes, rocks and predators (barracuda), on the herring killing rate. The herring
killing rate it taken as measurement because the most important function of schooling
is protection against predators. So by changing the schooling, the protection
and thus herring killing rate also changes.


THE MODEL
Gamefish contains the code to run a agent-based model in which the herring, rocks
and predators are represented as agent with own position and velocity.

The movement of a herring (boid) is based on the three rules:
- Separation: Herring do not get closer than some minimum distance
- Alignment: Herring heads in the direction of the neighbours within close distance.
- Cohesion: Herring moves to the position of the neighbours within close distance.

The speed of the herring is the normal average speed to which some value between
-1 SD and +1 SD added, to create some variation in the herring population.
It is possible to introduce rocks and predators, which will influence the behaviour
of a herring. Rocks can change the direction of a herring. Predators can change the
speed and direction of a herring. If a predator is within the perception length of
a herring, the herring's speed increases and the herring will move away from the
predator. The closer the predator the more the speed increase.

The movement of a predator is random unless it comes too close to another predator
then it will move away. To the normal average speed of a predator is some value between
-1 SD and +1 SD added, to create variation in the predator population. When rocks and
herring are introduced they influence the movement of a predator. Rocks can change the
direction of a predator. Herring can change the speed and direction of a predator. If
a herring is within the perception length of a predator, the predators speed increases
and the predator will move towards the herring. The closer the herring the more the
speed increase.

In the default function first the rocks get a random position, then the herring get a
different position close to each other to form a school and lastly the predators get
a random different position that is not within predator perception distance of a herring.
The predator is placed not within the perception distance of herring so the full attack
can be studied. The simulation is runned for the specified number of seconds. It is
possible to connect nearby rocks by introducing more rocks and to place the herring not
in one big school but random. If the simulation is runned for a long time it is possible
that the perception length of the predator gets changed over the time. The alignment
distance, cohesion distance and separation distance can also be change in order to determine
their influence.

The experiment fuction looks like this:
 - Experiment(nr herring, nr predator, nr rocks, duration, connect rocks, start as
        school, change perception predator, alignment distance, cohesion distance,
        separation distance)

The model returns the number of killed herring and the number of close herring or it
returns a list with the number of killed herring over the time and a list with the
perception lengths of the predators over the time.

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

Parameters that are fixed:
* HERRING_SIZE = the radius of the circle representing a herring in the simulation (float).
* HERRING_SPEED = the normal average speed of a herring (float).
* HERRING_SPEED_MAX = the highest speed a herring can have (float).
* PERCEPTION_LENGHT_HERRING = the length a herring can sense (float).
* KILL_DISTANCE = the distance between herring predator that the predator will kill
                  the herring (float).
* PREDATOR_SIZE = radius of the circle representing a herring in the simulation (float).
* PREDATOR_SPEED = the normal average speed of a barracuda (float).
* PREDATOR_SPEED_MAX = the highest speed a barracuda can have (float).
* PERCEPTION_LENGHT_PREDATOR = the length a barracuda can sense (float).
* ROCK_LENGHT = the length of the square representing a rock in the simulation (float).


THE VISUALISATION
Visualization contains the code to make plots that show the influence of environmental
changes on the herring killing rate. It uses the gamefish code to run an experiment.


MODEL MAKING WITH MATRICES (incomplete model)
Boids contains code to run a agent-based simulation of herring schools and possibly
rocks and/or predators. This code works with matrices and is therefore extremely fast.
Implementing the three Boid flocking rules (separation, alignment and cohesion) was
possible. However, by introducing rocks and predators, working with the matrices became
too difficult. So for that reason the code is not complete and we did not use it for
analyse. But it shows that we tried it this way.   


HOW TO RUN:

Command to run a simulation in the model with these values: herring_nr = 100, predator_nr = 1,
rock_nr = 10, simulation_duration = 20, extra_rocks = False, start_school = True, perception_
change = False, alignment_distance = 32, cohesion_distance = 32 and separation_distance = 6
- python gamefish.py

Command to make the plots
- python visualisation.py


Possibly:
Command to run a simulation in the incomplete model with the values: herring_nr = 20,
predator_nr = 1, rock_nr = 10.
- python boids.py

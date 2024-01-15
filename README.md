Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405


Parameters ????gamefish.py?????
Gamefish contains the code to run a agent-based simulation of herring schools and
possibly rocks and/or predators.

The plain movement of a herring (boid) is based on the three rules:
- Separation: Herring do not get closer than some minimum distance
- Alignment: Herring heads in the direction of the neighbours within close distance.
- Cohesion: Herring moves to the position of the neighbours within close distance.

It is possible to introduce rocks and predators, which will influence the behaviour
of a herring. Rocks can change the direction of a herring. Predators can change the
speed and direction of a herring. To the normal average speed of a herring is some
value between -1 SD and +1 SD added, to create variation.

The plain movement of a predator is random unless it comes too close to another
predator then it will move away. When rocks and herring are introduced they influence
the movement of a predator. Rocks can change the direction of a predator. Herring
can change the speed and direction of a predator. To the normal average speed of a
predator is some value between -1 SD and +1 SD added, to create variation.

In the default function first the rocks get a random position, then the herring get a
random different position and lastly the predators get are random different position
that is not within predator perception distance of a herring. The predator is placed
not within the perception distance of herring so the full attack can be studied.
The simulation is runned for the specified number of seconds. It is possible to connect
nearby rocks by introducing more rocks and to place the herring not random but in one
big school. If the simulation is runned for a long time it is possible that the
perception lenght of the predator gets changed over the time. The alignment distance,
cohesion distance and separation distance can also be change in order to determine their
influence.
 - Experiment(nr herring, nr predator, nr rocks, duration, connect rocks, start as
 school, change perception predator alignment distance, cohesion distance, separation distance)

The parameters of the this simulation are:
herring_nr = number of herrings added to the simulation.
predator_nr = number of predators added to the simulation.
rock_nr = number of rocks added to the simulation.
simulation_duration = the duration of a simulation is seconds.
RADIUS_HERRING = the radius of the circle representing a herring in the simulation.
HERRING_SPEED = the normal average speed of a herring.
HERRING_SPEED_MAX = the highest speed a herring can have.
PERCEPTION_LENGHT_HERRING = the length a herring can sense.
KILL_DISTANCE = the distance between herring barracuda that the predator barracuda will kill the herring.
SEPARATION_DISTANCE = if another herring is within this distance, it will be included in the separation rule.
ALIGNMENT_DISTANCE = if another herring is within this distance, it will be included in the alignment rule.
COHESION_DISTANCE = if another herring is within this distance, it will be included in the cohesion rule.
PREDATOR_RADIUS = the radius of the circle representing a herring in the simulation.
PREDATOR_SPEED = the normal average speed of a barracuda.
PREDATOR_SPEED_MAX = the highest speed a barracuda can have.
PERCEPTION_LENGHT_PREDATOR = the length a barracuda can sense.
ROCK_LENGHT = the length of the square representing a rock in the simulation

????? Visualisation ????
Visualization contains the code to make plots that show the influence of environmental
changes on the herring killing rate. It uses the ???gamefish??? code to run an
experiment.

Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279, 15159337, 13717405

THE GOAL  
The main goal of this project is to make a 2D agent-based model that simulates the
behaviour of a herring school. The aim is to assess the influence of the three boid
rules, as well as the impact of environmental changes, rocks and predators (barracuda),
on the killing rate within a herring school. For the parameter values of the predator 
the values from barracudas are taken.


THE MODEL: gamefish  
Gamefish.py contains the code to run an agent-based model in which the herring, rocks
and predators are represented as agents with their own positions and velocities.

Herring features  
The movement of a herring (boid) is based on three rules:
- Separation: Herring maintain a minimum distance between themselves and others within the group.
- Alignment: Herring aligns their direction with that of their closest neighbours
- Cohesion:  Herring remains in close proximity to their nearest neighbors.

The speed of the herring is the avarage speed for a herring. For a diversity of natural 
speeds within the group, a value of the standard deviation spread, ranging between -1 and 1, 
is also added to this. 
The presence of rocks and predators in the environment influences the behavior of herring, when 
it is in their perception range. Rocks alter the direction of herring, while predators can affect 
both their speed and direction. As predators draw closer, the herring's speed accelerates.

Barracuda features  
The movement of a barracuda is initially random, but it changes when it encounters another barracuda, 
causing it to change directions. Additionally, the presence of rocks and herring in the environment 
also influences a barracuda's movement. Rocks can alter the direction of a barracuda, while herring 
can impact both its speed and direction. When a herring is within the perception range of a barracuda, 
the predator's speed increases, and it will move towards the herring. Moreover, the closer the herring, 
the greater the acceleration of the barracuda's speed

Rock features  
The stones are randomly distributed. No creature can traverse these obstacles. When
parameter 'connect_rocks' is set to true, the stones will cluster. This is achieved
by identifying stones within a Euclidean distance of less than 60 units and placing
additional rocks along this distance line.

THE FUNCTION  
Experiment(herring_nr, predator_nr, rock_nr, simulation_duration,
connect_rocks, start_school, perception_change_predator, perception_change_herring,
alignment_distance, cohesion_distance, separation_distance, boids_influence)

In the default function, the rocks get a random position, and connect_rocks is set to
true. Start_school is also set to True, the herring get different positions
close to each other to form a school. The barracudas are assigned random positions that 
lie outside the perception range of any herring. This ensures that the entire attack is
shown. The simulation is run for a specified number of seconds. 
In the perception length of the herring and predator do not change, perception_change
_predator and perception_change_herring are set to False. And every boid rule has the
same amount of influence.

Specifications in model 
For longer simulation durations, the perception length of barracuda can dynamically change 
over time using the 'perception_change' parameter. Additionally, the alignment distance, 
cohesion distance, and separation distance are subject to modification to evaluate their 
individual effects. This adjustment aims to explore whether these rule alterations affect 
the killing rate of herring. If the 'boids_influence' parameter is set to a value other 
than 0, the impact of a rule will be weighted accordingly.

Output model  
In the default function, the model returns a dictionary that contains the number
of killed herring and the number of times herring came within the separation distance
of 6. If 'perception_change_herring' is set to True it also returns a list with the
perception length of the herring and with the killed herring count at every time point.
If 'perception_change_predator' is set to True it also returns a list with the perception
length of the predator and with the killed herring count at every time point.

FIXED PARAMETERS  
* HERRING_SIZE (float) = the radius of the circle wich represents herring in the simulation.
                         - Set to 3
* HERRING_SPEED (float) = the average speed of a herring.
                         - Set to 1.24 (SD = 0.05)
* HERRING_SPEED_MAX (float) = the maximum speed of a herring.
                         - Set to 18.44
* PERCEPTION_LENGHT_HERRING (float) = the length a herring can sense.
                         - Set to 32
* KILL_DISTANCE (float) = the distance where a predator wil kill a herring.
                         - Set to 3.6
* PREDATOR_SIZE (float) = radius of the wich represents a baracuda in the simulation.
                         - Set to 4
* PREDATOR_SPEED (float) = the normal average speed of a barracuda.
                         - Set to 3.6 (SD = 0.8)
* PREDATOR_SPEED_MAX (float) = the highest speed a barracuda can have.
                         - Set to 24.4
* PERCEPTION_LENGHT_PREDATOR (float)= the length a barracuda can sense.
                         - Set to 100
* ROCK_LENGHT (float) = the length of the square representing a rock in the simulation.
                         - Set to 10
* ROCK_AVOIDANCE_DIST (float) = the distance at which both creatures will start sensing rocks.
                               - Set to 16

CHANGEABLE PARAMETERS  
* herring_nr (int) = initial number of herring added to the simulation.
* predator_nr (int) = initial number of predators added to the simulation.
* rock_nr (int) = initial number of rocks added to the simulation.
* simulation_duration (int) = duration of a simulation in seconds.
* connected_rocks (bool) = parameter for adding clustering of the initial rocks.
* start_school (bool) = herring start as one school instead of randomly.
* perception_change_predator (bool) = change of the barracuda perception length over time.
* perception_change_herring (bool) = change of the herring perception length over time.
* SEPARATION_DISTANCE (float) = if another herring is within this distance, it will be
                          included in the separation rule.
* ALIGNMENT_DISTANCE (float) = if another herring is within this distance, it will be
                          included in the alignment rule.
* COHESION_DISTANCE (float) = if another herring is within this distance, it will be
                          included in the cohesion rule.
* boids_influence (int) = Indicates the influence of boids rules. 
                            0 --  all rules are equal, 
                            1 -- separation is weighted 3 times more, 
                            2 -- alignment is weighted 3 times more,
                            3 -- cohesion is weighted 3 times more.

HOW TO RUN:  
Command to simulate the default model with these values:
Experiment(herring_nr = 100, predator_nr = 3, rock_nr = 30, simulation_duration = 20,
      extra_rocks = False, start_school = True, perception_change_predator = False,
      perception_change_herring = False, alignment_distance = 32, cohesion_distance = 32,
      separation_distance = 6, boids_influence = 0)

- python gamefish.py


THE VISUALISATION: gamefish.py  
Visualization.py contains the code to make plots that show the influence of environmental
changes on the herring killing rate and school density. It uses the gamefish code to run
an experiment. The code also does some statistical tests provided by the code in statistic_test.py.

All plots are also provided in the folder data_visualisation.
* 4-perception_change_plot: Line plot that shows the change in perception length and
                  the resulting number of killed herring over the time.
                  - ####HOW TO RUN###

* Change_alignment_distance_plot: Line plot of the average killed herring + 1 SD error
                  bars at different alignment distances.
                  - ####HOW TO RUN###

* Change_predator_nr_plot: Violin plot of the distribution of the killed herring for
                  different numbers of barracudas with and without rocks.
                  - ####HOW TO RUN###

* Change_rock_nr_plot: Line plot of the average killed herring + 1 SD error bars in
                  environments with different numbers of rocks.
                  - ####HOW TO RUN###

* Density_Killing_combination_plot: Boxplots with strip plots overlap that show the
                  distribution of the herring count within the original separation distance
                  of 6 and the herring killing count across various conditions.
                  - ####HOW TO RUN###

* School_size_plot: Boxplot with strip plot overlap that shows the proportion of killed
                  herring in large and small schools, with and without rocks.
                  - ####HOW TO RUN###

* Boids_rules_influence_plot: Boxplot with strip plot overlap that shows the number of
                  killed herring when different boid-flocking rules are emphasised
                  - ####HOW TO RUN###

* Boid_rules_sensitivity_analysis_plot: Line plots of the average number of killed
                  herring + 1 SD error bars for different values of the alignment,
                  cohesion and separation distance as sensitivity analysis.
                  - ####HOW TO RUN###

- python visualisation.py.


THE STATISTICAL TESTS  
Statistic_tests.py contains the code to do the statistical test on the data obtained
in visualisation.py.

It contains 4 statistical tests:
- Test to determine if school size significantly changes the killing proportion.
- Test to determine if environmental changes significantly influence the school density.
- Test to determine if environmental changes significantly influence the killing rate.
- Test to determine if the different boid-flocking rules significantly influence the killing rate.

This cannot be run separately because it needs the data collected in visualisation.py.

INCOMPLETE MODEL: matrixes  
boids.py contains code to run an agent-based simulation of herring schools and possibly
rocks and/or predators. This code works with matrices.
Implementing the three boid flocking rules (separation, alignment and cohesion) was
possible. However, by introducing rocks and predators, working with the matrices became
too difficult. So for that reason, the code is not complete and we did not use it for
analysis. But it shows that we tried it this way.   

THE FUNCTION  
Experiment(lower_lim_flock, upper_lim_flock, lower_lim_veloc, upper_lim_veloc, nr_herring,
           nr_predators, nr_rocks)

FIXED PARAMETERS  
* perception_predator (float) = perception rate of predator.
                        - Set to 50.
* velocity_predator (float) = velocity of predator.
                        - Set to 2.
* attraction_to_center (float) = the strength of the centre movement method, where a
                    negative value implies repulsion and a positive value attraction.
                        - Set to 0.00008
* width_flock (float) = It determines the range or spread of the flocking behaviour
                    in the simulation.
                        - Set to upper_lim_flock - lower_lim_flock
* width_veloc (float) = It determines the range or spread of possible velocities for
                    entities in the simulation.
                        - Set to upper_lim_veloc - lower_lim_veloc
* iterations (int) = the number of times the experiment will be repeated.
                        - Set to 100.
* second_flock (bool) = enables/ disables a second flock of nr_herring.
                        - Set to False.
* min_distance (float) = minimum distance entities must maintain to avoid collisions
                    in the simulation.
                        - Set to 20.
* formation_flying_distance (float)= determines the distance at which entities align
                    with each other.
                        - Set to 10.
* formation_flying_strength (float)= controls the strength of the alignment. A higher value
                    increases the influence of alignment on entity direction within the
                    specified distance.
                        - Set to 0.8
* perception_length_herring (float)= the length a herring can sense.
                        - Set to 0.002

CHANGEABLE PARAMETERS  
* nr_herring (int) = initial number of herring added to the simulation.
* nr_predators (int) = initial number of predators added to the simulation.
* nr_rocks (int) = initial number of rocks added to the simulation.
* lower_lim_flock (float)= Minimum value where a herring of a flock can be placed.                        
* upper_lim_flock (float)= Maximum value where a herring of a flock can be placed.                
* lower_lim_veloc (float)= Minimum range of the velocity of a herring.                      
* upper_lim_veloc (float)= Maximum range of the velocity of a herring.


HOW TO RUN:  
Command to simulate the incomplete model with the values:
Experiment(lower_lim_flock, upper_lim_flock, lower_lim_veloc, upper_lim_veloc,
          nr_herring = 20, nr_predators = 2, nr_rocks = 10)

- python boids.py



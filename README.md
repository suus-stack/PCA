Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279, 15159337, 13717405

THE GOAL  
The main goal of this project is to make a 2D Agent-based model that simulates the
behaviour of a herring school. The aim is to assess the influence of the three boid
rules, as well as the impact of environmental changes, rocks and predators (barracuda),
on the herring killing rate.


THE MODEL: gamefish  
Gamefish.py contains the code to run an agent-based model in which the herring, rocks
and predators are represented as agents with their own positions and velocities.

Herring features  
The movement of a herring (boid) is based on three rules:
- Separation: Herring do not want to get closer than some minimum distance.
- Alignment: Herring align their direction with that of their closest neighbours
- Cohesion: Herring moves towards the position of their closest neighbours.

The speed of the herring is the average speed at which some value between -1 *standard
Deviation (SD) and +1* SD is added. This variation is introduced to create diversity
within the herring population. The presence of rocks and predators in the environment
influences the herring's behaviour. Rocks can alter the direction of a herring and
predators can affect both the speed and direction.  If a predator is within the perception
range of a herring, the herring's speed increases and the herring moves away from the
predator. The closer the predator, the more the speed increases.

Barracuda features  
The movement of a barracuda is random unless it comes too close to another barracuda
in which case it will move away. The speed of the barracuda is the average speed at
which some value between -1 * SD and +1* SD is added. This variation is introduced to
create diversity within the barracuda population. The presence of rocks and herring
in the environment influences the movement of a barracuda. Rocks can alter the direction
of a barracuda and herring can change the speed and direction. If a herring is within
the perception range of the barracuda, the barracuda's speed increases and the predator
will move towards the herring. The closer the herring the more the speed increases.

Rock features  
The stones are randomly distributed. No creature can traverse these obstacles. When
the parameter 'extra_rocks' is set to true, the stones will cluster. This is achieved
by identifying stones within a Euclidean distance of less than 60 units and placing
additional rocks along this distance line.

THE FUNCTION  
Experiment(herring_nr, predator_nr, rock_nr, simulation_duration,
extra_rocks, start_school, perception_change_predator, perception_change_herring,
alignment_distance, cohesion_distance, separation_distance, boids_influence)

In the default function, the rocks get a random position, and connect_rocks is set to
true. Because start_school is also set to True, the herring get different positions
close to each other to form a school. The barracudas get a random position that is not
within the barracuda's perception with a herring. This is done so the full attack can be
studied. The simulation is run for a specified number of seconds. In de default function
the perception length of the herring and predator do not change because perception_change
_predator and perception_change_herring are set to False. Every boid rule has the
same amount of influence.

Specifications in model (finetuning)  
When the 'start_school' parameter is set to False, herring will not be placed in a school
but rather randomly. For longer simulation durations, the perception length of barracuda
can dynamically change over time using the 'perception_change' parameter. Additionally,
the alignment distance, cohesion distance, and separation distance can be modified
to assess their respective influences. This is done to investigate whether these rule
adjustments have an impact on the killing rate of herring. It is also possible to change
the boids_influence parameter to make the influence of one rule bigger.

Returns model  
In the default function, the model returns a dictionary that always contains the number
of killed herring and the number of times herring came within the separation distance
of 6. If 'perception_change_herring' is set to True it also returns a list with the
perception length of the herring and with the killed herring count at every time point.
If 'perception_change_predator' is set to True it also returns a list with the perception
length of the predator and with the killed herring count at every time point.

FIXED PARAMETERS  
* HERRING_SIZE (float) = the radius of the circle representing herring in the simulation.
                      - Set to 3
* HERRING_SPEED (float) = the average speed of a herring.
                      - Set to 1.24 (SD = 0.05)
* HERRING_SPEED_MAX (float) = the maximum speed of a herring.
                      - Set to 18.44
* PERCEPTION_LENGHT_HERRING (float) = the length a herring can sense.
                      - Set to 32
* KILL_DISTANCE (float) = the distance between the herring and the predator that the
                        predator will kill the herring.
                      - Set to 3.6
* PREDATOR_SIZE (float) = radius of the circle representing a herring in the simulation.
                      - Set to 4
* PREDATOR_SPEED (float) = the normal average speed of a barracuda.
                      - Set to 3.6 (SD = 0.8)
* PREDATOR_SPEED_MAX (float) = the highest speed a barracuda can have.
                      - Set to 24.4
* PERCEPTION_LENGHT_PREDATOR (float)= the length a barracuda can sense.
                      - Set to 100
* ROCK_LENGHT (float) = the length of the square representing a rock in the simulation.
                      - Set to 10
* ROCK_AVOIDANCE_DIST (float) = the distance at which both creatures will start sensing
                              rocks they want to avoid.
                      - Set to 16

CHANGEABLE PARAMETERS  
* herring_nr (int) = initial number of herring added to the simulation.
* predator_nr (int) = initial number of predators added to the simulation.
* rock_nr (int) = initial number of rocks added to the simulation.
* simulation_duration (int) = duration of a simulation is seconds.
* extra_rocks (bool) = added rocks for the clustering/connecting of rocks.
* start_school (bool) = herring start as one school instead of randomly.
* perception_change_predator (bool) = change of the barracuda perception length over time.
* perception_change_herring (bool) = change of the herring perception length over time.
* SEPARATION_DISTANCE (float) = if another herring is within this distance, it will be
                          included in the separation rule.
* ALIGNMENT_DISTANCE (float) = if another herring is within this distance, it will be
                          included in the alignment rule.
* COHESION_DISTANCE (float) = if another herring is within this distance, it will be
                          included in the cohesion rule.
* boids_influence (int) = Indicates the influence of boids rules. 1 = all rules equal
                          important, 1 separation more important, 2 alignment more important
                          and 3 cohesion more important.

HOW TO RUN:  
Command to simulate the model with these values:
Experiment(herring_nr = 100, predator_nr = 3, rock_nr = 30, simulation_duration = 20,
      extra_rocks = False, start_school = True, perception_change_predator = False,
      perception_change_herring = False, alignment_distance = 32, cohesion_distance = 32,
      separation_distance = 6, boids_influence = 0)

- python gamefish.py


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
                  different numbers of predators with and without rocks.
                  - ####HOW TO RUN###

* Change_rock_nr_plot: Line plot of the average killed herring + 1 SD error bars in
                  environments with different numbers of rocks.
                  - ####HOW TO RUN###

* Density_Killing_combination_plot:  oxplots with strip plots overlap that show the
                  distribution of the herring count within the original separation distance
                  of 6 (left) and the herring killing count (right) across various conditions.
                  - ####HOW TO RUN###

* School_size_plot: Boxplot with strip plot overlap that shows the proportion of killed
                  herring in large and small schools, with and without rocks.
                  - ####HOW TO RUN###

* Boids_rules_influence_plot: Boxplot with strip plot overlap that shows the number of killed
                  herring when different boid rules are emphasised
                  - ####HOW TO RUN###

* Boid_rules_sensitivity_analysis_plot: Boxplots with strip plots overlap that show the
                  distribution of the herring count within the original separation distance
                  of 6 (left) and the herring killing count (right) across various conditions.
                  - ####HOW TO RUN###

- python visualisation.py.


THE STATISTICAL TESTS  
Statistic_tests.py contains the code to do the statistical test on the data obtained
in visualisation.py.

It contains 4 statistical tests:
- Test to determine if school size significantly changes the killing proportion.
- Test to determine if environmental changes significantly influence the school density.
- Test to determine if environmental changes significantly influence the killing rate.
- Test to determine if the different boid rules significantly influence the killing rate.

This cannot be run separately because it needs the data collected in visualisation.py.

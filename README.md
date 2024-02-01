THE MODEL:   
A systematic approach to determine the influence of environmental and behavioural changes
 on the schooling of herring and protection behaviour through 2D Agent-based modelling

Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279, 15159337, 13717405

The link to the GitHub containing the code is https://github.com/suus-stack/PCS

PYTHON AND LIBRARY VESIONS  
Python version 3.11.4 is used.

* numpy (version 1.26.0)
    - install: pip install numpy==1.26.0
* pygame (version 2.5.2)
    - install: pip install pygame==2.5.2
* pandas (version 2.1.3)
    - install: pip install pandas==2.1.3
* scipy (version 1.11.4)
    - install: pip install scipy==1.11.4
* seabron (version 0.13.0)
    - install: pip install seaborn==0.13.0

>> For a more elaborate explanation of the code and parameters check out the elaborated_readme file here:
>> https://github.com/suus-stack/PCS/blob/main/ELABORATED_README.md

THE CODE: herring_simulation.py  
It contains the code to run an 2-dimensional agent-based model in which the herring,
rocks and predators are represented as agents with their own positions and velocities.

OUTPUT: returns a dictionary with the number of killed herring and number of times
herring came to close with eachother.

HOW TO RUN DEFAULT  :
    - python3 herring_simulation.py


CODE VISUALISATION: visualization.py  
It contains the code to make plots that show the influence of environmental changes
on the killing rate and school density. It uses the herring_simulation.py code to
run an simulation.

HOW TO RUN
- python3 visualisation.py.


STATISTICAL TESTS: statistical_test.py  
It contains the code to do the statistical test on the data obtained in visualisation.py.
It cannot be run separately.


INCOMPLETE MODEL: vectorized implementation      
boids.py contains code to run an agent-based simulation of herring schools and
possibly rocks and/or predators.

HOW TO RUN
- python3 boids.py.

Authors:      Suze Frikkee, Luca Pouw, Eva Nieuwenhuis
University:   UvA
Course:       Project computational science
Student id's: 14773279 , 15159337, 13717405

Description: Agent-based model to simulate herring school movement dynamics. The
plain movement of a herring is based on three rules:
- Separation: Herring do not get closer than some minimum distance
- Alignment: Herring heads in the direction of the neighbours within close distance.
- Cohesion: Herring moves to the position of the neighbours within close distance.

It is possible to introduce rocks and predators in the experiment, which both
influence the movement of the herring. The herring will always move away from the
predator and will also accelerate its speed when a predator is near. The predator on the other hand
will always move towards the herring and also accelartes its speed when near herring. 
Both herring and predators cannot move through a rock and has to go around or move away from it. 
A small value around 1 standard deviation from the average is added to the current speed to create variation. 

In the default function rocks, herring and predators are initialized randomly. 
These initial locations cannot be overlapping in any way, within perception distance.  
Adding to this, the predator is placed outside of the perception range of the herring, so that
the full attack can be studied.
Furthermore, it is possible to connect nearby rocks to create larger structures by introducing more rocks 
and we can also initialize the herring in one large school. The alignment distance, cohesion distance and separation
distance can also be change in order to determine their influence.

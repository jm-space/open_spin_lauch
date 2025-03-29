![](design/logos/open_spin_launch_logo_text_black.png)

------------------------------------------------

## Mission Profile

- A spin launch system should be devised that will be used as the launch platform for many of our future projects. Probable missions that could be conducted with this launch platform could include: (i) deploy and propulsive landing, (ii) deploy and in-flight stage ignition, and (iii) deploy to UAV flight transition.
- The system's main objective is to support the goal of a propulsive landing (i) by accurately deploying it to a target altitude. 

## Spin Launcher

- Maximum achievable altitude: 150 m (theoretical altitude - drag not included)
- Maximum radius: 2 m
- Maximum rocket weight: 2 kg
- Spin up mechanism: 
the contraption should be built in a way so that it can either be spun up  (i) manually with human power through cycling or (ii) with the help of an asynchronous electric motor. 
For human cycling power, a maximum of 800 W is assumed for a maximum duration of 30 s.
- Spin-up retrofit: initially method (i) will be installed. However, method (ii) should be easily installable without any changes. In addition, a clutch should allow for seamless switching between the two modes. 
- Release mechanism: (i) must be able to release two attachment points at specific times, (ii) the release mechanism must be able to deploy the vehicle with a directional accuracy of 1°, which results in a landing zone deviation of +-10 m when launched to the absolute maximum altitude of 150 m with target direction 3°. (iii) The timing accuracy of the differential release mechanism must be high enough, such that if a remaining rotation is induced by the inaccuracy of the differential release, the fins are able to keep the altitude loss and trajectory deviation sufficiently small. 
- Counterweight: instead of utilizing a counterweight, a second (decoy) rocket should be attached that will be released in the same launch direction with a time offset of half a rotation. The axle should be able to withstand the half-rotation induced imbalance. 
- Frame structure: will be made of rectangular steel tubes that will be connected by welding.
- Movability: the contraption should be built on a movable platform for easy commuting. In addition, the platform could be powered by the integrated cycle.  
- Modularity: the individual components of the spin launcher should be split into modules to allow for easy replacements and upgrades. In addition, the entire spin launch system should be able to be retrofitted into a bus without much additional effort. 
- Video coverage: a camera should be installed in the spin launcher's arm so that it can capture the differential release of the vehicle. 

## Rocket

Requirements and expected feature changes:

- Structural integrity: the rocket must be able to withstand the highest occurring launch g-forces. 
- Attachment points: the rocket should integrate two attachment points with which it can be connected to the spin launcher. Those attachment points should be high-strength, durable, and should allow for rapid reuse. 
- Fins and COG: the rocket will have the landing engines and most of its weight in its front and fins in its rear, which allow for a passively stabilized launch. After reaching apogee, the rocket will flip into its stable descent orientation, with its fins being on top and the engine pointing downwards. 
- Thrust vector control: (i) the new TVC system should use off-the shelf gears for higher precision. (ii) it should utilize KST servos for faster actuation speeds and higher accuracy. (iii) and it should be available in two configurations - one for our self-developed solid rocket engines and one for a set of up to five Klima Raketenmodellbau engines. (iv) a life thrust measuring system should be incorporated into the new TVC system. 
- Solid rocket engines: over the course of this vehicle's development several types of engines should be devised: (i) a long-burning engine primarily used for landing maneuvers (ii) a high thrust engine for in-flight ignition, and (iii) a long burn time medium thrust version for rocket powered UAV flight.  
- Throttle mechanism: some mechanism should be devise that allows for sufficient throttle control to increase the likelihood of a successful landing. 
- GNSS receiver: for position and velocity determination a RTK GNSS receiver should be incorporated. 
- Video coverage: two cameras should be installed in the vehicle - one that is directed towards the TVC system and one that is filming the vehicle's exterior. 

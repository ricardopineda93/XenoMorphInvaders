# XenoMorphInvaders
A reimagined take on the classic Space Invaders side scroller utilizing Pygame as the engine behind the game and some creative display liberties. 

Several notes are written within the .py files themselves for clarity. 


Basic gameplay concepts, R+L keyboard arrows for right of left movement, space bar to shoot. Rather self explanitory on-screen presentation, rocket ship on bottom of screen is player controlled, enemy fleet of 8-bit Xenomorphs above move side to side and downwards towards player ship. Shoot to win, or be destoryed!


Game uses several classes and methods to initalize and render everything from the screen to the scoreboard, the aliens, player ship, bullets, etc. Bullets, ship, and aliens created as pygame sprites and managed as sprite Groups, initialized with specific .rect properties to be rendered and behave on screen as 'real' objects.

In order to keep memory usage and perfomance at optimal levels, each bullet fired is deleted as soon as it's object location passes the defined screen dimensions such that it is not shooting upwards into forever and continuing to use resources.



Game has several functionalities/features:

- Can be started on startup either clicking the button or pressing 'P' on keyboard, restarted anytime on the fly using keyboard buttons 'R', and quit using 'Q'.
- Dynamically keeps track of current player's score, as well as the level they are on.
- Keeps track of highest score on record and capable of overwritting new high score. High score displayed on screen.
- Dynamic difficulty: speed of alien fleet increases with each successful destruction of entire fleet array. Each alien's point value when destroyed also increments to a higher value with each succesful destruction of a fleet, i.e. the next level.
- Is capable of calculating accuracy based on shots fired vs. collision detections of bullets with aliens but will only register a shot as "missed" once the bullet is no longer in the frame of the game. However, this is still seemingly buggy when registering large clusters of bullets.
- Renders images of rocket ships to represent 'lives' on screen, which decrease by one each time a collision between the player's ship and alien ship is detected. 

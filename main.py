"""
    Progressive game development by implementation steps:
    ===================================
    * Introduction:
    ----------------
        The aim is to develop a very simple game where the majority of the
    panda3d game engine is implemented.
        A character has to reach a goal and avoid being killed by creatures. In
    order to have it done, the following features have to be put into play:
        1) mesh loading.
        2) lighting.
        3) materials and texturing.
        4) actor loading.
        5) animation (including partial).
        6) collision detection.
        7) physics.
        8) finite state machine.
        9) artificial intelligence.
        10) fog.
        11) particle system.
        12) user interface.
    * Game:
    ---------
        -Grid unit (GU)=1/7 character height=7 blender units.
        -Scenario: uneven terrain with slopes, water, objects (static, grabbable,
    breakable, throwable, climbable and moveable). Size: 256x256GU.
        -Character: human. Has to perform the following actions: idle, walk, run,
    jump (idle, walk or step, and long during run), climb (slope, ledge), grab
    (floor, height), lift, hit (punch, kick, object), throw, rotate (idle), swim,
    suffer, fall, drop (like dead?), eat, drink (ducked).
        -Props: still and animated.
        -AI creatures: dogs. Have to perform the following actions: idle, wander,
    run, attack.
        -Sounds?
"""

from game import Game

g=Game()
g.run()

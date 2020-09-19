from src import Props as props
import numpy as np


def AddProps(system):
    props.MIT_door(system, [-5, 3.3, 8.22])

    props.MIT_door(system, [12.56, 3.3, 1.5], 90)
    props.MIT_door(system, [12.56, 3.3, -8.5], 90)
    
    props.MIT_door(system, [12.56, 6.6, 3.5], 90)
    props.MIT_door(system, [12.56, 6.6, -8.5], 90)

    props.MIT_door(system, [7.25, 6.6, 12.1])

    props.painting(system, [12.5,2.0,-4], 'DemoBengan.png', np.pi/2)
    props.painting(system, [12.53,1.8,-5.35], 'bungeebengan_notes.png', np.pi/2, [0.2,0.27])
    props.painting(system, [-6,2.1,5], 'walkplanck.png', 0, [0.8,0.6])
    props.pokeball(system, [-0.35,0.85,-9.35], 0)
    props.sodacan(system, [-0.85,0.85,-9.35], 'schrodbull.png', 180)
    props.coin(system, [-0.25,0.85,-9.65])

    # In the staircase
    # props.pokeball(system, [7.35,4.85,2.5], 0)
    # props.pokeball(system, [7.355,5.05,2.55], 0)

    # On the dartboard
    props.pokeball(system, [1.95,1.501,-3.4], -45)
    props.sodacan(system, [2.02,1.501,-3.5], 'schrodbull.png')
    props.sodacan(system, [1.7,1.501,-3.3], 'joultcola.png')

    # props.dino(system, [5.75,0.85,-9.75], 210, .15)

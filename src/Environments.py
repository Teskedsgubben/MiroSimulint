from MiroClasses import MiroEnvironment as ME

from src import MIT_building as MIT
from src import Props as props

# MIT Environment
MIT_place = ME.MiroEnvironment()

MIT_place.Set_Initializer(MIT.build_MIT)

MIT_place.Set_Target([2, 2.1, -3], props.dartboard)

MIT_place.Add_Camview({
            'default': {
                'pos': [-7.5, 4, -1],
                'dir': [1,0,0],
                'lah': 10
            },
            '3rd floor staircase': {
                'pos': [2, 6, 7],
                'dir': [0.2,-0.2,-1],
                'lah': 0.05
            },
            '4th floor behind lander': {
                'pos': [12,10.25,-2],
                'dir': [-1,-0.4,0.1],
                'lah': 0.05
            },
            '2nd (ground) floor front view': {
                'pos': [-4,1.8,-2.5],
                'dir': [1,0.1,0.05],
                'lah': 0.05
            },
            '2nd (ground) floor side view': {
                'pos': [-0.5,1.25,-10.15],
                'dir': [0.25,0.3,1],
                'lah': 0.05
            },
            'maccans': {
                'pos': [1,15,-1.15],
                'dir': [0,-1,0],
                'lah': 0.05
            },
            '4th floor observing launcher': {
                'pos': [10.5,9.5,0.75],
                'dir': [-0.2,-0.1,-1],
                'lah': 2.75
            }
        })


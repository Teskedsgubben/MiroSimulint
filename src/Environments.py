from MiroClasses import MiroEnvironment as ME
from MiroClasses import MiroNotifier as MN

from src import MIT_building as MIT
from src import Props as props

# MIT Environment
MIT_place = ME.MiroEnvironment()

MIT_place.Set_Target([2, 1.5, -3], props.dartboard)

MIT_place.Set_Initializer(MIT.build_MIT)

MIT_place.Set_Notifier(MN.MiroNotifier([13.45, 8.5, 1], 84.125, 0))

MIT_place.Add_Lightsource([  5, 25,  20], [3, 0, -5], 100, 15, 40, 40, False)
MIT_place.Add_Lightsource([-20,  1,   0], [0, 2,  0],  24,  7, 40, 70, False)
MIT_place.Add_Lightsource([  0,  1, -20], [0, 2,  0],  24,  7, 40, 70, False)
MIT_place.Add_Lightsource([ 10,  2,  -9], [9, 3,  4],  24,  15, 40, 50, False)

MIT_place.Add_Camview({
            'default': {
                'pos': [-4.5, 4, -0.5],
                'dir': [1,0,0],
                'lah': 8
            },
            '3rd floor staircase': {
                'pos': [2, 4.9, 7],
                'dir': [0.2,-0.2,-1],
                'lah': 0.05
            },
            '4th floor behind lander': {
                'pos': [12,9,-2],
                'dir': [-1,-0.1,0.1],
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
            '4th floor observing launcher': {
                'pos': [10.5,8.3,-4.5],
                'dir': [-0.2,-0.2, 1],
                'lah': 2.5
            },
            'testpos': {
                'pos': [4.25,1.35,-9.45],
                'dir': [1,0,0],
                'lah': 1
            }
        })


from MiroClasses import MiroAPI_chrono as MiroAPI

def build(MiroSystem, SPEEDMODE = False):
    H = 3.32
    wall_t = 0.1 * 2
    topWall_pos = [0.6, 5/2*H, 5.1]
    if(SPEEDMODE):        
        MiroAPI.add_boxShape(MiroSystem, 11.8, H, wall_t, topWall_pos, 'MITwall_West.jpg')
    else:
        MiroAPI.add_boxShape(MiroSystem, 11.8, H, wall_t, topWall_pos, 'MITwall_West.jpg')
        MiroAPI.add_boxShape(MiroSystem, 1, 1, 1, topWall_pos)
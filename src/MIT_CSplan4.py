from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np

def build(MiroSystem, SPEEDMODE = False):
    H = 3.32
    wall_t = 0.1 * 2
    posW = np.array([0.6, 5/2*H, 5.1])
    posE = np.array([1.6, 3/2*H, -8.9])
    posS = np.array([-5.4, 3/2*H, -1.9]) #3/2 * H

    if(not SPEEDMODE):        
        MiroAPI.add_boxShape(MiroSystem, 11.8, H, wall_t, posW, 'MITwall_West.jpg')
        MiroAPI.add_boxShape(MiroSystem, 2*6.9, 3*H, wall_t, posE, 'textures/MITwall_East.jpg', [-4,-3])
        MiroAPI.add_boxShape(MiroSystem, wall_t, 3*H, 2*6.9, posS, 'textures/MITwall_South.jpg', [4,3])


    else:

        corner_windowpane0 = np.array([-5.29, 2*H+1.5, 4.99])
        first_windowpane0 = np.array([corner_windowpane0[0]+0.10, corner_windowpane0[1], corner_windowpane0[2]])
        corner_windowpane1 = np.array([-0.7, 2*H+1.5, 4.99])
        first_windowpane1 = np.array([corner_windowpane1[0]+0.25, corner_windowpane1[1], corner_windowpane1[2]])
        corner_windowpane2 = np.array([4.125, 2*H+1.5, 4.99])
        first_windowpane2 = np.array([corner_windowpane2[0]+0.25, corner_windowpane2[1], corner_windowpane2[2]])


        v_windowpane_size = np.array([0.05, 3, 0.01])  #vertical window pane size
        
        pos_down = np.array([posW[0], posW[1] - 1.26, posW[2]])
        pos_up = np.array([posW[0], posW[1] + 1.16, posW[2]])

        #concrete part under and over windows
        MiroAPI.add_boxShape(MiroSystem, 11.8, 0.8, 0.2, pos_down, texture='white concrete.jpg', scale=[9, 12])
        MiroAPI.add_boxShape(MiroSystem, 11.8, 1, 0.2, pos_up, texture='white concrete.jpg', scale=[9, 12])
        #1st window vertical
        MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], corner_windowpane0, texture='wood_ikea_style.png')
        
        spacingA = 0.61
        for k in range(0, 8):
            tmp = np.array([spacingA * k, 0, 0])
            MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], tmp + first_windowpane0, texture='wood_ikea_style.png')
            if k == 3:
                MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2],  np.array([spacingA/2, 0, 0]) + tmp + first_windowpane0, texture='wood_ikea_style.png')
        

        #2nd window vertical
        MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], corner_windowpane1, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], first_windowpane1, texture='wood_ikea_style.png')

        spacingB = 0.685
        for k in range(0, 7):
            tmp = np.array([spacingB * k, 0, 0])
            MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], tmp + first_windowpane1, texture='wood_ikea_style.png')

            if k == 1:
                MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2],np.array([spacingB/2, 0, 0]) + tmp + first_windowpane1, texture='wood_ikea_style.png')

            if k == 4:
                MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2],np.array([spacingB/2, 0, 0]) + tmp + first_windowpane1, texture='wood_ikea_style.png')

            if k == 6:
                MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], np.array([0.25, 0, 0]) + tmp + first_windowpane1, texture='wood_ikea_style.png')
        
        #3rd window vertical
        MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], corner_windowpane2, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], first_windowpane2, texture='wood_ikea_style.png')

        spacingC = 0.685
        for k in range(0, 4):
            tmp = np.array([spacingC * k, 0, 0])
            MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], tmp + first_windowpane2, texture='wood_ikea_style.png')
            if k == 2:
                MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2],  np.array([spacingC/2, 0, 0]) + tmp + first_windowpane2, texture='wood_ikea_style.png')
        

        #horizontal windowpanes
        h_windowpane_size = np.array([0.05, 4.25, 0.01])     #horizontal window pane size

        #2nd window horizontal
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]+0.6, h_windowpane_size[2], [1.51, 2*H+0.015, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]+0.6, h_windowpane_size[2], [1.51, 2*H+0.8, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]+0.6, h_windowpane_size[2], [1.51, pos_up[1] - 0.5, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]+0.6, h_windowpane_size[2], [1.51, 2*H+3, 4.98], rotZ=90, texture='wood_ikea_style.png')
        #1st window horizontal
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]+0.36, h_windowpane_size[2], [-3, 2*H+0.015, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]+0.36, h_windowpane_size[2], [-3, 2*H+0.8, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]+0.36, h_windowpane_size[2], [-3, pos_up[1] - 0.5, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]+0.36, h_windowpane_size[2], [-3, 2*H+3, 4.98], rotZ=90, texture='wood_ikea_style.png')
        #3rd window horizontal
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]/2+0.3, h_windowpane_size[2], [5.25, 2*H+0.015, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]/2+0.3, h_windowpane_size[2], [5.25, 2*H+0.8, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]/2+0.3, h_windowpane_size[2], [5.25, pos_up[1] - 0.5, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]/2+0.3, h_windowpane_size[2], [5.25, 2*H+3, 4.98], rotZ=90, texture='wood_ikea_style.png')

        test_posS = np.array([posS[0]+0.1, -0.16, posS[2]])        
        test_posE = np.array([posE[0], -0.16, posE[2]])

        make_window(v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], h_windowpane_size[0],
        h_windowpane_size[1], h_windowpane_size[2], test_posS, 'south', 0.685, MiroSystem)
        
        make_window(v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], h_windowpane_size[0],
        h_windowpane_size[1], h_windowpane_size[2], test_posE, 'east', 0.685, MiroSystem)

def make_window(size_vx, size_vy, size_vz, size_hx, size_hy, size_hz, mid_pos, wall, spacing, MiroSystem): #size_hx, size_hy, size_hz
    #wall sets orientation of window, set wall = 'south' or 'east'
    # pos sets position 
    #and spacing sets the spacing between windowpanes
    H = 3.32
    W = 4.6
    dists = np.array([97,207,358,436,510,654,802,876,951,1102,1213])
    dists = dists - (dists[-1] + dists[0])/2    
    dists = dists / dists[-1] * (W-3*0.16)/2
    test = 0.085

    if wall == 'south':
        for i in range(1, 6, 2):
            lvl_height = np.array([0, i/2*H, 0])
            for j in [-1, 0, 1]:
                lvl_width = np.array([0, 0, j*W])
                for k in range(0, len(dists)):
                    tmp = np.array([0, 0, dists[k]])
                    result_pos = mid_pos + lvl_width + lvl_height + tmp
                    MiroAPI.add_boxShape(MiroSystem, size_vx, size_vy, size_vz, result_pos, rotY=90,texture='wood_ikea_style.png')
                for n in [-1, 1]:
                    hzt_pos = np.array([0.02, 3/2, 0])
                    r_hzt_pos = mid_pos + n*hzt_pos + lvl_height + lvl_width
                    MiroAPI.add_boxShape(MiroSystem, size_hx, size_hy-test, size_hz, r_hzt_pos, rotX=90,rotZ=90,texture='wood_ikea_style.png')
                    if n == -1:
                        MiroAPI.add_boxShape(MiroSystem, size_hx, size_hy-test, size_hz, r_hzt_pos+np.array([0,0.8*n*(-1),0]) ,rotX=90,rotZ=90,texture='wood_ikea_style.png')
                    else:
                        MiroAPI.add_boxShape(MiroSystem, size_hx, size_hy-test, size_hz, r_hzt_pos+np.array([0,0.7*n*(-1),0]) ,rotX=90,rotZ=90,texture='wood_ikea_style.png')
    if wall == 'east':
        for i in range(1, 6, 2):
            lvl_height = np.array([0, i/2*H, 0])
            for j in [-1, 0, 1]:
                lvl_width = np.array([j*W, 0, 0])
                for k in range(0, len(dists)):
                    tmp = np.array([dists[k], 0, 0])
                    result_pos = mid_pos + lvl_width + lvl_height + tmp
                    MiroAPI.add_boxShape(MiroSystem, size_vz,  size_vy, size_vx, result_pos, rotY=90,texture='wood_ikea_style.png')
                for n in [-1, 1]:
                    hzt_pos = np.array([0, 3/2, 0.02])
                    r_hzt_pos = mid_pos + n*hzt_pos + lvl_height + lvl_width
                    MiroAPI.add_boxShape(MiroSystem, size_hx, size_hy-test, size_hz, r_hzt_pos, rotZ=90,texture='wood_ikea_style.png')
                    if n == -1:
                        MiroAPI.add_boxShape(MiroSystem, size_hx, size_hy-test, size_hz, r_hzt_pos+np.array([0,0.8*n*(-1),0]), rotZ=90,texture='wood_ikea_style.png')
                    else:
                        MiroAPI.add_boxShape(MiroSystem, size_hx, size_hy-test, size_hz, r_hzt_pos+np.array([0,0.7*n*(-1),0]), rotZ=90,texture='wood_ikea_style.png')

                     

    
    


#lägst 1/2 * H
#mitt 3/2 * H
#högst 5/2 * H
#W = 4.6

#13.8

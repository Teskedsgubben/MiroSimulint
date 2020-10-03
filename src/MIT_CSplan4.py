from MiroClasses import MiroAPI_chrono as MiroAPI
import pychrono.core as chrono

def build(MiroSystem, SPEEDMODE = False):
    H = 3.32
    wall_t = 0.1 * 2
    topWall_pos = [0.6, 5/2*H, 5.1]
    if(SPEEDMODE):        
        MiroAPI.add_boxShape(MiroSystem, 11.8, H, wall_t, topWall_pos, 'MITwall_West.jpg')
    else:
        corner_windowpane0 = [-5.29, 2*H+1.5, 4.99]
        first_windowpane0 = chrono.ChVectorD(corner_windowpane0[0]+0.10, corner_windowpane0[1], corner_windowpane0[2])
        corner_windowpane1 = [-0.7, 2*H+1.5, 4.99]
        first_windowpane1 = chrono.ChVectorD(corner_windowpane1[0]+0.25, corner_windowpane1[1], corner_windowpane1[2])
        corner_windowpane2 = [4.125, 2*H+1.5, 4.99]
        first_windowpane2 = chrono.ChVectorD(corner_windowpane2[0]+0.25, corner_windowpane2[1], corner_windowpane2[2])


        v_windowpane_size = [0.05, 3, 0.01]  #vertical window pane size
        
        pos_down = [topWall_pos[0], topWall_pos[1] - 1.26, topWall_pos[2]]
        pos_up = [topWall_pos[0], topWall_pos[1] + 1.16, topWall_pos[2]]

        #concrete part under and over windows
        MiroAPI.add_boxShape(MiroSystem, 11.8, 0.8, 0.2, pos_down, texture='white concrete.jpg', scale=[9, 12])
        MiroAPI.add_boxShape(MiroSystem, 11.8, 1, 0.2, pos_up, texture='white concrete.jpg', scale=[9, 12])
        #1st window vertical
        MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], corner_windowpane0, texture='wood_ikea_style.png')
        
        spacingA = 0.61
        for k in range(0, 8):
            tmp = chrono.ChVectorD(spacingA * k, 0, 0)
            MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], tmp + first_windowpane0, texture='wood_ikea_style.png')
            if k == 3:
                MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2],  chrono.ChVectorD(spacingA/2, 0, 0) + tmp + first_windowpane0, texture='wood_ikea_style.png')
        

        #2nd window vertical
        MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], corner_windowpane1, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], first_windowpane1, texture='wood_ikea_style.png')

        spacingB = 0.685
        for k in range(0, 7):
            tmp = chrono.ChVectorD(spacingB * k, 0, 0)
            MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], tmp + first_windowpane1, texture='wood_ikea_style.png')

            if k == 1:
                MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2],chrono.ChVectorD(spacingB/2, 0, 0) + tmp + first_windowpane1, texture='wood_ikea_style.png')

            if k == 4:
                MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2],chrono.ChVectorD(spacingB/2, 0, 0) + tmp + first_windowpane1, texture='wood_ikea_style.png')

            if k == 6:
                MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], chrono.ChVectorD(+0.25, 0, 0) + tmp + first_windowpane1, texture='wood_ikea_style.png')
        
        #3rd window vertical
        MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], corner_windowpane2, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], first_windowpane2, texture='wood_ikea_style.png')

        spacingC = 0.685
        for k in range(0, 4):
            tmp = chrono.ChVectorD(spacingC * k, 0, 0)
            MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2], tmp + first_windowpane2, texture='wood_ikea_style.png')
            if k == 2:
                MiroAPI.add_boxShape(MiroSystem, v_windowpane_size[0], v_windowpane_size[1], v_windowpane_size[2],  chrono.ChVectorD(spacingC/2, 0, 0) + tmp + first_windowpane2, texture='wood_ikea_style.png')
        

        #horizontal windowpanes
        h_windowpane_size = [0.05, 4.8, 0.01]     #horizontal window pane size

        #2nd window horizontal
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1], h_windowpane_size[2], [1.51, 2*H+0.015, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1], h_windowpane_size[2], [1.51, 2*H+0.8, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1], h_windowpane_size[2], [1.51, pos_up[1] - 0.5, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1], h_windowpane_size[2], [1.51, 2*H+3, 4.98], rotZ=90, texture='wood_ikea_style.png')
        #1st window horizontal
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1], h_windowpane_size[2], [-3, 2*H+0.015, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1], h_windowpane_size[2], [-3, 2*H+0.8, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1], h_windowpane_size[2], [-3, pos_up[1] - 0.5, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1], h_windowpane_size[2], [-3, 2*H+3, 4.98], rotZ=90, texture='wood_ikea_style.png')
        #3rd window horizontal
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]/2, h_windowpane_size[2], [5.25, 2*H+0.015, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]/2, h_windowpane_size[2], [5.25, 2*H+0.8, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]/2, h_windowpane_size[2], [5.25, pos_up[1] - 0.5, 4.98], rotZ=90, texture='wood_ikea_style.png')
        MiroAPI.add_boxShape(MiroSystem, h_windowpane_size[0], h_windowpane_size[1]/2, h_windowpane_size[2], [5.25, 2*H+3, 4.98], rotZ=90, texture='wood_ikea_style.png')




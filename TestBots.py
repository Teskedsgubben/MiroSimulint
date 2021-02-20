
from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
from MiroClasses.MiroModule import Module as MiroModule
from MiroClasses import MiroComponent as mc

from src import Components as C
import numpy as np


def MyRobot():

    MyBot = MiroModule('MyBot')

    Chassi = C.MC023()

    Front_Tire_Right = C.MC242()
    Front_Tire_Right.RotateX(90)

    Front_Tire_Left = C.MC242()
    Front_Tire_Left.RotateX(90)

    Rear_Tire_Right = C.MC242()
    Rear_Tire_Right.RotateX(90)

    Rear_Tire_Left = C.MC242()
    Rear_Tire_Left.RotateX(90)

    MyBot.AddComponent(Chassi, 'Chassi')
    MyBot.AddComponent(Front_Tire_Left, 'Front T L')
    MyBot.AddComponent(Front_Tire_Right, 'Front T R')
    MyBot.AddComponent(Rear_Tire_Left, 'Rear T L')
    MyBot.AddComponent(Rear_Tire_Right, 'Rear T R')

    MyBot.ConnectComponents('Chassi', 'I', 'Front T L', 'B', link_name = 'FL_tire', dist = 0.01)
    MyBot.ConnectComponents('Chassi', 'G', 'Front T R', 'A', link_name = 'FR_tire', dist = 0.01)
    MyBot.ConnectComponents('Chassi', 'H', 'Rear T L', 'B', link_name = 'RL_tire', dist = 0.01)
    MyBot.ConnectComponents('Chassi', 'F', 'Rear T R', 'A', link_name = 'RR_tire', dist = 0.01)

    MyBot.EnableMotor('FL_tire')
    MyBot.EnableMotor('FR_tire')

    return MyBot
# MiroSimulint
Simulation library built on PyChrono to build component based modules in a test environment

This lib requires pychrono installed to function

To get this running:

**Step 1)** Install Git:
    >Download Git from: https://git-scm.com/downloads

**Step 2)** Install Anaconda:
    > This is built using anaconda version 2019.10
    Download the installer for this version from:
    https://repo.anaconda.com/archive/
    
    >Run the installer, using the "Just for me" option.

**Step 3)** Install PyChrono and MiroSimulint:
    >Run Anaconda Prompt from the start menu or the 
    Anaconda Navigator page. Type the following commands

    >a) Download the MiroSimulint code by:

        >>git clone "link to this repo"

    >b) Create an environment and install PyChrono by:

        >>conda create -n MiroSim python=3.7 numpy pylint

        >>conda install -n MiroSim -c projectchrono pychrono
    
    >c) Optional. You should be able to run the program now. If you are familiar with code editing, you can just use this if you prefer. If you are new to coding, it is recommended you complete Step 4) and you do not have to do this part, unless you want to try it!

        >>cd MiroSimulint

        >>conda activate MiroSim

        >>python Main.py

**Step 4)** Install VScode:
    >This is the recommended code editor:
    https://code.visualstudio.com/download

    >For simplicity, mark the options:

        >>[ ] Add ”Open with Code” action to Windows Explorer file context menu

        >>[ ] Add ”Open with Code” action to Windows Explorer directory context menu
    
    >in the "Select Additional Tasks" step.

**Step 5)** Run the program:
    >Navigate to the directory where the repo was cloned.
    There should be a folder called "MiroSimulint" in your default directory.

    >Right click the folder and click "Open with Code"

    >If this option is not available, launch VS code and click File -> Open Folder
    to open the MiroSimulint folder.

    >When VS code is open, click View -> Command Palette... and type "Python: Select Interpreter" and click it. You can then select the ('MiroSim': conda) option. Clicking this will create a file telling VS code to use the MiroSim environment for this project.

    >Then, double click the Main.py file in the explorer menu on your left. When the file is open, click the green "Play Button" on the top right to run the code.

    >When (if) the program starts, press SPACE to release the launcher!

All done. The next time you open, you only need to open the Main-py file and press the Play button to run
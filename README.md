# MiroSimulint
Simulation library built on PyChrono to build component based modules in a test environment

This lib requires pychrono installed to function

To get this running:

1) Install Git and clone the repository:
    Download Git from:
    https://git-scm.com/downloads

    Run Git Bash
    
    type: git clone "link to this repo"

2) Install Anaconda:
    This is built using anaconda version 2019.10
    Download the installer for this version from:
    https://repo.anaconda.com/archive/
    
    Run the installer, using the "Just for me" option.

3) Install PyChrono:
    Run Anaconda Prompt from the start menu or the 
    Anaconda Navigator page.

    To ensure compatibility, start by typing:

    conda create -n MiroSim python=3.7 numpy pylint

    Press ENTER, accept by typing "y". When the process finishes, you can install PyChrono by:

    conda install -n MiroSim -c projectchrono pychrono

4) Install VScode:
    Recommended code editor:
    https://code.visualstudio.com/download

    For simplicity, mark the option:

    [ ] Add ”Open with Code” action to Windows Explorer directory context menu
    
    in the "Select Additional Tasks" step.

5) Run the program:
    Navigate to the directory where the repo was cloned.
    There should be a folder called "MiroSimulint" in your default directory.

    Right click the folder and click "Open with Code"

    If this option is not available, launch VS code and click File -> Open Folder
    to open the MiroSimulint folder.

    When VS code is open, click View -> Command Palette... and type "Python: Select Interpreter" and click it. You can then select the ('MiroSim': conda) option. Clicking this will create a file telling VS code to use the MiroSim environment for this project.

    Then, double click the Main.py file in the explorer menu on your left. When the file is open, click the green "Play Button" on the top right to run the code.

    When (if) the program starts, press SPACE to release the launcher!
# MiroSimulint

This is a simulation library built for creating modular constructions using a highly simplified interface. It supports different APIs and you only need to install support for the one you intend to use.

**AGX Dynamics** API: Physics engine used for real time simulations and interactive controls, such as robots and vehicles. Requires a license file to use.  
**PyChrono** API: Used for simulations without interactive controls, that are made for recording video rather than real time. Free to install and use.

To get MiroSimulint running:
___

## Installing Programs

### Step 1) *Install Git*

Download and install Git from:

> <https://git-scm.com/downloads>

### Step 2) *Download MiroSimulint*

When git is installed, you can clone this repository into a local directory. Open *Git Bash* on your computer, then download the MiroSimulint code by typing:

    git clone https://github.com/Teskedsgubben/MiroSimulint

You can change where to put MiroSimulint by first typing *cd NAMEOFDIRECTORY* which will change the directory git bash is in, and git clone will then put MiroSimulint into that directory.

### Step 3) *Install VS Code*

You need a program to edit your code. If you do not have one you already intend to use, this is the recommended code editor:

> <https://code.visualstudio.com/download>

__On Windows:__ We will need to change default shell in VS Code. To do this, open VS Code and click _View_ $\to$ _Command Pallette_ and type "shell". Select command prompt (cmd) and restart VS Code.

### Step 4a) *Install API: AGX Dynamics*

#### 4a.1) *Install AGX Dynamics*

Open the AGX download page

> <https://www.algoryx.se/download/?id=2079>

Find the download link that matches your system. Using Windows, which platform you install for will not matter for this library, but **make sure** you have the correct bits, most likely x64. If you are unsure, go to Control Panel $\to$ System to see your System type.

__Note:__ When installing in Windows, you will get prompted that Windows is blocking the installer. Click on _More information_ to show the _Run anyway_ button.

#### 4a.2) *Prepare License File*

When installed, you need a license file to place in your install directory. If you do not already have one, contact us. The directory should be:

On Windows: _C:\Program Files\Algoryx\AgX-YOURAGXVERSION_  
On Mac/Unix: _/opt/Algoryx/AgX-YOURAGXVERSION_

#### 4a.3) *Test AGX Viewer*

Open a terminal and navigate to the agx install directory. Then run the setup_env script

__On Windows:__
  
    cd "C:\Program Files\Algoryx\AgX-YOURAGXVERSION"
    setup_env.bat
    agxViewer --version

__On Mac/Unix:__

    cd /opt/Algoryx/AgX-YOURAGXVERSION
    source_env.bash
    agxViewer --version

### Step 4b) *Install API: PyChrono*

#### 4b.1) *Install Anaconda*

Download and install Anaconda from:

> <https://www.anaconda.com/products/individual>

_Note: MiroSimulint was built using the 2019.10 version of Anaconda. If you run into issues, you can try uninstalling your current Anaconda version and installing the older one from:_

> <https://repo.anaconda.com/archive/>

#### 4b.2) *Install PyChrono*

Note: *Skip this section if you do not need to use PyChrono*

Run Anaconda Prompt from the start menu or the Anaconda Navigator page. Type the follow commands:

Create an environment named MiroSim and install PyChrono by:

    conda create -n MiroSim python=3.7 numpy matplotlib pylint ffmpeg

    conda install -n MiroSim -c projectchrono pychrono

_Optional._ You should be able to run the program now. You can try it if you want, but we will do it a different way using VS Code in the next step. If you are familiar with code editing, you can just use this method and edit your files in your own editor, if you prefer.

    cd MiroSimulint

    conda activate MiroSim

    python Main.py

__Linux Users:__

On Linux (and possibly Mac) you need to install irrlicht, run these commands in a terminal window:

    sudo apt-get install libirrlicht1.8 libirrlicht-dev libirrlicht-doc

    sudo apt-get install freeglut3

If you get glibc version error, try checking the version by the command below and compare to your error.

    ldd --version

If your version of glibc (technically ldd, but they should be the same) is older than the error says that the program needs, you probably need to update to the latest LTS version of you distro. On Ubuntu, this is currently version 20.04 and this has been confirmed to work.

### Step 5) *Setup the program with VS Code*

To open the files, start VS Code and click _File -> Open Folder_ to open the *MiroSimulint* folder. This should be at you user directory, such as __C:\\Users\\*MyUsername*\\MiroSimulint__ unless you changed it in step __3a)__, or __C:\\Users\\*MyUsername*\\Documents\\MiroSimulint__.

There is a package needed to get full support for Python commands. When VS Code is open, click _View -> Extensions_, search for Python and install Microsofts Python package.

Once the Python package is installed, click _View -> Command Palette..._ and type _"Python: Select Interpreter"_ and click it.

_Using AGX (Windows):_ Click _Enter interpreter path..._ then click _Find..._ and navigate to the AGX install directory, then open the python folder and select the python.exe inside.

_Using AGX (Mac/Unix):_ If your python3 version (python3 --version) is the same as agxviewer (3.X, last digit may differ) you can create a virtual environment with:

    python3 -m venv MiroSim
    echo "source /opt/Algoryx/AgX-YOURAGXVERSION/setup_env.bash" >> MiroSim/bin/activate

_Using PyChrono:_ You can then select the _('MiroSim': conda)_ option.

Clicking this will create a file telling VS code to use the MiroSim environment for this project, and is only needed once.

### Step 6) *Run the program*

Open VS Code and open the MiroSimulint directory (_File -> Open Folder..._). Open the _Main.py_ file in the explorer menu on your left. When the file is open, click the green "Play Button" on the top right to run the code. If it starts, you're all set to begin coding. Otherwise, contact a supervisor with any error(s) you get.

__IN AGX:__ You must run a setup script in the terminal window before running the code for every new terminal. You should get an import error otherwise. Run the following in the terminal, just below the error:

__On Windows:__ "C:/Program Files/Algoryx/AgX-YOURAGXVERSION/setup_env.bat"
__On Mac/Unix:__ source MiroSim/bin/activate

__IN PYCHRONO:__ Some DirectX issues have been occuring. What happens is that the code runs, but the simulation only produces a black screen. See the folder OS Resources and follow the readme.txt instructions for a quickfix on this.

___

## Using MiroSimulint

### The Program

The file you run is called Main.py and is quite short. Here you create a system, add modules and start the simulation. It is recommended that you copy this file and create your own local copy which you run instead. This way, you can freely modify your local file without running into issues when doing a pull from the repository.

There are example modules in some files to check out, which makes you familiar with the code. Before modifying, it is recommended you create your own local file for this as well. You can either copy the example code and keep what you want, or start completely fresh. To access your local modules in your Main.py file, update the imports at the top to include your file.

### The Camera

Camera controls vary depending on API, but in the Main file you can find a function call Set_Perspective. This function controls where the camera is positioned and how it should behave. This is currently being reworked and may be outdated:

There are two special camera functions you can use as well.

__Follow:__ If you set the perspective to 'follow' and input the name of a module you have added to the system, the camera will follow that module. You can also specify from which direction the camera should view the module. Note that manual controls only work while the simulation is paused when using this.

__Cycle:__ You can add `cycle = True` to the end of the input arguments. This will override manual controls and circle the camera around the observation point. You can also add `cycle_laptime = X` to change the speed of the camera rotation, where `X` is any number you like. This can be used in combination with the follow perspective.

_Note: Laptime means how many simulation time seconds it takes for the camera to complete one revolution, meaning a laptime of 10 will create a video that takes 50 seconds to complete the lap, using the default 60 fps video and 300 fps simulation speed._

Your modules are built as MiroModules using MiroComponents. This means that you add the components you need, rotate them properly and then assemble them into a complete module. The order here is important, as connecting components 1 and 2 will move component 2 so that the connection points match. If you connect first and rotate the object after, things are going to get messy. However, that doesn't mean you shouldn't try it :bowtie:.

### Keeping MiroSimulint up to date

To get the latest updates we push to the repository, it's as simple as a couple clicks to always get the latest version. Go to _View_ -> _SCM_ or _Source Control_ click the three dots button ... and click Pull. This will get the latest versions of the files from the repository.

This requires that you have not modified the original files, and only work in local files. If this is not the case, follow these simple steps to reset, but keep your files intact.

Step 1) Rename the files you will or have worked with by adding the suffix "_local" to their names, e.g. Main_local.py and GroupLogo_local.png and so on. This will make git ignore the files.

Step 2) , which is the same as clicking the "fork" or "graph" symbol on your left side panel. Here, discard all changes in the list by hovering over the file name and clicking the "reverse" style arrow. This should reset the original file.

You then work in the files named _local instead of the ordinary files. After doing this once, you can always just pull directly to get the latest version again.

___

## OUTDATED

The following sections are outdated, but remain just in case. If you are having trouble, your can give these a look. Most of this is mentioned above, and the MiroAPI is now using AGX by default.

## Using AGX

MiroSimulint was built using PyChrono. It is currently being built to support AGX as well, allowing for other functionalities. To use MiroSim with AGX, you must first have a validated AGX installation on your computer. This means you download the AGX installer and place a provided license file in the install directory. See separate instructions for details.

To set MiroSimulint to use AGX you need to follow these steps:

Step 1) Locate the _MiroAPI\_selector.py_ file in the MiroClasses directory.

Step 2) Copy and paste the file into the same directory.

Step 3) Rename the copy: _MiroAPI\_local.py_

Step 4) Edit the local API file by removing the first if statement, lines 16 through 20. Then remove the indentation on the rows below (mark them then Shift+Tab).

Step 5) Change the API = 'PyChrono' to API = 'AGX'

You now have a local file selecting the API MiroSim will use. To change it back in the future, you only need to redo Step 5) in reverse and so on. However, you must select a python interpreter that is configured for AGX as well. Unless you knowingly configured it to be the same, you will most likely need to switch. This has to be done again if you decide to change API in the future as well.

Step 6) Go to _View_ -> _Command Palette_ and locate Python: Select Interpreter. The Python you want to run should be located in the AGX install directory, i.e. the .../Algoryx/AGX-YOURAGXVERSION directory. If you do not see the right one in the list, click _Enter interpreter path..._ and click _Find..._ so you can navigate to _C:\Program Files\Algoryx\AGX-YOURAGXVERSION\python-x64_ or similar, and select the _python.exe_ in that directory. You now have the right python selected.

Step 7) To setup the environment for agx, you must run the _setup\_env.bat_ in the terminal you are using. This is done by _"C:\Program Files\Algoryx\AGX-YOURAGXVERSION\setup\_env.bat"_, or if you are using powershell (it says __PS C:\Users...>__ rather than just __C:\Users...>__) you add an & before the path, like _& "C:\Program..."_. This needs to be run every time you start a new terminal for using AGX.

Step 8) You can add some lines to you local settings to make pylint find the agx functions. In VS Code, this is done by opening the local directory .vscode in the MiroSimulint directory. Here, modify (or create) the file _settings.json_ with the follow lines:

    {
        "python.pythonPath": "C:/Program Files/Algoryx/AGX-YOURAGXVERSION/python-x64/python.exe",
        "files.associations": {
            "*.agxPy": "python"
        },
        "python.autoComplete.extraPaths": [
            "C:/Program Files/Algoryx/AGX-YOURAGXVERSION/bin/x64/agxpy"
        ],
    }

Note that if you installed AGX somewhere else, you need to modify the above to the correct install directory.

### On Unix

The Python version in use must be the same as the one agxViewer is installed for. Once AGX is installed, you can navigate to the directory where AGX is installed, being /opt/Algoryx/AgX-YOURAGXVERSION. Here you can run the bash script for setting up the AGX environment by:

    source setup_env.bash

Once the script is sourced, the command agxViewer should be recognized. You can check the version of Python that was used by the command:

    agxViewer --version

The output should end with something like:

    Built with Python version: 3.X.Y

Then check your system Python version with:

    python3 --version

As long as the X in the versions are the same, things should be fine. If not, then you need to make sure to use the correct python version. To do this, you can use this.

You DO NOT have to do this if your python version is correct. Replace the X with the correct version:

    sudo apt install python3.X

Once you know you have the correct python version, these commands need to run as well. Replace the X with the right version:

    sudo apt install libglu1
    sudo apt install python3-dev
    sudo apt install python3-pip
    sudo apt install python3.X-venv

Now that the Python packages are in place, run this to get MiroSimulint. Navigate to the directory you want to put MiroSimulint in first, maybe with just "cd" to get to your $HOME directory:

    git clone https://github.com/Teskedsgubben/MiroSimulint
    cd MiroSimulint

From the MiroSimulint folder, setup a virtual environment:

    /usr/bin/python3.X -m venv MiroSim

You have to run both the virtual environment's activation script and the AGX setup_env script to run the program. You can put the command to run the AGX script into the venv script by:

    echo "source /opt/Algoryx/AgX-YOURAGXVERSION/setup_env.bash" >> MiroSim/bin/activate

Then, activate the MiroSim environment with:

    source MiroSim/bin/activate

The first time you do this, you need to install these two packages as well:

    pip install numpy
    pip install scipy

Done! To run the program:

    python Main.py
    --- OR ---
    agxViewer Main.py

The next time you start MiroSim, you repeat "source MiroSim/bin/activate" in the terminal and run the Main.py file again.

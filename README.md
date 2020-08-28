# MiroSimulint

This is a simulation library built on PyChrono. It can be used to build component based modules in a test environment.

To get this running:
___

## Installing Programs

### Step 1) *Install Git*

Download and install Git from: 

> https://git-scm.com/downloads

### Step 2) *Install Anaconda*

Download and install Anaconda from:

> https://www.anaconda.com/products/individual

_Note: MiroSimulint was built using the 2019.10 version of Anaconda. If you run into issues, you can try uninstalling your current Anaconda version and installing the older one from:_

> https://repo.anaconda.com/archive/

### Step 3) *Install PyChrono and MiroSimulint*

Run Anaconda Prompt from the start menu or the Anaconda Navigator page. Type the commands in the following steps.

__a)__ Download the MiroSimulint code by:

    git clone https://github.com/Teskedsgubben/MiroSimulint

__b)__ Create an environment and install PyChrono by:

    conda create -n MiroSim python=3.7 numpy pylint

    conda install -n MiroSim -c projectchrono pychrono
    
__c)__ _Optional._ You should be able to run the program now. You can try it if you want, but we will do it a different way using VS Code in the next step. If you are familiar with code editing, you can just use this method and edit your files in your own editor, if you prefer.

    cd MiroSimulint

    conda activate MiroSim

    python Main.py

### Step 4) *Install VS Code*

This is the recommended code editor:

> https://code.visualstudio.com/download


### Step 5) *Setup the program with VS Code*

To open the files, start VS Code and click _File -> Open Folder_ to open the *MiroSimulint* folder. This should be at you user directory, such as __C:\\Users\\*MyUsername*\\MiroSimulint__ unless you changed it in step __3a)__.

When VS Code is open, click _View -> Command Palette..._ and type _"Python: Select Interpreter"_ and click it. You can then select the _('MiroSim': conda)_ option. Clicking this will create a file telling VS code to use the MiroSim environment for this project, and is only needed once.

Then, open the _Main.py_ file in the explorer menu on your left. When the file is open, click the green "Play Button" on the top right to run the code. If it starts, you're all set to begin coding. Otherwise, contact a supervisor with any error(s) you get.

___

## Using MiroSimulint

### The Program

When the program starts, the program runs for few seconds and then pauses. This is so the lander can settle in to the launcher and allows you to find an epic camera angle before launching. You can then press SPACE to resume and release the launcher.

You will have a target that the launcher is supposed to hit

### The Camera

To rotate the camera, use the mouse with left-click to drag the view. You can use the arrow keys and _Page Up / Page Down_ to move the point the camera looks at, and the scroll wheel to move closer or further away from that point. Press _I_ and klick _Help_ for a full list of camera controls. There are also several pre-configured camera positions you can use, as can be seen in the comments in the _Main.py_ file.

### The Coding

You have three code files to work with: _Main.py_, _Landers.py_ and _Launchers.py_. Any code in the subfolders are free to read if you are curious, but do not change them. You will only submit the three files. 

_Main.py_ is the file that starts the program. Here you can change camera views, rendering resolution and initial start delay. You can also compute any arguments you want to pass along to your Lander or Launcher. An important feature here is __Speedmode__ which you find is set to __False__. Setting this to __True__ will remove many details in the program, speeding up the simulation. This is most likely more conviniet to use when running tests and so on.

_Landers.py_ is where you can define you Lander. You have a demo where a simple lander is built by adding a bottom and top plate and connecting them with rods. Note how the top plate is rotated 180 degrees so the connection points are at the bottom, and the order of the components being connected. Start by modifying this lander, try to add more components etc.

_Launchers.py_ defines your Launcher in the same way as above. To try different designs, you can define several Launchers here and choose which one to try out in the _Main.py:_ file. 

Your Lander and Launcher are both built as MiroModules using MiroComponents. This means that you add the components you need, rotate the properly and then assemble them into a complete module. The order here is important, as connecting components 1 and 2 will move component 2 so that the connection points match. If you connect first and rotate the object after, things are going to get messy. However, that doesn't mean you shouldn't try it :bowtie:.

### The Goal

The challenge is to create a compact, portable launcher, that can hit a specified target. The ultimate goal is that the lander is automatically calibrated by knowing its own position and the position of the target, adjusting aim and power to hit the target without manual tweaking.
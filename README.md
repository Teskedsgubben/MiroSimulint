# MiroSimulint

This is a simulation library built on PyChrono. It can be used to build component based modules in a test environment.

To get this running:
___

## Installing Programs

### Step 1) *Install Git*

Download and install Git from:

> <https://git-scm.com/downloads>

### Step 2) *Install Anaconda*

Download and install Anaconda from:

> <https://www.anaconda.com/products/individual>

_Note: MiroSimulint was built using the 2019.10 version of Anaconda. If you run into issues, you can try uninstalling your current Anaconda version and installing the older one from:_

> <https://repo.anaconda.com/archive/>

### Step 3) *Install PyChrono and MiroSimulint*

Run Anaconda Prompt from the start menu or the Anaconda Navigator page. Type the commands in the following steps.

__a)__ Download the MiroSimulint code by:

    git clone https://github.com/Teskedsgubben/MiroSimulint

__b)__ Create an environment and install PyChrono by:

    conda create -n MiroSim python=3.7 numpy matplotlib pylint ffmpeg

    conda install -n MiroSim -c projectchrono pychrono

__c)__ _Optional._ You should be able to run the program now. You can try it if you want, but we will do it a different way using VS Code in the next step. If you are familiar with code editing, you can just use this method and edit your files in your own editor, if you prefer.

    cd MiroSimulint

    conda activate MiroSim

    python Main.py

__Linux Users:__

You then need to install irrlicht, run these commands in a terminal window:

    sudo apt-get install libirrlicht1.8 libirrlicht-dev libirrlicht-doc

    sudo apt-get install freeglut3

If you get glibc version error, try checking the version by the command below and compare to your error.

    ldd --version

If your version of glibc (technically ldd, but they should be the same) is older than the error says that the program needs, you probably need to update to the latest LTS version of you distro. On Ubuntu, this is currently version 20.04 and this has been confirmed to work.

### Step 4) *Install VS Code*

This is the recommended code editor:

> <https://code.visualstudio.com/download>

### Step 5) *Setup the program with VS Code*

To open the files, start VS Code and click _File -> Open Folder_ to open the *MiroSimulint* folder. This should be at you user directory, such as __C:\\Users\\*MyUsername*\\MiroSimulint__ unless you changed it in step __3a)__, or __C:\\Users\\*MyUsername*\\Documents\\MiroSimulint__.

There is a package needed to get full support for Python commands. When VS Code is open, click _View -> Extensions_, search for Python and install Microsofts Python package.

Once the Python package is installed, click _View -> Command Palette..._ and type _"Python: Select Interpreter"_ and click it. You can then select the _('MiroSim': conda)_ option. Clicking this will create a file telling VS code to use the MiroSim environment for this project, and is only needed once.

You also need to set the command prompt to default shell. Click _View -> Command Palette..._ and type _"Terminal: Select Default Shell"_ and click it. Now choose _Command Prompt_ in the menu.

Now restart Visual Studio Code and the configuration is complete.

### Step 6) *Run the program*

Open VS Code and open the MiroSimulint directory (_File -> Open Folder..._). Open the _Main.py_ file in the explorer menu on your left. When the file is open, click the green "Play Button" on the top right to run the code. If it starts, you're all set to begin coding. Otherwise, contact a supervisor with any error(s) you get.

__IMPORTANT NOTE:__ Some DirectX issues have been occuring. What happens is that the code runs, but the simulation only produces a black screen. See the folder dx9_shaderfix and follow the readme.txt instructions for a quickfix on this. A reliable solution will be posted when ready.

___

## Using MiroSimulint

### The Program

When the program starts, the program runs for few seconds and then pauses. This is so the lander can settle in to the launcher and allows you to find an epic camera angle before launching. You can then press SPACE to resume and release the launcher. You will have a target that the launcher is supposed to hit.

### The Camera

To rotate the camera, use the mouse with left-click to drag the view. You can use the arrow keys and _Page Up / Page Down_ to move the observation point the camera looks at, and the scroll wheel to move closer or further away from that point. Press _I_ and click _Help_ for a full list of camera controls. There are also several pre-configured camera positions you can use, as can be seen in the comments in the _Main.py_ file.

There are two special camera functions you can use as well.

__Follow:__ If you set the perspective to 'follow' and input the name of a module you have added to the system, the camera will follow that module. You can also specify from which direction the camera should view the module. Note that manual controls only work while the simulation is paused when using this.

__Cycle:__ You can add `cycle = True` to the end of the input arguments. This will override manual controls and circle the camera around the observation point. You can also add `cycle_laptime = X` to change the speed of the camera rotation, where `X` is any number you like. This can be used in combination with the follow perspective.

_Note: Laptime means how many simulation time seconds it takes for the camera to complete one revolution, meaning a laptime of 10 will create a video that takes 50 seconds to complete the lap, using the default 60 fps video and 300 fps simulation speed._

### The Coding

You have four code files to work with: _Main.py_, _Landers.py_, _Launchers.py_ and _CustomComponents.py_. Any code in the subfolders are free to read if you are curious, but do not change them. You will only submit up to the four files, unless otherwise agreed upon.

_Main.py_ is the file that starts the program. Here you can change camera views, rendering resolution and initial start delay. You can also compute any arguments you want to pass along to your Lander or Launcher. An important feature here is __Speedmode__ which you find is set to __False__. Setting this to __True__ will remove many details in the program, speeding up the simulation. This is most likely more conviniet to use when running tests and so on.

_Landers.py_ is where you can define you Lander. You have a demo where a simple lander is built by adding a bottom and top plate and connecting them with rods. Note how the top plate is rotated 180 degrees so the connection points are at the bottom, and the order of the components being connected. Start by modifying this lander, try to add more components etc.

_Launchers.py_ defines your Launcher in the same way as above. To try different designs, you can define several Launchers here and choose which one to try out in the _Main.py:_ file.

_CustomComponents.py_ is where you can define your custom components that you either have imported from an object file (.obj) or agreed to create from component template function, like MC0XX. You do not have to use this file if you do not feel the need to.

There is also a _test\_main.py_ file which is a copy of the _Main.py_ file and will run the program as well. It shows some other tricks you can use for testing and camera controls. You can also use this file to try stuff out without having to change the Main file.

Before you start coding, copy these files in the same directory and rename them by adding _local. There should in other words be a Main.py file and a Main_local.py file etc. You can then edit the local files and still do a git pull to get the latest version of the Simulint files, and you also keep the original files as a refernce.

To do a git pull, go to Source Control _(View -> SCM)_ and click the three dots button ... to show the dropdown menu, then click Pull. If there are changes showing in the list, you need to discard them first. Save your changes in some way if you need to keep them, then discard them with the revert-like arrow button.

Your Lander and Launcher are both built as MiroModules using MiroComponents. This means that you add the components you need, rotate them properly and then assemble them into a complete module. The order here is important, as connecting components 1 and 2 will move component 2 so that the connection points match. If you connect first and rotate the object after, things are going to get messy. However, that doesn't mean you shouldn't try it :bowtie:.

### The Goal

The challenge is to create a compact, portable launcher, that can hit a specified target. The ultimate goal is that the launcher is automatically calibrated by knowing its own position and the position of the target, adjusting aim and power to hit the target with the lander without any manual tweaking.

### Create a Video File

We installed ffmpeg into the MiroSim environment to enable creating a video file from the simulation. For this to work properly, open your Display Settings and set scaling to 100%, otherwise the images will get skewed. Also, set the resolution of the simulation to something suitable for your monitor. Then, to generate the video, follow the steps below.

First, start the simulation as usual. When you press PrintScreen the program will start saving images into a directory called video_capture. Press PrtSc to start recording, then press it again or close the window to stop. You can move the camera during capture, and you can pause to change camera angle, no frames are saved while paused. You can also add "record": True to the simulation config, and it will record from the start. To then convert these images into a video file, we use ffmpeg.

From VS Code you can run the command below in the terminal window. If the terminal is not showing, click _View -> Terminal_ to open it. If you are not using VS Code, you can run the same command from the Anaconda Prompt in the MiroSimulint directory, just make sure MiroSim is your active environment as in Step 3c. The command to run is:

    ffmpeg -framerate 60 -i video_capture/screenshot%05d.bmp -b:v 128M video_capture/MiroSim.avi

This will put the screenshot files into a video file called MiroSim.avi in the video\_capture folder. The framerate of 60 can be changed to alter the speed of the video. A value of 300 is full speed, so using 60 renders the video in slow motion, but this is more suitable for seeing details. You can also change the quality and file size by changing the _128M_ to another number.

You can also add audio by supplying an audio file as input between the _d.bmp_ and _-b:v_ like below. If the audio file is too short and the video cuts too early, remove the -shortest command.

    ...d.bmp -i audiofile.mp3 -shortest -b:v...

__Convert to .mp4:__ The default video format is .avi which you can import in most video editors. If you just want to render a .mp4 file to play directly, you can use the command below.

    ffmpeg -i video_capture/MiroSim.avi -preset slow -codec:v libx264 -pix_fmt yuv420p -b:v 128M video_capture/MiroSim.mp4

Then open the MiroSim.mp4 file in the video_capture directory.

### Keeping MiroSimulint up to date

To get the latest updates we push to the repository, you can follow a simple procedure to set up the way you work. After that, it's as simple as a couple clicks to always get the latest version.

Step 1) Rename the files you will or have worked with by adding the suffix "_local" to their names, e.g. Main_local.py and GroupLogo_local.png and so on. This will make git ignore the files.

Step 2) Go to _View_ -> _SCM_ or _Source Control_, which is the same as clicking the "fork" or "graph" symbol on your left side panel. Here, discard all changes in the list by hovering over the file name and clicking the "reverse" style arrow. This should reset the original file.

Step 3) Once the list is completely empty, click the three dots button ... and click Pull. This will get the latest versions of the files from the repository.

You then work in the files named _local instead of the ordinary files. After doing this once, you only need to redo step 3 to get the latest version again.

___

## Using AGX

MiroSimulint was built using PyChrono. It is currently being built to support AGX as well, allowing for other functionalities. To use MiroSim with AGX, you must first have a validated AGX installation on your computer. This means you download the AGX installer and place a provided license file in the install directory. See separate instructions for details.

To set MiroSimulint to use AGX you need to follow these steps:

Step 1) Locate the _MiroAPI\_selector.py_ file in the MiroClasses directory.

Step 2) Copy and paste the file into the same directory.

Step 3) Rename the copy: _MiroAPI\_local.py_

Step 4) Edit the local API file by removing the first if statement, lines 16 through 20. Then remove the indentation on the rows below (mark them then Shift+Tab).

Step 5) Change the API = 'PyChrono' to API = 'AGX'

You now have a local file selecting the API MiroSim will use. To change it back in the future, you only need to redo Step 5) in reverse and so on. However, you must select a python interpreter that is configured for AGX as well. Unless you knowingly configured it to be the same, you will most likely need to switch. This has to be done again if you decide to change API in the future as well.

Step 6) Go to _View_ -> _Command Palette_ and locate Python: Select Interpreter. The Python you want to run should be located in the AGX install directory, i.e. the .../Algoryx/AGX-your\_version directory. If you do not see the right one in the list, click _Enter interpreter path..._ and click _Find..._ so you can navigate to _C:\Program Files\Algoryx\AGX-2.29.2.0\python-x64_ or similar, and select the _python.exe_ in that directory. You now have the right python selected.

Step 7) To setup the environment for agx, you must run the _setup\_env.bat_ in the terminal you are using. This is done by _"C:\Program Files\Algoryx\AGX-2.29.2.0\setup\_env.bat"_, or if you are using powershell (it says __PS C:\Users...>__ rather than just __C:\Users...>__) you add an & before the path, like _& "C:\Program..."_. This needs to be run every time you start a new terminal for using AGX.

Step 8) You can add some lines to you local settings to make pylint find the agx functions. In VS Code, this is done by opening the local directory .vscode in the MiroSimulint directory. Here, modify (or create) the file _settings.json_ with the follow lines:

    {
        "python.pythonPath": "C:/Program Files/Algoryx/AGX-2.29.2.0/python-x64/python.exe",
        "files.associations": {
            "*.agxPy": "python"
        },
        "python.autoComplete.extraPaths": [
            "C:/Program Files/Algoryx/AGX-2.29.2.0/bin/x64/agxpy"
        ],
    }

Note that if you installed AGX somewhere else, you need to modify the above to the correct install directory.

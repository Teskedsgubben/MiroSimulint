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

You have three code files to work with: _Main.py_, _Landers.py_ and _Launchers.py_. Any code in the subfolders are free to read if you are curious, but do not change them. You will only submit the three files.

_Main.py_ is the file that starts the program. Here you can change camera views, rendering resolution and initial start delay. You can also compute any arguments you want to pass along to your Lander or Launcher. An important feature here is __Speedmode__ which you find is set to __False__. Setting this to __True__ will remove many details in the program, speeding up the simulation. This is most likely more conviniet to use when running tests and so on.

_Landers.py_ is where you can define you Lander. You have a demo where a simple lander is built by adding a bottom and top plate and connecting them with rods. Note how the top plate is rotated 180 degrees so the connection points are at the bottom, and the order of the components being connected. Start by modifying this lander, try to add more components etc.

_Launchers.py_ defines your Launcher in the same way as above. To try different designs, you can define several Launchers here and choose which one to try out in the _Main.py:_ file.

_test\_main.py_ is a copy of the _Main.py_ file and will run the program as well. It shows some other tricks you can use for testing and camera controls. You can also use this file to try stuff out without having to change the Main file.

Your Lander and Launcher are both built as MiroModules using MiroComponents. This means that you add the components you need, rotate them properly and then assemble them into a complete module. The order here is important, as connecting components 1 and 2 will move component 2 so that the connection points match. If you connect first and rotate the object after, things are going to get messy. However, that doesn't mean you shouldn't try it :bowtie:.

### The Goal

The challenge is to create a compact, portable launcher, that can hit a specified target. The ultimate goal is that the launcher is automatically calibrated by knowing its own position and the position of the target, adjusting aim and power to hit the target with the lander without any manual tweaking.

### Create a Video File

We installed ffmpeg into the MiroSim environment to enable creating a video file from the simulation. This is not something you have to do, but if you want to use the video, here is how it works.

First, start the simulation as usual. When you press PrintScreen the program will start saving images into a directory called video_capture. Press PrtSc to start recording, then press it again or close the window to stop. You can move the camera during capture, and you can pause to change camera angle, no frames are saved while paused. To then convert these images into a video file, we use ffmpeg.

From VS Code you can run the command below in the terminal window. If the terminal is not showing, click _View -> Terminal_ to open it. If you are not using VS Code, you can run the same command from the Anaconda Prompt in the MiroSimulint directory, just make sure MiroSim is your active environment as in Step 3c. The command to run is:

    ffmpeg -framerate 60 -i video_capture/screenshot%05d.bmp -b:v 128M video_capture/MiroSim.avi

This will put the screenshot files into a video file called MiroSim.avi in the video\_capture folder. The framerate of 60 can be changed to alter the speed of the video. A value of 300 is full speed, so using 60 renders the video in slow motion, but this is more suitable for seeing details. You can also change the quality and file size by changing the _128M_ to another number.

You can also add audio by supplying an audio file as input between the _d.bmp_ and _-b:v_ like below. If the audio file is too short and the video cuts too early, remove the -shortest command.

    ...d.bmp -i audiofile.mp3 -shortest -b:v...

__Mac users:__ If you are using Mac OS and do not have VLC or similar installed, you may not me able to play the .avi file. In that case, try using the command below to produce a playable file.

    ffmpeg -i video_capture/MiroSim.avi -preset slow -codec:v libx264 -pix_fmt yuv420p -b:v 100M video_capture/MiroSimMAC.mp4

Then open the MiroSimMAC.mp4 file in the video_capture directory.

# Fractal Visualizer

This is a guide to using my Fractal Visualizer tool.


## Setup

### 0. Clone the Repo
---
run
```
git clone https://github.com/Vodiboi/Fractal-Visualizer.git
```
in a terminal window, within the folder you want this folder to show up in. Then, cd into the folder:
```
cd Fractal-Visualizer 
```

### 1. Installs
---
make sure to install manim, pillow, numpy, and flet from the requirements file:

```
pip3 install -r requirements.txt 
```

Alternatively, you can install manually. (in theory, the below installs should work. If not, do some googling, and maybe let me know if something is fundamentally wrong)

```
pip3 install manim==0.18.0
pip3 install Pillow==9.2.0
pip3 install numpy==1.24.3
pip3 install flet==0.15.0
pip3 install pygame==2.1.3
```

### 2. Run it

Now, run main.py
```
python3 main.py
```
and boom

Note: A popup may appear asking whether to allow flet to access files within a folder of the computer the code is running in. Allow it to, otherwise the images cannot be displayed. Flet is not trying to access your personal files, don't worry, it justs needs to access some files for the code.

## Full Guide to Using the Tool

### The Basics:

The basics of this tool can be learnt with the presets. Select a preset, and then click the button that says `use preset`. This button loads in the preset. By default, the start and end points are `0` and `1`, and the recursion depth is `1`. The start and end points represent the inital position (with that, scale and rotation) of your fractal. To see the fractal, click the `run` button. Play around with these parameters on some samples.

### In Depth:

Now, into the code itself. The language revolves around shapes, which are used as fractals. To learn this language, we will look at an example bit of code.


```
% The Koch Snowflake!
struct KochSnowflake{
    % variables, can be played around with
    let width = 0.5
    let height = 0.2
    
    line(0, (1-$width)/2)
    line((1-$width)/2, 0.5+(1j*$height))
    line(0.5+(1j*$height), (1+$width)/2)
    line((1+$width)/2, 1)
    subdivideList = "ALL_TRUE" % equivelent to 4 "True"s
}

struct Main{
    useshape KochSnowflake()
}
```

To define a shape, we say `struct SHAPENAME` followed by curly braces. Line breaks are neccecary, as opposed to semicolons. 

Comments are placed after a `%` symbol, similar to latex, and extend for the rest of the line, similar to python.

Lines are defined with the line command, which takes in 2 points (python complex numbers, containing a real and/or imaginary section (defined with a *1j), ex: `0.5`, `1+2j`, `(math.pi+4)*1j`) for a line to be placed between.

Variables are defined using the `let` command. They are very nitpicky. there should be exactly 1 space between the variable name and `=`, and at least 1 space afterwards. The variable name should not contain any spaces. Variables are accesed with `$VAR_NAME` where "VAR_NAME" is the name of the variable. The `$` prevents user overloading of commands in the code, among other things. 

subdivideList is a list of booleans(`True`/`False`) that represents which lines shapes should be placed upon in the next fractal iteration. It can be set to `"ALL_TRUE"` or `"ALL_FALSE"` to save writing many spaces. Don't use it as a variable.

The flow of the program revolves around the shape `Main`. `Main` is the shape that is visualized when clicking the `run` button. Typically, programs should minimize the code in Main directly, and instead reference other shapes using the `useshape` command.

The `useshape X()` command uses the shape `X`. This adds all lines from `X` in order to the shape the command is being called in, and adds on the subdivideList in order as well (works even for `"ALL_TRUE"` and `"ALL_FALSE"`). 

Shapes can also be defined in a different manner. Consider the code snippet: 

```
linelist RisingCantor = [(0+0.5j,1/3+0.5j),(2/3+0.5j,1+0.5j)];"ALL_TRUE"

struct Main{
    useshape RisingCantor()
}
```

Here, a shape is defined using the `linelist` command. This command treats the shape like a class object in some sense. There are 2 parameters, seperated by a semicolon. The first is the list of segments, written out as a list of tuples of complex numbers, where each tuple represents a line between its 2 elements. The second parameter is the subdivideList of this shape. This shape can then be used in the useshape command like any other shape.

## FAQ
### Q: "Why isn't the image loading"
There are 2 possible answers to this. 1, it might just be taking some time to load, or loading for the first time, in which case it should load within 15 seconds. If it takes longer than this, look to the terminal output of the code. If there is some sort of error, you likely inputted the code wrong. Possible issues include:
- You didn't access a variable x with \$x, but instead using x. The initialization for a variable should not include a "\$", but using that variable always should. 
- You didn't make the struct Main, in which case do so, and let it contain the shape(s) needed.
- A parenthesis was unmatched. Be careful with parentheses.
- You used "i" to reference a complex number. This program is based on python, so "j" should always be used

If there is no error and the screen doesn't update seemingly, it may be the case that your fractal is so dense that you can't notice the change when increasing recursion. 

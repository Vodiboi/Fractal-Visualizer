# Barry's Fractal Visualizer

This is a guide to using Barry's Fractal Visualizer.


## Setup

### 0. Installs
---
make sure to install manim, pillow, numpy, and flet
(in theory, the below installs should work. If not, do some googling, and maybe let me know if something is fundamentally wrong)

```
pip3 install manim
pip3 install pillow
pip3 install numpy
pip3 install flet
```
Alternatively, you can try installing from the requirements file (although this might not always work for you)

```
pip3 install -r requirements.txt 
```

### 1. Clone the Repo
---
```
git clone https://github.com/Vodiboi/Fractal-Generator.git
```
### 2. Run it

then, cd into the repo and run main.py
```
cd -
python3 main.py
```
and boom

## How to use the tool

The basics of this tool can be learnt with the presets. Select a preset, and then click the button that says `use preset`. This button loads in the preset. By default, the start and end points are `0` and `1`, and the recursion depth is `1`. The start and end points represent the inital position (with that, scale and rotation) of your fractal. To see the fractal, click the `run` button Play around with these parameters on some samples.

Now, into the code itself. The language revolves around shapes, which are used as fractals. To learn this language, we will look at an example bit of code.

```
% fractal of a man flexing his muscles, or a ram
struct BodyBuilder{
    % Use 9-10 recursions to see the man, and for optimal viewing set the starting position to be -2-2j and the ending position to be 2-2j
    line(0, 0.5+0.5j)
    line(0.5+0.5j, 1)
    subdivideList = "ALL_TRUE"
}

struct Main{
    useshape BodyBuilder()
}
```
To define a shape, we say `struct SHAPENAME` followed by curly braces. Line breaks are neccecary, as opposed to semicolons. 
Comments are placed after a `%` symbol, similar to latex.
Lines are defined with the line command, which takes in 2 points for a line to be placed between
subdivideList is a list of booleans(`True`/`False`) that represents which lines should shapes be placed upon in the next fractal iteration. It can be set to `"ALL_TRUE"` or `"ALL_FALSE"` to save writing many spaces.

The flow of the program revolves around the shape `Main`. `Main` is the shape that is visualized when clicking the `run` button. Typically, programs should minimize the code in Main directly, and instead reference other shapes using the `useshape` command.

The `useshape X()` command uses the shape `X`. This adds all lines from `X` in order to the shape the command is being called in, and adds on the subdivideList in order as well (works even for `"ALL_TRUE"` and `"ALL_FALSE"`). 



## FAQ
### Q: "Why isn't the image loading"
There are 2 possible answers to this. 1, it might just be taking some time to load, or loading for the first time, in which case it should load within 15 seconds. If it takes longer than this, look to the terminal output of the code. If there is some sort of error, you likely inputted the code wrong. Possible issues include:
- You didn't access a variable x with \$x, but instead using x. The initialization for a variable should not include a "\$", but using that variable always should. 
- You didn't make the struct Main, in which case do so, and let it contain all info needed.
- A parenthesis was unmatched. Be careful with parentheses.
- You used "i" to reference a complex number. This program is based on python, so "j" should always be run
If there is no error and the screen doesn't update seemingly, it may be the case that your fractal is so dense that you can't notice the change when increasing recursion, which I have personally run into myself. There is no fix for this, other than maybe moving the start and end coordinates of your fractal to enlarge it.

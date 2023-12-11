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

The basics of this tool can be learnt with the presets. Select a preset, and then 


## FAQ
### Q: "Why isn't the image loading"
There are 2 possible answers to this. 1, it might just be taking some time to load, or loading for the first time, in which case it should load within 15 seconds. If it takes longer than this, look to the terminal output of the code. If there is some sort of error, you likely inputted the code wrong. Possible issues include:
- You didn't access a variable x with \$x, but instead using x. The initialization for a variable should not include a "\$", but using that variable always should. 
- You didn't make the struct Main, in which case do so, and let it contain all info needed.
- A parenthesis was unmatched. Be careful with parentheses.
- You used "i" to reference a complex number. This program is based on python, so "j" should always be run
If there is no error and the screen doesn't update seemingly, it may be the case that your fractal is so dense that you can't notice the change when increasing recursion, which I have personally run into myself. There is no fix for this, other than maybe moving the start and end coordinates of your fractal to enlarge it.

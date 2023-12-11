import os
import base64
from io import BytesIO
import subprocess
import flet as ft
from PIL import Image as image
import numpy as np
import parseThing
from dimension import getDimension
from mathstuff import recursively_subdivide

_fsrc = os.getcwd() + "/mainManimImage.png"
_f2src = os.getcwd() + "/mainPygameImage.png"

def manim_visualizer(page: ft.Page):
    '''
    Flet App for a Fractal Visualizer using Manim to render the underlying image
    '''

    # page stuff
    page.title = "Barry's Fractal Visualizer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_maximized = True

    # most widgets
    f = ft.TextField(label="Write your code here", multiline=True)
    start_pos = ft.TextField(label="Starting Position")
    end_pos = ft.TextField(label="Ending Position")
    depth = ft.TextField(label="Number of Recursions")
    error_log = ft.TextField(label="Errors Listed Here:", read_only=True)
    error_log.value = ""
    dimension = ft.TextField(label="Dimension: ", read_only=True)
    presets = ft.Dropdown(
        width=400,
        options=[ft.dropdown.Option(i[:i.find(".txt")]) for i in os.listdir("presets/")],
        label="Select Preset"
    )

    def use_preset(*_):
        with open(f"presets/{presets.value}.txt") as filee:
            d = filee.read()
        f.value = d
        f.update()
        if (start_pos.value == ""):
            start_pos.value = "0"
            start_pos.update()
        if (end_pos.value == ""):
            end_pos.value = "1"
            end_pos.update()
        if (depth.value == ""):
            depth.value = "1"
            depth.update()

    # add the preset button
    usePreset = ft.TextButton("Use Preset", on_click=use_preset)

    # our main image
    img = ft.Image(src=_fsrc, width=500, height=500, fit=ft.ImageFit.CONTAIN)

    def reloadMath(structs):
        '''
        reloads data in mathstuff.py
        '''
        with open(os.getcwd() + "/mathInfo.py", "r") as filee:
            l = filee.read()
        l = l.split("\n")
        lines = [tuple([[complex(i).real, complex(i).imag] for i in j]) for j in structs["Main"]()]
        # print(len(lines), "LINECNT")
        for i in range(len(l)):
            if l[i].startswith("RECURSIVE_PARTS"):
                l[i] = "RECURSIVE_PARTS = " + str(lines)
            elif l[i].startswith("PARTS_TO_SUBDIVIDE"):
                subdiv = str(structs["Main"].partsToSubdivide)
                # print(subdiv)
                if (subdiv == "ALL_TRUE"):
                    l[i] = "PARTS_TO_SUBDIVIDE = " + str([True]*len(lines))
                elif subdiv == "ALL_FALSE":
                    l[i] = "PARTS_TO_SUBDIVIDE = " + str([False]*len(lines))
                else:
                    l[i] = "PARTS_TO_SUBDIVIDE = " + str(structs["Main"].partsToSubdivide)
            elif l[i].startswith("START = "):
                if start_pos.value == "" or (not isinstance(eval(start_pos.value), int) and not isinstance(eval(start_pos.value), complex) and not isinstance(eval(start_pos.value), float)):
                    error_log.value = "Error: Invalid Start Pos. Must Be Int or Complex or Float"
                    error_log.update()
                    return
                else:
                    l[i] = "START = " + start_pos.value
            elif l[i].startswith("END = "):
                if end_pos.value == "" or (not isinstance(eval(end_pos.value), int) and not isinstance(eval(end_pos.value), complex) and not isinstance(eval(start_pos.value), float)):
                    error_log.value = "Error: Invalid End Pos. Must Be Int or Complex or Float"
                    error_log.update()
                    return
                else:
                    l[i] = "END = " + end_pos.value
            elif l[i].startswith("NUM_RECURSIONS = "):
                if depth.value == "" or (not isinstance(eval(depth.value), int)):
                    error_log.value = "Error: Invalid Number of Recursions. Must Be Int"
                    error_log.update()
                    return
                else:
                    l[i] = "NUM_RECURSIONS = " + depth.value
            
        with open("mathInfo.py", "w") as filee:
            filee.write("\n".join(l))
        
        divided = [tuple([[complex(i).real, complex(i).imag] for i in j]) for j in recursively_subdivide(eval(start_pos.value), eval(end_pos.value), eval(depth.value))]
        # dimension.value = str(get_dim(get_grid(divided, 16)))
        dimension.value = str(np.log2(getDimension(divided, 64) / getDimension(divided, 32)))


    def update(*_):
        error_log.value = ""
        error_log.update()
        code = f.value
        structs = parseThing.generateShapes(code)
        reloadMath(structs=structs)
        d = _fsrc.replace(' ', '\\ ')
        if os.system(f"manim -r 1280,720 --renderer=opengl --disable_caching renderer_manim.py TestScene --format=png -o {d}"):
            # print("a")
            error_log.value = "Too many lines to render. Please reduce the # of recursions and/or the # of line segments."
            error_log.update()
            return
        dimension.update()

        # stack overflow shenanigans in order to use the image
        pil_photo = image.open(_fsrc)
        arr = np.asarray(pil_photo)
        pil_img = image.fromarray(arr)
        buff = BytesIO()
        pil_img.save(buff, format="PNG")
        newstring = base64.b64encode(buff.getvalue()).decode("utf-8")
        img.src_base64 = newstring
        img.update()

    # add the run button
    btn = ft.ElevatedButton(
        text="Run", 
        on_click=update, 
        icon="play_circle", 
        width=100, 
        height=50, 
    )

    # display layout. Everything in wrapped in a container in order to select padding
    r = ft.Container(content=ft.Row([
        ft.Column(controls=[
            btn,
            f
        ],
        expand=1, spacing=10, 
        scroll=ft.ScrollMode.ALWAYS,
        height=700
        ),
        ft.Column(controls=[
            ft.Row([presets, usePreset]),
            ft.Row([start_pos, end_pos]),
            ft.Row([depth, dimension]),
            error_log,
            img
        ]
        ),
    ]), padding=10)

    # kaboom!
    page.add(r)
    page.update()

def pygame_visualizer(page:ft.Page):
    '''
    Flet App for a Fractal Visualizer using Manim to render the underlying image
    '''

    # page stuff
    page.title = "J's Fractal Visualizer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_maximized = True

    # most widgets
    f = ft.TextField(label="Write your code here", multiline=True)
    start_pos = ft.TextField(label="Starting Position")
    end_pos = ft.TextField(label="Ending Position")
    depth = ft.TextField(label="Number of Recursions")
    error_log = ft.TextField(label="Errors Listed Here:", read_only=True)
    error_log.value = ""
    dimension = ft.TextField(label="Dimension: ", read_only=True)
    presets = ft.Dropdown(
        width=400,
        options=[ft.dropdown.Option(i[:i.find(".txt")]) for i in os.listdir("presets/")],
        label="Select Preset"
    )

    # def boxSliderChange(e):
    boxSliderLabel = ft.Text(value="The resolution of boxes: ")
    boxSlider = ft.Slider(
        min=0,
        max=8,
        divisions=8,
        label="{value}",
        value=0
    )
    boxCount = ft.TextField(label="Box Count: ", value="N/A", read_only=True)

    def use_preset(*_):
        with open(f"presets/{presets.value}.txt") as filee:
            d = filee.read()
        f.value = d
        f.update()
        if (start_pos.value == ""):
            start_pos.value = "0"
            start_pos.update()
        if (end_pos.value == ""):
            end_pos.value = "1"
            end_pos.update()
        if (depth.value == ""):
            depth.value = "1"
            depth.update()

    # add the preset button
    usePreset = ft.TextButton("Use Preset", on_click=use_preset)

    # our main image
    img = ft.Image(src=_f2src, width=500, height=500, fit=ft.ImageFit.CONTAIN)

    def reloadMath(structs):
        '''
        reloads data in mathstuff.py
        '''
        with open(os.getcwd() + "/mathInfo.py", "r") as filee:
            l = filee.read()
        l = l.split("\n")
        lines = [tuple([[complex(i).real, complex(i).imag] for i in j]) for j in structs["Main"]()]
        # print(len(lines), "LINECNT")
        for i in range(len(l)):
            if l[i].startswith("RECURSIVE_PARTS"):
                l[i] = "RECURSIVE_PARTS = " + str(lines)
            elif l[i].startswith("PARTS_TO_SUBDIVIDE"):
                subdiv = str(structs["Main"].partsToSubdivide)
                # print(subdiv)
                if (subdiv == "ALL_TRUE"):
                    l[i] = "PARTS_TO_SUBDIVIDE = " + str([True]*len(lines))
                elif subdiv == "ALL_FALSE":
                    l[i] = "PARTS_TO_SUBDIVIDE = " + str([False]*len(lines))
                else:
                    l[i] = "PARTS_TO_SUBDIVIDE = " + str(structs["Main"].partsToSubdivide)
            elif l[i].startswith("START = "):
                if start_pos.value == "" or (not isinstance(eval(start_pos.value), int) and not isinstance(eval(start_pos.value), complex) and not isinstance(eval(start_pos.value), float)):
                    error_log.value = "Error: Invalid Start Pos. Must Be Int or Complex or Float"
                    error_log.update()
                    return
                else:
                    l[i] = "START = " + start_pos.value
            elif l[i].startswith("END = "):
                if end_pos.value == "" or (not isinstance(eval(end_pos.value), int) and not isinstance(eval(end_pos.value), complex) and not isinstance(eval(start_pos.value), float)):
                    error_log.value = "Error: Invalid End Pos. Must Be Int or Complex or Float"
                    error_log.update()
                    return
                else:
                    l[i] = "END = " + end_pos.value
            elif l[i].startswith("NUM_RECURSIONS = "):
                if depth.value == "" or (not isinstance(eval(depth.value), int)):
                    error_log.value = "Error: Invalid Number of Recursions. Must Be Int"
                    error_log.update()
                    return
                else:
                    l[i] = "NUM_RECURSIONS = " + depth.value
            elif l[i].startswith("DRAW_BOXES"):
                l[i] = "DRAW_BOXES = " + str((None if boxSlider.value == 0 else int(10-boxSlider.value)))
            
        with open("mathInfo.py", "w") as filee:
            filee.write("\n".join(l))
        
        # divided = [tuple([[complex(i).real, complex(i).imag] for i in j]) for j in recursively_subdivide(eval(start_pos.value), eval(end_pos.value), eval(depth.value))]
        # dimension.value = str(get_dim(get_grid(divided, 16)))
        # dimension.value = str(np.log2(getDimension(divided, 64) / getDimension(divided, 32)))


    def update(*_):
        error_log.value = ""
        error_log.update()
        code = f.value
        structs = parseThing.generateShapes(code)
        reloadMath(structs=structs)
        # d = _f2src.replace(' ', '\\ ')

        try:
            process = subprocess.run(
                ["python3", "renderer_pygame.py"],
                capture_output=True,
                timeout=5.0,
                text=True
            )
            if process.returncode != 0:
                error_log.value = "Renderer error: " + process.stderr
                error_log.update()
                return
            output = process.stdout.strip().split("\n")
            dimension.value = output[0].strip()
            dimension.update()
            boxCount.value = "N/A" if boxSlider.value == 0 else output[1].strip()
            boxCount.update()
        except subprocess.TimeoutExpired:
            error_log.value = "Too many lines to render. Please reduce the # of recursions and/or the # of line segments."
            error_log.update()
            return
        
        # dimension.update()

        # stack overflow shenanigans in order to use the image
        pil_photo = image.open(_f2src)
        arr = np.asarray(pil_photo)
        pil_img = image.fromarray(arr)
        buff = BytesIO()
        pil_img.save(buff, format="PNG")
        newstring = base64.b64encode(buff.getvalue()).decode("utf-8")
        img.src_base64 = newstring
        img.update()

    # add the run button
    btn = ft.ElevatedButton(
        text="Run", 
        on_click=update, 
        icon="play_circle", 
        width=100, 
        height=50, 
    )

    # display layout. Everything in wrapped in a container in order to select padding
    r = ft.Container(content=ft.Row([
        ft.Column(controls=[
            btn,
            f
        ],
        expand=1, spacing=10, 
        scroll=ft.ScrollMode.ALWAYS,
        height=700
        ),
        ft.Column(controls=[
            ft.Row([presets, usePreset]),
            ft.Row([start_pos, end_pos]),
            ft.Row([depth, dimension]),
            ft.Row([boxSliderLabel, boxSlider, boxCount]),
            error_log,
            img
        ]
        ),
    ]), padding=10)

    # kaboom!
    page.add(r)
    page.update()

def runApp(view=ft.AppView.FLET_APP, version="manim"):
    match version:
        case "manim":
            ft.app(target=manim_visualizer, view=view)
        case "pygame":
            ft.app(target=pygame_visualizer, view=view)

    # code that runs when the app is closed
    i2 = image.open("defaultManimImg.png")
    i2.save(_fsrc)

    i3 = image.open("defaultPygameImage.png")
    i3.save(_f2src)

if __name__ == "__main__":
    runApp()
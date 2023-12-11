import flet as ft
import os
import parseThing
from io import BytesIO
from PIL import Image as image
import numpy as np
import base64
from dimension import getDimension
from mathstuff import recursively_subdivide

_fsrc = os.getcwd() + "/mainManimImage.png"

def main(page: ft.Page):
    '''
    Flet App for a Fractal Visualizer
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
        print(len(lines), "LINECNT")
        for i in range(len(l)):
            if l[i].startswith("RECURSIVE_PARTS"):
                l[i] = "RECURSIVE_PARTS = " + str(lines)
            elif l[i].startswith("PARTS_TO_SUBDIVIDE"):
                subdiv = str(structs["Main"].partsToSubdivide)
                print(subdiv)
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
            print("a")
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
    btn = ft.TextButton(text="Run", on_click=update)

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

def runApp(view=ft.AppView.FLET_APP):
    ft.app(target=main, view=view)

    # code that runs when the app is closed
    i2 = image.open("defaultManimImg.png")
    i2.save(_fsrc)
if __name__ == "__main__":
    runApp()
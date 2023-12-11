if __name__ != "__main__": exit(0)
from visualizer import runApp
import flet as ft
import sys


d = {
    "app":ft.AppView.FLET_APP,
    "website" : ft.AppView.WEB_BROWSER
}

match len(sys.argv):
    case 1:
        runApp()
    case 2:
        runApp(version=sys.argv[1].lower())
    case 3:
        runApp(version=sys.argv[1].lower(), view=d[sys.argv[2].lower()])
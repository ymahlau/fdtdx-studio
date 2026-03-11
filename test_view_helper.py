from nicegui import ui
import sys
import os

# Add src to path to import fdtdx_studio modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from fdtdx_studio.ui.scene_3d.main_section import MainSection

class DummyController:
    def choose_box(self, name):
        print(f"Clicked {name}")

ui.label("ViewHelper Testing")

main_section = MainSection(DummyController())
main_section.update([
    ["Simulation_Volume", "Volume", (10, 10, 10), (0, 0, 0), "#ffffff"],
    ["Box1", "Box", (2, 2, 2), (2, 2, 2), "#ff0000"]
])

ui.run(port=8080)

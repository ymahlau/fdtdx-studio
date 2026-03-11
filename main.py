from nicegui import ui
from fdtdx_studio.controller.main_controller import Controller
from fdtdx_studio.ui.ui_view import View
import tomllib as toml
import pathlib


#Loads the config from toml and returns the ONLY [ui] part as a dict
def load_ui_config(path: str | pathlib.Path = "src/fdtdx_studio/config/config.toml") -> dict:
    defaults = {
        "title": "FDTDX Studio",
        "favicon": None,
        "port": 8080,
        "host": "127.0.0.1",
        "dark": False,
        "reconnect_timeout": 3.0,
        "show": True,
        "reload": False,
        "uvicorn_logging_level": "warning",
    }
    """Load the `[ui]` section from the TOML config file."""
    cfg_path = pathlib.Path(path)
    if not cfg_path.is_file():
        print(f"[config] No config file found at {cfg_path!s}\n")
        return defaults
    with cfg_path.open("rb") as f:
        full_cfg = toml.load(f)
    ui_cfg= full_cfg.get("ui", {})
    return {**defaults, **ui_cfg}


uirun_options= load_ui_config()
favicon_path = pathlib.Path(uirun_options['favicon'])
if not favicon_path.is_file():
  print(f"[config] No file found at {favicon_path!s}\n")
  uirun_options['favicon']=None



@ui.page('/')
def index():
  controller = Controller()



ui.run(**uirun_options)
"""
main.py – FDTDX Studio entry point
===================================
Configure the server either by editing ServerOptions defaults below,
or by passing CLI flags at runtime:

    python main.py                          # all defaults
    python main.py --port 9090 --dark       # override on the fly
    python main.py --help                   # list every option
"""

from __future__ import annotations

import argparse
import pathlib
from dataclasses import dataclass
from typing import Any

from nicegui import ui
from fdtdx_studio.controller.main_controller import Controller
from fdtdx_studio.ui.ui_view import View


# ---------------------------------------------------------------------------
# 1.  Edit defaults here
# ---------------------------------------------------------------------------

@dataclass
class ServerOptions:
    title: str                       = "FDTDX Studio"
    favicon: str | None              = "src/fdtdx.svg"
    port: int                        = 8080
    host: str                        = "127.0.0.1"
    dark: bool | None                = None    # None → NiceGUI decides
    reconnect_timeout: float         = 3.0
    show: bool                       = True
    reload: bool                     = False
    uvicorn_logging_level: str       = "warning"
    ssl_keyfile: str | None          = None
    ssl_certfile: str | None         = None


# ---------------------------------------------------------------------------
# 2.  CLI parser  (one flag per field, defaults pulled from the dataclass)
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    d = ServerOptions()               # used only for default values in help text
    p = argparse.ArgumentParser(
        prog="fdtdx-studio",
        description="FDTDX Studio – NiceGUI server",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--title",              default=d.title,
                   help="Browser tab / window title")
    p.add_argument("--favicon",            default=d.favicon,    metavar="PATH",
                   help="Path or URL to the page favicon")
    p.add_argument("--port",               default=d.port,       type=int,
                   help="TCP port to listen on")
    p.add_argument("--host",               default=d.host,
                   help="Bind address")
    p.add_argument("--reconnect-timeout",  default=d.reconnect_timeout,
                   type=float, metavar="SECONDS",
                   help="NiceGUI reconnect timeout in seconds")
    p.add_argument("--log-level",          default=d.uvicorn_logging_level,
                   dest="uvicorn_logging_level",
                   choices=["critical", "error", "warning", "info", "debug", "trace"],
                   help="Uvicorn log level")

    # Boolean flags
    p.add_argument("--show",    dest="show",   action="store_true",  default=d.show,
                   help="Open a browser window on startup")
    p.add_argument("--no-show", dest="show",   action="store_false",
                   help="Do not open a browser window on startup")
    p.add_argument("--reload",    dest="reload", action="store_true",  default=d.reload,
                   help="Enable auto-reload on file changes")
    p.add_argument("--no-reload", dest="reload", action="store_false",
                   help="Disable auto-reload on file changes")

    # Dark mode: three-way (--dark / --light / omitted → None)
    dark_group = p.add_mutually_exclusive_group()
    dark_group.add_argument("--dark",  dest="dark", action="store_true",  default=None,
                            help="Force dark mode")
    dark_group.add_argument("--light", dest="dark", action="store_false",
                            help="Force light mode")

    # Optional TLS
    p.add_argument("--ssl-keyfile",  default=d.ssl_keyfile,  metavar="PATH",
                   help="Path to TLS private key (.pem)")
    p.add_argument("--ssl-certfile", default=d.ssl_certfile, metavar="PATH",
                   help="Path to TLS certificate (.pem)")
    return p


def parse_options() -> ServerOptions:
    """Return ServerOptions populated from CLI arguments (or defaults)."""
    ns = build_parser().parse_args()
    return ServerOptions(
        title                 = ns.title,
        favicon               = ns.favicon,
        port                  = ns.port,
        host                  = ns.host,
        dark                  = ns.dark,
        reconnect_timeout     = ns.reconnect_timeout,
        show                  = ns.show,
        reload                = ns.reload,
        uvicorn_logging_level = ns.uvicorn_logging_level,
        ssl_keyfile           = ns.ssl_keyfile,
        ssl_certfile          = ns.ssl_certfile,
    )


# ---------------------------------------------------------------------------
# 3.  Favicon validation
# ---------------------------------------------------------------------------

def resolve_favicon(opts: ServerOptions) -> str | None:
    """Return the favicon value if usable, else None (with a warning).

    - URLs (http:// / https://) are passed through as-is.
    - Local paths are checked for existence; missing files produce a warning.
    """
    if opts.favicon is None:
        return None
    if opts.favicon.lower().startswith(("http://", "https://")):
        return opts.favicon
    favicon_path = pathlib.Path(opts.favicon)
    if not favicon_path.is_file():
        print(f"[config] No favicon found at {favicon_path!s} – skipping.\n")
        return None
    return opts.favicon


# ---------------------------------------------------------------------------
# 4.  NiceGUI app
# ---------------------------------------------------------------------------

@ui.page("/")
def index():
    controller = Controller()


# ---------------------------------------------------------------------------
# 5.  Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    opts = parse_options()
    opts.favicon = resolve_favicon(opts)

    # Build the kwargs dict for ui.run(), dropping None-valued TLS keys
    run_kwargs = dict[str, Any](
        title                 = opts.title,
        favicon               = opts.favicon,
        port                  = opts.port,
        host                  = opts.host,
        dark                  = opts.dark,
        reconnect_timeout     = opts.reconnect_timeout,
        show                  = opts.show,
        reload                = opts.reload,
        uvicorn_logging_level = opts.uvicorn_logging_level,
    )
    if opts.ssl_keyfile:
        run_kwargs["ssl_keyfile"] = opts.ssl_keyfile
    if opts.ssl_certfile:
        run_kwargs["ssl_certfile"] = opts.ssl_certfile

    ui.run(**run_kwargs)
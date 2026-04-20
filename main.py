"""
FDTDX Studio – entry point.

Configure the server via CLI flags or by editing the UIConfig defaults below.

CLI examples
------------
    python main.py
    python main.py --port 9090 --no-reload
    python main.py --host 127.0.0.1 --title "My Sim"
    python main.py --dry-run          # print resolved config, don't start
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from dataclasses import dataclass
from typing import Optional


# In-code defaults

@dataclass
class UIConfig:
    title: str                   = "FDTDX Studio"
    favicon: str                 = "src/fdtdx_studio/fdtdx.svg"
    port: int                    = 8080
    host: str                    = "127.0.0.1"
    # TODO later change to dark=None when we support dark mode
    dark: Optional[bool]         = False  # None = NiceGUI decides, True/False forces it
    reconnect_timeout: float     = 3.0
    show: bool                   = False
    reload: bool                 = False
    uvicorn_logging_level: str   = "warning"
    ssl_keyfile: str             = ""
    ssl_certfile: str            = ""

    def to_nicegui_kwargs(self) -> dict:
        """Resolve favicon path, then return a dict ready for ui.run(**kwargs)."""
        favicon: Optional[str] = self.favicon or None
        if favicon and not favicon.startswith(("http://", "https://")):
            # Only validate local paths – URLs are passed through as-is
            p = pathlib.Path(favicon)
            if not p.is_file():
                print(f"[config] favicon not found at {p} – skipping")
                favicon = None

        kwargs = dict(
            title                 = self.title,
            favicon               = favicon,
            port                  = self.port,
            host                  = self.host,
            dark                  = self.dark,
            reconnect_timeout     = self.reconnect_timeout,
            show                  = self.show,
            reload                = self.reload,
            uvicorn_logging_level = self.uvicorn_logging_level,
        )
        if self.ssl_keyfile:
            kwargs["ssl_keyfile"] = self.ssl_keyfile
        if self.ssl_certfile:
            kwargs["ssl_certfile"] = self.ssl_certfile
        return kwargs


# CLI parser

def _build_parser() -> argparse.ArgumentParser:
    d = UIConfig()  # pull defaults from the dataclass
    p = argparse.ArgumentParser(
        prog="fdtdx-studio",
        description="FDTDX Studio – NiceGUI simulation front-end",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--title",   default=d.title,  help="Browser tab title")
    p.add_argument("--favicon", default=d.favicon, help="Path or URL to favicon")
    p.add_argument("--port",    default=d.port,   type=int)
    p.add_argument("--host",    default=d.host)
    p.add_argument("--reconnect-timeout", default=d.reconnect_timeout,
                   type=float, dest="reconnect_timeout", metavar="SECONDS")
    p.add_argument("--uvicorn-logging-level", default=d.uvicorn_logging_level,
                   dest="uvicorn_logging_level",
                   choices=["critical","error","warning","info","debug","trace"])
    p.add_argument("--ssl-keyfile",  default=d.ssl_keyfile,  dest="ssl_keyfile",  metavar="PATH")
    p.add_argument("--ssl-certfile", default=d.ssl_certfile, dest="ssl_certfile", metavar="PATH")

    dark_grp = p.add_mutually_exclusive_group()
    dark_grp.add_argument("--dark",      dest="dark", action="store_true",  default=d.dark)
    dark_grp.add_argument("--light",     dest="dark", action="store_false")
    dark_grp.add_argument("--auto-dark", dest="dark", action="store_const", const=None,
                          help="Let NiceGUI choose (default)")

    show_grp = p.add_mutually_exclusive_group()
    show_grp.add_argument("--show",    dest="show", action="store_true",  default=d.show)
    show_grp.add_argument("--no-show", dest="show", action="store_false")

    reload_grp = p.add_mutually_exclusive_group()
    reload_grp.add_argument("--reload",    dest="reload", action="store_true", default=d.reload)
    reload_grp.add_argument("--no-reload", dest="reload", action="store_false")

    p.add_argument("--dry-run", action="store_true",
                   help="Print resolved config and exit without starting the server")
    return p


def _parse_args(argv: list[str] | None = None) -> tuple[UIConfig, bool]:
    ns = _build_parser().parse_args(argv)
    cfg = UIConfig(
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
    return cfg, ns.dry_run


# App

def _register_pages() -> None:
    """Import NiceGUI + app code and register all routes.

    Kept in a function so the import-time side effects of NiceGUI and the
    controller only fire when we actually intend to run the server — never on
    a dry-run or a plain ``import main``.

    Called in two places:
      1. _run()  – by the parent process, just before ui.run().
      2. The reload-worker hook below – by uvicorn worker processes that
         re-import this module from scratch and therefore never reach main().
    """
    from nicegui import ui                                        # noqa: PLC0415
    from fdtdx_studio.controller.main_controller import Controller  # noqa: PLC0415
    # from fdtdx_studio.ui.ui_view import View  # uncomment if needed

    @ui.page("/")
    def index():
        Controller()


def _run(cfg: UIConfig) -> None:
    _register_pages()
    from nicegui import ui
    ui.run(**cfg.to_nicegui_kwargs())


# Reload-worker hook

import os as _os
if _os.environ.get("NICEGUI_WORKER"):
    _register_pages()


# Entry point

def main(argv: list[str] | None = None) -> None:
    cfg, dry_run = _parse_args(argv)

    if dry_run:
        print("Resolved UIConfig:")
        for f_name, value in cfg.__dict__.items():
            print(f"  {f_name:<28} = {value!r}")
        print("\nNiceGUI kwargs:")
        for k, v in cfg.to_nicegui_kwargs().items():
            print(f"  {k:<28} = {v!r}")
        sys.exit(0)

    _run(cfg)


if __name__ == "__main__":
    main()

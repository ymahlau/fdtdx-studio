from nicegui import ui
from fdtdx_studio.ui.panels.simulation_parameters_panel import simulation_parameters_panel

class RightDrawer:
    """Creates the right drawer UI visible on the main view, used for configuring simulation or object parameters.
    
    Contains controls for adjusting various simulation settings.
    """

    def __init__(self, view, controller):
        """Initializes the RightDrawer with references to the main view and controller."""
        self.controller = controller
        self.view = view
        self.simparpanel = simulation_parameters_panel(self, controller)
        self.build()

    def build(self):
        """Builds the right drawer UI components."""
        with ui.right_drawer(elevated=True).style('background-color: #E3E3E3') as self.right_drawer:
            with ui.column().classes('w-full h-full justify-between gap-1'):
                ui.label('Configuration').style('font-size: 18px; margin-bottom: 8px; font-weight: bold;')
                with ui.scroll_area().classes('justify-start items-start h-full').style('padding: 0px;') as self.config_panel:
                    self.view.config_panel = self.config_panel
                    # Render sim params panel by default on startup
                    with self.config_panel:
                        self.simparpanel.simulation_param_panel()
                ui.button(
                    'Simulation Parameters',
                    on_click=self.show_sim_panel
                ).classes('w-full').style('margin-bottom: 16px;')

    def show_sim_panel(self):
        """Clears the config panel and renders the simulation parameters panel."""
        if self.config_panel is not None:
            self.config_panel.clear()
            with self.config_panel:
                self.simparpanel.button = None  # Reset so new button widget is created
                self.simparpanel.simulation_param_panel()

    async def update_drawer(self):
        """Reloads the Simulation Parameter Panel. MUST BE CALLED TO REFRESH NEW VALUES."""
        if self.config_panel is not None:
            self.config_panel.clear()
            await ui.context.client.connected()  # Ensures UI is ready
            with self.config_panel:
                self.simparpanel.button = None
                self.simparpanel.simulation_param_panel()
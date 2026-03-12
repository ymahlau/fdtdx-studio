from nicegui import ui
from fdtdx_studio.ui.popups.base_detector_popup import BaseDetectorPopup


class EnergyDetectorPopup(BaseDetectorPopup):
    """
    UI popup for creating an fdtdx.EnergyDetector.

    Responsibilities:
    - define detector-specific UI fields
    - collect detector-specific parameters
    - provide DETECTOR_TYPE for controller dispatch

    IMPORTANT:
    - does NOT own a dialog
    - does NOT talk to the controller directly
    """

    # Used by BaseDetectorPopup._call_add()
    # >>> CONTROLLER DISPATCH KEY <<<
    DETECTOR_TYPE = 'ENERGY'

    def __init__(self, controller):

        self.input_as_slices = None
        self.input_reduce_volume = None

        self.input_x_slice = None
        self.input_y_slice = None
        self.input_z_slice = None

        self.input_aggregate = None

        # Initialize BaseDetectorPopup (stores controller, sets button)
        super().__init__(controller)

    # --------------------------------------------------
    # DETECTOR-SPECIFIC UI
    # --------------------------------------------------

    def build_detector_specific_ui(self):
        """
        Build UI elements specific to EnergyDetector.

        This method is called from BaseDetectorPopup.build_dialog_inside().
        """
        # >>> UI ONLY <<<

        # Mode toggles
        self.input_as_slices = ui.checkbox(
            'Return as 2D slices (as_slices)',
            value=False,
        )
        self.input_reduce_volume = ui.checkbox(
            'Reduce volume (reduce_volume)',
            value=False,
        )

        ui.separator().classes('my-3')

        ui.label('Slice positions (optional)') \
            .style('font-size: 13px; font-weight: 600; margin-bottom: 6px')

        ui.label('Set a slice position (in relative/object coordinates as expected by fdtdx). Leave empty for None.') \
            .style('font-size: 12px; opacity: 0.8; margin-bottom: 8px')

        # Optional slice positions
        with ui.row().classes('w-full gap-3'):
            self.input_x_slice = ui.number(
                label='x_slice',
                value=None,
                format='%.6f',
            ).classes('w-full')

            self.input_y_slice = ui.number(
                label='y_slice',
                value=None,
                format='%.6f',
            ).classes('w-full')

            self.input_z_slice = ui.number(
                label='z_slice',
                value=None,
                format='%.6f',
            ).classes('w-full')
    # --------------------------------------------------
    # DATA COLLECTION (UI → Controller)
    # --------------------------------------------------

    def collect_detector_kwargs(self) -> dict:
        """
        Collect parameters specific to FieldDetector. --> ENERGY?!?!!?!??!

        Returned dict is merged into the controller call in
        BaseDetectorPopup._call_add().
        """

                # >>> UI ONLY <<<
        def _none_if_empty(val):
            # NiceGUI number can be None; keep it robust if it returns '' or similar.
            if val is None:
                return None
            if isinstance(val, str) and val.strip() == '':
                return None
            return val
        
        assert self.input_as_slices is not None
        assert self.input_reduce_volume is not None
        assert self.input_x_slice is not None
        assert self.input_y_slice is not None
        assert self.input_z_slice is not None

        return {
            'as_slices': bool(self.input_as_slices.value),
            'reduce_volume': bool(self.input_reduce_volume.value),

            'x_slice': _none_if_empty(self.input_x_slice.value),
            'y_slice': _none_if_empty(self.input_y_slice.value),
            'z_slice': _none_if_empty(self.input_z_slice.value),


        }
    # --------------------------------------------------
    # RESET (NO dialog handling!)
    # --------------------------------------------------

    def close_self(self):
        """
        Reset detector-specific UI state.

        Called by:
        - DetectorPopup when switching detector types
        - Controller after successful detector creation
        """
        # >>> UI ONLY <<<
        super().close_self()

        # Reset EnergyDetector-specific fields
        assert self.input_as_slices is not None
        assert self.input_reduce_volume is not None 
        self.input_as_slices.value = False
        self.input_reduce_volume.value = False
        assert self.input_x_slice is not None
        assert self.input_y_slice is not None
        assert self.input_z_slice is not None
        self.input_x_slice.value = None
        self.input_y_slice.value = None
        self.input_z_slice.value = None



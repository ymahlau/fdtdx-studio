from typing import Any, cast
from nicegui import ui
from fdtdx_studio.ui.popups.new_pop_up import new_pop_up as NewPopUp


class BaseDetectorPopup(NewPopUp):
    """
    Base class for all detector popups.

    Responsibilities:
    - build common detector UI (name, geometry, color)
    - collect common detector parameters
    - dispatch detector creation to controller

    IMPORTANT:
    - does NOT own a dialog
    - does NOT open or close windows
    """

    # Must be overridden by subclasses (e.g. 'FIELD', 'POWER')
    DETECTOR_TYPE = None

    def __init__(self, controller, ):
        # >>> UI ONLY <<<
        # Store controller reference, but do NOT call it here
        super().__init__(controller)

        # Optional reference to the owning dialog. Set by the dialog owner
        # (see DetectorDialog wrapper) when the popup is rendered inside a
        # ui.dialog(). Do NOT touch this from the controller.
        self._dialog_owner = None

        # Button configuration:
        # clicking the button will trigger _call_add()
        self.button_label = 'Add Detector'
        self.button_function = lambda: self._call_add()

    # --------------------------------------------------
    # UI BUILDING (rendered INSIDE DetectorPopup)
    # --------------------------------------------------

    def build_dialog_inside(self, parent):
        """
        Build this detector's UI inside an external dialog container.

        This method:
        - builds layout
        - creates input fields
        - wires the Add button
        - does NOT talk to the controller
        """
        # >>> UI ONLY <<<
        with parent:
            with ui.row():

                # LEFT COLUMN: common detector parameters
                with ui.column():
                    self.build_common_ui()
                # RIGHT COLUMN: detector-specific parameters
                with ui.column():
                    self.build_detector_specific_ui()
                    
        # change standard values of size according to detector standards
        assert self.input_width is not None
        assert self.input_length is not None
        assert self.input_height is not None

        self.input_width.value = 10e-6
        self.input_length.value = 10e-6
        self.input_height.value = 0
        #Makes Sure teh first detector is also named New Detector
        assert self.input_name is not None
        self.input_name.value = 'New Detector'
        # Button wired to self._call_add() CONTROLLERANBINDUG
        self.add_button(self.button_function, self.button_label)

    def build_detector_specific_ui(self):
        """
        Hook for subclasses.

        FieldDetectorPopup / PowerDetectorPopup override this method
        to add their specific UI elements.
        """
        # >>> UI ONLY <<<
        ui.label('Detector')

    # --------------------------------------------------
    # DATA COLLECTION (UI → Python data)
    # --------------------------------------------------

    def collect_common_kwargs(self) -> dict:
        """
        Collect parameters common to ALL detectors.

        No logic here, just reading UI state.
        """

        assert self.input_name is not None
        assert self.input_length is not None
        assert self.input_width is not None
        assert self.input_height is not None
        # >>> UI ONLY <<<
        return {
            'name': self.input_name.value,
            'length': self.input_length.value,
            'width': self.input_width.value,
            'height': self.input_height.value,
            'color': self.input_color,
        }

    def collect_detector_kwargs(self) -> dict:
        """
        Hook for subclasses.

        Returns detector-specific keyword arguments.
        """
        # >>> UI ONLY <<<
        return {}

    # --------------------------------------------------
    # CONTROLLER DISPATCH (CRITICAL SECTION)
    # --------------------------------------------------

    def _call_add(self):
        """
        This method is called when the user clicks 'Add Detector'.

        This is the SINGLE point where UI hands control over
        to the controller.
        """


        if self.DETECTOR_TYPE is None:
            raise RuntimeError('DETECTOR_TYPE must be set in subclass')

        # >>> CONTROLLER ENTRY <<<
        self.controller.add_new_detector(
            detector_type=self.DETECTOR_TYPE,

            # reference passed back so controller can reset fields
            popup=self,

            # tells the controller where to list the detector in the UI
            typ='scrollarea_sim_detectors',

            # common parameters (name, geometry, color)
            **self.collect_common_kwargs(),

            # detector-specific parameters (field, average, normalize, ...)
            **self.collect_detector_kwargs(),
        )
        # Close the dialog if an owner was provided by the dialog wrapper.
        # This is the ONLY place where the popup closes the dialog.
        if getattr(self, '_dialog_owner', None) is not None:
            try:
                assert self._dialog_owner is not None
                self._dialog_owner.close()
            except Exception:
                pass

        # Reset UI state (does not close any dialog)
        self.close_self()
        # >>> CONTROLLER EXPECTS <<<
        # Controller must:
        # - interpret detector_type
        # - create the correct fdtdx detector
        # - add it to the simulation
        # - update the drawer
        # - call popup.close_self()

    # --------------------------------------------------
    # RESET (NO dialog handling!)
    # --------------------------------------------------

    def close_self(self):
        """
        Reset common detector UI fields.

        IMPORTANT:
        - does NOT close a dialog
        - does NOT call controller
        """
        # >>> UI ONLY <<<
        assert self.color_show is not None
        assert self.input_length is not None
        assert self.input_width is not None
        assert self.input_height is not None
        assert self.input_name is not None

        self.color_show.set_value('#FF0000')
        self.input_color = '#FF0000'
        self.input_length.value = 1
        self.input_width.value = 1
        self.input_height.value = 1
        self.input_name.value = 'New Detector'

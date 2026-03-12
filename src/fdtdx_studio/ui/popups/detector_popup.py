from nicegui import ui
from fdtdx_studio.ui.popups.field_detector_popup import FieldDetectorPopup
from fdtdx_studio.ui.popups.energy_detector_popup import EnergyDetectorPopup
from fdtdx_studio.ui.popups.poynting_flux_detector_popup import PoyntingFluxDetectorPopup
from fdtdx_studio.ui.popups.mode_overlap_detector_popup import ModeOverlapDetectorPopup
from fdtdx_studio.ui.popups.phasor_detector_popup import PhasorDetectorPopup


class DetectorPopup:
    """
    Dispatcher popup for all detector types.

    Responsibilities:
    - owns the dialog window
    - provides a type selector (FIELD / POWER / ...)
    - renders exactly ONE detector popup at a time
    - switches detector UI without closing the dialog

    IMPORTANT:
    - does NOT create detectors
    - does NOT call the controller directly
    """

    def __init__(self, controller):
        # Controller reference is stored but intentionally unused here
        # >>> INTENTIONALLY NO CONTROLLER <<<
        self.controller = controller

        # Registry of concrete detector popups
        # Each popup knows how to collect its own data
        # >>> UI ONLY <<<
        self.popups = {
            'FIELD': FieldDetectorPopup(controller),
            'ENERGY': EnergyDetectorPopup(controller),
            'POYNTING': PoyntingFluxDetectorPopup(controller),
            'MODE_OVERLAP': ModeOverlapDetectorPopup(controller),
            'PHASOR': PhasorDetectorPopup(controller),
        }

        # Current detector state
        self.current_type = 'FIELD'
        self.current_popup = self.popups[self.current_type]

        # UI elements owned by this class
        # >>> OWNS DIALOG <<<
        self.dialog = None
        self.type_button = None

        # Build dialog once
        self._build_dialog()

    # --------------------------------------------------
    # UI BUILDING (Dialog Owner)
    # --------------------------------------------------

    def _build_dialog(self):
        """
        Builds the detector dialog.

        This method:
        - creates the dialog window
        - places the type selector
        - creates a container for detector-specific UI
        """
        # >>> OWNS DIALOG <<<
        with ui.dialog() as self.dialog, ui.card():

            # Type selector at the top
            # >>> UI ONLY <<<
            with ui.dropdown_button('Type: FIELD').classes('w-full') as self.type_button:
                ui.item('FIELD', on_click=lambda: self._set_type('FIELD'))
                ui.item('ENERGY', on_click=lambda: self._set_type('ENERGY'))
                ui.item('POYNTING', on_click=lambda: self._set_type('POYNTING'))
                ui.item('MODE_OVERLAP', on_click=lambda: self._set_type('MODE_OVERLAP'))
                ui.item('PHASOR', on_click=lambda: self._set_type('PHASOR'))

            # Container for the active detector popup
            # >>> UI ONLY <<<
            self.content = ui.column().classes('w-full')
                        
            # Give each popup a reference to the owning dialog so the
            # popup can close the dialog at the approved point.
            for p in self.popups.values():
                setattr(p, '_dialog_owner', self.dialog)

            # Render initial detector UI
            self._render_current_popup()

    def _render_current_popup(self):
        """
        Clears and re-renders the currently selected detector popup.

        IMPORTANT:
        - does NOT create or destroy dialogs
        - only replaces UI content inside the dialog
        """
        # >>> UI ONLY <<<
        self.content.clear()
        with self.content:
            self.current_popup.build_dialog_inside(self.content)

    # --------------------------------------------------
    # TYPE SWITCHING (UI STATE MANAGEMENT)
    # --------------------------------------------------

    def _set_type(self, detector_type: str):
        """
        Switches between detector types.
        """
        if detector_type == self.current_type:
            assert self.type_button is not None
            self.type_button.close()
            return

        # Reset UI state of previous detector
        # >>> UI ONLY <<<
        self.current_popup.close_self()

        # Switch active detector
        self.current_type = detector_type
        self.current_popup = self.popups[self.current_type]
        
        # Ensure dialog owner is set (safety check)
        setattr(self.current_popup, '_dialog_owner', self.dialog)

        # Update dropdown label
        assert self.type_button is not None
        self.type_button.text = f'Type: {detector_type}'
        self.type_button.close()

        # Re-render detector-specific UI
        self._render_current_popup()

    # --------------------------------------------------
    # OPEN / CLOSE (Dialog Control)
    # --------------------------------------------------

    def open(self):
        """
        Opens the detector dialog.

        Called by LeftDrawer.
        """
        # >>> OWNS DIALOG <<<
        assert self.dialog is not None
        self.dialog.open()

    def close(self):
        """
        Closes the detector dialog.

        May be called by the controller AFTER successful creation.
        """
        # >>> OWNS DIALOG <<<
        assert self.dialog is not None
        self.dialog.close()

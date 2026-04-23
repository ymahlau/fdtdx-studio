from typing import Any, cast

from nicegui import ui

from fdtdx_studio.ui.popups.new_pop_up import new_pop_up as NewPopUp


class pop_up_new_material(NewPopUp):
    def __init__(self, controller):
        super().__init__(controller)
        self.kind_button: Any = None
        self.pop_up_new_material = None
        self.input_kind = "Scalar"
        self.build_dialog()

    def build_dialog(self):
        """building popup"""
        with ui.dialog() as self.pop_up_new_material, ui.card():
            ui.label("New Material")
            # Option for making Materials with XYZ Values
            # with ui.dropdown_button(f'Input Type: {self.input_kind}').classes('w-full') as self.kind_button:
            #  ui.item('Scalar', on_click=lambda: self.set_kind('Scalar'))
            #  ui.item('XYZ Values', on_click=lambda: self.set_kind('XYZ Values'))

            cast(Any, self.make_source_mode_options)()

    def set_kind(self, kind):
        self.input_kind = kind
        if self.kind_button:
            self.kind_button.close()
            self.kind_button.text = f"Input Type: {kind}"
        self.make_source_mode_options.refresh()

    def open_new_material_popup(self):
        assert self.pop_up_new_material is not None
        self.pop_up_new_material.open()

    def add_material(self, Permittivity, Permeability, Electrical_conductivity, Magnetic_conductivity, name):
        """adds material with given settings"""
        assert self.pop_up_new_material is not None
        self.pop_up_new_material.close()
        self.pop_up_new_material.on(
            "hide",
            lambda: (
                self.controller.add_material(
                    Permittivity, Permeability, Electrical_conductivity, Magnetic_conductivity, name
                ),
                ui.timer(0, lambda: self.controller.project.localmaterial_save(), once=True),
            ),
        )
        ui.notify("Material added successfully", position="bottom", color="green")

    def isFloat(self, element: "str") -> bool:
        """check if an input value is float"""
        if not element:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def checkButton(self, permittivity, permeability, e_conductivity, m_conductivity, name, label):
        obj = self.controller.model.material.material_exists_settings(
            permeability=permeability,
            permittivity=permittivity,
            e_conductivity=e_conductivity,
            m_conductivity=m_conductivity,
        )
        if obj == -1:
            self.add_material(
                Permittivity=permittivity,
                Permeability=permeability,
                Electrical_conductivity=e_conductivity,
                Magnetic_conductivity=m_conductivity,
                name=name,
            )
        else:
            label.set_text("Material with the same settings already exists: " + obj[0])
            label.set_visibility(True)

    @ui.refreshable
    def make_source_mode_options(self):
        """Makes a refreshable part of the Dialog that changes based on which Input Type is selected"""
        # Different Input types have not been implemented completely according to the TNT´s wishes. The Code is there and can be used if needed.
        name = "Unknown Material"

        def setName(new):
            nonlocal name
            name = new

        if self.input_kind == "Scalar":
            ui.label("Name").style("font-size: 13px; font-weight: bold;")
            ui.input(value="Unknown Material", on_change=lambda e: setName(e.value))
            ui.label("Permittivity").style("font-size: 13px; font-weight: bold;")
            pitty = ui.number(value=1.0, min=0, step=0.1, validation=self._validate).classes("w-1/2")
            ui.label("Permeability").style("font-size: 13px; font-weight: bold;")
            perm = ui.number(value=1.0, min=0, step=0.1, validation=self._validate).classes("w-1/2")
            ui.label("Electric_conductivity").style("font-size: 13px; font-weight: bold;")
            e_cond = ui.number(value=0.0, min=0, max=1.0, step=0.1, validation=self._validate_conductivity).classes(
                "w-1/2"
            )
            ui.label("Magnetic_conductivity").style("font-size: 13px; font-weight: bold;")
            m_cond = ui.number(value=0.0, min=0, max=1.0, step=0.1, validation=self._validate_conductivity).classes(
                "w-1/2"
            )
            Error = ui.label("Material with the same Settings already exists").style("color: red; font-size: 13px;")
            Error.set_visibility(False)
            self.save = ui.button(
                "Save",
                on_click=lambda: self.checkButton(
                    permittivity=pitty.value,
                    permeability=perm.value,
                    e_conductivity=e_cond.value,
                    m_conductivity=m_cond.value,
                    name=name,
                    label=Error,
                ),
            )
        else:
            ui.label("Name").style("font-size: 13px; font-weight: bold;")
            ui.input(value="Unknown Material", on_change=lambda e: setName(e.value))
            ui.label("Permittivity").style("font-size: 13px; font-weight: bold;")
            with ui.row().classes("w-full flex-nowrap gap-1") as permittivity:
                pittyX = ui.number("x", value=1.0, min=0, step=0.1, validation=self._validate).classes("w-1/6")
                pittyY = ui.number("y", value=1.0, min=0, step=0.1, validation=self._validate).classes("w-1/6")
                pittyZ = ui.number("z", value=1.0, min=0, step=0.1, validation=self._validate).classes("w-1/6")
            ui.label("Permeability").style("font-size: 13px; font-weight: bold;")
            with ui.row().classes("w-full flex-nowrap gap-1") as permeability:
                permX = ui.number("x", value=1.0, min=0, step=0.1, validation=self._validate).classes("w-1/6")
                permY = ui.number("y", value=1.0, min=0, step=0.1, validation=self._validate).classes("w-1/6")
                permZ = ui.number("z", value=1.0, min=0, step=0.1, validation=self._validate).classes("w-1/6")
            ui.label("Electric_conductivity").style("font-size: 13px; font-weight: bold;")
            with ui.row().classes("w-full flex-nowrap gap-1") as electric_conductivity:
                e_condX = ui.number(
                    "x", value=0.0, min=0, max=1.0, step=0.1, validation=self._validate_conductivity
                ).classes("w-1/6")
                e_condY = ui.number(
                    "y", value=0.0, min=0, max=1.0, step=0.1, validation=self._validate_conductivity
                ).classes("w-1/6")
                e_condZ = ui.number(
                    "z", value=0.0, min=0, max=1.0, step=0.1, validation=self._validate_conductivity
                ).classes("w-1/6")
            ui.label("Magnetic_conductivity").style("font-size: 13px; font-weight: bold;")
            with ui.row().classes("w-full flex-nowrap gap-1") as magnetic_conductivity:
                m_condX = ui.number(
                    "x", value=0.0, min=0, max=1.0, step=0.1, validation=self._validate_conductivity
                ).classes("w-1/6")
                m_condY = ui.number(
                    "y", value=0.0, min=0, max=1.0, step=0.1, validation=self._validate_conductivity
                ).classes("w-1/6")
                m_condZ = ui.number(
                    "z", value=0.0, min=0, max=1.0, step=0.1, validation=self._validate_conductivity
                ).classes("w-1/6")
            self.save = ui.button(
                "Save",
                on_click=lambda: self.add_material(
                    [pittyX.value, pittyY.value, pittyZ.value],
                    [permX.value, permY.value, permZ.value],
                    [e_condX.value, e_condY.value, e_condZ.value],
                    [m_condX.value, m_condY.value, m_condZ.value],
                    name,
                ),
            )

    def _validate(self, value):
        """validates time and resolution inputs"""
        try:
            if self.isFloat(value):
                if value > 0:
                    self.save.enable()
                    return None

                else:
                    self.save.disable()
                    return "Number must be greater than zero"
            else:
                self.save.disable()
                return "Input must be a number"
        except (TypeError, ValueError):
            self.save.disable()
            return "Input must be a number"

    def _validate_conductivity(self, value):
        """validates conductivity inputs"""
        try:
            if self.isFloat(value):
                if value < 1 or value > 0:
                    self.save.enable()
                    return None
                else:
                    self.save.disable()
                    return "Number must be between 0 and 1"
            else:
                self.save.disable()
                return "Input must be a number"
        except (TypeError, ValueError):
            self.save.disable()
            return "Input must be a number"

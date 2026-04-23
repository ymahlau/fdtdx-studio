from typing import TypeAlias, cast

from nicegui import ui

tooltip_explanation = {}

ConstraintAtom: TypeAlias = str | int | float | bool | tuple[int, ...]
ConstraintValue: TypeAlias = ConstraintAtom | tuple[ConstraintAtom, ...]


class Pop_up_constraints:
    def __init__(self, ocp):
        self.con_value = {}
        self.pop_up = ui.dialog()
        self.stepper = None
        self.back_cancel = None
        self.canback = False
        self.ocp = ocp
        self.other_object_list = []

    def open_pop_up(
        self,
        typ,
        other_object_list,
        Con={},
    ):
        self.other_object_list = other_object_list
        self.remove_tuple(Con, typ)
        self.pop_up.clear()
        self.canback = False
        with self.pop_up, ui.card():
            match typ:
                case "SizeExtensionConstraint":
                    self.build_size_ex_con()
                case "PositionConstraint":
                    self.build_pos_con()
                case "GridCoordinateConstraint":
                    self.build_grid_con()
                case "SizeConstraint":
                    self.build_size_con()
                case "new_con":
                    self.canback = True
                    self.build_make_new_con()
        self.pop_up.open()

    def name_for_new(self):
        x = 0
        name = "new_Constraint"

        while name in self.other_object_list:
            name = "new_Constraint_" + str(x)
            x += 1

        return name

    def remove_tuple(self, Con, typ):
        self.con_value: dict[str, str | int | float | bool | tuple[int, ...] | None] = {
            "key": self.name_for_new(),
            "type": "not set",
        }
        a = iter(range(3))
        coor = ("x", "y", "z")
        for key, value in Con.items():
            if key == "axes":
                for i in range(len(coor)):
                    self.con_value[(key + "_" + coor[i])] = True if i in value else False
            elif isinstance(value, (list, tuple)) and key != "axes":
                for i in range(len(coor)):
                    self.con_value[(key + "_" + coor[i])] = value[next(a, 0)] if i in Con["axes"] else None
                a = iter(range(3))  # to reset the internal next counter
            else:
                self.con_value[key] = value

    def get_val_with_tuple(self):
        result: dict[str, ConstraintValue] = {"new": self.canback}
        coor = ("_x", "_y", "_z")
        for key, value in self.con_value.items():
            if value is not None:
                if any(item in key for item in coor):
                    result[key[:-2]] = (
                        (value,) if key[:-2] not in result.keys() else cast(tuple, result[key[:-2]]) + (value,)
                    )
                else:
                    result[key] = value
        if result["type"] != "SizeExtensionConstraint":
            axes_list = cast(list | tuple, result["axes"])
            result.update({"axes": tuple(i for i in range(len(axes_list)) if axes_list[i])})
        return result

    def close_pop_up(self):
        self.ocp.save_con(self.get_val_with_tuple())
        self.pop_up.close()

    def build_pos_con(self):
        ui.select(
            options=self.other_object_list,
            with_input=True,
            on_change=lambda e: self.con_value.update({"other_object": e.value}),
        ).bind_value(self.con_value, "other_object")

        with ui.row():
            ui.label("Axes:")
            show_x = ui.checkbox(text="X").bind_value(self.con_value, "axes_x")
            show_y = ui.checkbox(text="Y").bind_value(self.con_value, "axes_y")
            show_z = ui.checkbox(text="Z").bind_value(self.con_value, "axes_z")

            with ui.row().classes("w-full flex-nowrap gap-1"):
                # Column for Label of what this stat is
                with ui.column().classes("pt-3"):
                    ui.label("Object Position:").classes("h-[56px] flex items-center")
                    ui.label("Other Object Position:").classes("h-[56px] flex items-center")
                    ui.label("Margins:").classes("h-[56px] flex items-center")
                    ui.label("Grid Margins:").classes("h-[56px] flex items-center")

                    # Column for X-con_value
                with ui.column().bind_visibility_from(show_x, "value").classes("flex-1").props("dense"):
                    ui.number().bind_value(self.con_value, "object_positions_x")
                    ui.number().bind_value(self.con_value, "other_object_positions_x")
                    ui.number().bind_value(self.con_value, "margins_x")
                    ui.number().bind_value(self.con_value, "grid_margins_x")

                    # Column for Y-con_value
                with (
                    ui.column().bind_visibility_from(show_y, "value").classes("w-1/4").classes("flex-1").props("dense")
                ):
                    ui.number().bind_value(self.con_value, "object_positions_y")
                    ui.number().bind_value(self.con_value, "other_object_positions_y")
                    ui.number().bind_value(self.con_value, "margins_y")
                    ui.number().bind_value(self.con_value, "grid_margins_y")

                    # Column for Z-con_value
                with (
                    ui.column().bind_visibility_from(show_z, "value").classes("w-1/4").classes("flex-1").props("dense")
                ):
                    ui.number().bind_value(self.con_value, "object_positions_z")
                    ui.number().bind_value(self.con_value, "other_object_positions_z")
                    ui.number().bind_value(self.con_value, "margins_z")
                    ui.number().bind_value(self.con_value, "grid_margins_z")

        with ui.row():
            ui.button("Save Changes", on_click=self.close_pop_up)
            if self.canback:
                assert self.stepper is not None
                ui.button(text="Back", on_click=self.stepper.previous).props("flat")
            else:
                ui.button(text="Cancel", on_click=self.close_pop_up)

    def build_grid_con(self):
        with ui.row():
            ui.label("Axes:")
            show_x = ui.checkbox(text="X").bind_value(self.con_value, "axes_x")
            show_y = ui.checkbox(text="Y").bind_value(self.con_value, "axes_y")
            show_z = ui.checkbox(text="Z").bind_value(self.con_value, "axes_z")

        with ui.row():
            with ui.column():
                ui.label("Sides:").classes("h-[52px] flex items-center")
                ui.label("Coordinates:").classes("h-[60px] flex items-center")

            with ui.column().classes("flex-1").props("dense").bind_visibility_from(show_x, "value"):
                ui.toggle({0: "-", 1: "+"}).bind_value(
                    self.con_value,
                    "sides_x",
                    forward=lambda v: None if v is None else ("-" if v == 0 else "+"),
                    backward=lambda v: None if v is None else (0 if v == "-" else 1),
                )
                ui.number().bind_value(self.con_value, "coordinates_x")

            with ui.column().classes("flex-1").props("dense").bind_visibility_from(show_y, "value"):
                ui.toggle({0: "-", 1: "+"}).bind_value(
                    self.con_value,
                    "sides_y",
                    forward=lambda v: None if v is None else ("-" if v == 0 else "+"),
                    backward=lambda v: None if v is None else (0 if v == "-" else 1),
                )
                ui.number().bind_value(self.con_value, "coordinates_y")

            with ui.column().classes("flex-1").props("dense").bind_visibility_from(show_z, "value"):
                ui.toggle({0: "-", 1: "+"}).bind_value(
                    self.con_value,
                    "sides_z",
                    forward=lambda v: None if v is None else ("-" if v == 0 else "+"),
                    backward=lambda v: None if v is None else (0 if v == "-" else 1),
                )
                ui.number().bind_value(self.con_value, "coordinates_z")

        with ui.row():
            ui.button("Save Changes", on_click=self.close_pop_up)
            if self.canback:
                assert self.stepper is not None
                ui.button(text="Back", on_click=self.stepper.previous).props("flat")
            else:
                ui.button(text="Cancel", on_click=self.close_pop_up)

    def build_size_con(self):
        ui.select(
            options=self.other_object_list,
            with_input=True,
            on_change=lambda e: self.con_value.update({"other_object": e.value}),
        ).bind_value(self.con_value, "other_object")

        with ui.row():
            ui.label("Axes:")
            show_x = ui.checkbox(text="X", value=True).bind_value(self.con_value, "axes_x")
            show_y = ui.checkbox(text="Y", value=True).bind_value(self.con_value, "axes_y")
            show_z = ui.checkbox(text="Z", value=True).bind_value(self.con_value, "axes_z")

        with ui.row().classes("w-full flex-nowrap gap-1"):
            # Column for Label of what this stat is
            with ui.column().classes("pt-3"):
                ui.label("other Axes:").classes("h-[56px] flex items-center")
                ui.label("Proportions:").classes("h-[56px] flex items-center")
                ui.label("Offset:").classes("h-[56px] flex items-center")
                ui.label("Grid Offset:").classes("h-[56px] flex items-center")

                # Column for X-con_value
            with ui.column().bind_visibility_from(show_x, "value").classes("flex-1").props("dense"):
                ui.number().bind_value(
                    self.con_value, "other_axes_x", forward=lambda v: int(v) if v is not None else None
                )
                ui.number().bind_value(self.con_value, "proportions_x")
                ui.number().bind_value(self.con_value, "offsets_x")
                ui.number().bind_value(self.con_value, "grid_offset_x")

                # Column for Y-con_value
            with ui.column().bind_visibility_from(show_y, "value").classes("w-1/4").classes("flex-1").props("dense"):
                ui.number().bind_value(
                    self.con_value, "other_axes_y", forward=lambda v: int(v) if v is not None else None
                )
                ui.number().bind_value(self.con_value, "proportions_y")
                ui.number().bind_value(self.con_value, "offsets_y")
                ui.number().bind_value(self.con_value, "grid_offset_y")

                # Column for Z-con_value
            with ui.column().bind_visibility_from(show_z, "value").classes("w-1/4").classes("flex-1").props("dense"):
                ui.number().bind_value(
                    self.con_value, "other_axes_z", forward=lambda v: int(v) if v is not None else None
                )
                ui.number().bind_value(self.con_value, "proportions_z")
                ui.number().bind_value(self.con_value, "offsets_z")
                ui.number().bind_value(self.con_value, "grid_offset_z")

        with ui.row():
            ui.button("Save Changes", on_click=self.close_pop_up)
            if self.canback:
                assert self.stepper is not None
                ui.button(text="Back", on_click=self.stepper.previous).props("flat")
            else:
                ui.button(text="Cancel", on_click=self.close_pop_up)

    def build_size_ex_con(self):
        ui.select(
            options=self.other_object_list,
            with_input=True,
            on_change=lambda e: self.con_value.update({"other_object": e.value}),
        ).bind_value(self.con_value, "other_object")

        with ui.row():
            with ui.column():
                ui.label("Axis:").classes("h-[56px] flex items-center")
                ui.label("Direction:").classes("h-[56px] flex items-center")
                ui.label("Other Position:").classes("h-[56px] flex items-center")
                ui.label("Offset:").classes("h-[56px] flex items-center")
                ui.label("Grid Offset:").classes("h-[56px] flex items-center")

            with ui.column():
                ui.radio({0: "x", 1: "y", 2: "z"}).props("inline").bind_value(self.con_value, "axis")
                ui.toggle({0: "-", 1: "+"}).props("inline").bind_value(
                    self.con_value,
                    "direction",
                    forward=lambda v: None if v is None else ("-" if v == 0 else "+"),
                    backward=lambda v: None if v is None else (0 if v == "-" else 1),
                )
                ui.number().bind_value(self.con_value, "other_position")
                ui.number().bind_value(self.con_value, "offset")
                ui.number().bind_value(self.con_value, "grid_offset")

        with ui.row():
            ui.button("Save Changes", on_click=self.close_pop_up)
            if self.canback:
                assert self.stepper is not None
                ui.button(text="Back", on_click=self.stepper.previous).props("flat")
            else:
                ui.button(text="Cancel", on_click=self.close_pop_up)

    def build_make_new_con(self):
        the_list = ["SizeConstraint", "PositionConstraint", "SizeExtensionConstraint", "GridCoordinateConstraint"]
        with ui.stepper().props("vertical").classes("w-full") as self.stepper:
            with ui.step("choose Constrains Typ"):
                ui.label("Choose the Typ of Constrains you want to make")
                ui.radio(the_list).props("vertikal").bind_value_to(self.con_value, "type")
                ui.button(
                    "Next",
                    on_click=lambda: (
                        self.create_in_step(step2)
                        if self.con_value["type"] in the_list
                        else ui.notification("you need to pick a ConstraintTyp")
                    ),
                )
            with ui.step("Edit Constrain") as step2:
                pass

        ui.button(text="Cancel", on_click=self.pop_up.close)

    def create_in_step(self, the_step):
        the_step.clear()
        with the_step:
            match self.con_value["type"]:
                case "SizeConstraint":
                    self.build_size_con()
                case "PositionConstraint":
                    self.build_pos_con()
                case "SizeExtensionConstraint":
                    self.build_size_ex_con()
                case "GridCoordinateConstraint":
                    self.build_grid_con()

        assert self.stepper is not None
        self.stepper.next()

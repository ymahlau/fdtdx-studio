from dataclasses import replace

from fdtdx import GridCoordinateConstraint, PositionConstraint, SizeConstraint, SizeExtensionConstraint


class Constraints:
    def __init__(self) -> None:
        self.constraints: dict = {}
        self._cons: int = 0

    # Functions to add Constraints
    def uniqueName(self, key: str | None = None):
        self._cons += 1
        return key if key and "new_" not in key else f"Constraint_{self._cons}"

    def add_pos_con(
        self,
        obj: str,
        other_object: str,
        axes: tuple[int, ...],
        object_positions: tuple[float, ...],
        other_object_positions: tuple[float, ...],
        margins: tuple[float, ...] = (),
        grid_margins: tuple[int, ...] = (),
        key: str | None = None,
    ):
        new = {
            self.uniqueName(key): PositionConstraint(
                object=obj,
                other_object=other_object,
                axes=axes,
                object_positions=object_positions,
                other_object_positions=other_object_positions,
                margins=margins,
                grid_margins=grid_margins,
            )
        }
        self.constraints.update(new)

    def add_size_con(
        self,
        obj: str,
        other_object: str,
        axes: tuple[int, ...],
        other_axes: tuple[int, ...],
        proportions: tuple[float, ...],
        offsets: tuple[float, ...],
        grid_offset: tuple[int, ...],
        key: str | None = None,
    ):
        new = {
            self.uniqueName(key): SizeConstraint(
                object=obj,
                other_object=other_object,
                axes=axes,
                other_axes=other_axes,
                proportions=proportions,
                offsets=offsets,
                grid_offsets=grid_offset,
            )
        }
        self.constraints.update(new)

    def add_size_ex_con(
        self,
        obj: str,
        other_object: str | None,
        axis: int,
        direction,
        other_position: float,
        offset: float,
        grid_offset: int,
        key: str | None = None,
    ):
        new = {
            self.uniqueName(key): SizeExtensionConstraint(
                object=obj,
                other_object=other_object,
                axis=axis,
                direction=direction,
                other_position=other_position,
                offset=offset,
                grid_offset=grid_offset,
            )
        }
        self.constraints.update(new)

    def add_grid_con(
        self, obj: str, axes: tuple[int, ...], sides, coordinates: tuple[int, ...], key: str | None = None
    ):
        new = {
            self.uniqueName(key): GridCoordinateConstraint(object=obj, axes=axes, sides=sides, coordinates=coordinates)
        }
        self.constraints.update(new)

    # Deletes a given Constraint
    def delete_constraint(self, key: str):
        """Deletes a constraint"""
        self.constraints.pop(key)

    def get_obj_constraints(self, object_name: str):
        """Returns all the Constraints that affect a given Object"""
        return [
            {**vars(v), "type": type(v).__name__, "key": k}
            for k, v in self.constraints.items()
            if object_name == v.object and "hidden" not in k
        ]

    def delete_obj_constraints(self, object_name: str):
        keys = []
        for k, v in self.constraints.items():
            if v.object == object_name:
                keys.append(k)
            elif not isinstance(v, GridCoordinateConstraint):
                if v.other_object == object_name:
                    keys.append(k)
        for k in keys:
            self.constraints.pop(k)

    def list_to_constraints(self, liste):
        for item in liste:
            if isinstance(item, list):
                if item[0] != "NoneGiven":
                    self.constraints[self.uniqueName(item[0])] = item[1]
            else:
                self.constraints[self.uniqueName()] = item

    # Maybe just dont give them names to reduce work
    def update_object_names(self, old, new):
        for k, v in self.constraints.items():
            if v.object == old:
                self.constraints[k] = replace(v, object=new)
            elif not isinstance(v, GridCoordinateConstraint):
                if v.other_object == old:
                    self.constraints[k] = replace(v, other_object=new)

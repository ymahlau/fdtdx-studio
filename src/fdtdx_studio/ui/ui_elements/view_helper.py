from nicegui.element import Element

class ViewHelper(Element, component='view_helper.js'):
    def __init__(self, source_scene) -> None:
        super().__init__()
        self._props['sourceSceneId'] = source_scene.id

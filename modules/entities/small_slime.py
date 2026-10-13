from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.registry import Enemies
    from modules.world import GridCoordinate

class SmallSlime:
    def __init__(self, coordinate: GridCoordinate, _type: Enemies):
        self.coordinate = coordinate
        self._type      = _type

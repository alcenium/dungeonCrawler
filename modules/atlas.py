import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygame import Surface

class Atlas:
    """
    Mỗi vật thể của class chứa tọa độ các sprite được gán theo tên,
    và atlas(hình ảnh) chứa toàn bộ sprite trong set đó
    """
    def __init__(self, atlas_file: str, atlas_index_file: str, tile_size: int) -> None:
        self.tile_size = tile_size
        self.atlas_index_file = atlas_index_file

        self.indexes: dict[str, tuple[int, int]] = {}
        self.image: Surface = pygame.image.load(atlas_file).convert()

        self.extract_indexes()

    def get(self, item_name:str) -> Surface:
        """ Trả về subsurface chứa sprite được yêu cầu """
        tile_pos: tuple[int, int] = self.indexes[item_name]
        return self.image.subsurface(tile_pos[1] * self.tile_size,
                                     tile_pos[0] * self.tile_size,
                                     self.tile_size,
                                     self.tile_size)

    def debug(self) -> None:
        """ Hiển thị danh sách tên các sprite: tọa độ """
        for key, value in self.indexes.items():
            print(f"{key}: {value}")

    def extract_indexes(self) -> None:
        """
        Mở file index và lưu tất cả tọa độ của các sprite vào indexes
        'rouge': (1, 1)
        """
        with open(self.atlas_index_file) as file:
            column = 0
            row    = 0

            lines = file.read().splitlines()
            for line in lines:
                if len(line) != 0:
                    name = line.split(sep='.')[2]
                    self.indexes[name.lstrip()] = (row, column)
                    column += 1
                else:
                    column = 0
                    row += 1

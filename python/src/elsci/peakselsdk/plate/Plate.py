import json


class PlateLocation:
    def __init__(self, row: int, col: int):
        self.row: int = row
        self.col: int = col

    def __eq__(self, that) -> bool:
        if not isinstance(that, PlateLocation):
            return False
        return self.row == that.row and self.col == that.col

    def __str__(self) -> str:
        return json.dumps(self, default=vars)
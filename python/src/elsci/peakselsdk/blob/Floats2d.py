class Floats2d:
    def __init__(self, x: tuple[float, ...], y: tuple[float, ...]):
        if len(x) != len(y):
            raise Exception(f"Different number of values in x ({len(x)}) and y ({len(y)}) in 2D-signal")
        self.x: tuple[float, ...] = x
        self.y: tuple[float, ...] = y

    def __len__(self):
        return len(self.x)
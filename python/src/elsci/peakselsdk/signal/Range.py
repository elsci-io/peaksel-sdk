class FloatRange:
    def __init__(self, lower: float, upper: float):
        self.lower: float = lower
        self.upper: float = upper

    @staticmethod
    def from_json(json: dict) -> "FloatRange":
        return FloatRange(**json)

    @staticmethod
    def from_jsons(jsons: list[dict]) -> "list[FloatRange]":
        result: list[FloatRange] = []
        for json in jsons:
            result.append(FloatRange.from_json(json))
        return result
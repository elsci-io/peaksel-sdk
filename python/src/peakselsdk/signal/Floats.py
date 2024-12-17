class FloatPoint:
    def __init__(self, index: int, value: float):
        self.index: float = index
        self.value: float = value

    @staticmethod
    def from_json(json: dict) -> "FloatPoint":
        return FloatPoint(**json)

    @staticmethod
    def from_jsons(jsons: list[dict]) -> "list[FloatPoint]":
        result: list[FloatPoint] = []
        for json in jsons:
            result.append(FloatPoint.from_json(json))
        return result
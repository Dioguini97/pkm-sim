class Ability:
    def __init__(self, name: str, description: str, id: int):
        self.name = name
        self.description = description
        self.id = id

    def use(self):
        return f"{self.name} used with power {self.power}!"
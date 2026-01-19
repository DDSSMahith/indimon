class Move:
    def __init__(self, name, move_type, power, accuracy, category):
        self.name = name
        self.type = move_type
        self.power = power
        self.accuracy = accuracy
        self.category = category

    def is_damaging(self):
        return self.power > 0

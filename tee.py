# tee character will be updated sooner or later 


class Tee:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def __str__(self):
        return f"{self.name} (HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense})"
            
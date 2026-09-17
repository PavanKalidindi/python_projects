class GameCharacter:
    def __init__(self, name):
        self._name = name
        self.health = 100
        self.mana = 50
        self._level = 1

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_health):
        if new_health < 0:
            self._health = 0
            return
        if new_health > 100:
            self._health = 100
            return
        self._health = new_health

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, new_mana):
        if new_mana < 0:
            self._mana = 0
            return
        if new_mana > 50:
            self._mana = 50
            return
        self._mana = new_mana

    @property
    def level(self):
        return self._level

    def __str__(self):
        s = f"Name: {self._name}\n"
        s += f"Level: {self.level}\n"
        s += f"Health: {self.health}\n"
        s += f"Mana: {self.mana}"
        return s

    def level_up(self):
        self._level += 1
        self.health = 100
        self.mana = 50
        print(f"{self._name} leveled up to {self.level}!")
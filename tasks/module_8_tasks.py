class Food:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __repr__(self):
        return f"Name: {self.name}; Kind: {self.kind}"

    def describe(self):
        print(f"Name: {self.name}; Kind: {self.kind}")


class Meat(Food):
    def cook(self):
        print("Cooking the meat")


class Fruit(Food):
    def clean(self):
        print("Cleaning the fruit")


banana = Fruit("banana", "fruity")
print(banana)

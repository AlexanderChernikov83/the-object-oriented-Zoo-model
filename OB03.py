import json


# ---------- 1. Базовый класс Animal ----------
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        return "Some generic animal sound"

    def eat(self):
        return f"{self.name} ест пищу."


# ---------- 2. Подклассы животных ----------
class Bird(Animal):
    def __init__(self, name, age, can_fly=True):
        super().__init__(name, age)
        self.can_fly = can_fly

    def make_sound(self):
        return "Чирик-чирик"


class Mammal(Animal):
    def __init__(self, name, age, fur_color="brown"):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        return "Р-р-р-р"


class Reptile(Animal):
    def __init__(self, name, age, is_venomous=False):
        super().__init__(name, age)
        self.is_venomous = is_venomous

    def make_sound(self):
        return "Шшшшш..."


# ---------- 3. Полиморфизм ----------
def animal_sound(animals):
    print("\n🔊 Звуки животных:")
    for animal in animals:
        print(f"{animal.name} говорит: {animal.make_sound()}")


# ---------- 4. Класс Zoo (композиция) ----------
class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def add_staff(self, staff_member):
        self.staff.append(staff_member)

    def show_info(self):
        print(f"\n📍 Зоопарк: {self.name}")
        print("Животные:")
        for animal in self.animals:
            print(f" - {animal.name}, {animal.age} лет, говорит: {animal.make_sound()}")
        print("Сотрудники:")
        for staff in self.staff:
            print(f" - {staff.name} ({staff.__class__.__name__})")

    def save_to_file(self, filename):
        data = {
            "zoo_name": self.name,
            "animals": [
                {
                    "type": animal.__class__.__name__,
                    "name": animal.name,
                    "age": animal.age
                } for animal in self.animals
            ],
            "staff": [
                {
                    "type": staff.__class__.__name__,
                    "name": staff.name
                } for staff in self.staff
            ]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.name = data["zoo_name"]
            self.animals = []
            self.staff = []

            for a in data["animals"]:
                if a["type"] == "Bird":
                    self.animals.append(Bird(a["name"], a["age"]))
                elif a["type"] == "Mammal":
                    self.animals.append(Mammal(a["name"], a["age"]))
                elif a["type"] == "Reptile":
                    self.animals.append(Reptile(a["name"], a["age"]))

            for s in data["staff"]:
                if s["type"] == "ZooKeeper":
                    self.staff.append(ZooKeeper(s["name"]))
                elif s["type"] == "Veterinarian":
                    self.staff.append(Veterinarian(s["name"]))


# ---------- 5. Классы сотрудников ----------
class ZooKeeper:
    def __init__(self, name):
        self.name = name

    def feed_animal(self, animal):
        print(f"{self.name} кормит {animal.name}. {animal.eat()}")


class Veterinarian:
    def __init__(self, name):
        self.name = name

    def heal_animal(self, animal):
        print(f"{self.name} лечит {animal.name}. {animal.name} теперь чувствует себя лучше!")


# ---------- Пример использования ----------
if __name__ == "__main__":
    # Создаём зоопарк
    my_zoo = Zoo("Зооленд")

    # Добавляем животных
    my_zoo.add_animal(Bird("Попугай", 2))
    my_zoo.add_animal(Mammal("Тигр", 5))
    my_zoo.add_animal(Reptile("Змея", 3, is_venomous=True))

    # Добавляем сотрудников
    zookeeper = ZooKeeper("Иван")
    vet = Veterinarian("Ольга")
    my_zoo.add_staff(zookeeper)
    my_zoo.add_staff(vet)

    # Информация о зоопарке
    my_zoo.show_info()

    # Полиморфизм: звуки животных
    animal_sound(my_zoo.animals)

    # Действия сотрудников
    zookeeper.feed_animal(my_zoo.animals[1])
    vet.heal_animal(my_zoo.animals[2])

    # Сохраняем в файл
    my_zoo.save_to_file("zoo_data.json")
    print("\n📁 Данные зоопарка сохранены.")

    # Загружаем в новый объект
    loaded_zoo = Zoo("Пусто")
    loaded_zoo.load_from_file("zoo_data.json")
    print("\n📥 Загруженные данные:")
    loaded_zoo.show_info()

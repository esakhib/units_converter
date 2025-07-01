from categories import UnitCategory
from converter import UnitConverter, output_result
import re,ast
from collections.abc import Iterable
def get_categories():
    return [cls for cls in UnitCategory.__subclasses__() if cls.get_units()]


def choose_category(categories_classes):
    while True:
        print("Выберите категорию единиц измерения (или введите 'stop' для выхода):")
        for i, category in enumerate(categories_classes, start=1):
            print(f"{i}. {str(category())}")

        raw = input("Введите номер категории: ").strip()
        if raw.lower() == "stop":
            return None

        try:
            category_choice = int(raw)
            if 1 <= category_choice <= len(categories_classes):
                return categories_classes[category_choice - 1]
            else:
                print("Выберите правильную категорию.")
        except ValueError:
            print("Пожалуйста, введите корректное значение.")


def choose_units(selected_category):
    units = selected_category.get_units()
    print("Выберите единицу измерения:")
    for i, unit in enumerate(units, start=1):
        print(f"{i}. {unit.abbr}")
    return units


def main():
    source_unit = None
    target_unit = None
    values = None
    categories_classes = get_categories()

    while True:
        selected_category = choose_category(categories_classes)
        if selected_category is None:
            print("Завершение работы")
            break

        print(f"Вы выбрали категорию: {str(selected_category())}")

        units = choose_units(selected_category)

        while True:
            try:
                from_unit_value = int(input("Введите номер исходной единицы: "))
                if from_unit_value < 1 or from_unit_value > len(units):
                    print("Выберите номер из предложенных единиц.")
                    continue
                source_unit = units[from_unit_value - 1]

                to_unit_value = int(input("Введите номер целевой единицы: "))
                if to_unit_value < 1 or to_unit_value > len(units):
                    print("Выберите номер из предложенных единиц.")
                    continue
                target_unit = units[to_unit_value - 1]

                raw = input("Введите количество (или несколько значений, любой Python-литерал или через пробел/запятую): ")
                s = raw.strip()

                try:
                    literal = ast.literal_eval(s)
                    if isinstance(literal,(int,float)):
                        values = [float(literal)]
                    elif isinstance(literal,Iterable) and not isinstance(literal,(str,bytes)):
                        values = [float(x) for x in literal]
                    else:
                        raise ValueError
                except(ValueError,SyntaxError):
                    parts = re.split(r"[/s,]+",raw.strip())
                    values = [float(p) for p in parts if p]


                if not values:
                    print("Введите хотя бы одно значение.")
                    continue

                break
            except ValueError:
                print("Пожалуйста, введите корректное значение.")

        result = UnitConverter.convert_unit(source_unit, target_unit, values)
        output_result(source_unit, target_unit, values, result)


if __name__ == "__main__":
    main()
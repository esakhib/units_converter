import inspect
from unit_converter import UnitConverter, Pressure, VolumeFlowRate, UnitCategory, output_result


def main():
    categories = [cls for _, cls in inspect.getmembers(__import__(__name__), inspect.isclass)
                  if issubclass(cls, UnitCategory) and cls is not UnitCategory]

    # Выбор категории
    while True:
        source_unit = None
        target_unit = None
        quantity = None

        print("Выберите категорию единиц измерения:")
        for i, category in enumerate(categories, start=1):
            print(f"{i}. {category.__name__}")

        try:
            category_choice = int(input("Введите номер категории: "))
            if 1 <= category_choice <= len(categories):
                selected_category = categories[category_choice - 1]
                break
            else:
                print("Выберите правильную категорию.")
        except ValueError:
            print("Пожалуйста, введите корректное значение.")

    print(f"Вы выбрали категорию: {selected_category.__name__}")

    while True:
        print("Выберите единицу измерения:")
        units = selected_category.get_units()

        for i, unit in enumerate(units, start=1):
            print(f"{i}. {unit.symbol}")

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

            user_input = input("Введите количество (или несколько значений через пробел): ")
            values = list(map(float, user_input.split()))

            if not values:
                print("Введите хотя бы одно значение.")
                continue

            quantity = values
            break
        except ValueError:
            print("Пожалуйста, введите корректное значение.")

    result = UnitConverter.convert_unit(source_unit, target_unit, quantity)
    output_result(source_unit, target_unit, quantity, result)


if __name__ == "__main__":
    main()

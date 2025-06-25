from unit_converter import UnitConverter, PressureUnitCategory, VolumeFlowRateUnitCategory, VolumeRationsUnitCategory, \
    output_result


def get_categories():
    return list((PressureUnitCategory, VolumeFlowRateUnitCategory, VolumeRationsUnitCategory))


def choose_category(categories_classes):
    while True:
        print("Выберите категорию единиц измерения:")
        for i, category in enumerate(categories_classes, start=1):
            print(f"{i}. {category.__name__}")

        try:
            category_choice = int(input("Введите номер категории: "))
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
        print(f"{i}. {unit.symbol}")
    return units


def main():
    source_unit = None
    target_unit = None
    values = None
    categories_classes = get_categories()

    selected_category = choose_category(categories_classes)
    print(f"Вы выбрали категорию: {selected_category.__name__}")

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

            user_input = input("Введите количество (или несколько значений через пробел): ")
            values = list(map(float, user_input.split()))

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

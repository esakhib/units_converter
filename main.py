from unit_converter import Unit, UnitConverter, output_result


def main():
    source_unit = None
    target_unit = None
    quantity = None

    while True:
        print("Выберите категорию единиц измерения:")
        print("1. Pressure")
        print("2. Volume Flow Rate")

        try:
            category_choice = int(input("Введите номер категории: "))
            if category_choice == 1:
                selected_category = 'pressure'
                break
            elif category_choice == 2:
                selected_category = 'volume_flow_rate'
                break
            else:
                print("Выберите правильную категорию.")
        except ValueError:
            print("Пожалуйста, введите корректное значение.")

    print(f"Вы выбрали категорию: {selected_category}")

    while True:
        print("Выберите единицу измерения:")
        if selected_category == 'pressure':
            selected_unit_class = [unit for unit in Unit if unit.value <= 8]
        else:
            selected_unit_class = [unit for unit in Unit if unit.value >= 9]

        for i, unit in enumerate(selected_unit_class, start=1):
            print(f"{i}. {unit.name.replace('_', '/')}")

        try:
            from_unit_value = int(input("Введите номер исходной единицы: "))
            if from_unit_value < 1 or from_unit_value > len(selected_unit_class):
                print("Выберите номер из предложенных единиц.")
                continue
            source_unit = selected_unit_class[from_unit_value - 1]

            to_unit_value = int(input("Введите номер целевой единицы: "))
            if to_unit_value < 1 or to_unit_value > len(selected_unit_class):
                print("Выберите номер из предложенных единиц.")
                continue
            target_unit = selected_unit_class[to_unit_value - 1]

            user_input = input("Введите количество (или несколько значений через пробел): ")
            values = list(map(float, user_input.split()))

            if not values:
                print("Введите хотя бы одно значение.")
                continue

            quantity = values
            break
        except ValueError:
            print("Пожалуйста, введите корректное значение.")

    result = UnitConverter.convert_unit(selected_category, source_unit, target_unit, quantity)

    output_result(source_unit, target_unit, quantity, result)


main()

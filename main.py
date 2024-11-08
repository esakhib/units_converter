from unit_converter import UnitVolumeFlowRate, UnitPressure, UnitPAConverter, UnitConverter, output_result


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
                selected_unit_class = UnitPressure
                break
            elif category_choice == 2:
                selected_unit_class = UnitVolumeFlowRate
                break
            else:
                print("Выберите правильную категорию.")
        except ValueError:
            print("Пожалуйста, введите корректное значение.")

    print(f"Вы выбрали категорию: {selected_unit_class.__name__}")

    while True:
        print("Выберите единицу измерения:")
        for unit in selected_unit_class:
            print(f"{unit.value}. {unit.name.replace('_', '/')}")

        try:
            from_unit_value = int(input("Введите номер исходной единицы: "))
            if from_unit_value < 1 or from_unit_value > len(selected_unit_class):
                print("Выберите номер из предложенных единиц.")
                continue
            source_unit = selected_unit_class(from_unit_value)

            to_unit_value = int(input("Введите номер целевой единицы: "))
            if to_unit_value < 1 or to_unit_value > len(selected_unit_class):
                print("Выберите номер из предложенных единиц.")
                continue
            target_unit = selected_unit_class(to_unit_value)

            quantity = float(input("Введите количество: "))
            if quantity < 0:
                print("Количество не может быть отрицательным.")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите корректное значение.")

    # Конвертация значения
    if selected_unit_class == UnitPressure:
        result = UnitPAConverter.convert_unit(source_unit, target_unit, quantity)
    else:
        result = UnitConverter.convert_unit(source_unit, target_unit, quantity)

    output_result(source_unit, target_unit, quantity, result)


main()

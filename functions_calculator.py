import inspect
import sys
from typing import get_type_hints

from petrocalc.tree_for_functions import function_tree
from petrocalc.units import Units

# TODO: разделить на файлы

stop_words = ["stop", "break", "exit", "-"]
back_words = ["back", "return", "prev"]


def out(input: str):
    if input in stop_words:
        sys.exit(0)


def input_args(func):
    hints = get_type_hints(func)
    sig = inspect.signature(func)
    args = dict()
    for name, parameter in sig.parameters.items():
        ann = hints.get(name, str).__name__
        unit = Units.get(name, "it")
        prompt = f"Введите {name} ({ann}"

        if unit:
            prompt += f", {unit}"
        prompt += "): "

        while True:
            raw = input(prompt).strip().lower()
            out(raw)
            try:
                args[name] = float(raw)
                break
            except ValueError:
                print(f"Неверный ввод для `{name}`. Попробуйте снова или введите stop.")
    return args


class BackToRoot(Exception):
    pass


def navigate(node, path=None):
    if path is None: path = []

    # node is a function
    if not isinstance(node, dict):
        print(f"\n>>> {' > '.join(path)}\n")
        params = input_args(node)
        print(f"\nРезультат: {node(**params)}\n")
        raise BackToRoot()
    # node is a dictionary
    while True:
        print("\n" + (" / ".join(path) or "Главное меню") + ":")
        keys = list(node.keys())
        for i, key in enumerate(keys, 1):
            print(f"  {i}. {key}")

        choice = input("Выберите пункт: ").strip().lower()
        out(choice)
        if choice in back_words:
            return

        try:
            sel = keys[int(choice) - 1]
        except:
            print("Введен неверный номер.")
            continue

        navigate(node[sel], path + [sel])


def main():
    while True:
        try:
            navigate(function_tree)
        except BackToRoot:
            continue
        except SystemExit:
            break


if __name__ == "__main__":
    main()

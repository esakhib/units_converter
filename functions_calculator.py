import inspect
import sys

from functions import Units, function_tree


def input_args(func):
    sig = inspect.signature(func)
    args = dict()
    for name, parameter in sig.parameters.items():
        unit = Units.get(name, "it")
        prompt = f"Введите {name} ({parameter.annotation.__name__}"

        if unit:
            prompt += f", {unit}"
        prompt += "): "

        while True:
            raw = input(prompt).strip()
            if raw.lower() == "stop":
                sys.exit(0)
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
        if choice == "stop":
            if not path:
                sys.exit(0)
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

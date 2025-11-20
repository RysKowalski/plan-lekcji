import json


def load_data():
    with open("raw.json", "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    print(load_data())

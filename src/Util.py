def dict_to_json(data):
    return {f"{i},{j}": value for (i, j), value in data.items()}


def json_to_dict(data):
    return {
        tuple(map(int, key.split(","))): value
        for key, value in data.items()
    }
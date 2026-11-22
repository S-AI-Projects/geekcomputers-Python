# coding: utf-8
def my_found(req):
    """Translates international women's underwear size to country-specific sizing.

    Contract:
        Preconditions:
            - Source line 3: `my_dict` maps 'XXS' to country base sizes [42, 36, 8, 38, 24]
              and subsequent sizes ('XS'..'XXXL') to integer increments (2, 4, ..., 14).
            - Source line 14: When req[0] != 'XXS', answ = my_dict['XXS'][req[1] - 1] + my_dict[req[0]].
            - Source line 16: When req[0] == 'XXS', answ = my_dict['XXS'][req[1] - 1].
            - Source line 20: `country` defines valid indices 1..5 corresponding to
              {1: 'Россия', 2: 'Германия', 3: 'США', 4: 'Франция', 5: 'Великобритания'}.
            - Source line 29: `req` is a list/sequence of [size_string, country_index]
              where req[0] is uppercase size in my_dict and 1 <= req[1] <= 5.
        Inputs:
            req (list/tuple): [size (str), country_code (int)]
        Returns:
            int: Converted size value for the requested country.
        Mutation:
            Pure function. Does not mutate the input sequence `req` or global state.
    """
    my_dict = {
        "XXS": [42, 36, 8, 38, 24],
        "XS": (2),
        "S": (4),
        "M": (6),
        "L": (8),
        "XL": (10),
        "XXL": (12),
        "XXXL": (14),
    }
    if req[0] != "XXS":
        answ = my_dict["XXS"][req[1] - 1] + my_dict[req[0]]
    else:
        answ = my_dict["XXS"][req[1] - 1]
    return answ


country = {1: "Россия", 2: "Германия", 3: "США", 4: "Франция", 5: "Великобритания"}


def main():
    print(
        "Программа перевода размеров женского белья из\n"
        "международной системы в системы следующих стран:\n"
        "1 - Россия, 2 - Германия, 3 - США, 4 - Франция, 5 - Великобритания.\n"
        "Справка (международная система): XXS, XS, S, M, L, XL, XXL, XXXL"
    )

    req = []
    while len(req) <= 1:
        req = list(
            input(
                ">>> Введите через пробел международный размер и страну,\n"
                "в систему которой перевести данный размер: "
            ).split()
        )
        req[0] = req[0].upper()
        if len(req) <= 1:
            print("Вы таки что-то сделали не так... \nНужно повторить попытку!")
        else:
            req[1] = int(req[1])

    print(
        f'Выбранный Вами размер "{req[0]}" в системе размеров "{country[req[1]]}" будет: {my_found(req)}'
    )


if __name__ == "__main__":
    main()

from acessories.converter_valores import converter_string_flutuante


def convert_two_decimal_places(number):

    try:

        number = converter_string_flutuante(number)
        formatted_number = f"{number:.2f}"
        formatted_number = formatted_number.zfill(16)
        return formatted_number
    except Exception as e:
        print(f'erro na conversao para decima', e)

        return formatted_number

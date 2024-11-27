def converter_string_flutuante(valor):
    
    valor = str(valor)

    if '.' in valor and ',' in valor:
        valor = float(valor.replace('.', '').replace(',', '.'))
    elif ',' in valor:
        valor = float(valor.replace(',', '.'))
    valor = float(valor)
    return round(valor, 2)


def converter_flutuante_string(valor):
    valor = str(valor).replace('.', ',')
    return valor




    
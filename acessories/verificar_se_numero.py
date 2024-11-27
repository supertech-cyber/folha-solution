def eh_numero(valor):
    try:
        val = int(valor)
        return True
    except ValueError:
        return False
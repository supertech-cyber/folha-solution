import re


def get_competencia_folha(texto):

    regex_data = r'(JANEIRO|FEVEREIRO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)/(\d{4})'

    datas_encontradas = re.findall(regex_data, texto.upper())

    return f'{datas_encontradas[0][0]}/{datas_encontradas[0][1]}'


def get_competencia_provisao(texto):

    regex_data = r'(01|02|03|04|05|06|07|08|09|10|11|12)/(\d{4})'

    datas_encontradas = re.findall(regex_data, texto.upper())

    return f'{datas_encontradas[0][0]}/{datas_encontradas[0][1]}'


def get_cnpj(texto):

    regex_cnpj = r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b'

    cnpj_encontrado = re.findall(regex_cnpj, texto)

    return cnpj_encontrado

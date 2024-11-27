from datetime import datetime, timedelta
import calendar


def encontrar_numero_mes(mes_extenso):
    # Dicionário para mapear os nomes dos meses em português para seus números correspondentes
    meses = {
        'janeiro': 1,
        'fevereiro': 2,
        'março': 3,
        'abril': 4,
        'maio': 5,
        'junho': 6,
        'julho': 7,
        'agosto': 8,
        'setembro': 9,
        'outubro': 10,
        'novembro': 11,
        'dezembro': 12
    }

    # Nome do mês
    # mes_extenso = 'SETEMBRO'

    # Converte o nome do mês para minúsculas e encontra o número do mês
    numero_mes = meses.get(mes_extenso.lower(), None)

    return numero_mes


def retorna_data_arquivo_prov(competencia):

    try:

        numero_mes = competencia.split('/')[0]
        ano = competencia.split('/')[-1]

        # numero_mes = encontrar_numero_mes(numero_mes)

        # Define a data como o primeiro dia de setembro de 2023
        # data = datetime(year=int(ano), month=int(numero_mes), day=1)

        year = int(ano)
        month = int(numero_mes)

        last_day = calendar.monthrange(year, month)[1]

        # Adiciona um mês e subtrai um dia para obter o último dia de setembro de 2023
        # data_formatada = (data.replace(month=data.month + 1, day=1) -
        #                   timedelta(days=1)).strftime('%Y%m%d')
        # data_historico = (data.replace(month=data.month + 1, day=1) -
        #                   timedelta(days=1)).strftime('%m/%Y')
        data_formatada = datetime(
            year=year, month=month, day=last_day).strftime('%Y%m%d')
        data_historico = datetime(
            year=year, month=month, day=last_day).strftime('%m/%Y')

    except Exception as e:
        print(f'erro no calculo da data', e)

    return data_formatada, data_historico

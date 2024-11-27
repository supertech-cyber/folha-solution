from controller.read_excel_provisoes import ReadExcelProvisoes
from controller.relatorio_base import RelatorioBase
from datetime import datetime
from dateutil.relativedelta import relativedelta
from models.provisions_manager_solution import ProvisionsManagerSolution
from models.provisions_manager_sul_veiculos import ProvisionsManagerSulVeiculos

from models.solution_ import Solution


def convert_date(string):

    date = datetime.strptime(string, "%m/%Y")

    return date


def gerar_provisoes(files_path):

    # files_path = Logs(filename='arquivos gerados\\logs.log')

    relatorio_base = RelatorioBase()
    relatorio_base.find_relatorios_folha(word_to_find='Relatório de provisão')

    listas_relatorios_provisoes = []

    print('LENDO FOLHA PROVISÕES...\n')
    for conjunto_relatorio_base in relatorio_base.relatorios_folha:

        read_excel_fopag = ReadExcelProvisoes(
            address_folha_prov=conjunto_relatorio_base.address_folha, address_db=conjunto_relatorio_base.address_db)
        read_excel_fopag.capturar_dados_planilha()

        listas_relatorios_provisoes.append(read_excel_fopag)

    for read_excel_fopag in listas_relatorios_provisoes:

        read_excel_fopag.folha_provisoes.competencia = convert_date(
            read_excel_fopag.folha_provisoes.competencia)

        # print(read_excel_fopag.folha_provisoes.competencia)

    tam = len(listas_relatorios_provisoes)

    print('GERANDO LAYOUT SAIDA DAS PROVISÕES...\n')
    for read_excel_fopag in listas_relatorios_provisoes:

        for i in range(tam):

            if read_excel_fopag.folha_provisoes.competencia + relativedelta(months=1) == listas_relatorios_provisoes[i].folha_provisoes.competencia and \
                    read_excel_fopag.folha_provisoes.tipo == listas_relatorios_provisoes[i].folha_provisoes.tipo and read_excel_fopag.folha_provisoes.cnpj_prov == listas_relatorios_provisoes[i].folha_provisoes.cnpj_prov:

                # print(read_excel_fopag.folha_provisoes.cnpj_prov,
                #       listas_relatorios_provisoes[i].folha_provisoes.cnpj_prov)
                # print(read_excel_fopag.folha_provisoes.tipo,
                #       listas_relatorios_provisoes[i].folha_provisoes.tipo)
                # print(read_excel_fopag.folha_provisoes.competencia + relativedelta(months=1),
                #       listas_relatorios_provisoes[i].folha_provisoes.competencia)

                solution = Solution(address_db=read_excel_fopag.address_db)
                solution.read_plan_bd()

                # if '20190046' in solution.address_db or '02637401' in solution.address_db or '03074939' in solution.address_db:

                provisions_manager = ProvisionsManagerSolution(
                    base_dados=solution.planilhas,
                    folha_pagto=[read_excel_fopag.folha_provisoes,
                                 listas_relatorios_provisoes[i].folha_provisoes],
                    files_path=files_path
                )

                provisions_manager.percorrer_relatorio_provisao_mes_posterior()

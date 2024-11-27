from controller.read_excel_fopag_ import ReadExcelFopag
from models.solution_ import Solution
from controller.output_solution_folha_ import OutPutSolutionFolha
from controller.output_sul_veiculos_folha import OutPutSulVeiculosFolha

from controller.relatorio_base import RelatorioBase
from models.logs import Logs


def gerar_folha(files_path):

    # files_path = Logs(filename='arquivos gerados\\logs.log')

    relatorio_base = RelatorioBase()

    relatorio_base.find_relatorios_folha(word_to_find='Espelho')

    for conjunto_relatorio_base in relatorio_base.relatorios_folha:
        print('LENDO A FOLHA DE PAGTO...\n')
        read_excel_fopag = ReadExcelFopag(
            address_folha=conjunto_relatorio_base.address_folha, address_db=conjunto_relatorio_base.address_db)
        read_excel_fopag.capturar_dados_planilha()

        print('LENDO O BANCO DE DADOS...\n')
        solution = Solution(address_db=conjunto_relatorio_base.address_db)
        solution.read_plan_bd()

        print('GERANDO LAYOUT SAÍDA DA FOLHA DE PAGTO...\n')
        # if '20190046' in solution.address_db or '02637401' in solution.address_db or '03074939' in solution.address_db:

        output_solution = OutPutSolutionFolha(
            base_dados=solution.planilhas, folha_pagto=read_excel_fopag.folha_pagto, files_path=files_path)

        output_solution.gerar_arquivo_saida_folha()

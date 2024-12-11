from openpyxl import load_workbook
from controller.regex_ import get_competencia_folha, get_cnpj
from acessories.verificar_se_numero import eh_numero
from models.folha_pagamento import FolhaPagto, Empresa, CentroCusto, Evento
import os


class ReadExcelFopag:

    def __init__(self, address_folha, address_db):
        self.address_folha = address_folha
        self.address_db = address_db

    def maiuscula(self, valor):
        try:
            valor = valor.upper()
        except:
            pass

        finally:

            return valor

    def _organizar_planilha(self):

        workbook = load_workbook(filename=self.address_folha)

        planilha = workbook.active

        planilha_nova = []

        for linha in planilha.values:
            nova_lista = []
            for lista_velha in linha:
                if lista_velha:
                    nova_lista.append(lista_velha)
            planilha_nova.append(nova_lista)

        return planilha_nova

    def _adicionar_eventos(self, registro, nova_empresa, centro_custo, numero):

        if len(registro) == 3 and eh_numero(registro[0]):

            novo_centro_custo = nova_empresa.procurar_centro_custo(
                centro_custo)

            if not novo_centro_custo:
                novo_centro_custo = CentroCusto(nome=centro_custo)
                nova_empresa.add_centro_custo(novo_centro_custo)

            novo_evento = Evento(
                codigo=registro[0], descricao=registro[1], valor=registro[2])

            novo_centro_custo.add_evento(novo_evento)

        if len(registro) == 4 and eh_numero(registro[0]):

            novo_centro_custo = nova_empresa.procurar_centro_custo(
                centro_custo)

            if not novo_centro_custo:
                novo_centro_custo = CentroCusto(nome=centro_custo)
                nova_empresa.add_centro_custo(novo_centro_custo)

            novo_evento = Evento(
                codigo=registro[0], descricao=registro[1], valor=registro[3])

            novo_centro_custo.add_evento(novo_evento)

        elif len(registro) == 8 and eh_numero(registro[0]):

            novo_centro_custo = nova_empresa.procurar_centro_custo(
                centro_custo)

            if not novo_centro_custo:
                novo_centro_custo = CentroCusto(nome=centro_custo)
                nova_empresa.add_centro_custo(novo_centro_custo)

            novo_evento = Evento(
                codigo=registro[0], descricao=registro[1], valor=registro[3])

            novo_centro_custo.add_evento(novo_evento)

            novo_evento = Evento(
                codigo=registro[4], descricao=registro[5], valor=registro[7])

            novo_centro_custo.add_evento(novo_evento)

        elif len(registro) == 6 and eh_numero(registro[0]):

            novo_centro_custo = nova_empresa.procurar_centro_custo(
                centro_custo)

            if not novo_centro_custo:
                novo_centro_custo = CentroCusto(nome=centro_custo)
                nova_empresa.add_centro_custo(novo_centro_custo)

            novo_evento = Evento(
                codigo=registro[0], descricao=registro[1], valor=registro[2])

            novo_centro_custo.add_evento(novo_evento)

            novo_evento = Evento(
                codigo=registro[3], descricao=registro[4], valor=registro[5])

            novo_centro_custo.add_evento(novo_evento)

        elif len(registro) == 7 and eh_numero(registro[0]):

            novo_centro_custo = nova_empresa.procurar_centro_custo(
                centro_custo)

            if not novo_centro_custo:
                novo_centro_custo = CentroCusto(nome=centro_custo)
                nova_empresa.add_centro_custo(novo_centro_custo)

            if type(registro[2]) is str:

                novo_evento = Evento(
                    codigo=registro[0], descricao=registro[1], valor=registro[3])

                novo_centro_custo.add_evento(novo_evento)

                novo_evento = Evento(
                    codigo=registro[4], descricao=registro[5], valor=registro[6])

                novo_centro_custo.add_evento(novo_evento)

            else:

                novo_evento = Evento(
                    codigo=registro[0], descricao=registro[1], valor=registro[2])

                novo_centro_custo.add_evento(novo_evento)

                novo_evento = Evento(
                    codigo=registro[3], descricao=registro[4], valor=registro[6])

                novo_centro_custo.add_evento(novo_evento)

    def capturar_dados_planilha(self):

        planilha_nova = self._organizar_planilha()
        flag_proventos = False
        achou_centro_custo = False
        achou_empresa = False
        folha_decimo = False

        self.folha_pagto = FolhaPagto()

        for registro in planilha_nova:

            if registro:

                if len(registro) == 1:
                    continue

                # Pegar competência
                try:
                    if 'espelho'.upper() in self.maiuscula(registro[0]):

                        competencia = get_competencia_folha(
                            texto=' '.join(registro))
                    if 'espelho'.upper() in self.maiuscula(registro[0]) and '13º' in registro[0].upper():
                        folha_decimo = True

                except Exception as e:
                    pass

                # Pegar CNPJ
                try:
                    if 'empresa'.upper() in self.maiuscula(registro[0]):
                        achou_empresa = True
                        cnpj = get_cnpj(texto=' '.join(registro))
                        if cnpj:
                            nova_empresa = self.folha_pagto.procurar_empresa(
                                cnpj)
                            if not nova_empresa:

                                nova_empresa = Empresa(
                                    cnpj=cnpj, competencia=competencia)
                                self.folha_pagto.add_empresa(nova_empresa)
                            pass
                except:
                    pass

                # Pegar Centro de Custo
                try:
                    if 'centro de custo'.upper() in self.maiuscula(registro[0]):
                        achou_centro_custo = True
                        centro_custo = registro[1].strip()
                        nova_empresa.add_centro_custo(
                            CentroCusto(nome=centro_custo))
                except:
                    pass

                # Setar saida dos eventos
                if 'resumo geral'.upper() in self.maiuscula(registro[0]):
                    flag_proventos = False
                    continue

                # Setar Entrada dos eventos
                if 'proventos'.upper() in self.maiuscula(registro[0]):
                    flag_proventos = True
                    continue

                if flag_proventos and achou_empresa and achou_centro_custo:

                    if len(registro) == 3 and eh_numero(registro[0]):

                        self._adicionar_eventos(
                            registro, nova_empresa, centro_custo, 3)

                    if len(registro) == 4 and eh_numero(registro[0]):

                        self._adicionar_eventos(
                            registro, nova_empresa, centro_custo, 4)

                    elif len(registro) == 6 and eh_numero(registro[0]):

                        self._adicionar_eventos(
                            registro, nova_empresa, centro_custo, 6)

                    elif len(registro) == 7 and eh_numero(registro[0]):

                        self._adicionar_eventos(
                            registro, nova_empresa, centro_custo, 7)

                    elif len(registro) == 8 and eh_numero(registro[0]):

                        self._adicionar_eventos(
                            registro, nova_empresa, centro_custo, 8)

                if ('VALOR GFD MENSAL 8%'.upper() == self.maiuscula(registro[0]) or 'VALOR GFD 2%'.upper() == self.maiuscula(registro[0]) or
                    'FGTS GRF 2%'.upper() == self.maiuscula(registro[0]) or 'FGTS GRF 8%'.upper() == self.maiuscula(registro[0])) \
                        and achou_centro_custo:

                    novo_centro_custo = nova_empresa.procurar_centro_custo(
                        centro_custo)

                    if not novo_centro_custo:
                        novo_centro_custo = CentroCusto(nome=centro_custo)
                        nova_empresa.add_centro_custo(novo_centro_custo)

                    novo_evento = Evento(codigo=registro[0].upper(
                    ), descricao=self.maiuscula(registro[0]), valor=registro[1])

                    novo_centro_custo.add_evento(novo_evento)

                if ('total GFD'.upper() == self.maiuscula(registro[0])):

                    if folha_decimo:
                        achou_centro_custo = False
                        achou_empresa = False
                        continue

                if 'GPS patronal'.upper() in self.maiuscula(registro[0]) and achou_centro_custo:
                    novo_centro_custo = nova_empresa.procurar_centro_custo(
                        centro_custo)

                    if not novo_centro_custo:
                        novo_centro_custo = CentroCusto(nome=centro_custo)
                        nova_empresa.add_centro_custo(novo_centro_custo)

                    novo_evento = Evento(
                        codigo='GPS patronal', descricao='GPS patronal', valor=registro[-1].replace('(Líquido GPS patronal)', '').strip())

                    novo_centro_custo.add_evento(novo_evento)

                    # Setar Fim de Folha
                if 'GPS patronal'.upper() in self.maiuscula(registro[0]):
                    achou_centro_custo = False
                    achou_empresa = False
                    continue


if __name__ == '__main__':
    read_excel_fopag = ReadExcelFopag()
    read_excel_fopag.capturar_dados_planilha()

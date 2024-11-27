from openpyxl import load_workbook
from controller.regex_ import get_competencia_provisao, get_cnpj
from models.folha_provisoes import FolhaProvisoes, Empresa, CentroCusto


class ReadExcelProvisoes:

    def __init__(self, address_folha_prov, address_db):

        self.address_folha_prov = address_folha_prov
        self.address_db = address_db
        self.folha_provisoes = ''

    def _organizar_planilha(self):

        workbook = load_workbook(filename=self.address_folha_prov)

        planilha = workbook.active

        planilha_nova = []

        for linha in planilha.values:
            nova_lista = []
            for lista_velha in linha:
                if lista_velha:
                    nova_lista.append(lista_velha)
            planilha_nova.append(nova_lista)

        return planilha_nova

    def capturar_dados_planilha(self):

        planilha_nova = self._organizar_planilha()
        flag_proventos = False
        achou_centro_custo = False
        achou_empresa = False

        self.folha_provisoes = FolhaProvisoes()

        for registro in planilha_nova:

            if registro:

                # Pegar competência
                if 'relatório de provisão'.upper() in registro[0].upper():
                    self.folha_provisoes.competencia = get_competencia_provisao(
                        texto=' '.join(registro))
                    if 'férias'.upper() in registro[0].upper():
                        self.folha_provisoes.tipo = 'férias'
                    else:
                        self.folha_provisoes.tipo = 'décimo'

                # Pegar CNPJ
                if 'empresa'.upper() in registro[0].upper():
                    achou_empresa = True
                    cnpj = get_cnpj(texto=' '.join(registro))
                    if cnpj:
                        self.folha_provisoes.cnpj_prov = cnpj[0][0:10]
                        nova_empresa = self.folha_provisoes.procurar_empresa(
                            cnpj)
                        if not nova_empresa:

                            nova_empresa = Empresa(
                                cnpj=cnpj, competencia=self.folha_provisoes.competencia)
                            self.folha_provisoes.add_empresa(nova_empresa)
                        pass

                # Pegar Centro de Custo
                if 'total centro de custo'.upper() in registro[0].upper():
                    achou_centro_custo = True
                    centro_custo = registro[0].split(':')[-1].strip()
                    novo_centro_custo = CentroCusto(nome=centro_custo)
                    nova_empresa.add_centro_custo(
                        novo_centro_custo)

                # # Setar total
                if achou_centro_custo and 'total saldo'.upper() in registro[0].upper():

                    achou_centro_custo = False

                    if self.folha_provisoes.tipo == 'férias':

                        total_saldo = registro[1]
                        total_abono = registro[2]
                        total_fgts = registro[3]
                        total_inss = registro[4]
                        total_inss_terc = registro[5]
                        total_inss_rat = registro[6]

                        novo_centro_custo.set_saldos_ferias(
                            vlr_saldo_provisao=total_saldo,
                            vlr_saldo_abono=total_abono,
                            vlr_saldo_fgts_prov=total_fgts,
                            vlr_saldo_inss_prov=total_inss,
                            vlr_saldo_terc_prov=total_inss_terc,
                            vlr_saldo_rat_prov=total_inss_rat
                        )

                    else:

                        total_saldo = registro[1]
                        total_fgts = registro[2]
                        total_inss = registro[3]
                        total_inss_terc = registro[4]
                        total_inss_rat = registro[5]
                        novo_centro_custo.set_saldos_decimo(
                            vlr_saldo_provisao=total_saldo,
                            vlr_saldo_fgts_prov=total_fgts,
                            vlr_saldo_inss_prov=total_inss,
                            vlr_saldo_terc_prov=total_inss_terc,
                            vlr_saldo_rat_prov=total_inss_rat
                        )


if __name__ == '__main__':
    read_excel_fopag = ReadExcelProvisoes()
    read_excel_fopag.capturar_dados_planilha()

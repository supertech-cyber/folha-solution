class FolhaProvisoes:

    def __init__(self):
        self.tipo = ''
        self.empresas = []

    def add_empresa(self, empresa):
        self.empresas.append(empresa)

    def procurar_empresa(self, cnpj):
        try:
            return [empresa for empresa in self.empresas if empresa.cnpj == cnpj][0]
        except:
            return False


class Empresa:

    def __init__(self, cnpj, competencia):
        self.cnpj = cnpj
        self.competencia = competencia
        self.centros_custos = []

    def add_centro_custo(self, centro_custo):
        self.centros_custos.append(centro_custo)

    def procurar_centro_custo(self, nome):
        try:
            return [centro_custo for centro_custo in self.centros_custos if centro_custo.nome == nome][0]
        except:
            return False


class CentroCusto:

    def __init__(self, nome):
        self.nome = nome

    def set_saldos_decimo(self, vlr_saldo_provisao, vlr_saldo_fgts_prov, vlr_saldo_inss_prov, vlr_saldo_terc_prov, vlr_saldo_rat_prov):
        self.vlr_saldo_provisao_13 = vlr_saldo_provisao
        self.vlr_saldo_fgts_13 = vlr_saldo_fgts_prov
        self.vlr_saldo_inss_13 = vlr_saldo_inss_prov
        self.vlr_saldo_terc_13 = vlr_saldo_terc_prov
        self.vlr_saldo_rat_13 = vlr_saldo_rat_prov

    def set_saldos_ferias(self, vlr_saldo_provisao, vlr_saldo_abono, vlr_saldo_fgts_prov, vlr_saldo_inss_prov, vlr_saldo_terc_prov, vlr_saldo_rat_prov):
        self.vlr_saldo_provisao_ferias = vlr_saldo_provisao
        self.vlr_saldo_abono = vlr_saldo_abono
        self.vlr_saldo_fgts_ferias = vlr_saldo_fgts_prov
        self.vlr_saldo_inss_ferias = vlr_saldo_inss_prov
        self.vlr_saldo_terc_ferias = vlr_saldo_terc_prov
        self.vlr_saldo_rat_ferias = vlr_saldo_rat_prov

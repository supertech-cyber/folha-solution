class FolhaPagto:

    def __init__(self):
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
        self.eventos = []

    def add_evento(self, evento):
        self.eventos.append(evento)


class Evento:
    def __init__(self, codigo, descricao, valor):
        self.codigo = codigo
        self.descricao = descricao
        self.valor = valor

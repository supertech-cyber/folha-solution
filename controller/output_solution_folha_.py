from acessories.retorna_data_formatada import retorna_data_arquivo
from acessories.convert_two_decimal_places_ import convert_two_decimal_places


class OutPutSolutionFolha:

    def __init__(self, base_dados, folha_pagto, files_path):
        self.base_dados = base_dados
        self.folha_pagto = folha_pagto
        self.files_path = files_path

    def _gerar_txt_saida(self, competencia, codigo_evento, cnpj):

        value_two_decimal = convert_two_decimal_places(self.valor)

        data_formatada, data_historico = retorna_data_arquivo(competencia)
        cc_debito_geral = str(self.debito_evento_geral).zfill(6)
        cc_credito_geral = str(self.credito_evento_geral).zfill(6)
        cod_custo = str(self.cod_custo).zfill(7)
        historico = 'VLR FOLHA DE PAGAMENTO'
        espacamento = ' ' * 50

        try:

            cnpj = cnpj[0].replace('.', '').replace(
                '/', '').replace('-', '')[0:8]
            nome_txt = f'arquivos gerados\\{cnpj}_{
                data_formatada.replace('/', '_')}.txt'
        except Exception as e:
            print(f'erro cnpj', e)

        if codigo_evento.upper() == 'VALOR GFD MENSAL 8%' or codigo_evento.upper() == 'VALOR GFD 2%'\
                or codigo_evento.upper() == 'FGTS GRF 2%' or codigo_evento.upper() == 'FGTS GRF 8%':
            espacamento = ' ' * 43
            historico = 'VLR FGTS S/FOLHA DE PAGAMENTO'

        elif codigo_evento == 'GPS patronal':
            espacamento = ' ' * 43
            historico = 'VLR INSS S/FOLHA DE PAGAMENTO'

        with open(nome_txt, 'a', encoding='utf-8') as folha:
            if self.tipo_custo == 'Geral':
                folha.write(
                    f"LANCTO  0{23 * ' '}I{data_formatada}E{cc_debito_geral}{cc_credito_geral}{value_two_decimal}{cod_custo}{'0'.zfill(37)}{historico} {data_historico}{espacamento}{self.cod_empresa_arq}\n")
            else:
                folha.write(
                    f"LANCTO  0{23 * ' '}I{data_formatada}E{cc_debito_geral}{cc_credito_geral}{value_two_decimal}{cod_custo}{'0'.zfill(37)}{historico} {data_historico}{espacamento}{self.cod_empresa_arq}\n")

    def gerar_arquivo_saida_folha(self):

        for empresa in self.folha_pagto.empresas:

            try:
                self.cod_empresa_arq = self.base_dados['empresas'].get(empresa.cnpj[0])[
                    'SOLUTION']

            except Exception as e:

                self.files_path.create_warning(f'Empresa de CNPJ "{
                    empresa.cnpj[0]}" não cadastrada')
                continue

            for centro_custo in empresa.centros_custos:

                codigo_custo = (centro_custo.nome.split('-')[0].strip())

                try:
                    self.cod_custo = self.base_dados['custo'][codigo_custo]['SOLUTION']
                    self.tipo_custo = self.base_dados['custo'][codigo_custo]['TIPO']

                except:
                    self.files_path.create_warning(f'{empresa.cnpj[0]} - Centro de Custo "{
                        centro_custo.nome}"  não cadastrado')
                    continue

                for evento in centro_custo.eventos:

                    try:

                        if self.tipo_custo == 'Geral':

                            self.debito_evento_geral = self.base_dados[
                                'eventos'][evento.codigo]['DÉBITO GERAL']
                            self.credito_evento_geral = self.base_dados[
                                'eventos'][evento.codigo]['CRÉDITO GERAL']

                        elif self.tipo_custo == 'Serviços':

                            self.debito_evento_geral = self.base_dados[
                                'eventos'][evento.codigo]['DÉBITO SERVIÇOS']
                            self.credito_evento_geral = self.base_dados[
                                'eventos'][evento.codigo]['CRÉDITO SERVIÇOS']

                        self.valor = evento.valor

                        self._gerar_txt_saida(
                            empresa.competencia, evento.codigo, empresa.cnpj)

                    except Exception as e:

                        self.files_path.create_warning(
                            f'{empresa.cnpj[0]} - Conta Não cadastrada para o evento {evento.codigo} centro de custo {centro_custo.nome}')


if __name__ == '__main__':
    pass

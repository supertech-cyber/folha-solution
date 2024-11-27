from acessories.retorna_data_formatada import retorna_data_arquivo
from acessories.convert_two_decimal_places_ import convert_two_decimal_places


class OutPutSulVeiculosFolha:

    def __init__(self, base_dados, folha_pagto, files_path):
        self.base_dados = base_dados
        self.folha_pagto = folha_pagto
        self.files_path = files_path

    def _gerar_txt_saida(self, competencia, codigo_evento, cnpj):

        value_two_decimal = convert_two_decimal_places(self.valor)
        value_two_decimal = value_two_decimal.replace('.', ',')
        data_formatada, data_historico = retorna_data_arquivo(competencia)
        cc_debito_geral = str(self.debito_evento_geral).replace('.', '')
        cc_credito_geral = str(self.credito_evento_geral).replace('.', '')
        cod_custo = str(self.cod_custo)
        historico = 'VLR FOLHA DE PAGAMENTO'

        try:

            cnpj = cnpj[0].replace('.', '').replace(
                '/', '').replace('-', '')[0:8]
            nome_txt = f'arquivos gerados\\{cnpj}_{
                data_formatada.replace('/', '_')}.txt'

        except Exception as e:
            print(f'erro cnpj', e)

        if codigo_evento == 'FGTS GRF 8%' or codigo_evento == 'FGTS GRF 2%':

            historico = 'VLR FGTS S/FOLHA DE PAGAMENTO'

        elif codigo_evento == 'GPS patronal':

            historico = 'VLR INSS S/FOLHA DE PAGAMENTO'

        historico = historico + ' ' + data_historico

        # nome_txt = f'arquivos gerados\\{cnpj}_{data_formatada}.txt'

        with open(nome_txt, 'a', encoding='utf-8') as folha:

            folha.write(
                f"FP{8 * ' '}{self.cod_empresa_arq}{self.codigo_filial}{cc_debito_geral}{
                    8 * ' '}{cod_custo}{21 * ' '}{cc_credito_geral}{8 * ' '}"
                f"{cod_custo}{33 * ' '}{historico.ljust(250, ' ')}{data_formatada}{data_formatada}{20 * ' '}{value_two_decimal}{54 * ' '}\n")

    def gerar_arquivo_saida_folha(self):

        for empresa in self.folha_pagto.empresas:

            try:
                self.cod_empresa_arq = self.base_dados['empresas'].get(empresa.cnpj[0])[
                    'EMPRESA']
                self.codigo_filial = self.base_dados['empresas'].get(empresa.cnpj[0])[
                    'FILIAL']

            except Exception as e:

                self.files_path.create_warning(f'Empresa de CNPJ "{
                    empresa.cnpj[0]}" não cadastrada')
                continue

            for centro_custo in empresa.centros_custos:

                codigo_custo = (centro_custo.nome.split('-')[0].strip())

                try:
                    self.cod_custo = self.base_dados['custo'][codigo_custo]['SUL VEICULOS']

                except:
                    self.files_path.create_warning(f'{empresa.cnpj[0]} - Centro de Custo "{
                        centro_custo.nome}"  não cadastrado')
                    continue

                for evento in centro_custo.eventos:

                    try:

                        self.debito_evento_geral = self.base_dados[
                            'eventos'][evento.codigo]['DÉBITO']
                        self.credito_evento_geral = self.base_dados[
                            'eventos'][evento.codigo]['CRÉDITO']

                        self.valor = evento.valor

                        self._gerar_txt_saida(
                            empresa.competencia, evento.codigo, empresa.cnpj)

                    except Exception as e:

                        self.files_path.create_warning(
                            f'{empresa.cnpj[0]} - Conta Não cadastrada para o evento {evento.codigo} centro de custo {centro_custo.nome}')


if __name__ == '__main__':
    pass

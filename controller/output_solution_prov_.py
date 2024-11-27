from acessories.retorna_data_formatada_prov import retorna_data_arquivo_prov
from acessories.convert_two_decimal_places_ import convert_two_decimal_places
from acessories.converter_valores import converter_string_flutuante


class OutPutSolutionProvisao:

    def __init__(self, base_dados, folha_pagto, files_path):
        self.base_dados = base_dados
        self.folha_pagto = folha_pagto
        self.files_path = files_path

    def _gerar_txt_saida(self, competencia, cnpj, valor):

        try:

            value_two_decimal = convert_two_decimal_places(valor)
            data_formatada, data_historico = retorna_data_arquivo_prov(
                competencia)
            cc_debito_geral = str(self.debito_evento_geral).zfill(6)
            cc_credito_geral = str(self.credito_evento_geral).zfill(6)
            cod_custo = str(self.cod_custo).zfill(6)
            historico = 'VLR PROVISÕES TRABALHISTAS'
            espacamento = ' ' * 36

            try:

                cnpj = cnpj[0].replace('.', '').replace(
                    '/', '').replace('-', '')[0:8]
                nome_txt = f'arquivos gerados\\{cnpj}_{data_formatada}.txt'

            except Exception as e:

                print(f'erro cnpj', e)

            with open(nome_txt, 'a', encoding='utf-8') as folha:

                if self.tipo_custo == 'Geral':

                    folha.write(
                        f"LANCTO  0{23 * ' '}I{data_formatada}E{cc_debito_geral}{cc_credito_geral}{value_two_decimal}0{cod_custo}{'0'.zfill(37)}{historico} {data_historico}{espacamento}{self.cod_empresa_arq}\n")
                else:
                    folha.write(
                        f"LANCTO  0{23 * ' '}I{data_formatada}E{cc_debito_geral}{cc_credito_geral}{value_two_decimal}0{cod_custo}{'0'.zfill(37)}{historico} {data_historico}{espacamento}{self.cod_empresa_arq}\n")

        except Exception as e:
            print('erro ao gerar o arquivo', e)

    def gerar_arquivo_saida_folha(self):

        i = 1

        for empresa in self.folha_pagto[1].empresas:

            try:
                self.cod_empresa_arq = self.base_dados['empresas'].get(empresa.cnpj[0])[
                    'SOLUTION']

            except Exception as e:

                self.files_path.create_warning(f'Empresa de CNPJ "{
                    empresa.cnpj[1]}" não cadastrada')
                continue

            for centro_custo in empresa.centros_custos:

                codigo_custo = (centro_custo.nome.split('-')[1].strip())

                try:
                    self.cod_custo = self.base_dados['custo'][codigo_custo]['SOLUTION']
                    self.tipo_custo = self.base_dados['custo'][codigo_custo]['TIPO']

                    i += 1

                except:
                    self.files_path.create_warning(f'{empresa.cnpj[1]} - Centro de Custo "{
                        centro_custo.nome}"  não cadastrado')
                    continue

                if self.folha_pagto[1].tipo == 'décimo':

                    if self.tipo_custo == 'Geral':
                        debito = 'DÉBITO GERAL'
                        credito = 'CRÉDITO GERAL'
                    else:
                        debito = 'DÉBITO SERVIÇOS'
                        credito = 'CRÉDITO SERVIÇOS'

                    empresa_procurada = self.folha_pagto[0].procurar_empresa(
                        empresa.cnpj)

                    if empresa_procurada:

                        centro_custo_procurado = empresa_procurada.procurar_centro_custo(
                            centro_custo.nome)

                        if centro_custo_procurado:

                            try:

                                self.debito_evento_geral = self.base_dados[
                                    'eventos']['13º Salário'][debito]
                                self.credito_evento_geral = self.base_dados[
                                    'eventos']['13º Salário'][credito]

                                provisao_13 = converter_string_flutuante(
                                    centro_custo_procurado.vlr_saldo_provisao_13) - converter_string_flutuante(centro_custo.vlr_saldo_provisao_13)

                                provisao_13 = round(provisao_13, 2)

                                if provisao_13 < 0:

                                    provisao_13 *= -1
                                    self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

                                self._gerar_txt_saida(
                                    empresa_procurada.competencia, empresa.cnpj, provisao_13)

                            except:

                                self.files_path.create_warning(
                                    f'{empresa.cnpj[1]} - Conta Não cadastrada para o evento 13º Salário - centro de custo {centro_custo.nome}')

                            try:

                                self.debito_evento_geral = self.base_dados[
                                    'eventos']['FGTS s/13º'][debito]
                                self.credito_evento_geral = self.base_dados[
                                    'eventos']['FGTS s/13º'][credito]

                                fgts_provisao_13 = converter_string_flutuante(
                                    centro_custo_procurado.vlr_saldo_fgts_13) - converter_string_flutuante(centro_custo.vlr_saldo_fgts_13)

                                fgts_provisao_13 = round(fgts_provisao_13, 2)

                                if fgts_provisao_13 < 0:

                                    fgts_provisao_13 *= -1
                                    self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

                                self._gerar_txt_saida(
                                    empresa_procurada.competencia, empresa.cnpj, fgts_provisao_13)

                            except:

                                self.files_path.create_warning(
                                    f'{empresa.cnpj[1]} - Conta Não cadastrada para o evento FGTS s/13º - centro de custo {centro_custo.nome}')

                            try:

                                self.debito_evento_geral = self.base_dados[
                                    'eventos']['INSS s/13º'][debito]
                                self.credito_evento_geral = self.base_dados[
                                    'eventos']['INSS s/13º'][credito]

                                inss_provisao_13_2 = converter_string_flutuante(centro_custo_procurado.vlr_saldo_inss_13) + \
                                    converter_string_flutuante(centro_custo_procurado.vlr_saldo_terc_13) + \
                                    converter_string_flutuante(
                                        centro_custo_procurado.vlr_saldo_rat_13)

                                inss_provisao_13_1 = converter_string_flutuante(centro_custo.vlr_saldo_inss_13) + \
                                    converter_string_flutuante(centro_custo.vlr_saldo_terc_13) + \
                                    converter_string_flutuante(
                                        centro_custo.vlr_saldo_rat_13)

                                inss_provisao_13 = inss_provisao_13_2 - inss_provisao_13_1

                                inss_provisao_13 = round(inss_provisao_13, 2)

                                if inss_provisao_13 < 0:

                                    inss_provisao_13 *= -1
                                    self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

                                self._gerar_txt_saida(
                                    empresa_procurada.competencia, empresa.cnpj, inss_provisao_13)

                            except:

                                self.files_path.create_warning(
                                    f'{empresa.cnpj[1]} - Conta Não cadastrada para o evento INSS s/13º - centro de custo {centro_custo.nome}')

                if self.folha_pagto[1].tipo == 'férias':

                    if self.tipo_custo == 'Geral':
                        debito = 'DÉBITO GERAL'
                        credito = 'CRÉDITO GERAL'
                    else:
                        debito = 'DÉBITO SERVIÇOS'
                        credito = 'CRÉDITO SERVIÇOS'

                    empresa_procurada = self.folha_pagto[0].procurar_empresa(
                        empresa.cnpj)

                    if empresa_procurada:

                        centro_custo_procurado = empresa_procurada.procurar_centro_custo(
                            centro_custo.nome)

                        if centro_custo_procurado:

                            try:

                                self.debito_evento_geral = self.base_dados[
                                    'eventos']['Férias'][debito]
                                self.credito_evento_geral = self.base_dados[
                                    'eventos']['Férias'][credito]

                                provisao_ferias_2 = converter_string_flutuante(
                                    centro_custo_procurado.vlr_saldo_provisao_ferias) + converter_string_flutuante(centro_custo_procurado.vlr_saldo_abono)

                                provisao_ferias_1 = converter_string_flutuante(
                                    centro_custo.vlr_saldo_provisao_ferias) + converter_string_flutuante(centro_custo.vlr_saldo_abono)

                                provisao_ferias = provisao_ferias_2 - provisao_ferias_1

                                provisao_ferias = round(provisao_ferias, 2)

                                if provisao_ferias < 0:

                                    provisao_ferias *= -1
                                    self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

                                self._gerar_txt_saida(
                                    empresa_procurada.competencia, empresa.cnpj, provisao_ferias)

                            except:

                                self.files_path.create_warning(
                                    f'{empresa.cnpj[1]} - Conta Não cadastrada para o evento Férias - centro de custo {centro_custo.nome}')

                            try:

                                self.debito_evento_geral = self.base_dados[
                                    'eventos']['FGTS s/Férias'][debito]
                                self.credito_evento_geral = self.base_dados[
                                    'eventos']['FGTS s/Férias'][credito]

                                fgts_provisao_ferias = converter_string_flutuante(
                                    centro_custo_procurado.vlr_saldo_fgts_ferias) - converter_string_flutuante(centro_custo.vlr_saldo_fgts_ferias)

                                fgts_provisao_ferias = round(
                                    fgts_provisao_ferias, 2)

                                if fgts_provisao_ferias < 0:

                                    fgts_provisao_ferias *= -1
                                    self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

                                self._gerar_txt_saida(
                                    empresa_procurada.competencia, empresa.cnpj, fgts_provisao_ferias)

                            except:

                                self.files_path.create_warning(
                                    f'{empresa.cnpj[1]} - Conta Não cadastrada para o evento FGTS s/Férias - centro de custo {centro_custo.nome}')

                            try:

                                self.debito_evento_geral = self.base_dados[
                                    'eventos']['INSS s/Férias'][debito]
                                self.credito_evento_geral = self.base_dados[
                                    'eventos']['INSS s/Férias'][credito]

                                inss_provisao_ferias_2 = converter_string_flutuante(centro_custo_procurado.vlr_saldo_inss_ferias) + \
                                    converter_string_flutuante(centro_custo_procurado.vlr_saldo_terc_ferias) + \
                                    converter_string_flutuante(
                                        centro_custo_procurado.vlr_saldo_rat_ferias)

                                inss_provisao_ferias_1 = converter_string_flutuante(centro_custo.vlr_saldo_inss_ferias) + \
                                    converter_string_flutuante(centro_custo.vlr_saldo_terc_ferias) + \
                                    converter_string_flutuante(
                                        centro_custo.vlr_saldo_rat_ferias)

                                inss_provisao_ferias = inss_provisao_ferias_2 - inss_provisao_ferias_1

                                inss_provisao_ferias = round(
                                    inss_provisao_ferias, 2)

                                if inss_provisao_ferias < 0:

                                    inss_provisao_ferias *= -1
                                    self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

                                self._gerar_txt_saida(
                                    empresa_procurada.competencia, empresa.cnpj, inss_provisao_ferias)

                            except:

                                self.files_path.create_warning(
                                    f'{empresa.cnpj[1]} - Conta Não cadastrada para o evento INSS s/Férias - centro de custo {centro_custo.nome}')


if __name__ == '__main__':
    pass

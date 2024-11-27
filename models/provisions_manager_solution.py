from acessories.converter_valores import converter_flutuante_string, converter_string_flutuante
from acessories.convert_two_decimal_places_ import convert_two_decimal_places
from acessories.retorna_data_formatada_prov import retorna_data_arquivo_prov


class ProvisionsManagerSolution:
    def __init__(self, base_dados, folha_pagto, files_path) -> None:
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
            cod_custo = str(self.cod_custo).zfill(7)
            historico = 'VLR PROVISÕES TRABALHISTAS'
            espacamento = ' ' * 46

            try:

                cnpj_completo = cnpj[0].replace('.', '').replace(
                    '/', '').replace('-', '')
                cnpj = cnpj[0].replace('.', '').replace(
                    '/', '').replace('-', '')[0:8]
                nome_txt = f'arquivos gerados\\{cnpj}_{
                    data_formatada.replace('/', '_')}.txt'

            except Exception as e:

                print(f'erro cnpj', e)

            with open(nome_txt, 'a', encoding='utf-8') as folha:

                if self.tipo_custo == 'Geral':

                    folha.write(
                        f"LANCTO  0{23 * ' '}I{data_formatada}E{cc_debito_geral}{cc_credito_geral}{value_two_decimal}{cod_custo}{'0'.zfill(37)}{historico} {data_historico}{espacamento}{self.cod_empresa_arq}\n")
                else:
                    folha.write(
                        f"LANCTO  0{23 * ' '}I{data_formatada}E{cc_debito_geral}{cc_credito_geral}{value_two_decimal}{cod_custo}{'0'.zfill(37)}{historico} {data_historico}{espacamento}{self.cod_empresa_arq}\n")

        except Exception as e:
            print('erro ao gerar o arquivo', e)

    def _se_empresa_esta_no_banco_dados(self, empresa):
        try:

            self.cod_empresa_arq = self.base_dados['empresas'].get(empresa.cnpj[0])[
                'SOLUTION']

            return True

        except Exception as e:

            self.files_path.create_warning(f'Empresa de CNPJ "{
                empresa.cnpj[1]}" não cadastrada')
            return False

    def _se_centro_custo_cadastrado_banco_dados(self, centro_custo, empresa):

        codigo_custo = (centro_custo.nome.split('-')[0].strip())

        try:
            self.cod_custo = self.base_dados['custo'][codigo_custo]['SOLUTION']
            self.tipo_custo = self.base_dados['custo'][codigo_custo]['TIPO']

            return True

        except:

            self.files_path.create_warning(f'{empresa.cnpj} - Centro de Custo "{
                centro_custo.nome}"  não cadastrado')

            return False

    def _se_empresa_esta_no_mes_anterior(self, empresa_procurada):
        for empresa in self.folha_pagto[0].empresas:
            if empresa.cnpj[0] == empresa_procurada.cnpj[0]:

                return empresa
        return False

    def _se_centro_custo_esta_no_mes_anterior(self, centro_custo_procurado, empresa_procurada):
        for empresa in self.folha_pagto[0].empresas:
            for centro_custo in empresa.centros_custos:
                if centro_custo.nome == centro_custo_procurado.nome and empresa.cnpj[0] == empresa_procurada.cnpj[0]:
                    return centro_custo
        return False

    def _verificar_tipo_custo(self):

        if self.tipo_custo == 'Geral':
            self.debito = 'DÉBITO GERAL'
            self.credito = 'CRÉDITO GERAL'
        else:
            self.debito = 'DÉBITO SERVIÇOS'
            self.credito = 'CRÉDITO SERVIÇOS'

    def _gerar_lancamento_decimo(self, lcto_unico, centro_custo, empresa):

        self._verificar_tipo_custo()

        self.debito_evento_geral = self.base_dados['eventos']['13º Salário'][self.debito]
        self.credito_evento_geral = self.base_dados['eventos']['13º Salário'][self.credito]

        if lcto_unico:

            provisao_13 = converter_string_flutuante(
                centro_custo.vlr_saldo_provisao_13)
        else:
            provisao_13 = converter_string_flutuante(
                centro_custo.vlr_saldo_provisao_13) - converter_string_flutuante(self.centro_custo_origem.vlr_saldo_provisao_13)

        provisao_13 = round(provisao_13, 2)

        if provisao_13 < 0:

            provisao_13 *= -1
            self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

        self._gerar_txt_saida(empresa.competencia,
                              empresa.cnpj, provisao_13)

    def _gerar_lancamento_decimo_fgts(self, lcto_unico, centro_custo, empresa):

        self._verificar_tipo_custo()

        self.debito_evento_geral = self.base_dados['eventos']['FGTS s/13º'][self.debito]
        self.credito_evento_geral = self.base_dados['eventos']['FGTS s/13º'][self.credito]

        if lcto_unico:

            provisao_13 = converter_string_flutuante(
                centro_custo.vlr_saldo_fgts_13)
        else:
            provisao_13 = converter_string_flutuante(
                centro_custo.vlr_saldo_fgts_13) - converter_string_flutuante(self.centro_custo_origem.vlr_saldo_fgts_13)

        provisao_13 = round(provisao_13, 2)

        if provisao_13 < 0:

            provisao_13 *= -1
            self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

        self._gerar_txt_saida(empresa.competencia,
                              empresa.cnpj, provisao_13)

    def _gerar_lancamento_decimo_inss(self, lcto_unico, centro_custo, empresa):

        self._verificar_tipo_custo()

        self.debito_evento_geral = self.base_dados['eventos']['INSS s/13º'][self.debito]
        self.credito_evento_geral = self.base_dados['eventos']['INSS s/13º'][self.credito]

        if lcto_unico:

            provisao_13 = converter_string_flutuante(centro_custo.vlr_saldo_inss_13) + \
                converter_string_flutuante(centro_custo.vlr_saldo_terc_13) + \
                converter_string_flutuante(centro_custo.vlr_saldo_rat_13)
        else:

            provisao_2 = converter_string_flutuante(centro_custo.vlr_saldo_inss_13) + \
                converter_string_flutuante(centro_custo.vlr_saldo_terc_13) + \
                converter_string_flutuante(centro_custo.vlr_saldo_rat_13)

            provisao_1 = converter_string_flutuante(self.centro_custo_origem.vlr_saldo_inss_13) + \
                converter_string_flutuante(self.centro_custo_origem.vlr_saldo_terc_13) + \
                converter_string_flutuante(
                    self.centro_custo_origem.vlr_saldo_rat_13)

            provisao_13 = provisao_2 - provisao_1

        provisao_13 = round(provisao_13, 2)

        if provisao_13 < 0:

            provisao_13 *= -1
            self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

        self._gerar_txt_saida(empresa.competencia,
                              empresa.cnpj, provisao_13)

    def _gerar_lancamento_ferias(self, lcto_unico, centro_custo, empresa):

        self._verificar_tipo_custo()

        self.debito_evento_geral = self.base_dados['eventos']['Férias'][self.debito]
        self.credito_evento_geral = self.base_dados['eventos']['Férias'][self.credito]

        if lcto_unico:

            provisao_13 = converter_string_flutuante(centro_custo.vlr_saldo_provisao_ferias) + converter_string_flutuante(
                centro_custo.vlr_saldo_abono)
        else:
            provisao_ferias_2 = converter_string_flutuante(
                centro_custo.vlr_saldo_provisao_ferias) + converter_string_flutuante(centro_custo.vlr_saldo_abono)

            provisao_ferias_1 = converter_string_flutuante(
                self.centro_custo_origem.vlr_saldo_provisao_ferias) + converter_string_flutuante(self.centro_custo_origem.vlr_saldo_abono)

            provisao_13 = provisao_ferias_2 - provisao_ferias_1

        provisao_13 = round(provisao_13, 2)

        if provisao_13 < 0:

            provisao_13 *= -1
            self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

        self._gerar_txt_saida(empresa.competencia,
                              empresa.cnpj, provisao_13)

    def _gerar_lancamento_ferias_fgts(self, lcto_unico, centro_custo, empresa):

        self._verificar_tipo_custo()

        self.debito_evento_geral = self.base_dados['eventos']['FGTS s/Férias'][self.debito]
        self.credito_evento_geral = self.base_dados['eventos']['FGTS s/Férias'][self.credito]

        if lcto_unico:

            provisao_13 = converter_string_flutuante(
                centro_custo.vlr_saldo_fgts_ferias)

        else:

            provisao_13 = converter_string_flutuante(
                centro_custo.vlr_saldo_fgts_ferias) - converter_string_flutuante(self.centro_custo_origem.vlr_saldo_fgts_ferias)

        provisao_13 = round(provisao_13, 2)

        if provisao_13 < 0:

            provisao_13 *= -1
            self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

        self._gerar_txt_saida(empresa.competencia,
                              empresa.cnpj, provisao_13)

    def _gerar_lancamento_ferias_inss(self, lcto_unico, centro_custo, empresa):

        self._verificar_tipo_custo()

        self.debito_evento_geral = self.base_dados['eventos']['INSS s/Férias'][self.debito]
        self.credito_evento_geral = self.base_dados['eventos']['INSS s/Férias'][self.credito]

        if lcto_unico:

            provisao_13 = converter_string_flutuante(centro_custo.vlr_saldo_inss_ferias) + \
                converter_string_flutuante(centro_custo.vlr_saldo_terc_ferias) + \
                converter_string_flutuante(centro_custo.vlr_saldo_rat_ferias)

        else:

            provisao_ferias_2 = converter_string_flutuante(centro_custo.vlr_saldo_inss_ferias) + \
                converter_string_flutuante(centro_custo.vlr_saldo_terc_ferias) + \
                converter_string_flutuante(centro_custo.vlr_saldo_rat_ferias)
            provisao_ferias_1 = converter_string_flutuante(self.centro_custo_origem.vlr_saldo_inss_ferias) + \
                converter_string_flutuante(self.centro_custo_origem.vlr_saldo_terc_ferias) + \
                converter_string_flutuante(
                    self.centro_custo_origem.vlr_saldo_rat_ferias)

            provisao_13 = provisao_ferias_2 - provisao_ferias_1

        provisao_13 = round(provisao_13, 2)

        if provisao_13 < 0:

            provisao_13 *= -1
            self.debito_evento_geral, self.credito_evento_geral = self.credito_evento_geral, self.debito_evento_geral

        self._gerar_txt_saida(empresa.competencia,
                              empresa.cnpj, provisao_13)

    def _gerar_lancamento_provisao(self, centro_custo, empresa, lcto_unico=False):

        if self.folha_pagto[1].tipo == 'décimo':

            self._gerar_lancamento_decimo(
                lcto_unico, centro_custo, empresa)
            self._gerar_lancamento_decimo_fgts(
                lcto_unico, centro_custo, empresa)
            self._gerar_lancamento_decimo_inss(
                lcto_unico, centro_custo, empresa)

        elif self.folha_pagto[1].tipo == 'férias':
            self._gerar_lancamento_ferias(lcto_unico, centro_custo, empresa)
            self._gerar_lancamento_ferias_fgts(
                lcto_unico, centro_custo, empresa)
            self._gerar_lancamento_ferias_inss(
                lcto_unico, centro_custo, empresa)

    def percorrer_relatorio_provisao_mes_posterior(self):

        for empresa in self.folha_pagto[1].empresas:

            if self._se_empresa_esta_no_banco_dados(empresa):
                self.empresa_origem = self._se_empresa_esta_no_mes_anterior(
                    empresa)
                if self.empresa_origem:

                    for centro_custo in empresa.centros_custos:
                        if self._se_centro_custo_cadastrado_banco_dados(
                                centro_custo, empresa):
                            self.centro_custo_origem = self._se_centro_custo_esta_no_mes_anterior(
                                centro_custo, empresa)
                            if self.centro_custo_origem:

                                self._gerar_lancamento_provisao(
                                    centro_custo, empresa)
                            else:
                                self._gerar_lancamento_provisao(centro_custo, empresa,
                                                                lcto_unico=True)
                else:
                    self._gerar_lancamento_provisao(
                        centro_custo, empresa, lcto_unico=True)

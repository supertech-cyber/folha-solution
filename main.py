from controller.controller_prov import gerar_provisoes
from controller.controller_folha import gerar_folha
from acessories.clean_ import clean_generated_files
from models.logs import Logs
from time import sleep
import os

if __name__ == '__main__':

    try:

        sucesso = True

        print('\n\nINICIANDO O PROCESSO...\n')

        sleep(2)

        print('LIMPANDO ARQUIVOS GERADOS ANTERIORMENTE...\n')
        clean_generated_files()

        logs = Logs(filename='arquivos gerados\\logs.log')

        gerar_folha(logs)

        gerar_provisoes(logs)

        print('FINALIZANDO O PROCESSO...\n')

        sleep(3)

        logs.check_sucess()

    except Exception as e:
        print(f'ops...erro --> {e}')
        sucesso = False

    finally:
        if sucesso:
            print('PROCESSO FINALIZADO COM SUCESSO!!!\n')
        os.system('pause')

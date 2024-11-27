import logging


class Logs:

    def __init__(self, filename):

        self.filename = filename

        logging.basicConfig(filename=self.filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

    def create_warning(self, text):

        logging.warning(text)

    def check_sucess(self):

        with open(self.filename, 'r') as file:
            registers = file.readlines()

        if len(registers) == 0:
            logging.info("Mas tá louco, deu certo tchê \\o/")

        else:
            print(registers)

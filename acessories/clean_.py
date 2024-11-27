import os


def clean_generated_files():

    for file_path in os.listdir('arquivos gerados'):

        if os.path.exists(os.path.join('arquivos gerados', file_path)):
            os.remove(os.path.join('arquivos gerados', file_path))

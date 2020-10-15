#!/usr/bin/python3
import zipfile
import os
import json
import csv
from collections import defaultdict

# Pasta raiz onde o subdiretório '/intents/' pode ser encontrado.
DEFAULT_INTENTS_PARENT_LOCATION = 'TeleCOVID'

# Arquivo .csv resultante. É escrito no diretório onde o programa foi executado.
DEFAULT_OUTPUT_CSV_FILE = 'new_qa - Sheet1.csv'

# Sufixo de arquivos '.json' que contém as interações feitas por um usuário.
DEFAULT_QUESTION_SUFFIX = '_usersays_pt-br.json'

def convert_intents_to_csv(directory: str = None, output_name: str = None, suffix: str = None):
    # Procura por todos os intents/perguntas na pasta '/intents/' do diretório fornecido e monta tabela csv com os mesmos.
    #
    # directory := diretório onde deve-se procurar por '/intents/'
    # output_name := nome do arquivo .csv gerado
    # suffix := formato do sufixo que diferencia um .json de intent de um .json questão
    #

    if not directory:
        directory = DEFAULT_INTENTS_PARENT_LOCATION

    if not output_name:
        output_name = DEFAULT_OUTPUT_CSV_FILE

    if not output_name.endswith('.csv'):
        output_name = output_name + '.csv'

    if not suffix:
        suffix = DEFAULT_QUESTION_SUFFIX 

    search_dir = directory + '/intents/'

    if not os.path.isdir(search_dir):
        print('Não foi possível encontrar o subdiretório: ', search_dir)
        sys.exit(2)

    intent_files = [file for file in os.listdir(search_dir) if suffix not in file]
    
    # Abrindo separadamente para ser possível fechar ao fim
    output_file = open(output_name, 'w+')
    output_writer = csv.writer(output_file, delimiter=';', quotechar='\"', quoting=csv.QUOTE_MINIMAL)

    # Header
    output_writer.writerow(['RESPONSE_ID', 'INTENT_NAME', 'QUESTION', 'MESSAGE_SEQ', 'VERBALIZATION_ID', 'TEXT'])
    
    for file in intent_files:
        file_dir = search_dir + file

        with open(file_dir, 'r') as intent:
            response_data = json.load(intent)
            
            response_id = response_data['id']
            response_name = response_data['name']
            questions = {}

            question_file_name = search_dir  + response_name +  suffix

            if os.path.isfile(question_file_name):
                with open(question_file_name, 'r') as question_file:
                    questions_data = json.load(question_file)
                    for chunck in questions_data:
                        question_id = chunck['id'] if 'id' in chunck else 'Sem ID'
                        question_text = ''.join(chunck['data'][i]['text'] for i in range(len(chunck['data'])))
                        questions[question_id] = question_text
            else:
                questions[0] = 'Sem pergunta'

            response_text = defaultdict(list) # Dicionário (ID : Texto)
            for block in response_data['responses']:
                speech_blocks = [x['speech'] for x in block['messages'] if 'speech' in x]
                
                for (number, text_list) in enumerate(speech_blocks):
                    for text in text_list:
                        response_text[number].append(text)
                    
            for key in questions.keys():
                for text_count in response_text.keys():
                    for text in response_text[text_count]:
                        output_writer.writerow([
                            response_id,
                            response_name,
                            questions[key],
                            text_count,
                            key,
                            text
                        ])
                break # Adiciona apenas a primeira variante encontrada da questão.

    output_file.close()

if __name__ == '__main__':
    import sys

    intents_location = sys.argv[1] if len(sys.argv) > 1 else None
    output_name = sys.argv[2] if len(sys.argv) > 2 else None
    suffix_format = sys.argv[3] if len(sys.argv) > 3 else None

    convert_intents_to_csv(intents_location, output_name, suffix_format)

    
        
'''
baixe o csv do google docs, certifique-se que o nome do arquivo baixado é:'new_qa - Sheet1.csv'
baixe o zip do dialogflow,extraia e certifique-se qeu ele a pasta se chama 'TeleCOVID'
deixe esses 2 arquivos na mesma pasta desse script
rode 'python3 csv2json.py'
faça upload do zip gerado no dialogflow

'''

import pandas as pd
import os
import json
import csv
import numpy as np
import math
import shutil



#esse e o nome padrao quando voce baixa o csv no google docs
df = pd.read_csv('new_qa - Sheet1.csv')

#criando um dicionario com os intents e as respostas pra esses intents
#que estao presentes no csv
intent_and_answers = {}

names = df['INTENT NAME'].unique()

for name in names:
	#answers = []
	df_name = df.where(df['INTENT NAME'] == name).dropna()

	#answers.append(df_name['TEXT'].tolist())
	intent_and_answers[name] = df_name['TEXT'].tolist()

#cria um log com os intents que não estao no dialog flow
with open('log.txt', 'w') as f:
	f.write("LISTA DE INTENTS QUE AINDA NÃO ESTÃO NO DIALOGFLOW \n\n\n")

for name, answer in intent_and_answers.items():
	fname = name + '.json'
	if fname in os.listdir('TeleCOVID/intents'):
		file = json.load(open(os.path.join('TeleCOVID/intents/', fname)))
		    
		for response in file['responses']:
		    #aqui trocamos as respostas pelas encontradas no csv
		    for message in response['messages']:
		        message['speech'] = intent_and_answers[name]

		#reescrevedo o arquivo com as respostas corretas        
		with open(os.path.join('TeleCOVID/intents/',fname), 'w') as fp:
		    json.dump(file, fp, ensure_ascii=False, indent=4)
	else:
		#atualiza o log
		with open('log.txt', 'a+') as f:
			f.write(name + '\n')



#fazendo um zip ja alterado que pode ser upado no dialogflow
shutil.make_archive('TeleCOVID', 'zip', 'TeleCOVID')


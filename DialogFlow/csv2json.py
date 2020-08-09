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

for i in range(len(df)):
    intent_name =df['INTENT NAME'][i]

    answers = []

    #comeca do 5 por ser onde comecam as respostas
    j = 5
    size = len(df.columns.tolist())

    #verifico se nao e Nan ja que  Nan sao do tipo float
    while type(df.iloc[i][j]) == type('string'):
        answers.append(df.iloc[i][j]) 
        j+=1

        if j == size:
            break
            
    intent_and_answers[intent_name] = answers



#percorre todos os intents que estao no dicionario
for i in range(len(list(intent_and_answers.keys()))):

	#pega o nome do intent
	name = list(intent_and_answers.keys())[i]
	fname = name + '.json'
	if fname in os.listdir('TeleCOVID/intents'):
		file = json.load(open(os.path.join('TeleCOVID/intents/', fname)))
		    
		for response in file['responses']:
		    j = 0
		    #aqui trocamos as respostas pelas encontradas no csv
		    for message in response['messages']:
		        message['speech'] = intent_and_answers[name]

		#reescrevedo o arquivo com as respostas corretas        
		with open(os.path.join('TeleCOVID/intents/',fname), 'w') as fp:
		    json.dump(file, fp, ensure_ascii=False, indent=4)
	else:
		print('Ainda não existe a intent ' + fname + ' no dialogflow')




#fazendo um zip ja alterado que pode ser upado no dialogflow
shutil.make_archive('TeleCOVID', 'zip', 'TeleCOVID')


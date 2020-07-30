__autho__="thiagocastroferreira"

"""
Name: Thiago Castro Ferreira
Date: 30/07/2020
Description:
	Read the answers from different DialogFlow's intents and structure them in a .csv file.
"""

import csv
import os
import json

data = []
for fname in os.listdir('TeleCovid/intents'):
    if '_usersays_pt-br' not in fname:
        try:
            intent = json.load(open(os.path.join('TeleCovid/intents', fname)))
            intent_name = intent['name']
            questions = json.load(open(os.path.join('TeleCovid/intents', intent_name + '_usersays_pt-br.json')))
            question = []
            for row in questions[0]['data']:
                question.append(row['text'].strip())
            question = ' '.join(question)
            
            for response in intent['responses']:
                for message in response['messages']:
                    speech = message['speech']
                    data.append([intent_name, question, speech])
        except:
            print(fname)

with open('qa.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    for row in sorted(data, key=lambda x: x[0]):
        writer.writerow(row) 
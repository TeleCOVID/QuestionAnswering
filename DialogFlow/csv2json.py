import csv
import os
import json
from collections import defaultdict

DEFAULT_CSV_NAME = 'new_qa - Sheet1.csv'

def convert_csv_to_intents(csv_name: str = None):
    if not csv_name:
        csv_name = DEFAULT_CSV_NAME

    csv_intent_responses = defaultdict(set)
    with open(csv_name, 'r') as file:
        csv_file = csv.DictReader(file, delimiter=';')
        for row in csv_file:
            csv_intent_responses[(row['INTENT_NAME'], int(row['MESSAGE_SEQ']))].add(row['TEXT'].replace('\r', '').replace('\n', ''))

    search_dir = 'TeleCOVID/intents/'
    for intent_file_name in os.listdir(search_dir):
        if 'usersays' not in intent_file_name:
            with open(search_dir + intent_file_name, 'r') as intent_file:
                intent_data = json.load(intent_file)

                actual_name = intent_data['name']
                messages_speech_blocks = [block for block in intent_data['responses'][0]['messages'] if 'speech' in block]
                for seq, response_block in enumerate(messages_speech_blocks):
                    possible_responses = set([response.replace('\r', '').replace('\n', '') for response in response_block['speech']])

                    if possible_responses == csv_intent_responses[(actual_name, seq)]:
                        pass
                    else:
                        response_block['speech'] = list(csv_intent_responses[(actual_name, seq)] - possible_responses)

            with open(search_dir + intent_file_name, 'w') as intent_file:
                json.dump(intent_data, intent_file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    import sys

    csv_name = sys.argv[1] if len(sys.argv) > 1 else None

    convert_csv_to_intents(csv_name)
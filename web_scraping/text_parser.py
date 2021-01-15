import json
from difflib import SequenceMatcher

imp_str_lst = [
    ' CEO ',
    ' C.E.O ',
    ' stock ',
    ' AMD ',
    'bull',
    'bear',
    ' market',
    ' high ',
    ' low ',
    ' overperform ',
    ' underperform ',
    ' rip ',
    ' death ',
    ' pop ',
    ' drop ',
    ' CFO ',
    ' C.F.O ',
    ' overreact',
    ' quarter ',
    ' quartile ',
    ' percent ',
    '%',
]

def compare_strings(class_data, string):
    for cnt, element in enumerate(class_data):
        if SequenceMatcher(lambda x: x in [' ', ' and ', ' the ', ' to ', ' is ', '\n', '\t'],  element['text'], string).ratio() > 0.50:
            print(element['text'])
            print('SIMILARITY SCORE TO')
            print(string)
            return cnt
    return -1 

def find_important_strings(string, string_list):
    for s in string_list:
        if s.lower() in string.lower():
            return 1
    return 0


def read_web_text_json_file(path):
    with open(path) as inputfile:
        data = json.load(inputfile)
    """Structure of data is as follows:
       data:{dates:{sites:{text:[str], links:[str]}}}"""
    classified_data = []
    for date in data.keys():
        for site in data[date]:
            for link in data[date][site]:
                for text in data[date][site][link]['text']:
                    if find_important_strings(text, imp_str_lst):
                        compare_string_reuslt = -1
                        if classified_data:
                            compare_string_reuslt = compare_strings(classified_data, text)
                        
                        if compare_string_reuslt == -1:
                            text_classification = None
                            while text_classification == None:
                                print("Please classify as good(+), bad(-), or indifferent(0): ")
                                print(text)
                                inp = input()
                                if  inp == '=':
                                    text_classification = 1
                                elif inp == '-':
                                    text_classification = -1
                                elif inp == '0':
                                    text_classification = 0
                                elif inp == 'end':
                                    return classified_data

                            classified_data.append(
                                {'date': date,
                                'site': site,
                                'text': text,
                                'class': text_classification
                                }
                            )
                        elif compare_string_reuslt == 1:
                            pass
                        else:
                            classified_data.append(
                                {'date': date,
                                'site': site,
                                'text': text,
                                'class': classified_data[compare_string_reuslt]['class']
                                }
                            )
                    else:
                        classified_data.append(
                                {'date': date,
                                'site': site,
                                'text': text,
                                'class': 0
                                }
                            )
    return classified_data


import csv
import json

def retorno_de_json(direccion):
    with open(direccion,newline= '') as File:
        reader = csv.reader(File)
        dic_adc  = {'ADC':[]}
        for row in reader:
            dic_adc['ADC'].append(row[2])
        json_a_enviar = json.dumps(dic_adc)
        return json_a_enviar     
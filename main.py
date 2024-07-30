from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def calc_turnaround_fifo():
    lista_processos = request.json
    tempo_atual = turn_total = 0
    lista_ordenada_tempo_chegada = sorted(lista_processos, key=lambda dicionario: dicionario['T_chegada']) #Isso ordena os processos pelo tempo de chegada
    for k, v in enumerate(lista_ordenada_tempo_chegada): #Acessar individualmente cada dicionario(processo) dentro da lista
        if tempo_atual < v['T_chegada']:
                tempo_atual = v['T_chegada']
        tempo_atual += v['T_exec']
        v['Termino'] = tempo_atual
        v['Turnaround'] = v['Termino'] - v['T_chegada']
        turn_total += v['Turnaround']
    turn_medio = turn_total / len(lista_ordenada_tempo_chegada)


    response = {
         "turnaround" : turn_medio
    }
    return jsonify(response)


if __name__ == '__main__':
     app.run(debug=True)




#meu_dicionario = [{'T_chegada': 11, 'T_exec': 3, 'Termino': 0, 'Turnaround': 0}, {'T_chegada': 4, 'T_exec': 4, 'Termino': 0, 'Turnaround': 0}, {'T_chegada': 2, 'T_exec': 1, 'Termino': 0, 'Turnaround': 0}, {'T_chegada': 2, 'T_exec': 3, 'Termino': 0, 'Turnaround': 0}] # Caso de teste




# [{"T_chegada": 11, "T_exec": 3, "Termino": 0, "Turnaround": 0}, {"T_chegada": 4, "T_exec": 4, "Termino": 0, "Turnaround": 0}, {"T_chegada": 2, "T_exec": 1, "Termino": 0, "Turnaround": 0}, {"T_chegada": 2, "T_exec": 3, "Termino": 0, "Turnaround": 0}] # Caso de teste no postman
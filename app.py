from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/fifo/submit', methods=['POST'])
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


@app.route('/sjf/submit', methods=['POST'])
def calc_turnaround_sjf(dicionario):
        lista_processos = dicionario
        tempo_atual = turn_total = 0
        processos_restantes = sorted(lista_processos, key=lambda dicionario: (dicionario['T_chegada'], dicionario['T_exec']))
        
        while processos_restantes:
            processos_disponiveis = []
            for k, v in enumerate(processos_restantes):
                if v['T_chegada'] <= tempo_atual:
                    processos_disponiveis.append(v)

            
            if not processos_disponiveis:
                tempo_atual = processos_restantes[0]['T_chegada']
                processos_disponiveis = []
                for k, v in enumerate(processos_restantes):
                    if v['T_chegada'] <= tempo_atual:
                        processos_disponiveis.append(v)

            processo = min(processos_disponiveis, key=lambda dicionario: dicionario['T_exec'])
            processos_restantes.remove(processo)
            
            tempo_atual += processo['T_exec']
            processo['Termino'] = tempo_atual  # Atualizado para calcular o tempo de término
            processo['Turnaround'] = processo['Termino'] - processo['T_chegada']
            turn_total += processo['Turnaround']
        
        turn_medio = turn_total / len(lista_processos)
        return jsonify(turn_medio) 




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)




#meu_dicionario = [{'T_chegada': 11, 'T_exec': 3, 'Termino': 0, 'Turnaround': 0}, {'T_chegada': 4, 'T_exec': 4, 'Termino': 0, 'Turnaround': 0}, {'T_chegada': 2, 'T_exec': 1, 'Termino': 0, 'Turnaround': 0}, {'T_chegada': 2, 'T_exec': 3, 'Termino': 0, 'Turnaround': 0}] # Caso de teste




# [{"T_chegada": 11, "T_exec": 3, "Termino": 0, "Turnaround": 0}, {"T_chegada": 4, "T_exec": 4, "Termino": 0, "Turnaround": 0}, {"T_chegada": 2, "T_exec": 1, "Termino": 0, "Turnaround": 0}, {"T_chegada": 2, "T_exec": 3, "Termino": 0, "Turnaround": 0}] # Caso de teste no postman
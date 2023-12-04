from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

def primeiroNome(nome):
    primeiro_nome = nome.capitalize()
    return primeiro_nome

@app.route('/nome', methods=['POST'])
def process_request():
    try:
        data = request.get_json()
        if 'nome' in data:
            nome = data['nome']
            separa = nome.split(' ')
            nome = separa[0]

            return jsonify({'primeiro_nome': primeiroNome(nome)})
        else:
            return jsonify({'error': 'Chave "nome" ausente nos dados enviados'}), 400
    except Exception as e:
        return jsonify({'error': 'Ocorreu um erro ao processar a requisição'}), 500

@app.route('/update_nome', methods=['POST'])
def update_nome():
    data = request.get_json()

    idcliente = data.get('idcliente')
    nome = data.get('nome')

    if idcliente is None or nome is None:
        return jsonify({"error": "Missing 'idcliente' or 'nome' parameter"}), 400

    token = "6c7d502747be67acc199b483803a28a0c9b95c09"
    url = f"https://api.pipedrive.com/v1/persons/{idcliente}?api_token={token}"

    payload = json.dumps({
        "1ea178345045fc92ba5ddc78b96240937e203674": nome
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': '__cf_bm=PfhXJIqvOvf8O4wDqcy27JjtFDIsMP_X6Je1HnEatQ4-1691098322-0-Afh40xDURFcJGZx3WEJl0eIOttDvPKGZU0Vb51tqEKrQ+VxwnCyOghViyqubnNHeur94KdjysCmgW3ofXzcfR/A='
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    if response.ok:
        return jsonify({"success": True, "message": "Nome atualizado com sucesso!"}), 200
    else:
        return jsonify({"success": False, "message": "Falha ao atualizar o nome"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

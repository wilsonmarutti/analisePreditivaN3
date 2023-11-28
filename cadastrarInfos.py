import random
from pymongo import MongoClient

def gerar_dados_ficticios():
    idade = random.randint(18, 80)
    salarioAnual = random.randint(20000, 180000)
    sexo = random.choice(['Masculino', 'Feminino'])
    estadoCivil = random.choice(['Solteiro', 'Casado', 'Divorciado', 'Viúvo'])
    escolaridade = random.choice(['Doutorado', 'Mestrado', 'Graduação', 'Pós-graduação'])
    nivelCargo = random.choice(['trainee', 'Junior', 'Pleno', 'Senior'])
    nome = "******"
    sobrenome = "******"


    dados = {
        'nome': nome,
        'sobrenome': sobrenome,
        'idade': idade,
        'sexo': sexo,
        'estadoCivil': estadoCivil,
        'escolaridade': escolaridade,
        'nivelCargo': nivelCargo,
        'salarioAnual': salarioAnual,
    }

    return dados

if __name__ == '__main__':
    client = MongoClient("mongodb+srv://wilsonmarutti:6S0oLpmf8IchaNlm@cluster0.uvdvhmj.mongodb.net/?retryWrites=true&w=majority")

    db = client.get_database('Cluster0')
    collection = db.mycollection

    num_registros = 500

    data_to_insert = []

    for i in range(num_registros):
        funcionario = gerar_dados_ficticios()
        data_to_insert.append(funcionario)


    # Inserir dados na coleção
    inserted_data = collection.insert_many(data_to_insert)

    # Verificar se a inserção foi bem-sucedida
    if inserted_data.acknowledged:
        print("Dados inseridos com sucesso. ID:", inserted_data)
    else:
        print("Falha ao inserir dados.")

    # Fechar a conexão com o MongoDB

    print(list(collection.find()))

    client.close()
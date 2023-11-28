# ETL completo
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

# Conexão com o MongoDB
client = MongoClient("mongodb+srv://wilsonmarutti:6S0oLpmf8IchaNlm@cluster0.uvdvhmj.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('Cluster0')
collection = db.mycollection

# Extração
dados = list(collection.find())

# Transformação
data = pd.DataFrame(dados)

# Substituir valores desconhecidos
data['nome'] = data['nome'].replace('******', 'Desconhecido')
data['sobrenome'] = data['sobrenome'].replace('******', 'Desconhecido')

# Pré-processamento adicional para a modelagem
# Convertendo dados categóricos em numéricos usando a técnica one-hot encoding
data = pd.get_dummies(data, columns=['sexo', 'estadoCivil', 'escolaridade', 'nivelCargo'])

# Dividindo os dados em características (features) e variável alvo (target)
X = data.drop(columns=['_id', 'nome', 'sobrenome', 'idade'])  # Removendo colunas não utilizadas
y = data['idade'].astype(int)  # Certificando-se de que a idade é um inteiro

# Dividindo os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Construindo o modelo de regressão
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Realizando previsões no conjunto de teste
y_pred = modelo.predict(X_test)

# Calculando as métricas
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)

# Imprimindo as métricas
print(f"Erro Quadrático Médio: {mse:.2f}")
print(f"Erro Quadrático Médio Raiz: {rmse:.2f}")
print(f"Erro Absoluto Médio: {mae:.2f}")

# Carregamento
# Criar ou obter a nova coleção
collection_processed = db.mycollection_processed

# Excluir dados existentes (opcional, mas evita duplicatas)
collection_processed.delete_many({})

# Carregar os dados pré-processados
collection_processed.insert_many(data.to_dict('records'))

print("Dados pré-processados carregados com sucesso!")
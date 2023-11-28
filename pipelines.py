import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Conexão com o MongoDB
client = MongoClient("mongodb+srv://wilsonmarutti:6S0oLpmf8IchaNlm@cluster0.uvdvhmj.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('Cluster0')
collection = db.mycollection

# Carregando os dados
dados = list(collection.find())

# Convertendo os dados para um DataFrame do Pandas
data = pd.DataFrame(dados)

# Pré-processamento inicial
data['nome'] = data['nome'].replace('******', 'Desconhecido')
data['sobrenome'] = data['sobrenome'].replace('******', 'Desconhecido')
data['salarioAnual'] = data['salarioAnual'].astype(int)

# Separando os dados (features) e os rótulos (labels)
X = data.drop('idade', axis=1)
y = data['idade']

# Dividindo os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline para variáveis categóricas
categorical_features = ['sexo', 'estadoCivil', 'escolaridade', 'nivelCargo']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Pipeline para variáveis numéricas
numeric_features = ['salarioAnual']
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Combinando os pipelines em um único pré-processador
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
])

# Pipeline completo incluindo pré-processamento e modelo
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor())
])

# Treinando o modelo com os dados de treino
model.fit(X_train, y_train)

# Predizendo as idades no conjunto de teste
y_pred = model.predict(X_test)

# Avaliando o modelo usando o erro quadrático médio (MSE)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Encerrando a conexão com o banco de dados
client.close()

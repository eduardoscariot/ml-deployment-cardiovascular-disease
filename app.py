import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import requests
import json
import sys

# URL da API local
API_URL = "http://127.0.0.1:8000"

# Verificar senha de acesso
#if not util.check_password():
#    st.stop()  # Se tiver incorreta, não permite prosseguir na aplicação.

# Recuperar os dados via API - Diagnóstico de Doenças Cardiovasculares
response = requests.get(f"{API_URL}/get-dataset")

# Se o código da resposta da API for diferente de 200, apresenta mensagem de erro e da exceção 
if response.status_code != 200:
    msg = f"Falha ao recuperar os dados: {response.status_code}"
    print(msg)
    raise Exception(msg)

# Fazer a conversão do JSON de retorno para dataframe
dados_json = json.loads(response.json())
dados = pd.DataFrame(dados_json)

# Montar layout
st.title('App dos dados de diagnóstico de doença cardiovascular')
data_analyses_on = st.toggle('Exibir análise dos dados')

# Se foi selecionado para apresentar os dados, apresenta o dataframe, um histograma de idades e a quantidade de registros com e sem doença.
if data_analyses_on:

    st.dataframe(dados)

    st.header("Histograma - Idade")
    fig = plt.figure()
    plt.hist(dados['age'], bins=30)
    plt.xlabel("Idade")
    plt.ylabel("Quantidade")
    st.pyplot(fig)

    st.header("Diagnóstico de doença cardíaca (diagnóstico angiográfico)")
    st.bar_chart(dados.target.value_counts())

# Vai montar as linhas de campos de entrada de dados
st.header('Preditor de doença cardíaca')

# Row 1
col1, col2, col3 = st.columns(3)
with col1:
    #age - idade em anos
    age = st.number_input("Age in years", step=1, min_value=0)

with col2:
    #sex - sexo do paciente [0: mulher, 1: homem]
    classes = ["Female", "Male"]
    sex = st.selectbox('Sex', classes)

with col3:
    #cp - tipo da dor torácica [1: angina típica, 2: angina atípica, 3: dor não cardíaca, 4: assintomática]
    classes = ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"]
    cp = st.selectbox('Chest pain', classes)

# Row 2
col1, col2, col3 = st.columns(3)
with col1:
    #trestbps - pressão arterial em repouso
    trestbps = st.number_input("Resting Blood Pressure", step=1, min_value=0)

with col2:
    #chol - colesterol sérico (mg/dl)
    chol = st.number_input("Serum Cholesterol (mg/dl)", step=1, min_value=0)

with col3:
    #fbs - açucar no sangue em jejum > 120mg/dl [0: False, 1: True]
    classes = ["False", "True"]
    fbs = st.selectbox('Fasting Blood Sugar > 120mg/dl', classes)

# Row 3
col1, col2, col3 = st.columns(3)
with col1:
    #restecg - resultado do eletrocardiografia de repouso 
    #[0: normal, 
    # 1: anormalidades de ST-T (inversão da onda T e elevação ou depressão de > 0.05mV), 
    # 2: hipertrofia ventricular esquerda provável ou definitiva (pelos critérios de Romhilt-Estes)]
    classes = ["Normal", "ST-T abnormalities", "Probable or definite left ventricular hypertrophy"]
    restecg = st.selectbox("Resting Electrocardiography Result", classes)

with col2:
    #thalach - frequência cardíaca máxima atingida
    thalach = st.number_input("Maximum Heart Rate Reached", step=1, min_value=0)

with col3:
    #exang - angina induzida pelo exercício [0: não, 1: sim]
    classes = ["No", "Yes"]
    exang = st.selectbox('Exercise-induced Angina', classes)

# Row 4
col1, col2, col3 = st.columns(3)
with col1:
    #oldpeak - depessão do segmento ST induzida pelo exercício em relação ao repouso
    oldpeak = st.number_input("Exercise-induced ST segment depression relative to rest", step=0.1, min_value=0.0)

with col2:
    #slope - inclinação do segmento ST no pico do exercício
    classes = ["Upsloping", "Flat", "Downsloping"]
    slope = st.selectbox('Slope of the Peak Exercise ST Segment', classes)

with col3:
    #ca - número de vasos principais colorido por fluoroscopia
    classes = [0, 1, 2, 3]
    ca = st.selectbox('Number of Major Vessels Colored by Flourosopy', classes)

# Row 4
col1, col2, col3 = st.columns(3)
with col1:
    # thal (Thalassemia) - teste de esforço cardíaco [3: normal, 6: defeito fixo, 7: defeito reversível]
    classes = ["Normal", "Fixed defect", "Reversible defect"]
    thal = st.selectbox('Thalassemia', classes)

with col2:
     # Botão para realizar a predição
     submit = st.button("Verificar")

# Dicionário para armazenar dados do paciente
paciente = {}

# Verificar se o botão de fazer a predição foi pressionado ou se o campo 'target' está em cache
if submit or 'target' in st.session_state:
    # Alimentar o objeto do paciente
    paciente = {
        'age': age,
        'sex': sex,
        'cp': cp,
        'trestbps': trestbps,
        'chol': chol,
        'fbs': fbs,
        'restecg': restecg,
        'thalach': thalach,
        'exang': exang,
        'oldpeak': oldpeak,
        'slope': slope,
        'ca': ca,
        'thal': thal,
    }

    # Realiza uma requisição POST para a nossa API, com o intuito de realizar a predição
    # Para a predição é enviado o objeto do paciente como um JSON.
    response = requests.post(f"{API_URL}/predict", json=json.dumps(paciente))
    result = None

    # Se o código da resposta da API for diferente de 200, apresenta mensagem de erro e da exceção 
    if response.status_code != 200:
        msg = f"Falha ao efetuar a predição: {response.status_code}"
        print(msg)
        raise Exception(msg)

    # Recuperar o retorno da API
    result = response.json()

    if result is not None:
        disease = result

        # Resultado: 1 = no disease | 2 = disease
        if disease == 1:
            st.subheader("Paciente não tem problemas cardíacos.")
            if 'target' not in st.session_state:
                st.balloons()
        else:
            st.subheader("Detectado problema cardíaco")
            if 'target' not in st.session_state:
                st.snow()

        # Armazenar o resultado da predição na sessão
        st.session_state['target'] = disease

    # Validação para solicitar feedback quando for feita uma nova predição
    if paciente and 'target' in st.session_state:
        st.write("A predição está correta?")

        col1, col2, col3 = st.columns([1,1,5])
        with col1:
            correct_prediction = st.button("👍")
        with col2:
            wrong_prediction = st.button("👎")

        if correct_prediction or wrong_prediction:
            message = "Muito obrigado pelo seu feedback. "
            if wrong_prediction:
                message += "Iremos utilizar esses dados para melhorar nosso modelo."

            if correct_prediction:
                paciente['CorrectPrediction'] = True
            elif wrong_prediction:
                paciente['CorrectPrediction'] = False

            paciente['target'] = st.session_state['target']
            st.write(message)

            # Salvar predição
            response = requests.post(f"{API_URL}/save-prediction", json=json.dumps(paciente))
            if response.status_code != 200:
                msg = f"Falha ao salvar a predição: {response.status_code}"
                print(msg)
                raise Exception(msg)


    col1, col2, col3 = st.columns(3)

    with col2:
        new_test = st.button("Iniciar nova análise")

        if new_test and 'target' in st.session_state:
            del st.session_state['target']
            st.rerun()

accuracy_prediction_on = st.toggle("Exibir acurácia")

if accuracy_prediction_on:
    # Recuperar as predições
    response = requests.get(f"{API_URL}/get-all-predictions")
    if response.status_code != 200:
        msg = f"Falha ao recuperar as predições: {response.status_code}"
        print(msg)
        raise Exception(msg)

    predictions = response.json()

    num_total_predictions = len(predictions)
    correct_predictions = 0
    total = 0
    accuracy_hist = []
    for index, paciente in enumerate(predictions):
        
        total = total + 1
        if paciente['CorrectPrediction'] == True:
            correct_predictions += 1

        temp_accuracy = correct_predictions / total if total else 0
        accuracy_hist.append(round(temp_accuracy, 2))

    accuracy = correct_predictions / num_total_predictions if num_total_predictions else 0

    st.metric("Acurácia", round(accuracy, 2))

    st.subheader("Histórico de acurácia")
    st.line_chart(accuracy_hist)



import pandas as pd
import json
import pickle

def load_data():
    dados = pd.read_csv('./data/heart-disease-uci.csv')
    return dados

def get_all_predictions():
    data = None
    with open('predictions.json', 'r') as f:
        data = json.load(f)
        
    return data

SEX_MAP = {
    'Female': 0,
    'Male': 1,
}
CHEST_PAIN_MAP = {
    'Typical Angina': 1, 
    'Atypical Angina': 2, 
    'Non-anginal Pain': 3, 
    'Asymptomatic': 4,
}
FBS_MAP = {
    'False': 0, 
    'True': 1,
}
RESTECG_MAP = {
    'Normal': 0, 
    'ST-T abnormalities': 1,
    'Probable or definite left ventricular hypertrophy': 2,
}
EXANG_MAP = {
    'No': 0, 
    'Yes': 1,
}
SLOPE_MAP = {
    'Upsloping': 1, 
    'Flat': 1,
    'Downsloping': 3,
}
THAL_MAP = {
    'Normal': 3, 
    'Fixed defect': 6,
    'Reversible defect': 7,
}

def save_prediction(paciente):
    paciente['sex'] = SEX_MAP[paciente['sex']]
    paciente['cp'] = CHEST_PAIN_MAP[paciente['cp']]
    paciente['fbs'] = FBS_MAP[paciente['fbs']]
    paciente['restecg'] = RESTECG_MAP[paciente['restecg']]
    paciente['exang'] = EXANG_MAP[paciente['exang']]
    paciente['slope'] = SLOPE_MAP[paciente['slope']]
    paciente['thal'] = THAL_MAP[paciente['thal']]

    data = get_all_predictions()
    data.append(paciente)
    with open('predictions.json', 'w') as f:
        json.dump(data, f)

def diagnosis_predict(paciente):
    paciente['sex'] = SEX_MAP[paciente['sex']]
    paciente['cp'] = CHEST_PAIN_MAP[paciente['cp']]
    paciente['fbs'] = FBS_MAP[paciente['fbs']]
    paciente['restecg'] = RESTECG_MAP[paciente['restecg']]
    paciente['exang'] = EXANG_MAP[paciente['exang']]
    paciente['slope'] = SLOPE_MAP[paciente['slope']]
    paciente['thal'] = THAL_MAP[paciente['thal']]

    values = pd.DataFrame([paciente])
    
    # Recuperar o modelo
    model = pickle.load(open('./models/heart_disease_model.pkl', 'rb'))

    results = model.predict(values)
    result = None

    if len(results) == 1:
        result = int(results[0])

    return result


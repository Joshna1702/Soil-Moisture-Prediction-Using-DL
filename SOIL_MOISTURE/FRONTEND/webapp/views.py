from django.shortcuts import render, HttpResponse
import numpy as np
import pickle
import joblib

# Load the models and scaler
cnn_model = pickle.load(open('cnn_model.pkl', 'rb'))
lstm_model = pickle.load(open('lstm_model.pkl', 'rb'))
lgbm_model = pickle.load(open('lgbm_model.pkl', 'rb'))
scaler = joblib.load('scaler.pkl')

def home(request):
    return render(request, 'index.html')

def input(request):
    file_name = 'account.txt'
    name = request.POST.get('name')
    password = request.POST.get('password')
    with open(file_name, 'r') as file:
        account_list = [line.split() for line in file]
    for account in account_list:
        if account[0] == name and account[1] == password:
            return render(request, 'input.html')
    return HttpResponse('Wrong Password or Name', content_type='text/plain')

def output(request):
    if request.method == 'POST':
        # Collect data from form inputs
        features = [
            float(request.POST.get('N')),
            float(request.POST.get('P')),
            float(request.POST.get('K')),
            float(request.POST.get('temperature')),
            float(request.POST.get('humidity')),
            float(request.POST.get('ph')),
            float(request.POST.get('rainfall'))
        ]

        # Reshape and scale input data
        scaled_features = scaler.transform([features])
        reshaped_cnn = scaled_features.reshape((1, scaled_features.shape[1], 1))  # CNN format
        reshaped_lstm = scaled_features.reshape((1, 1, scaled_features.shape[1]))  # LSTM format

        # Get selected algorithm from the form
        algorithm = request.POST.get('algorithm')

        # Predictions based on the selected algorithm
        if algorithm == 'cnn':
            prediction = cnn_model.predict(reshaped_cnn)[0][0]
        elif algorithm == 'lstm':
            prediction = lstm_model.predict(reshaped_lstm)[0][0]
        elif algorithm == 'lgbm':
            prediction = lgbm_model.predict(scaled_features)[0]
        else:
            prediction = None

        return render(request, 'output.html', {
            'algorithm': algorithm,
            'cnn_prediction': cnn_model.predict(reshaped_cnn)[0][0] if algorithm == 'cnn' else None,
            'lstm_prediction': lstm_model.predict(reshaped_lstm)[0][0] if algorithm == 'lstm' else None,
            'lgbm_prediction': lgbm_model.predict(scaled_features)[0] if algorithm == 'lgbm' else None,
            'prediction': prediction  # Can be used if you need a generic prediction variable
        })

    return render(request, 'input.html')

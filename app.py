import os
from flask import Flask, jsonify, request, url_for
from werkzeug.utils import secure_filename
import joblib
import pandas as pd
from datatime import datetime


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Passar o path do modelo a ser usado
# model = joblib.load('path')

@app.route('/classify', methods=['GET', 'POST'])
def classify_fruits():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'Erro': 'Nenhum arquivo foi enviado na request'}), 400
    
        file = request.file['file']
        if file.filename == '':
            return jsonify({'Erro': 'Nenhum arquivo foi enviado na request'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = f'{filename.split(".")[0]}_{str(datetime.now())}.csv'
            save_location = os.path.join('savedCsv', new_filename)
            file.save(save_location)
        try:
            df = pd.read_csv(save_location)

            #Falta colocar as features
            features = df[['feature1', 'feature2', 'feature3']]  # example features

            predictions = model.predict(features)

            response = {
                'predictions': predictions.tolist()
            }

            return jsonify(response)

        except Exception as e:
            return jsonify({'Erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
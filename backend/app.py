from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import yagmail
import os
from obtener_datos_frontera import obtener_datos_frontera
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Hardcodear los valores de configuración del correo electrónico
EMAIL_USER = "luiscarlospxr@gmail.com"
EMAIL_PASS = "funnrjgilrohagbe"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Imprimir los valores de las variables de configuración
print("EMAIL_USER:", EMAIL_USER)
print("EMAIL_PASS:", EMAIL_PASS)
print("SMTP_SERVER:", SMTP_SERVER)
print("SMTP_PORT:", SMTP_PORT)

@app.route('/')
def home():
    return jsonify({"message": "Backend está funcionando correctamente"})

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Received a request at /upload")
    file = request.files['file']
    date = request.form['date']
    email = request.form['email']

    # Imprimir los datos recibidos
    print(f"File received: {file.filename}")
    print(f"Date received: {date}")
    print(f"Email received: {email}")

    sic_codes_df = pd.read_excel(file)
    Fronteras = NEU_API(sic_codes_df, date)
    print("ARCHIVO GENERADO EN CONSULTA:", Fronteras)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"Fronteras_{date}_{current_time}.xlsx"
    Fronteras.to_excel(file_name, index=False)

    # Enviar el correo electrónico
    send_email(email, file_name)
    os.remove(file_name)

    return jsonify({
        'message': 'File processed and email sent successfully!',
        'fileName': file_name,
        'date': date,
        'email': email
    })

@app.route('/send-email', methods=['POST'])
def send_email_route():
    data = request.get_json()
    email = data['email']
    file_name = data['fileName']
    send_email(email, file_name)
    os.remove(file_name)
    return jsonify({'message': 'Email sent successfully!'})

def send_email(to_email, file_name):
    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
    yag.send(
        to=to_email,
        subject='Fronteras Data',
        contents='Please find the attached file.',
        attachments=file_name,
    )

def NEU_API(sic_codes_df, date):
    # Crear un dataframe vacío para almacenar los resultados
    Fronteras = pd.DataFrame()

    # Recorrer todos los valores de sic_code y obtener los datos de frontera
    for sic_code in sic_codes_df.iloc[:, 0]:
        Frontera = obtener_datos_frontera(sic_code, date)
        if Frontera is not None:
            Fronteras = pd.concat([Fronteras, Frontera], ignore_index=True)
    return Fronteras

if __name__ == '__main__':
    print("Iniciando servidor Flask en http://127.0.0.1:3000")
    app.run(host='127.0.0.1', port=3000, debug=True)
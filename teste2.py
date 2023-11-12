# Por favor professor ver a documentação e principalmente o README para poder rodar o projeto. 

import random
import cv2 
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for, send_from_directory
from ultralytics import YOLO
import pytesseract
from PIL import Image
import cx_Oracle
import re

app = Flask(__name__, static_folder='static')

#informaçoes banco de dados

db_user = 'rm99150'
db_password = '180101'
db_dsn = cx_Oracle.makedsn(host="oracle.fiap.com.br", port=1521, sid="orcl")



# Carregue o modelo YOLOv8n pré-treinado

model = YOLO("weights/yolov8n.pt", "v8")

# Carregar a lista de classes do COCO
class_list_path = "img/coco-classes.txt"
with open(class_list_path, "r") as file:
    class_list = file.read().split("\n")


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Função para gerar quadros da webcam
def generate():

    

    video_capture = cv2.VideoCapture(0)  # Usar a webcam (índice 0)

    while True:
        ret, frame = video_capture.read()

        if ret:
            frame = detect_bike(frame)
            _, jpg = cv2.imencode('.jpg', frame)
            frame_data = jpg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

# Rota para a página de streaming
@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Gerar cores aleatórias para cada classe
detection_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in class_list]

# Pasta para armazenar as imagens capturadas
captured_images_folder = "captured_images/"

# Função para realizar a detecção e processar os quadros da webcam

def detect_bike(frame):

    detect_params = model.predict(source=[frame], conf=0.45, save=False)

    bike_detected = False  # Flag para verificar se uma bicicleta foi detectada

    if len(detect_params[0]) != 0:
        for i, box in enumerate(detect_params[0].boxes):
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]

            cv2.rectangle(
                frame,
                (int(bb[0]), int(bb[1])),
                (int(bb[2]), int(bb[3])),
                detection_colors[int(clsID)],
                3,
            )

            # Mostrar nome da classe e confiança
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(
                frame,
                f"{class_list[int(clsID)]} {conf:.3f}%",
                (int(bb[0]), int(bb[1]) - 10),
                font,
                1,
                (255, 255, 255),
                2,
            )


            # Verificar se uma bicicleta foi detectada
            if class_list[int(clsID)] == "bicicleta":
                bike_detected = True

    if bike_detected:
        # Mostrar mensagem se uma bicicleta foi detectada
        cv2.putText(frame, "Bicicleta detectada", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    else:
        # Mostrar mensagem se nenhuma bicicleta foi detectada
        cv2.putText(frame, "mostre uma bicicleta", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return frame



# Rota para renderizar a página inicial
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    # Lógica para renderizar a página de cadastro
    return render_template('cadastro.html')

@app.route('/processar_cadastro', methods=['POST'])
def processar_cadastro():
    bike_modelo = request.form.get('bike_modelo')
    ano_fabricacao = request.form.get('ano_fabricacao')
    numero_serie = request.form.get('numero_serie')
    bike_cor = request.form.get('bike_cor')
    bike_marca = request.form.get('bike_marca')
    bike_valor = request.form.get('bike_valor')

    try:
        cx_Oracle.init_oracle_client(lib_dir=r"E:\oracle\instantclient_21_12")
    except cx_Oracle.ProgrammingError as e:
        pass

    # Conecte-se ao banco de dados Oracle
    connection = cx_Oracle.connect(db_user, db_password, db_dsn)
    cursor = connection.cursor()


    sql = "INSERT INTO bicicleta (bike_modelo, ano_fabricacao, numero_serie, bike_cor, bike_marca, bike_valor) VALUES (:bike_modelo, :ano_fabricacao, :numero_serie, :bike_cor, :bike_marca, :bike_valor)"
    cursor.execute(sql, (bike_modelo, ano_fabricacao, numero_serie, bike_cor, bike_marca, bike_valor))

   
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('reconhecimento'))

@app.route('/reconhecimento')
def reconhecimento():
    return render_template('reconhecimento.html')

@app.route('/video/<filename>')
def video(filename):
    return send_from_directory('static', filename)

@app.route('/partes')
def partes():
    return render_template('partes.html')

def extract_text_from_image(image_path):
    try:
        # Abrir a imagem usando a biblioteca Pillow (PIL)
        img = Image.open(image_path)

        # Extrair o texto da imagem usando o Tesseract OCR
        text = pytesseract.image_to_string(img)

        # Verificar se o texto atende ao formato de chassi de bicicleta
        #asdsad
        if re.match(r'^[A-Z]{2}\d{1,10}$', text):
            return text
        else:
            return "Não é possível identificar o chassi de bicicleta."

    except Exception as e:
        return str(e)

@app.route('/texto', methods=['POST'])
def extrair_texto():
    try:
        if 'image' in request.files:
            image = request.files['image']
            image.save('temp_image.jpeg')  # Salva temporariamente a imagem

            text = extract_text_from_image('temp_image.jpeg')

            return jsonify({"text": text})
        else:
            return jsonify({"error": "Nenhuma imagem recebida"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/texto', methods=['GET'])
def texto():
    return render_template('texto.html')
    



@app.route('/yoloteste')
def yoloteste():

    return render_template('yoloteste.html')

@app.route('/video_feed_yoloteste')
def video_feed_yoloteste():
    return Response(generate_yoloteste(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_yoloteste():
    video_capture = cv2.VideoCapture(0)  # Usar a webcam (índice 0)

    model2 = YOLO("yolov8n.pt", "v8")

    while True:
        ret, frame = video_capture.read()

        if ret:
            # Detecte usando o modelo2 (model2) em vez de detect_bike
            detect_params = model2.predict(source=[frame], conf=0.45, save=False)

            deteccao = False  # Flag para verificar se uma bicicleta foi detectada

            for i, box in enumerate(detect_params[0].boxes):
                clsID = box.cls.numpy()[0]
                conf = box.conf.numpy()[0]
                bb = box.xyxy.numpy()[0]

                cv2.rectangle(
                    frame,
                    (int(bb[0]), int(bb[1])),
                    (int(bb[2]), int(bb[3])),
                    detection_colors[int(clsID)],
                    3,
                )

                # Mostrar nome da classe e confiança
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(
                    frame,
                    f"{class_list[int(clsID)]} {conf:.3f}%",
                    (int(bb[0]), int(bb[1]) - 10),
                    font,
                    1,
                    (255, 255, 255),
                    2,
                )


                # Verificar se uma bicicleta foi detectada
                if class_list[int(clsID)] == 'person':
                    deteccao = True

            if deteccao:
                # Exibir a mensagem "Estamos no NEXT!" no vídeo
                cv2.putText(frame, "Estamos no NEXT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # Exibir a mensagem "Onde estou?" no vídeo
                cv2.putText(frame, "Onde estou?", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)



            _, jpg = cv2.imencode('.jpg', frame)
            frame_data = jpg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
            
            

# Rota para capturar e salvar a imagem
@app.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_data = data.get("image")

    if image_data:
        # Salvar a imagem capturada no servidor
        image_filename = captured_images_folder + "captured_image.jpg"
        with open(image_filename, "wb") as file:
            file.write(image_data.encode())

        return jsonify({"message": "Imagem enviada com sucesso!", "image_path": image_filename})
    else:
        return jsonify({"error": "Nenhum dado de imagem recebido"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
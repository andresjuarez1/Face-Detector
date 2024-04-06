import cv2
import face_recognition
from flask import Flask, render_template, Response

app = Flask(__name__)

imagen_conocida = face_recognition.load_image_file("carota\carota.jpg")
codificacion_conocida = face_recognition.face_encodings(imagen_conocida)[0]

def detectar_caras():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()

        ubicaciones = face_recognition.face_locations(frame)
        codificaciones = face_recognition.face_encodings(frame, ubicaciones)
        
        for (top, right, bottom, left), codificacion in zip(ubicaciones, codificaciones):
            coincidencias = face_recognition.compare_faces([codificacion_conocida], codificacion)
            if True in coincidencias:
                mensaje = "Soy yo mero andres"
                color = (255, 0, 0)
            else:
                mensaje = "Desconocido"
                color = (0, 0, 255)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, mensaje, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(detectar_caras(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

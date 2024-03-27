import cv2
import face_recognition

imagen_conocida = face_recognition.load_image_file("carota\carota.jpg")
codificacion_conocida = face_recognition.face_encodings(imagen_conocida)[0]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    ubicaciones = face_recognition.face_locations(frame)
    codificaciones = face_recognition.face_encodings(frame, ubicaciones)
    
    mensaje = "Desconocido"
    
    for codificacion in codificaciones:
        coincidencias = face_recognition.compare_faces([codificacion_conocida], codificacion)
        if True in coincidencias:
            mensaje = "Andres"
            color = (255, 0, 0)
        else:
            color = (0, 0, 255)
            
        for (top, right, bottom, left) in ubicaciones:
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, mensaje, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

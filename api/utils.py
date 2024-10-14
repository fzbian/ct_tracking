import requests

def send_message(tipo_mensaje, tracking_id, numero, estado):
    mensaje_crear_pedido = f"¡Bienvenido a Chinatown Logistic! 🐉\n\nNos complace informarle que su pedido ha sido creado exitosamente.\nSu tracking ID es: *{tracking_id}*.\nApreciamos su confianza en nuestro servicio exclusivo.\nPuede rastrear el estado de su pedido en cualquier momento en el siguiente enlace\n👉 https://tracking.chinatownlogistic.com/es/track/{tracking_id}/\nEstamos aquí para asegurarnos de que su experiencia de importación sea fluida y satisfactoria.\n\n¡Gracias por elegirnos!"
    
    mensaje_actualizar_pedido = f"¡Estimado cliente!\n\nQueremos informarle que el estado de su pedido con tracking ID *{tracking_id}* ha sido actualizado a: *{estado}*.\nEn Chinatown Logistic, nos esforzamos por brindarle un servicio exclusivo y una experiencia de importación inigualable.\n\nPara más detalles sobre su pedido y su progreso, por favor visite el siguiente enlace\n👉 https://tracking.chinatownlogistic.com/es/track/{tracking_id}/\nAgradecemos su confianza y quedamos a su disposición para cualquier consulta."
    
    if tipo_mensaje == 0:
        mensaje = mensaje_crear_pedido
    elif tipo_mensaje == 1:
        mensaje = mensaje_actualizar_pedido
    else:
        raise ValueError("Tipo de mensaje inválido. Use 0 para crear pedido o 1 para actualizar estado.")

    data = {
        "number": f"57{numero}",
        "message": mensaje
    }

    try:
        response = requests.post('http://23.254.225.197:3000/send-message', json=data)
        
        if response.status_code == 200:
            print("Mensaje enviado correctamente:", response.json())
        else:
            print(f"Error enviando el mensaje. Código de estado: {response.status_code}")
            print(response.json())

    except Exception as e:
        print("Ocurrió un error:", str(e))

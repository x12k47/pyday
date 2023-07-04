from imapclient import IMAPClient
import html2text
from email import message_from_bytes

# Reemplaza con tus credenciales de correo
email_address = 'correo'
email_password = 'contraseña'

# Conectar al servidor de correo
with IMAPClient(host='servidor_correo') as client:
    client.login(email_address, email_password)
    client.select_folder('INBOX')

    # Recorrido de los mensajes en la bandeja de entrada
    messages = client.search('UNSEEN')
    correos = []  # Lista para almacenar los correos

    if not messages:
        print("La bandeja de entrada está limpia, todos los correos están leídos.")
    else:
        for msgid, data in client.fetch(messages, ['ENVELOPE', 'BODY[]']).items():
            envelope = data[b'ENVELOPE']
            Emisor = envelope.from_[0].mailbox.decode() + '@' + envelope.from_[0].host.decode()
            Asunto = envelope.subject.decode()
            Timestamp = envelope.date.strftime('%d/%m/%Y %H:%M:%S')  # Formatear la fecha y hora

            # Aquí obtienes el cuerpo del correo
            if b'BODY[]' in data:
                raw_message = data[b'BODY[]']
                email_message = message_from_bytes(raw_message)

                # Buscar la parte de texto del correo
                if email_message.is_multipart():
                    for part in email_message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            Cuerpo = part.get_payload()
                else:
                    Cuerpo = email_message.get_payload()

                # Convertir HTML a texto si es necesario
                if 'html' in Cuerpo:
                    h = html2text.HTML2Text()
                    h.ignore_links = True
                    Cuerpo = h.handle(Cuerpo)
            else:
                Cuerpo = ''

            # Almacenar el correo en la lista
            correos.append((Emisor, Asunto, Timestamp, Cuerpo))

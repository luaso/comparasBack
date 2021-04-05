import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import jsonify, request
from functools import wraps

from app import ObjectNotFound
from app.inicioSesion.models.mantenimiento_Usuario_model import Usuarios
from app.inicioSesion.schemas.mantenimiento_Usuario_schema import RolSchemaToken, UserSchemaToken
import jwt
from config.configuration import DevelopmentConfig
#from config.configuration import ProductionConfig          #Configuracion para produccion

rolSchemaToken = RolSchemaToken()
userSchemaToken = UserSchemaToken()

secret_Key = DevelopmentConfig.SECRET_KEY
#secret_Key = ProductionConfig.SECRET_KEY                   #Configuracion para produccion


def check_for_token(token_ur):

    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    try:
        data = jwt.decode(token_ur, secret_Key)
        userRol = Usuarios.get_email_token(data.get("user"))
        resultado = rolSchemaToken.dump(userRol)

        rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"), 'status': data.get("status"), 'idUsuario':userRol.idUsuario, 'rol': resultado["Rol.idRol"]}
    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}

    return rept


def check_for_token_id_rol(token_ur,id,rolUser):
    '''Funcion que valida si el token es correcto; si el id y el token pertenecen al mismo usuario; tambien si el rol puesto concuerda con los anteriores parametros '''
    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    if not id:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token no concuerda con el ID', 'status': '403'}
    try:
        data = jwt.decode(token_ur, secret_Key)

        userRol = Usuarios.get_rol(id)
        resultado = rolSchemaToken.dump(userRol, many=True)

        if (resultado[0]["Rol.idRol"] != rolUser):
            rept = {'user': 'invalid', 'exp': '0', 'message': 'El usuario no puede realizar esta accion', 'status': '403'}
        elif (data.get("user") != resultado[0]["Usuarios.email"]):
            rept = {'user': 'invalid', 'exp': '0', 'message': 'no concuerda el id con el usuario del token', 'status': '403'}
        else:
            rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"), 'status': data.get("status"), 'rol': resultado[0]["Rol.idRol"], 'idUser':1}

    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    return   rept

def check_for_token_rol(token_ur):
    '''Funcion que valida si el token es correcto y devuelve el di y rol del usuario del token '''
    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}

    try:
        data = jwt.decode(token_ur, secret_Key)

        userRol = Usuarios.get_email_token(data.get("user"))
        resultado = rolSchemaToken.dump(userRol)
        print(resultado)
        if (resultado["Rol.idRol"] != 3):
            rept = {'user': 'invalid', 'exp': '0', 'message': 'El usuario no puede realizar esta accion', 'status': '403'}
        else:
            rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"), 'status': data.get("status"), 'rol': resultado["Rol.idRol"]}

    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    return   rept


def check_for_token_id(token_ur,idUser):
    '''Funcion que valida si el token es correcto; tambien si el idUser pertenece al mismo usaurio que el del token '''
    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    if not idUser:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token no concuerda con el ID', 'status': '403'}
    try:
        data = jwt.decode(token_ur, secret_Key)

        userRol = Usuarios.get_query(idUser)

        emailUser = userRol.email

        if (data.get("user") != emailUser):
            rept = {'user': 'invalid', 'exp': '0', 'message': 'Token no concuerda el id con el usuario del token', 'status': '403'}
        else:
            rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"), 'status': data.get("status")}

    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    return   rept


def sendEmailrecoverPassword(usuario, password):
    print(usuario, password)
    try:
        # me == my email address
        # you == recipient's email address
        me = "nelsonwalter1997@gmail.com"
        you = usuario

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Solicitud de contraseña"
        msg['From'] = me
        msg['To'] = you

        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        html = """\
            <html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <style type="text/css">
                a[x-apple-data-detectors] {color: inherit !important;}
            </style>
        </head>
        <body style="margin: 0; padding: 0;">
            <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td style="padding: 20px 0 30px 0;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
            <tr>
                <td align="center" bgcolor="red" style="padding: 40px 0 30px 0;">
              <h1 style="color:white !important;"><a href="COMPARAS.PE" style="color: white;">COMPARAS.PE</a></h1>
                </td>
            </tr>
            <tr>
                <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                        <tr>
                            <td style="color: #153643; font-family: Arial, sans-serif;">
                                <h1 style="font-size: 24px; margin: 0;">Recibimos tu solicitud de contraseña!</h1>
                            </td>
                        </tr>
                        <tr>
                            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 24px; padding: 20px 0 30px 0;">
                                <p style="margin: 0;">Su contraseña temporal para ingresar a Comparas es: """ + password + """ </p>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                                    <tr>
                                        <td width="260" valign="top">

                                        </td>
                                        <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
                                        <td width="260" valign="top">

                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td bgcolor="#ee4c50" style="padding: 30px 30px;">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                        <tr>
                            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
                                <p style="margin: 0;">&reg;  Comparas <br/>
                             <a href="#" style="color: #ffffff;">Comparas.pe</a> </p>
                            </td>
                            <td align="right"> 
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

                    </td>
                </tr>
            </table>
        </body>
        </html>
            """

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()

        mail.starttls()
        mail.login('nelsonwalter1997@gmail.com', 'fbudewhzhbjxarlq')

        #mail.login('Comparas@jlranalytics.com', 'Saturno*1valid')

        mail.sendmail(me, you, msg.as_string())
        mail.quit()
        print('realizado')
    except Exception as ex:
        print('error')
        raise ObjectNotFound(ex)

    return "Enviado"

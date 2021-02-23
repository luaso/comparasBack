from config.configuration import DevelopmentConfig
from app import create_app
from flask import Flask, jsonify, request, session, make_response, flash, render_template
from functools import wraps
import jwt
import datetime

#settings_module = os.getenv('APP_SETTINGS_MODULE')
#app = create_app(settings_module)flask
config = DevelopmentConfig

app = create_app(config)


#def check_for_token(func):
    #@wraps(func)
    #def wrapped(*args, **kwargs):
      # token = request.headers.get('token')
      # if not token:
       # return jsonify({'message': 'Token no ingresado'}), 403
        #try:
         #   data = jwt.decode(token, app.config['SECRET_KEY'])

        #except:
         #   return jsonify({'message': 'Token Caudcado ó invalido'}), 403

       #return func(*args, **kwargs)
    #return wrapped

def getsecre_key():
    return  app.config['SECRET_KEY']

def getToken_generate(usuario):
    token = jwt.encode({
        'user': usuario,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4),
        'message':'ok',
        'status':'400'
    },  app.config['SECRET_KEY'])

    return   token.decode('utf-8')

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('login.html')
        #return 'actualmente conectado'


@app.route('/public')
def public():
    return 'Cualquiera puede ver esto'


@app.route('/auth_nm',methods=['POST'])
#@check_for_token
def authorised():
    return 'Esto solo se puede ver con un token'


@app.route('/login_prueba', methods=['POST'])
def login_prueba():
    print('ENTRO A LOGIN__')
    if request.form['username'] and request.form['password'] == 'password':
        session['logged_in'] = True
        user_form = request.form['username']
        token=getToken_generate(user_form)
        return jsonify({'tokens': token})

    else:
        return make_response('incapaz de verificar', 403, {'WWW-Autenticate': 'Basic login'})



if __name__ == '__main__':
	app.run()

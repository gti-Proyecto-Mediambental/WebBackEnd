from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from FicheroMedicion import Medicion
import json
# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcrud'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM medidas')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', medidas = data)

@app.route('/obtenerMedicionesWeb', methods = ['GET'])
def obtenerMedicionesWeb():
    return redirect(url_for('Index'))

@app.route('/guardarMedicionesWeb', methods=['POST'])
def guardarMedicionesWeb():
    if request.method == 'POST':
        #id = request.form['id']
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        co2 = request.form['co2']
        fecha = request.form['fecha']
        hora = request.form['hora']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO medidas (latitud, longitud, co2, fecha, hora) VALUES (%s,%s,%s,%s,%s)", (latitud, longitud, co2, fecha, hora))
        mysql.connection.commit()
        flash('medida Added successfully')
        return redirect(url_for('Index'))




@app.route('/obtenerUltimasMedicionesWeb', methods = ['GET'])
def obtenerUltimasMedicionesWeb():
    if request.method == 'GET':
        cantidadMedicioes = request.args['cantidadMedicioes']        
        cur = mysql.connection.cursor()
        print(cantidadMedicioes)
        cur.execute("SELECT * FROM medidas ORDER BY id DESC LIMIT {}".format(cantidadMedicioes))
        data = cur.fetchall()
        cur.close()
    return render_template('index.html', medidas = data)

# ---------------- Metodos APIREST

@app.route('/obtenerUltimasMediciones', methods = ['GET'])
def obtenerUltimasMediciones():
    if request.method == 'GET':
        cantidadMedicioes = request.args['cantidadMedicioes']        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM medidas ORDER BY id DESC LIMIT {}".format(cantidadMedicioes))
        data = cur.fetchall()
        cur.close()
        res = {}
        res['mediciones'] = []
        for row in data:
            res['mediciones'].append(Medicion(row[0],row[1],row[2],row[3],row[4],row[5]).toJson())
    return json.dumps(res,indent=4)



@app.route('/obtenerMediciones', methods = ['GET'])
def obtenerMediciones():    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM medidas')
    data = cur.fetchall()
    cur.close()
    res = {}
    res['mediciones'] = []
    for row in data:
        res['mediciones'].append(Medicion(row[0],row[1],row[2],row[3],row[4],row[5]).toJson())
    return json.dumps(res,indent=4)



@app.route('/guardarMediciones', methods = ['POST'])
def guardarMediciones():
    request_data = request.get_json()


    if request_data:

        latitud = request_data['latitud']
        print(latitud)
        longitud = request_data['longitud']

        co2 = request_data['co2']

        fecha = request_data['fecha']

        hora = request_data['hora']
    return '''
           The latitud value is: {}
           The longitud value is: {}
           The co2 value is: {}
           The fecha value is: {}
           The hora value is: {}
           The medicion value is: {} '''.format( latitud, longitud, co2, fecha, hora)


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)

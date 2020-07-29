# render_tamplate te sirve para renderisar plantilla como index.html
# redirect redireciona y url_for sirve para darle nobre de la ruta
# flash sirve para mostar mensajes entre vistas
from flask import Flask, render_template, request,redirect, url_for,flash
from flask_mysqldb import MySQL

app = Flask(__name__)
print()

# Conectarse a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud_flask'

# Session
app.secret_key = 'mysecretkey' # Como va ir protecgida

mysql = MySQL(app)


# Cada vez que nuestro usuario entre a una ruta principal uestre algo
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    # Obtengo los datos de la tabla contactos
    cur.execute('SELECT * FROM contactos')
    data = cur.fetchall() # Ejecuto el query, y almaceno e una variable
    #print(data)
    return render_template('index.html', contactos=data) #Te carga un template , No se le pone nombre de la carpeta por flask template ya conoce

@app.route('/agregar_contacto', methods=['POST'])
def agregar_contacto():

    # Si envia a esta ruta mediante post hace esto
    if request.method == 'POST':
       nombre_resivido =  request.form['nombres']
       telefono_resivido =  request.form['telefono']
       email_resivido =  request.form['email']

       # Abrir y ejecutar un query MySQL
       cur = mysql.connection.cursor()

       cur.execute('INSERT INTO contactos(nombre,telefono,email) VALUES (%s,%s,%s)', (nombre_resivido,telefono_resivido,email_resivido))
       mysql.connection.commit()

       # Muestra un mensaje de agregación
       flash('Contacto agregado exitosamente')

       # Redirige al index
       return redirect(url_for('Index'))

@app.route('/editar_contacto/<id>')
def editar_contacto(id):
    # Consulta sql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contactos WHERE idcontactos={}".format(id))
    valor = data = cur.fetchall() # Ejecuto el query, y almaceno e una variable
    #print(valor[0])
    return render_template('editar_contacto.html', retorna_contacto= valor[0])

@app.route('/actualizar_contacto/<id>', methods = ['POST'])
def actualizar_contacto(id):
    if request.method == 'POST':
        nombre_resivido =  request.form['nombres']
        telefono_resivido =  request.form['telefono']
        email_resivido = request.form['email']

        # Consulta sql
        cur = mysql.connection.cursor()
        cur.execute("UPDATE contactos SET nombre = '{}', telefono='{}', email='{}'  WHERE idcontactos='{}'".format(nombre_resivido,telefono_resivido,email_resivido, id))
        mysql.connection.commit()
        flash('Contacto Actualizado')
        return redirect(url_for('Index'))

@app.route('/eliminar_contacto/<id>')
def eliminar_contacto(id):
    # Consulta sql
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contactos WHERE idcontactos= {0}".format(id))
    mysql.connection.commit()

    flash('Contacto Eliminado')
    return redirect(url_for('Index'))


if (__name__ == '__main__'):
    app.run(port=3000, debug=True) # Para que sepa el puerto y cada vez que haga cambio se reinicie

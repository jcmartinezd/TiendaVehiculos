import pyodbc
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()

# Configuración de la base de datos
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LENOVO2;'
        'DATABASE=VentaVehiculos;'
        'UID=sa;'
        'PWD=123456;'
        'TrustServerCertificate=yes;'
    )
    return conn

# Definición de usuarios y contraseñas
usuarios = {
    "juan": "2025",
    "maria": "2025"
}

@auth.verify_password
def verify_password(usuario, contraseña):
    if usuario in usuarios and usuarios[usuario] == contraseña:
        return usuario
    return None

# ----- OPERACIONES PARA VEHÍCULOS -----

# Ruta para obtener todos los vehículos (Read)
@app.route('/Vehiculos', methods=['GET'])
@auth.login_required
def obtener_vehiculos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT IdVehiculo, Marca FROM Vehiculos')
        vehiculos = cursor.fetchall()
        conn.close()
        return jsonify(
            vehiculos=[{
                'idVehiculo': vehiculo[0],
                'Marca': vehiculo[1]
            } for vehiculo in vehiculos]
        )
    except Exception as e:
        print(f"Error en obtener_vehiculos: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para obtener un vehículo específico (Read)
@app.route('/Vehiculos/<int:id_vehiculo>', methods=['GET'])
@auth.login_required
def obtener_vehiculo(id_vehiculo):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT IdVehiculo, Marca FROM Vehiculos WHERE IdVehiculo = ?', (id_vehiculo,))
        vehiculo = cursor.fetchone()
        conn.close()
        
        if vehiculo:
            return jsonify({
                'idVehiculo': vehiculo[0],
                'Marca': vehiculo[1]
            })
        else:
            return jsonify({"error": "Vehículo no encontrado"}), 404
    except Exception as e:
        print(f"Error en obtener_vehiculo: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para insertar un nuevo vehículo (Create)
@app.route('/Vehiculos', methods=['POST'])
@auth.login_required
def insertar_vehiculo():
    try:
        marca = request.form.get('Marca')
        if not marca:
            return jsonify({"error": "El campo 'Marca' es requerido"}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Vehiculos (Marca) VALUES (?)", (marca,))
        conn.commit()
        
        # Obtener el ID del vehículo recién insertado usando SCOPE_IDENTITY()
        cursor.execute("SELECT SCOPE_IDENTITY()")
        id_vehiculo = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            "mensaje": "Vehículo insertado correctamente",
            "idVehiculo": id_vehiculo
        }), 201
    except Exception as e:
        print(f"Error en insertar_vehiculo: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para actualizar un vehículo (Update)
@app.route('/Vehiculos/<int:id_vehiculo>', methods=['PUT'])
@auth.login_required
def actualizar_vehiculo(id_vehiculo):
    try:
        marca = request.form.get('Marca')
        if not marca:
            return jsonify({"error": "El campo 'Marca' es requerido"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Vehiculos SET Marca = ? WHERE IdVehiculo = ?", (marca, id_vehiculo))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Vehículo actualizado correctamente"})
    except Exception as e:
        print(f"Error en actualizar_vehiculo: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para eliminar un vehículo (Delete)
@app.route('/Vehiculos/<int:id_vehiculo>', methods=['DELETE'])
@auth.login_required
def eliminar_vehiculo(id_vehiculo):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Vehiculos WHERE IdVehiculo = ?", (id_vehiculo,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Vehículo eliminado correctamente"})
    except Exception as e:
        print(f"Error en eliminar_vehiculo: {e}")
        return jsonify({"error": str(e)}), 500

# ----- OPERACIONES PARA CLIENTES -----

# Ruta para obtener todos los clientes (Read)
@app.route('/Clientes', methods=['GET'])
@auth.login_required
def obtener_clientes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT IdCliente, Nombre FROM Cliente")
        clientes = cursor.fetchall()
        conn.close()
        return jsonify(
            clientes=[{
                'idCliente': cliente[0],
                'Nombre': cliente[1]
            } for cliente in clientes]
        )
    except Exception as e:
        print(f"Error en obtener_clientes: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para obtener un cliente específico (Read)
@app.route('/Clientes/<int:id_cliente>', methods=['GET'])
@auth.login_required
def obtener_cliente(id_cliente):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT IdCliente, Nombre FROM Cliente WHERE IdCliente = ?", (id_cliente,))
        cliente = cursor.fetchone()
        conn.close()
        
        if cliente:
            return jsonify({
                'idCliente': cliente[0],
                'Nombre': cliente[1]
            })
        else:
            return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        print(f"Error en obtener_cliente: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para insertar un nuevo cliente (Create)
@app.route('/Clientes', methods=['POST'])
@auth.login_required
def insertar_cliente():
    try:
        data = request.get_json()  # Aseguramos que los datos se reciben como JSON
        
        if not data or 'IdCliente' not in data or 'Nombre' not in data:
            return jsonify({"error": "Los campos 'IdCliente' y 'Nombre' son requeridos"}), 400

        id_cliente = data['IdCliente']
        nombre = data['Nombre']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar el cliente proporcionando el ID manualmente
        cursor.execute("INSERT INTO Cliente (IdCliente, Nombre) VALUES (?, ?)", (id_cliente, nombre))
        conn.commit()
        conn.close()

        return jsonify({
            "mensaje": "Cliente insertado correctamente",
            "idCliente": id_cliente
        }), 201
    except Exception as e:
        print(f"Error en insertar_cliente: {e}")
        return jsonify({"error": str(e)}), 500



# Ruta para actualizar un cliente (Update)
@app.route('/Clientes/<int:id_cliente>', methods=['PUT'])
@auth.login_required
def actualizar_cliente(id_cliente):
    try:
        nombre = request.form.get('Nombre')
        if not nombre:
            return jsonify({"error": "El campo 'Nombre' es requerido"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Cliente SET Nombre = ? WHERE IdCliente = ?", (nombre, id_cliente))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Cliente actualizado correctamente"})
    except Exception as e:
        print(f"Error en actualizar_cliente: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para eliminar un cliente (Delete)
@app.route('/Clientes/<int:id_cliente>', methods=['DELETE'])
@auth.login_required
def eliminar_cliente(id_cliente):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Cliente WHERE IdCliente = ?", (id_cliente,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Cliente eliminado correctamente"})
    except Exception as e:
        print(f"Error en eliminar_cliente: {e}")
        return jsonify({"error": str(e)}), 500

# ----- OPERACIONES PARA VENTAS -----

# Ruta para obtener todas las ventas (Read)
@app.route('/Ventas', methods=['GET'])
@auth.login_required
def obtener_ventas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT IdVenta, IdCliente, IdVehiculo, Precio, Fecha FROM Ventas")
        ventas = cursor.fetchall()
        conn.close()
        return jsonify(
            ventas=[{
                'idVenta': venta[0],
                'idCliente': venta[1],
                'idVehiculo': venta[2],
                'Precio': venta[3],
                'Fecha': venta[4]
            } for venta in ventas]
        )
    except Exception as e:
        print(f"Error en obtener_ventas: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para obtener una venta específica (Read)
@app.route('/Ventas/<int:id_venta>', methods=['GET'])
@auth.login_required
def obtener_venta(id_venta):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT IdVenta, IdCliente, IdVehiculo, Precio, Fecha FROM Ventas WHERE IdVenta = ?", (id_venta,))
        venta = cursor.fetchone()
        conn.close()
        
        if venta:
            return jsonify({
                'idVenta': venta[0],
                'idCliente': venta[1],
                'idVehiculo': venta[2],
                'Precio': venta[3],
                'Fecha': venta[4]
            })
        else:
            return jsonify({"error": "Venta no encontrada"}), 404
    except Exception as e:
        print(f"Error en obtener_venta: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para insertar una nueva venta (Create)
@app.route('/Ventas', methods=['POST'])
@auth.login_required
def insertar_venta():
    try:
        id_cliente = request.form.get('IdCliente')
        id_vehiculo = request.form.get('IdVehiculo')
        precio = request.form.get('Precio')
        fecha = request.form.get('Fecha')
        
        if not all([id_cliente, id_vehiculo, precio, fecha]):
            return jsonify({"error": "Todos los campos (IdCliente, IdVehiculo, Precio, Fecha) son requeridos"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Ventas (IdCliente, IdVehiculo, Precio, Fecha) VALUES (?, ?, ?, ?)", 
                       (id_cliente, id_vehiculo, precio, fecha))
        conn.commit()
        
        # Obtener el ID de la venta recién insertada usando SCOPE_IDENTITY()
        cursor.execute("SELECT SCOPE_IDENTITY()")
        id_venta = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            "mensaje": "Venta insertada correctamente",
            "idVenta": id_venta
        }), 201
    except Exception as e:
        print(f"Error en insertar_venta: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para actualizar una venta (Update)
@app.route('/Ventas/<int:id_venta>', methods=['PUT'])
@auth.login_required
def actualizar_venta(id_venta):
    try:
        data = request.form
        updates = []
        params = []
        
        if 'IdCliente' in data:
            updates.append("IdCliente = ?")
            params.append(data.get('IdCliente'))
        if 'IdVehiculo' in data:
            updates.append("IdVehiculo = ?")
            params.append(data.get('IdVehiculo'))
        if 'Precio' in data:
            updates.append("Precio = ?")
            params.append(data.get('Precio'))
        if 'Fecha' in data:
            updates.append("Fecha = ?")
            params.append(data.get('Fecha'))
        
        if not updates:
            return jsonify({"error": "No se proporcionaron campos para actualizar"}), 400
        
        params.append(id_venta)
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "UPDATE Ventas SET " + ", ".join(updates) + " WHERE IdVenta = ?"
        cursor.execute(sql, params)
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Venta actualizada correctamente"})
    except Exception as e:
        print(f"Error en actualizar_venta: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para eliminar una venta (Delete)
@app.route('/Ventas/<int:id_venta>', methods=['DELETE'])
@auth.login_required
def eliminar_venta(id_venta):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ventas WHERE IdVenta = ?", (id_venta,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Venta eliminada correctamente"})
    except Exception as e:
        print(f"Error en eliminar_venta: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

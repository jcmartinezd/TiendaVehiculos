import requests

# Función para establecer la autenticación
def establecer_aut(usuario, contraseña):
    global auth
    auth = (usuario, contraseña)

# ----- OPERACIONES PARA VEHÍCULOS -----

# Función para obtener todos los vehículos (Read)
def obtener_vehiculos():
    try:
        response = requests.get('http://localhost:5000/Vehiculos', auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al obtener vehículos: {e}')
        return []

# Función para obtener un vehículo específico (Read)
def obtener_vehiculo(id_vehiculo):
    try:
        response = requests.get(f'http://localhost:5000/Vehiculos/{id_vehiculo}', auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al obtener vehículo con ID {id_vehiculo}: {e}')
        return None

# Función para insertar un nuevo vehículo (Create)
# Según el diagrama, Vehiculos solo tiene IdVehiculo y Marca
def insertar_vehiculo(marca):
    try:
        data = {'Marca': marca}
        response = requests.post('http://localhost:5000/Vehiculos', data=data, auth=auth)
        response.raise_for_status()
        print("Respuesta del servidor:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al insertar vehículo: {e}')
        return None

# Función para actualizar un vehículo (Update)
def actualizar_vehiculo(id_vehiculo, marca):
    try:
        data = {'Marca': marca}
        response = requests.put(f'http://localhost:5000/Vehiculos/{id_vehiculo}', 
                               data=data, auth=auth)
        response.raise_for_status()
        print("Respuesta del servidor:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al actualizar vehículo con ID {id_vehiculo}: {e}')
        return None

# Función para eliminar un vehículo (Delete)
def eliminar_vehiculo(id_vehiculo):
    try:
        response = requests.delete(f'http://localhost:5000/Vehiculos/{id_vehiculo}', auth=auth)
        response.raise_for_status()
        print("Respuesta del servidor:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al eliminar vehículo con ID {id_vehiculo}: {e}')
        return None

# ----- OPERACIONES PARA CLIENTES -----

# Función para obtener todos los clientes (Read)
def obtener_clientes():
    try:
        response = requests.get('http://localhost:5000/Clientes', auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al obtener clientes: {e}')
        return []

# Función para obtener un cliente específico (Read)
def obtener_cliente(id_cliente):
    try:
        response = requests.get(f'http://localhost:5000/Clientes/{id_cliente}', auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al obtener cliente con ID {id_cliente}: {e}')
        return None

# Función para insertar un nuevo cliente (Create)
# Según el diagrama, Cliente solo tiene IdCliente y Nombre
def insertar_cliente(id_cliente, nombre):
    try:
        data = {'IdCliente': id_cliente, 'Nombre': nombre}
        response = requests.post('http://localhost:5000/Clientes', json=data, auth=auth)  # Cambiamos data a json
        response.raise_for_status()
        print("Respuesta del servidor:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al insertar cliente: {e}')
        return None


# Función para actualizar un cliente (Update)
def actualizar_cliente(id_cliente, nombre):
    try:
        data = {'Nombre': nombre}
        response = requests.put(f'http://localhost:5000/Clientes/{id_cliente}', 
                               data=data, auth=auth)
        response.raise_for_status()
        print("Respuesta del servidor:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al actualizar cliente con ID {id_cliente}: {e}')
        return None

# Función para eliminar un cliente (Delete)
def eliminar_cliente(id_cliente):
    try:
        response = requests.delete(f'http://localhost:5000/Clientes/{id_cliente}', auth=auth)
        response.raise_for_status()
        print("Respuesta del servidor:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al eliminar cliente con ID {id_cliente}: {e}')
        return None

# ----- OPERACIONES PARA VENTAS -----

# Función para obtener todas las ventas (Read)
def obtener_ventas():
    try:
        response = requests.get('http://localhost:5000/Ventas', auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al obtener ventas: {e}')
        return []

# Función para obtener una venta específica (Read)
def obtener_venta(id_venta):
    try:
        response = requests.get(f'http://localhost:5000/Ventas/{id_venta}', auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al obtener venta con ID {id_venta}: {e}')
        return None

# Función para insertar una nueva venta (Create)
def insertar_venta(id_cliente, id_vehiculo, precio, fecha):
    try:
        data = {
            'IdCliente': id_cliente,
            'IdVehiculo': id_vehiculo,
            'Precio': precio,
            'Fecha': fecha
        }
        response = requests.post('http://localhost:5000/Ventas', data=data, auth=auth)
        response.raise_for_status()
        print("Respuesta del servidor:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al insertar venta: {e}')
        return None

# Función para actualizar una venta (Update)
def actualizar_venta(id_venta, id_cliente=None, id_vehiculo=None, precio=None, fecha=None):
    try:
        data = {}
        if id_cliente is not None:
            data['IdCliente'] = id_cliente
        if id_vehiculo is not None:
            data['IdVehiculo'] = id_vehiculo
        if precio is not None:
            data['Precio'] = precio
        if fecha is not None:
            data['Fecha'] = fecha
            
        response = requests.put(f'http://localhost:5000/Ventas/{id_venta}', 
                              data=data, auth=auth)
        response.raise_for_status()
        print("Respuesta del servidor:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al actualizar venta con ID {id_venta}: {e}')
        return None

# Función para eliminar una venta (Delete)
def eliminar_venta(id_venta):
    try:
        response = requests.delete(f'http://localhost:5000/Ventas/{id_venta}', auth=auth)
        response.raise_for_status()
        print("Respuesta del servidor:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error al eliminar venta con ID {id_venta}: {e}')
        return None

if __name__ == '__main__':
    # Establecer autenticación
    establecer_aut("juan", "2025")
    
    # Ejemplos de uso para el CRUD completo
    print("\n=== EJEMPLOS DE USO DEL CRUD ===\n")

    # 1. Trabajando con clientes
    print("\n--- OPERACIONES CON CLIENTES ---")
    
    # Obtener todos los clientes
    print("\n1. Obtener todos los clientes:")
    clientes = obtener_clientes()
    print(clientes)
    
    # Insertar un nuevo cliente
    print("\n2. Insertar un nuevo cliente:")
    nuevo_id = 4  # Puedes calcularlo basándote en el máximo IdCliente de la base de datos
    resultado = insertar_cliente(nuevo_id, "Carlos")
    
    # Si la inserción fue exitosa, usar el ID devuelto para operaciones posteriores
    if resultado and 'idCliente' in resultado:
        nuevo_id = resultado['idCliente']
        
        # Obtener el cliente recién insertado
        print(f"\n3. Obtener cliente con ID {nuevo_id}:")
        print(obtener_cliente(nuevo_id))
        
        # Actualizar el cliente
        print(f"\n4. Actualizar cliente con ID {nuevo_id}:")
        actualizar_cliente(nuevo_id, "Carlos López Actualizado")
        
        # Mostrar cliente actualizado
        print(f"\n5. Cliente actualizado:")
        print(obtener_cliente(nuevo_id))
        
        # Opcionalmente eliminar el cliente
        # print(f"\n6. Eliminar cliente con ID {nuevo_id}:")
        # eliminar_cliente(nuevo_id)
    
    # 2. Trabajando con vehículos
    print("\n--- OPERACIONES CON VEHÍCULOS ---")
    
    # Obtener todos los vehículos
    print("\n1. Obtener todos los vehículos:")
    vehiculos = obtener_vehiculos()
    print(vehiculos)
    
    # Insertar un nuevo vehículo
    print("\n2. Insertar un nuevo vehículo:")
    resultado = insertar_vehiculo("Ford")
    
    # Si la inserción fue exitosa, usar el ID devuelto para operaciones posteriores
    if resultado and 'idVehiculo' in resultado:
        nuevo_id = resultado['idVehiculo']
        
        # Obtener el vehículo recién insertado
        print(f"\n3. Obtener vehículo con ID {nuevo_id}:")
        print(obtener_vehiculo(nuevo_id))
        
        # Actualizar el vehículo
        print(f"\n4. Actualizar vehículo con ID {nuevo_id}:")
        actualizar_vehiculo(nuevo_id, "Ford Mustang")
        
        # Mostrar vehículo actualizado
        print(f"\n5. Vehículo actualizado:")
        print(obtener_vehiculo(nuevo_id))
        
        # Opcionalmente eliminar el vehículo
        # print(f"\n6. Eliminar vehículo con ID {nuevo_id}:")
        # eliminar_vehiculo(nuevo_id)
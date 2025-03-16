-- 1. Crear la base de datos
CREATE DATABASE VentaVehiculos;
GO

-- 2. Utilizar la base de datos recién creada
USE VentaVehiculos;
GO

-- 3. Crear la tabla Cliente
CREATE TABLE Cliente (
    IdCliente INT NOT NULL IDENTITY(1,1), -- Generación automática del ID
    Nombre NCHAR(10) NOT NULL,
    CONSTRAINT PK_Cliente PRIMARY KEY (IdCliente)
);

-- 4. Crear la tabla Vehiculos
CREATE TABLE Vehiculos (
    IdVehiculo INT NOT NULL IDENTITY(1,1),
    Marca NCHAR(10) NOT NULL,
    CONSTRAINT PK_Vehiculos PRIMARY KEY (IdVehiculo)
);

-- 5. Crear la tabla Ventas
CREATE TABLE Ventas (
    IdVenta INT NOT NULL IDENTITY(1,1),
    IdCliente INT NOT NULL,
    IdVehiculo INT NOT NULL,
    Precio INT NOT NULL,
    Fecha DATE NOT NULL,
    CONSTRAINT PK_Ventas PRIMARY KEY (IdVenta),
    CONSTRAINT FK_Ventas_Cliente FOREIGN KEY (IdCliente)
        REFERENCES Cliente (IdCliente),
    CONSTRAINT FK_Ventas_Vehiculos FOREIGN KEY (IdVehiculo)
        REFERENCES Vehiculos (IdVehiculo)
);

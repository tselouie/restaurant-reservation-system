CREATE TABLE IF NOT EXISTS Tables (
    TableID INT PRIMARY KEY AUTO_INCREMENT,
    TableNumber INT NOT NULL,
    Capacity INT NOT NULL,
    Status ENUM('Available', 'Occupied') DEFAULT 'Available'
);

CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Reservations (
    ReservationID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT NOT NULL,
    TableID INT NOT NULL,
    ReservationDateTime DATETIME NOT NULL,
    NumberOfGuests INT NOT NULL,
    Status ENUM('Confirmed', 'Cancelled','Completed') DEFAULT 'Confirmed',
    SpecialRequests TEXT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (TableID) REFERENCES Tables(TableID)
);



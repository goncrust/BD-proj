CREATE TABLE Customer (
    cust_no SERIAL NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone NUMERIC(9, 0) NOT NULL,
    address VARCHAR(255) NOT NULL,
    PRIMARY KEY(cust_no)
);

-- (IC-2) Every Order (order_no) must participate in the contains association
CREATE TABLE "Order" (
    order_no SERIAL NOT NULL,
    "date" DATE NOT NULL,
    cust_no INT NOT NULL,
    PRIMARY KEY(order_no),
    FOREIGN KEY(cust_no) REFERENCES Customer(cust_no)
);

CREATE TABLE Sale (
    order_no INT NOT NULL,
    PRIMARY KEY(order_no),
    FOREIGN KEY(order_no) REFERENCES "Order"(order_no)
);

-- (IC-1) Customers can only pay for the Sale of an Order they have placed themselves ((order_no, cust_no) in (Order.order_no, Order.cust_no))
CREATE TABLE pay (
    order_no INT NOT NULL,
    cust_no INT NOT NULL,
    PRIMARY KEY(order_no),
    FOREIGN KEY(order_no) REFERENCES Sale(order_no),
    FOREIGN KEY(cust_no) REFERENCES Customer(cust_no)
);

-- (IC-3) Every Product (sku) must participate in the supply-contract association
CREATE TABLE Product (
    sku VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    price INT NOT NULL,
    PRIMARY KEY(sku)
);

CREATE TABLE "EAN Product" (
    sku VARCHAR(255) NOT NULL,
    ean VARCHAR(255) NOT NULL,
    PRIMARY KEY(sku),
    FOREIGN KEY(sku) REFERENCES Product(sku)
);

CREATE TABLE contains (
    order_no INT NOT NULL,
    sku VARCHAR(255) NOT NULL,
    qty INT NOT NULL,
    PRIMARY KEY(order_no, sku),
    FOREIGN KEY(order_no) REFERENCES "Order"(order_no),
    FOREIGN KEY(sku) REFERENCES Product(sku)
);

-- (IC-4) Every Supplier (TIN) must participate in the supply-contract association
CREATE TABLE Supplier (
    TIN NUMERIC(9, 0) NOT NULL,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    PRIMARY KEY(TIN)
);

CREATE TABLE "supply-contract" (
    TIN NUMERIC(9, 0) NOT NULL,
    sku VARCHAR(255) NOT NULL,
    "date" DATE NOT NULL,
    PRIMARY KEY(TIN),
    FOREIGN KEY(TIN) REFERENCES Supplier(TIN),
    FOREIGN KEY(sku) REFERENCES Product(sku)
);

-- (IC-5) Every Employee (ssn) must participate in the works association
CREATE TABLE Employee (
    ssn NUMERIC(11, 0) NOT NULL,
    TIN NUMERIC(9, 0) NOT NULL UNIQUE,
    bdate DATE NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(ssn)
);

CREATE TABLE process (
    order_no INT NOT NULL,
    ssn NUMERIC(11, 0) NOT NULL,
    PRIMARY KEY(order_no, ssn),
    FOREIGN KEY(order_no) REFERENCES "Order"(order_no),
    FOREIGN KEY(ssn) REFERENCES Employee(ssn)
);

CREATE TABLE Department (
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(name)
);

CREATE TABLE Workplace (
    address VARCHAR(255) NOT NULL,
    lat NUMERIC(8, 6) NOT NULL,
    "long" NUMERIC(9, 6) NOT NULL,
    UNIQUE(lat, "long"),
    PRIMARY KEY(address)
);

CREATE TABLE Office (
    address VARCHAR(255) NOT NULL,
    PRIMARY KEY(address),
    FOREIGN KEY(address) REFERENCES Workplace(address)
);

CREATE TABLE Warehouse (
    address VARCHAR(255) NOT NULL,
    PRIMARY KEY(address),
    FOREIGN KEY(address) REFERENCES Workplace(address)
);

CREATE TABLE works (
    ssn NUMERIC(11, 0) NOT NULL,
    department VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    PRIMARY KEY(ssn, department, address),
    FOREIGN KEY(ssn) REFERENCES Employee(ssn),
    FOREIGN KEY(department) REFERENCES Department(name),
    FOREIGN KEY(address) REFERENCES Workplace(address)
);

CREATE TABLE delivery (
    address VARCHAR(255) NOT NULL,
    TIN NUMERIC(9, 0) NOT NULL,
    PRIMARY KEY(address, TIN),
    FOREIGN KEY(address) REFERENCES Warehouse(address),
    FOREIGN KEY(TIN) REFERENCES "supply-contract"(TIN)
);

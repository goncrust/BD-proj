#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, flash, url_for
from psycopg_pool import ConnectionPool
import psycopg
import os
import re

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://db:db@postgres/db")
pool = ConnectionPool(conninfo=DATABASE_URL)
app = Flask(__name__)

@app.route("/", methods=("GET",))
def home():
    elements =  [
        {
            "url": "/gerir-clientes",
            "title": "Gerir Clientes"
        },
        {
            "url": "/gerir-produtos",
            "title": "Gerir Produtos"
        },
        {
            "url": "/gerir-fornecedores",
            "title": "Gerir Fornecedores"
        },
        {
            "url": "/editar-produtos",
            "title": "Editar Produtos"
        },
        {
            "url": "/pagar-encomenda",
            "title": "Pagar Encomenda"
        },
        {
            "url": "/realizar-encomenda",
            "title": "Realizar Encomenda"
        }
    ]
    return render_template('index.html', elements=elements)

@app.route("/gerir-clientes", methods=("GET",))
def gerir_clientes():
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT cust_no, name FROM customer;")
            parser = lambda el : {"id": el[0], "name": el[1]}
            clients = list(map(parser, cursor.fetchall()))
    return render_template("gerir-clientes.html", clients=clients)

@app.route("/gerir-clientes/<cust_no>/delete", methods=("POST",))
def gerir_clientes_delete(cust_no):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM customer WHERE cust_no = %(cust_no)s;", {"cust_no": cust_no})
    return redirect("/gerir-clientes")

@app.route("/gerir-clientes/add", methods=("POST",))
def gerir_clientes_add():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"] if request.form["phone"] else "NULL"
    address = request.form["address"] if request.form["address"] else "NULL"
    error = ""
    
    if not name:
        error = "Nome inválido"
    elif not email or not re.fullmatch(email_regex, email):
        error = "Email inválido"
    elif phone != "NULL" and not phone.isnumeric():
        error = "Telemóvel inválido"

    if error:
        flash(error)
    else:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                existing_email = cursor.execute("SELECT email FROM customer WHERE email = %(email)s;", {"email": email}).fetchone()[0]
                if existing_email:
                    flash("O email já existe")
                else:
                    cust_no = cursor.execute("SELECT MAX(cust_no) FROM customer;").fetchone()[0]
                    if not cust_no:
                        cust_no = 1
                    else:
                        cust_no += 1

                    cursor.execute(
                        """
                        INSERT INTO customer VALUES
                        (%(cust_no)s, %(name)s, %(email)s, %(phone)s, %(address)s);
                        """,
                        {"cust_no": cust_no, "name": name, "email": email, "phone": phone, "address": address})

    return redirect("/gerir-clientes")

@app.route("/gerir-produtos", methods=("GET",))
def gerir_produtos():
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT SKU, name FROM product;")
            parser = lambda el : {"id": el[0], "name": el[1]}
            products = list(map(parser, cursor.fetchall()))
    return render_template("gerir-produtos.html", products=products)

@app.route("/gerir-produtos/<sku>/delete", methods=("POST",))
def gerir_produtos_delete(sku):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM product WHERE sku = %(sku)s;", {"sku": sku})
    return redirect("/gerir-produtos")

@app.route("/gerir-produtos/add", methods=("POST",))
def gerir_produtos_add():
    sku = request.form["sku"]
    name = request.form["name"]
    description = request.form["description"] if request.form["description"] else "NULL"
    price = request.form["price"]
    ean = request.form["ean"] if request.form["ean"] else "NULL"
    error = ""
    
    if not sku:
        error = "Sku inválido"
    elif not name:
        error = "Nome inválido"
    elif not price or not price.isnumeric():
        error = "Preço inválido"
    elif ean != "NULL" and not ean.isnumeric():
        error = "EAN inválido"

    if error:
        flash(error)
    else:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                existing_sku = cursor.execute("SELECT sku FROM product WHERE sku = %(sku)s;", {"sku": sku}).fetchone()[0]
                if existing_sku:
                    error = "O SKU já existe"
                existing_ean = cursor.execute("SELECT ean FROM product WHERE ean = %(ean)s;", {"ean": ean}).fetchone()[0]
                if existing_ean:
                    error = "O EAN já existe"

                if error:
                    flash(error)
                else:
                    cursor.execute(
                        """
                        INSERT INTO product VALUES
                        (%(sku)s, %(name)s, %(email)s, %(phone)s, %(address)s);
                        """,
                        {"sku": sku, "name": name, "description": description, "price": price, "ean": ean})

    return redirect("/gerir-clientes")

@app.route("/gerir-fornecedores", methods=("GET",))
def gerir_fornecedores():
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT TIN, name FROM supplier;")
            parser = lambda el : {"id": el[0], "name": el[1]}
            suppliers = list(map(parser, cursor.fetchall()))
    return render_template("gerir-fornecedores.html", suppliers=suppliers)

@app.route("/gerir-fornecedores/<tin>/delete", methods=("POST",))
def gerir_fornecedores_delete(tin):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM supplier WHERE tin = %(tin)s;", {"tin": tin})
    return redirect("/gerir-fornecedores")

@app.route("/gerir-fornecedores/add", methods=("POST",))
def gerir_fornecedores_add():
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            pass
    return redirect("/gerir-fornecedores")

@app.route("/editar-produtos", methods=["POST", "GET"])
def editar_produtos():
    if request.method == "POST":
        ean = request.form["ean"] if request.form["ean"] else "NULL"
        with psycopg.connect("dbname=postgres user=postgres") as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE product SET name = %s, description = %s, price = %s, ean = %s WHERE sku = %s",
                    request.form["name"], request.form["desc"], request.form["price"], ean, request.form["sku"])
        return redirect("/")
    else:
        with psycopg.connect("dbname=postgres user=postgres") as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT SKU, name FROM product")
                parser = lambda el : {"id": el[0], "name": el[1]}
                products = cursor.fetchall().map(parser)
        return render_template("editar-produtos.html", products=products)

@app.route("/pagar-encomenda", methods=["POST", "GET"])
def pagar_encomenda():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("pagar-encomenda.html")

@app.route("/realizar-encomenda", methods=["POST", "GET"])
def realizar_encomenda():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("realizar-encomenda.html")

if __name__ == "__main__":
    app.run()
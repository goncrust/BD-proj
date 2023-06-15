#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, flash, url_for
from psycopg_pool import ConnectionPool
from datetime import datetime
import psycopg
import os
import re

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
float_regex = re.compile(r'\d{1,}[.,]\d{1,}')

DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://db:db@postgres/db")
pool = ConnectionPool(conninfo=DATABASE_URL)

app = Flask(__name__)
app.secret_key = "12345"

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
            "url": "/gerir-encomendas",
            "title": "Gerir Encomendas"
        }
    ]
    return render_template('index.html', elements=elements)

@app.route("/gerir-clientes", methods=("GET",))
def gerir_clientes():
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT cust_no, name FROM customer WHERE NOT email = 'deleted';")
            parser = lambda el : {"id": el[0], "name": el[1]}
            clients = list(map(parser, cursor.fetchall()))
    return render_template("gerir-clientes.html", clients=clients)

@app.route("/gerir-clientes/<cust_no>/delete", methods=("POST",))
def gerir_clientes_delete(cust_no):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE customer SET name = 'deleted', email = 'deleted', phone = NULL, ADDRESS = NULL WHERE cust_no = %(cust_no)s;", {"cust_no": cust_no})
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
                cursor.execute("START TRANSACTION;")
                existing_email = cursor.execute("SELECT email FROM customer WHERE email = %(email)s;", {"email": email}).fetchone()
                if existing_email:
                    flash("O email já existe")
                    return redirect("/gerir-clientes")

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
                cursor.execute("COMMIT;")

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
            cursor.execute("START TRANSACTION;")
            cursor.execute("UPDATE supplier SET sku = NULL WHERE sku = %(sku)s;", {"sku": sku})
            cursor.execute("DELETE FROM contains WHERE sku = %(sku)s;", {"sku": sku})
            cursor.execute(
                """
                DELETE FROM orders
                WHERE NOT order_no IN
                (SELECT DISTINCT order_no FROM contains)
                """)
            cursor.execute("DELETE FROM product WHERE sku = %(sku)s;", {"sku": sku})
            cursor.execute("COMMIT;")
    return redirect("/gerir-produtos")

@app.route("/gerir-produtos/<sku>/edit", methods=("POST", "GET"))
def gerir_produtos_edit(sku):
    if request.method == "GET":
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM product WHERE sku = %(sku)s;", {"sku": sku})
                parser = lambda el : {"sku": el[0], "name": el[1],
                                      "description": el[2] if el[2] != "NULL" else "",
                                      "price": el[3],
                                      "ean": el[4] if el[4] != "NULL" else ""}
                product = parser(cursor.fetchone())
        return render_template("editar-produto.html", product=product)
    else:
        name = request.form["name"]
        description = request.form["description"] if request.form["description"] else "NULL"
        price = request.form["price"]
        ean = request.form["ean"] if request.form["ean"] else "NULL"
        error = ""
        
        if not name:
            error = "Nome inválido"
        elif not price or (not price.isnumeric() and not re.fullmatch(float_regex, price)):
            error = "Preço inválido"
        elif ean != "NULL" and not ean.isnumeric():
            error = "EAN inválido"
    
        if error:
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("START TRANSACTION;")
                    existing_sku = cursor.execute("SELECT sku FROM product WHERE sku = %(sku)s;", {"sku": sku}).fetchone()
                    if not existing_sku:
                        error = "O SKU não existe"
                    elif ean != "NULL":
                        existing_ean = cursor.execute("SELECT ean FROM product WHERE ean = %(ean)s AND NOT sku = %(sku)s;", {"ean": ean, "sku": sku}).fetchone()
                        if existing_ean:
                            error = "O EAN já existe"
    
                    if error:
                        flash(error)
                    else:
                        cursor.execute(
                            """
                            UPDATE product SET
                            name = %(name)s, description = %(description)s, price = %(price)s, ean = %(ean)s
                            WHERE sku = %(sku)s;
                            """,
                            {"sku": sku, "name": name, "description": description, "price": price, "ean": ean})
                    cursor.execute("COMMIT;")
    
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
        error = "SKU inválido"
    elif not name:
        error = "Nome inválido"
    elif not price or (not price.isnumeric() and not re.fullmatch(float_regex, price)):
        error = "Preço inválido"
    elif ean != "NULL" and not ean.isnumeric():
        error = "EAN inválido"

    if error:
        flash(error)
    else:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("START TRANSACTION;")
                existing_sku = cursor.execute("SELECT sku FROM product WHERE sku = %(sku)s;", {"sku": sku}).fetchone()
                if existing_sku:
                    error = "O SKU já existe"
                elif ean != "NULL":
                    existing_ean = cursor.execute("SELECT ean FROM product WHERE ean = %(ean)s;", {"ean": ean}).fetchone()
                    if existing_ean:
                        error = "O EAN já existe"

                if error:
                    flash(error)
                else:
                    cursor.execute(
                        """
                        INSERT INTO product VALUES
                        (%(sku)s, %(name)s, %(description)s, %(price)s, %(ean)s);
                        """,
                        {"sku": sku, "name": name, "description": description, "price": price, "ean": ean})
                cursor.execute("COMMIT;")

    return redirect("/gerir-produtos")

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
            cursor.execute("START TRANSACTION;")
            cursor.execute("DELETE FROM delivery WHERE tin = %(tin)s;", {"tin": tin})
            cursor.execute("DELETE FROM supplier WHERE tin = %(tin)s;", {"tin": tin})
            cursor.execute("COMMIT;")
    return redirect("/gerir-fornecedores")

@app.route("/gerir-fornecedores/add", methods=("POST",))
def gerir_fornecedores_add():
    tin = request.form["tin"]
    name = request.form["name"] if request.form["name"] else "NULL"
    address = request.form["address"] if request.form["address"] else "NULL"
    sku = request.form["sku"]
    error = ""
    
    if not tin:
        error = "TIN inválido"
    elif not sku:
        error = "SKU inválido"

    if error:
        flash(error)
    else:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("START TRANSACTION;")
                existing_tin = cursor.execute("SELECT tin FROM supplier WHERE tin = %(tin)s;", {"tin": tin}).fetchone()
                if existing_tin:
                    error = "O TIN já existe"
                existing_sku = cursor.execute("SELECT sku FROM supplier WHERE sku = %(sku)s;", {"sku": sku}).fetchone()
                if not existing_sku:
                    error = "O SKU não existe"
                if error:
                    flash(error)
                else:
                    cursor.execute(
                        """
                        INSERT INTO supplier VALUES
                        (%(tin)s, %(name)s, %(address)s, %(sku)s, %(date)s);
                        """,
                        {"tin": tin, "name": name, "address": address, "sku": sku, "date": datetime.now().strftime("%Y-%m-%d")})
                cursor.execute("COMMIT;")
    return redirect("/gerir-fornecedores")

@app.route("/gerir-encomendas", methods=("GET",))
def gerir_encomendas():
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT order_no FROM orders WHERE NOT order_no IN (SELECT order_no FROM pay);")
            orders = []
            for order_no in cursor.fetchall():
                order = {"id": order_no[0]}
                cursor.execute(
                    """
                    SELECT name, qty
                    FROM contains INNER JOIN product ON contains.sku = product.sku
                    WHERE order_no = %(order_no)s;
                    """,
                    {"order_no": order_no[0]})
                parser = lambda el : {"name": el[0], "qty": el[1]}
                order["products"] = list(map(parser, cursor.fetchall()))
                orders.append(order)

            parser = lambda el : {"id": el[0], "customer": el[1]}
            cursor.execute("SELECT order_no, cust_no FROM pay;")
            sales = list(map(parser, cursor.fetchall()))

    return render_template("gerir-encomendas.html", orders=orders, sales=sales)

@app.route("/gerir-encomendas/new", methods=("POST", "GET"))
def gerir_encomendas_new():
    if request.method == "POST":
        cust_no = request.form["cust_no"]
        products = []
        error = ""
        for key in request.form.keys():
            if key != "cust_no" and request.form[key] != "0":
                products.append((key, request.form[key]))
    
        if not cust_no:
            error = "Número de cliente inválido"
    
        if error:
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("START TRANSACTION;")
                    existing_cust_no = cursor.execute("SELECT cust_no FROM customer WHERE cust_no = %(cust_no)s AND NOT email = 'deleted';", {"cust_no": cust_no}).fetchone()
                    if not existing_cust_no:
                        error = "O número de cliente não existe"
                    else:
                        for product in products:
                            existing_sku = cursor.execute("SELECT sku FROM product WHERE sku = %(sku)s;", {"sku": product[0]}).fetchone()
                            if not existing_sku:
                                error = f"O produto {product[0]} já não existe"
                                break
                    if error:
                        flash(error)
                    else:
                        order_no = cursor.execute("SELECT MAX(order_no) FROM orders;").fetchone()[0]
                        if not order_no:
                            order_no = 1
                        else:
                            order_no += 1
                        
                        cursor.execute(
                            """
                            INSERT INTO orders
                            VALUES (%(order_no)s, %(cust_no)s, %(date)s);
                            """,
                            {"order_no": order_no, "cust_no": cust_no, "date": datetime.now().strftime("%Y-%m-%d")})

                        for product in products:
                            cursor.execute("INSERT INTO contains VALUES (%(order_no)s, %(sku)s, %(quantity)s);", {"order_no": order_no, "sku": product[0], "quantity": product[1]})

                    cursor.execute("COMMIT;")
        return redirect("/gerir-encomendas")
    else:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT sku, name FROM product;")
                parser = lambda el : {"id": el[0], "name": el[1]}
                products = list(map(parser, cursor.fetchall()))
        return render_template("realizar-encomenda.html", products=products)

@app.route("/gerir-encomendas/pay", methods=("POST",))
def realizar_encomenda():
    cust_no = request.form["cust_no"]
    order_no = request.form["order_no"]
    error = ""

    if not cust_no:
        error = "Número de cliente inválido"
    elif not order_no:
        error = "Número de encomenda inválido"

    if error:
        flash(error)
    else:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("START TRANSACTION;")
                existing_cust_no = cursor.execute("SELECT cust_no FROM customer WHERE cust_no = %(cust_no)s AND NOT email = 'deleted';", {"cust_no": cust_no}).fetchone()
                if not existing_cust_no:
                    error = "O número de cliente não existe"
                existing_order_no = cursor.execute("SELECT order_no FROM orders WHERE order_no = %(order_no)s;", {"order_no": order_no}).fetchone()
                if not existing_order_no:
                    error = "O número de encomenda não existe"

                if error:
                    flash(error)
                else:
                    cursor.execute(
                        """
                        INSERT INTO pay VALUES
                        (%(order_no)s, %(cust_no)s);
                        """,
                        {"order_no": order_no, "cust_no": cust_no})
                cursor.execute("COMMIT;")

    return redirect("/gerir-encomendas")

if __name__ == "__main__":
    app.run()
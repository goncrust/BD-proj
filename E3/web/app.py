from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
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

@app.route("/gerir-clientes", methods=["POST", "GET"])
def gerir_clientes():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("gerir-clientes.html")

@app.route("/gerir-produtos", methods=["POST", "GET"])
def gerir_produtos():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("gerir-produtos.html")

@app.route("/gerir-fornecedores", methods=["POST", "GET"])
def gerir_fornecedores():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("gerir-fornecedores.html")

@app.route("/editar-produtos", methods=["POST", "GET"])
def editar_produtos():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("editar-produtos.html")

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
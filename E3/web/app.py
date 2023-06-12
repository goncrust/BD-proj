from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    elements =  [
        {
            "url": "/gerir-clientes",
            "title": "Gerir Clientes"
        },
        {
            "url": "/gerir-fornecedores",
            "title": "Gerir Fornecedores"
        },
        {
            "url": "/gerir-produtos",
            "title": "Gerir Produtos"
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

@app.route("/<action>")
def gerir_produtos():
    return render_template(f"{action}.html")
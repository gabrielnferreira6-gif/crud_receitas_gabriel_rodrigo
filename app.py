from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)


def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        database="Receitas",
        user="postgres",
        password="senai",
        port="5432"
    )
    return banco


# PAGINA INICIAL
@app.route("/")
def index():
    return render_template("index.html")


# LISTAR INGREDIENTES
@app.route("/ingredientes")
def ingredientes():
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("SELECT * FROM ingrediente ORDER BY id")
    lista = cursor.fetchall()

    cursor.close()
    banco.close()

    return render_template("ingredientes.html", ingredientes=lista)


# ABRIR FORMULARIO DE CADASTRO
@app.route("/ingredientes/adicionar")
def adicionar_ingrediente():
    return render_template("adicionar_ingrediente.html")


# CADASTRAR INGREDIENTE
@app.route("/ingredientes/enviar", methods=["POST"])
def enviar_ingrediente():
    nome = request.form["nome"]
    unidade = request.form["unidade"]
    estoque = request.form["estoque"]
    data_validade = request.form["data_validade"]

    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""
            INSERT INTO ingrediente
            (nome, unidade, estoque, data_validade)
            VALUES (%s, %s, %s, %s)
    """, (nome, unidade, estoque, data_validade))

    banco.commit()

    cursor.close()
    banco.close()

    return redirect("/ingredientes")

@app.route("/ingredientes/editar/<int:id>")
def editar_ingrediente(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "SELECT * FROM ingrediente WHERE id = %s",
        (id,)
    )

    ingrediente = cursor.fetchone()

    cursor.close()
    banco.close()

    if ingrediente is None:
        return "Ingrediente não encontrado",

    return render_template(
        "editar_ingrediente.html",
        ingrediente=ingrediente
    )

@app.route("/ingredientes/atualizar/<int:id>", methods=["POST"])
def atualizar_ingrediente(id):
    nome = request.form["nome"]
    unidade = request.form["unidade"]
    estoque = request.form["estoque"]
    data_validade = request.form["data_validade"]

    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        UPDATE ingrediente
        SET nome = %s,
            unidade = %s,
            estoque = %s,
            data_validade = %s
        WHERE id = %s
    """, (nome, unidade, estoque, data_validade, id))

    banco.commit()

    cursor.close()
    banco.close()

    return redirect("/ingredientes")


@app.route("/ingredientes/excluir/<int:id>", methods=["POST"])
def excluir_ingrediente(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "DELETE FROM ingrediente WHERE id = %s",
        (id,)
    )

    banco.commit()

    cursor.close()
    banco.close()

    return redirect("/ingredientes")


if __name__ == "__main__":
    app.run(debug=True)

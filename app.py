from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Configurações

app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///financeiro.db"
db = SQLAlchemy(app)

#Dataclass / Models

class Lancamento(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(150), nullable = False)
    tipo = db.Column(db.String(10))
    valor = db.Column(db.Float)
    data_lancamento = db.Column(db.DateTime, default = datetime.now)

    def __init__(self, descricao, tipo, valor):
        self.descricao = descricao
        self.tipo = tipo
        self.valor = valor

with app.app_context():
    db.create_all()

#Rotas

@app.route("/", methods = ["POST", "GET"])
def index():
    
    #Adicionar lançamento
    if request.method == "POST":
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        valor = float(request.form['valor'])
        novo_lancamento = Lancamento(descricao, tipo, valor)
        try:
            db.session.add(novo_lancamento)
            db.session.commit()
            return redirect("/")
        except Exception as err:
            print(f"Erro: {err}")
            return f"ERROR: {err}"
    else:
        lancamentos = Lancamento.query.order_by(Lancamento.data_lancamento).all()
        return render_template("index.html", lancamentos=lancamentos)
    

#Deletar elemento
@app.route("/delete/<int:id>")

def delete_by_id(id: int):
    lancamento_deletado = Lancamento.query.get_or_404(id)
    try:
        db.session.delete(lancamento_deletado)
        db.session.commit()
        return redirect("/")
    except Exception as err:
        return f"ERRO: {err}"

if __name__ in "__main__":
    app.run(debug=True)
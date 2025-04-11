from flask import Flask, render_template, request, redirect
from collections import defaultdict
from datetime import datetime
import zoneinfo
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from datetime import datetime
import pytz

def hora_brasil():
    utc_now = datetime.utcnow()
    fuso_sp = pytz.timezone("America/Sao_Paulo")
    return utc_now.replace(tzinfo=pytz.utc).astimezone(fuso_sp)

# Modelos
class ItemEstoque(db.Model):
    __tablename__ = 'itens_estoque'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    quantidade_inicial = db.Column(db.Integer, default=0)
    quantidade_atual = db.Column(db.Integer, default=0)

class Registro(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))  # retirada ou devolucao
    nome = db.Column(db.String(100))
    chapa = db.Column(db.String(20))
    area = db.Column(db.String(100))
    ordem = db.Column(db.String(100))
    data = db.Column(db.DateTime, default=lambda: hora_brasil())
    itens = db.relationship("ItemRegistro", backref="registro", cascade="all, delete-orphan")

class ItemRegistro(db.Model):
    __tablename__ = 'itens_registro'
    id = db.Column(db.Integer, primary_key=True)
    registro_id = db.Column(db.Integer, db.ForeignKey('registros.id'))
    nome_item = db.Column(db.String(50))
    quantidade = db.Column(db.Integer)

estoque_inicial = {}
estoque_atual = {}
retiradas = []
devolucoes = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tipo = request.form.get("tipo")

        if tipo == "estoque":
            for item in ["Refletores", "Extensões", "Exaustores"]:
                qtd = int(request.form.get(item, 0))
                item_db = ItemEstoque.query.filter_by(nome=item).first()
                if not item_db:
                    item_db = ItemEstoque(nome=item, quantidade_inicial=qtd, quantidade_atual=qtd)
                    db.session.add(item_db)
                else:
                    item_db.quantidade_inicial = qtd
                    item_db.quantidade_atual = qtd
            db.session.commit()

        elif tipo == "retirada":
            nome = request.form["nome"]
            chapa = request.form["chapa"]
            area = request.form["area"]
            ordem = request.form["ordem"]

            registro = Registro(tipo="retirada", nome=nome, chapa=chapa, area=area, ordem=ordem)

            for item_nome in ["Refletores", "Extensões", "Exaustores"]:
                qtd = int(request.form.get(item_nome, 0))
                if qtd > 0:
                    item_registro = ItemRegistro(nome_item=item_nome, quantidade=qtd)
                    registro.itens.append(item_registro)

                    item_estoque = ItemEstoque.query.filter_by(nome=item_nome).first()
                    if item_estoque:
                        item_estoque.quantidade_atual -= qtd

            db.session.add(registro)
            db.session.commit()

        elif tipo == "devolucao":
            nome = request.form["nome"]
            chapa = request.form["chapa"]
            area = request.form["area"]
            ordem = request.form["ordem"]

            registro = Registro(tipo="devolucao", nome=nome, chapa=chapa, area=area, ordem=ordem)

            for item_nome in ["Refletores", "Extensões", "Exaustores"]:
                qtd = int(request.form.get(item_nome, 0))
                if qtd > 0:
                    item_registro = ItemRegistro(nome_item=item_nome, quantidade=qtd)
                    registro.itens.append(item_registro)

                    item_estoque = ItemEstoque.query.filter_by(nome=item_nome).first()
                    if item_estoque:
                        item_estoque.quantidade_atual += qtd

            db.session.add(registro)
            db.session.commit()

        return redirect("/")

    return render_template("index.html")

@app.route("/finalizar")
def finalizar():
    registros = Registro.query.order_by(Registro.data.asc()).all()
    saldo_individual = defaultdict(lambda: defaultdict(int))
    extraviados = defaultdict(int)

    for r in registros:
        chave = (
            r.nome.strip().lower(),
            r.chapa.strip().lower(),
            r.area.strip().lower(),
            r.ordem.strip().lower()
        )
        for item in r.itens:
            if r.tipo == "retirada":
                saldo_individual[chave][item.nome_item] += item.quantidade
            elif r.tipo == "devolucao":
                saldo_individual[chave][item.nome_item] -= item.quantidade

    pessoas_nao_devolveram = []
    for chave, itens in saldo_individual.items():
        faltando = {k: v for k, v in itens.items() if v > 0}
        if faltando:
            for k, v in faltando.items():
                extraviados[k] += v
            pessoas_nao_devolveram.append({
                "nome": chave[0].title(),
                "chapa": chave[1],
                "area": chave[2].title(),
                "ordem": chave[3],
                "faltando": faltando
            })

    return render_template("relatorio.html", extraviados=extraviados, pessoas=pessoas_nao_devolveram)

@app.route("/dashboard")
def dashboard():
    registros = Registro.query.order_by(Registro.data.asc()).all()
    saldo_individual = defaultdict(lambda: defaultdict(int))
    extraviados = defaultdict(int)
    area_contador = defaultdict(int)

    for r in registros:
        chave = (
            r.nome.strip().lower(),
            r.chapa.strip().lower(),
            r.area.strip().lower(),
            r.ordem.strip().lower()
        )
        for item in r.itens:
            if r.tipo == "retirada":
                saldo_individual[chave][item.nome_item] += item.quantidade
            elif r.tipo == "devolucao":
                saldo_individual[chave][item.nome_item] -= item.quantidade

    pessoas_nao_devolveram = []
    for chave, itens in saldo_individual.items():
        faltando = {k: v for k, v in itens.items() if v > 0}
        if faltando:
            for k, v in faltando.items():
                extraviados[k] += v
            pessoas_nao_devolveram.append({
                "nome": chave[0].title(),
                "chapa": chave[1],
                "area": chave[2].title(),
                "ordem": chave[3],
                "faltando": faltando
            })
            area_contador[chave[2]] += sum(faltando.values())

    area_top = max(area_contador.items(), key=lambda x: x[1])[0] if area_contador else "Nenhuma"

    itens_estoque = ItemEstoque.query.all()
    estoque_final = {item.nome: item.quantidade_atual for item in itens_estoque}
    estoque_inicial = {item.nome: item.quantidade_inicial for item in itens_estoque}

    return render_template("dashboard.html", 
                           estoque_inicial=estoque_inicial,
                           estoque_final=estoque_final,
                           extraviados=extraviados,
                           pessoas=pessoas_nao_devolveram,
                           area_top=area_top)

@app.route("/retiradas_ativas")
def retiradas_ativas():
    registros = Registro.query.filter_by(tipo="retirada").order_by(Registro.data.desc()).all()
    print("Registros encontrados:", registros)
    return render_template("retiradas_ativas.html", retiradas=registros, zoneinfo=zoneinfo)

@app.route("/devolucoes")
def listar_devolucoes():
    registros = Registro.query.filter_by(tipo="devolucao").order_by(Registro.data.desc()).all()
    return render_template("devolucoes.html", registros=registros)  # <-- aqui a correção

@app.route("/resetar", methods=["POST"])
def resetar():
    db.session.query(ItemRegistro).delete()
    db.session.query(Registro).delete()
    db.session.query(ItemEstoque).delete()
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
from collections import defaultdict

app = Flask(__name__)

estoque_inicial = {}
estoque_atual = {}
retiradas = []
devolucoes = []

@app.route("/", methods=["GET", "POST"])
def index():
    global estoque_inicial, estoque_atual
    if request.method == "POST":
        tipo = request.form.get("tipo")

        if tipo == "estoque":
            for item in ["Refletores", "Extensões", "Exaustores"]:
                qtd = int(request.form.get(item, 0))
                estoque_inicial[item] = qtd
                estoque_atual[item] = qtd

        elif tipo in ["retirada", "devolucao"]:
            registro = {
                "nome": request.form["nome"],
                "chapa": request.form["chapa"],
                "area": request.form["area"],
                "ordem": request.form["ordem"],
                "itens": {},
            }
            chave = (
                registro["nome"].strip().lower(),
                registro["chapa"].strip().lower(),
                registro["area"].strip().lower(),
                registro["ordem"].strip().lower()
            )

            if tipo == "devolucao":
                retiradas_keys = {
                    (
                        r["nome"].strip().lower(),
                        r["chapa"].strip().lower(),
                        r["area"].strip().lower(),
                        r["ordem"].strip().lower()
                    )
                    for r in retiradas
                }
                if chave not in retiradas_keys:
                    mensagem = f"⚠️ Devolução ignorada: {registro['nome'].title()} (chapa {registro['chapa']}) não possui retirada registrada."
                    return render_template("index.html", estoque=estoque_atual, mensagem=mensagem)
                if chave not in retiradas_keys:
                    print(f"Ignorando devolução de {registro['nome']} - {registro['chapa']}: não há retirada registrada.")
                    return redirect("/")

            for item in ["Refletores", "Extensões", "Exaustores"]:
                qtd = int(request.form.get(item, 0))
                if qtd:
                    registro["itens"][item] = qtd
                    if item not in estoque_atual:
                        estoque_atual[item] = 0
                    estoque_atual[item] -= qtd if tipo == "retirada" else -qtd

            if tipo == "retirada":
                retiradas.append(registro)
            else:
                devolucoes.append(registro)

    return render_template("index.html", estoque=estoque_atual)

@app.route("/finalizar")
def finalizar():
    extraviados = defaultdict(int)
    saldo_individual = {}

    for r in retiradas:
        chave = (
            r["nome"].strip().lower(),
            r["chapa"].strip().lower(),
            r["area"].strip().lower(),
            r["ordem"].strip().lower()
        )
        if chave not in saldo_individual:
            saldo_individual[chave] = defaultdict(int)
        for item, qtd in r["itens"].items():
            saldo_individual[chave][item] += qtd

    for d in devolucoes:
        chave = (
            d["nome"].strip().lower(),
            d["chapa"].strip().lower(),
            d["area"].strip().lower(),
            d["ordem"].strip().lower()
        )
        if chave in saldo_individual:
            for item, qtd in d["itens"].items():
                saldo_individual[chave][item] -= qtd
        else:
            print(f"Ignorando devolução de {d['nome']} - {d['chapa']} pois não há retirada registrada.")

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
    extraviados = defaultdict(int)
    saldo_individual = {}
    area_contador = defaultdict(int)

    for r in retiradas:
        chave = (
            r["nome"].strip().lower(),
            r["chapa"].strip().lower(),
            r["area"].strip().lower(),
            r["ordem"].strip().lower()
        )
        if chave not in saldo_individual:
            saldo_individual[chave] = defaultdict(int)
        for item, qtd in r["itens"].items():
            saldo_individual[chave][item] += qtd

    for d in devolucoes:
        chave = (
            d["nome"].strip().lower(),
            d["chapa"].strip().lower(),
            d["area"].strip().lower(),
            d["ordem"].strip().lower()
        )
        if chave not in saldo_individual:
            saldo_individual[chave] = defaultdict(int)
        for item, qtd in d["itens"].items():
            saldo_individual[chave][item] -= qtd

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

    return render_template("dashboard.html", estoque_inicial=estoque_inicial,
                           estoque_final=estoque_atual,
                           extraviados=extraviados,
                           pessoas=pessoas_nao_devolveram,
                           area_top=area_top)

@app.route("/retiradas_ativas")
def retiradas_ativas():
    saldo_individual = {}

    for r in retiradas:
        chave = (
            r["nome"].strip().lower(),
            r["chapa"].strip().lower(),
            r["area"].strip().lower(),
            r["ordem"].strip().lower()
        )
        if chave not in saldo_individual:
            saldo_individual[chave] = defaultdict(int)
        for item, qtd in r["itens"].items():
            saldo_individual[chave][item] += qtd

    for d in devolucoes:
        chave = (
            d["nome"].strip().lower(),
            d["chapa"].strip().lower(),
            d["area"].strip().lower(),
            d["ordem"].strip().lower()
        )
        if chave not in saldo_individual:
            saldo_individual[chave] = defaultdict(int)
        for item, qtd in d["itens"].items():
            saldo_individual[chave][item] -= qtd

    retiradas_ativas = []
    for chave, itens in saldo_individual.items():
        ativos = {k: v for k, v in itens.items() if v > 0}
        if ativos:
            retiradas_ativas.append({
                "nome": chave[0].title(),
                "chapa": chave[1],
                "area": chave[2].title(),
                "ordem": chave[3],
                "ativos": ativos
            })

    return render_template("retiradas_ativas.html", retiradas=retiradas_ativas)

@app.route("/resetar", methods=["POST"])
def resetar():
    global estoque_inicial, estoque_atual, retiradas, devolucoes
    estoque_inicial = {}
    estoque_atual = {}
    retiradas = []
    devolucoes = []
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

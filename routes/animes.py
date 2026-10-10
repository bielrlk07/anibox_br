from flask import Blueprint, redirect, render_template, request, session  # type: ignore

from dados import (  # Importando os dados do seu arquivo novo
    historico_acoes,
    meus_animes,
)

animes_bp = Blueprint("animes", __name__)


@animes_bp.route("/")
def index():

    if "usuario_logado" not in session:  # Se o usuário não estiver logado, redireciona para a página de login
        return redirect("/login")
    
    return render_template("listadeanimes.html", lista_animes=meus_animes, historico_acoes=historico_acoes)     # O render_template vai buscar um arquivo HTML e nós 'injetamos' a lista nele,
        #Enviamos a lista de histórico inteira para o HTML



@animes_bp.route("/atualizar", methods=["POST"])
def atualizar():

    nome = request.form.get("nome_anime")     # Avisa o Python que vamos modificar a memória global
    novos_eps = int(request.form.get("novos_eps")) # Pega as informações que vieram do HTML

    for anime in meus_animes: # Pega o número que a pessoa digitou lá na caixinha
        if anime["nome"] == nome:

            # ANTES de somar os episódios novos, nós tiramos uma "fotografia" do estado atual
            historico_acoes.append({
                "nome": anime["nome"],
                "eps_vistos_antes": anime["eps_vistos"],
                "finalizado_antes": anime["finalizado"]
            })

            anime["eps_vistos"] += novos_eps # O += soma o valor atual com os novos episódios

            if anime["eps_vistos"] >= anime["total_eps"]: # Verificação de segurança: se a soma bater ou passar do total, finaliza!
                anime["eps_vistos"] = anime["total_eps"]
                anime["finalizado"] = True

            break # Como já achamos e atualizamos o anime, podemos parar o loop

    return redirect("/")



@animes_bp.route("/desfazer",methods=["POST"]) # NOVA ROTA: Responsável por reverter a ação quando o botão Desfazer for clicado
def desfazer():

    if len(historico_acoes) > 0: # Só tenta desfazer se a lista de histórico NÃO estiver vazia (len > 0)
        acao_revertida = historico_acoes.pop() # O .pop() pega a última ação salva e arranca ela da lista

        for anime in meus_animes: 
            if anime["nome"] == acao_revertida["nome"]:
                anime["eps_vistos"] = acao_revertida["eps_vistos_antes"] # Devolve os valores antigos para o anime
                anime["finalizado"] = acao_revertida["finalizado_antes"]
                break

        
    return redirect("/")

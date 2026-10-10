import sqlite3

from flask import Blueprint, redirect, render_template, request, session

animes_bp = Blueprint('animes', __name__)

def conectar_banco():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row
    return conexao

# 1. TELA INICIAL: Minha Lista Pessoal
@animes_bp.route("/")
def index():
    if "usuario_logado" not in session:
        return redirect("/login")
        
    usuario_atual = session["usuario_logado"]
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # O JOIN mágico: Busca na 'minha_lista' e cruza com a tabela 'animes' para pegar o nome
    cursor.execute('''
        SELECT ml.id as lista_id, a.id as anime_id, a.nome, a.tipo, a.total_eps, 
               ml.eps_vistos, ml.finalizado
        FROM minha_lista ml
        JOIN animes a ON ml.anime_id = a.id
        WHERE ml.username = ?
    ''', (usuario_atual,))
    
    meus_animes = [dict(row) for row in cursor.fetchall()]
    conexao.close()
    
    return render_template("listadeanimes.html", animes=meus_animes, usuario_logado=usuario_atual)

# 2. NOVA ABA: Catálogo Global
@animes_bp.route("/catalogo")
def catalogo():
    if "usuario_logado" not in session:
        return redirect("/login")
        
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Pega todos os animes cadastrados globalmente
    cursor.execute("SELECT * FROM animes")
    todos_animes = [dict(row) for row in cursor.fetchall()]
    conexao.close()
    
    return render_template("catalogo.html", animes=todos_animes)

# 3. ROTA PARA ADICIONAR DO CATÁLOGO PARA A LISTA PESSOAL
@animes_bp.route("/adicionar_lista", methods=["POST"])
def adicionar_lista():
    if "usuario_logado" not in session:
        return redirect("/login")
        
    anime_id = request.form.get("anime_id")
    usuario_atual = session["usuario_logado"]
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    try:
        # Tenta inserir na lista pessoal com 0 episódios vistos
        cursor.execute('''
            INSERT INTO minha_lista (username, anime_id, eps_vistos, finalizado)
            VALUES (?, ?, 0, 0)
        ''', (usuario_atual, anime_id))
        conexao.commit()
    except sqlite3.IntegrityError:
        # Se der erro de integridade (UNIQUE), é porque a pessoa já tem esse anime na lista
        pass 
        
    conexao.close()
    return redirect("/")

# 4. ROTA DE ATUALIZAR EPISÓDIOS
@animes_bp.route("/atualizar", methods=["POST"])
def atualizar():
    if "usuario_logado" not in session:
        return redirect("/login")
        
    lista_id = request.form.get("lista_id")
    eps_para_adicionar = int(request.form.get("eps", 1))
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Busca quantos eps a pessoa já viu
    cursor.execute('''
        SELECT ml.eps_vistos, a.total_eps 
        FROM minha_lista ml
        JOIN animes a ON ml.anime_id = a.id
        WHERE ml.id = ?
    ''', (lista_id,))
    
    resultado = cursor.fetchone()
    
    if resultado:
        eps_vistos_atual = resultado["eps_vistos"]
        total_eps = resultado["total_eps"]
        
        novos_eps = eps_vistos_atual + eps_para_adicionar
        
        # Limita para não passar do total e marca como finalizado
        if novos_eps >= total_eps:
            novos_eps = total_eps
            finalizado = 1
        else:
            finalizado = 0
            
        cursor.execute("UPDATE minha_lista SET eps_vistos = ?, finalizado = ? WHERE id = ?", (novos_eps, finalizado, lista_id))
        conexao.commit()
        
    conexao.close()
    return redirect("/")
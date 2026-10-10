import sqlite3

from flask import Blueprint, redirect, render_template, request, session

auth_bp = Blueprint('auth', __name__)

# Função auxiliar para conectar ao banco facilmente
def conectar_banco():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row # Permite acessar as colunas pelo nome
    return conexao

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario_digitado = request.form.get("username") 
        senha_digitada = request.form.get("password")

        conexao = conectar_banco()
        cursor = conexao.cursor()
        
        # Faz um SELECT buscando alguém que tenha exatamente esse usuário e senha
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND senha = ?", (usuario_digitado, senha_digitada))
        usuario_encontrado = cursor.fetchone()
        
        conexao.close()

        if usuario_encontrado: 
            session["usuario_logado"] = usuario_encontrado["username"]  
            return redirect("/")  
        else:
            return render_template("login.html", erro_no_login="Usuário ou senha incorretos!")  

    return render_template("login.html") 

@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        novo_usuario = request.form.get("username")
        nova_senha = request.form.get("password")
        
        conexao = conectar_banco()
        cursor = conexao.cursor()
        
        # Tenta inserir. Se der erro (porque o username é UNIQUE), ele avisa
        try:
            cursor.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", (novo_usuario, nova_senha))
            conexao.commit()
        except sqlite3.IntegrityError:
            conexao.close()
            return render_template("cadastro.html", erro_no_cadastro="Esse nome de usuário já está em uso!")
            
        conexao.close()
        
        # Login automático após cadastro
        session["usuario_logado"] = novo_usuario
        return redirect("/")
        
    return render_template("cadastro.html")

@auth_bp.route("/logout")
def logout():
    session.pop("usuario_logado", None) 
    return redirect("/login")
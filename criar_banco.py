import sqlite3

# Isso cria o arquivo "banco.db" na sua pasta (ou apenas conecta, se ele já existir)
conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

# Criação da tabela com SQL puro
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
''')

# Salvando algumas contas de teste diretamente no banco
cursor.execute("INSERT OR IGNORE INTO usuarios (username, senha) VALUES ('admin', '1234')")
cursor.execute("INSERT OR IGNORE INTO usuarios (username, senha) VALUES ('gabriel', 'senha123')")

conexao.commit()
conexao.close()

print("Banco de dados 'banco.db' criado e populado com sucesso!")
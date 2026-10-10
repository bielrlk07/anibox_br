import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

# 1. Tabela de Usuários
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        username TEXT PRIMARY KEY,
        senha TEXT NOT NULL
    )
''')

# 2. Tabela Global de Animes (O Catálogo Oficial)
# Repare que tiramos os eps_vistos daqui. Essa tabela é fixa!
cursor.execute('''
    CREATE TABLE IF NOT EXISTS animes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        tipo TEXT NOT NULL,
        total_eps INTEGER NOT NULL
    )
''')

# 3. Tabela de Relacionamento (A lista pessoal de cada um)
# Aqui salvamos QUEM está assistindo O QUE, e em qual episódio parou
cursor.execute('''
    CREATE TABLE IF NOT EXISTS minha_lista (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        anime_id INTEGER NOT NULL,
        eps_vistos INTEGER DEFAULT 0,
        finalizado BOOLEAN DEFAULT 0,
        FOREIGN KEY (username) REFERENCES usuarios (username),
        FOREIGN KEY (anime_id) REFERENCES animes (id),
        UNIQUE(username, anime_id) -- Impede que a pessoa adicione o mesmo anime duas vezes na lista
    )
''')

# --- POPULANDO O BANCO COM DADOS INICIAIS ---

# Inserindo contas de teste
cursor.execute("INSERT OR IGNORE INTO usuarios (username, senha) VALUES ('admin', '1234')")
cursor.execute("INSERT OR IGNORE INTO usuarios (username, senha) VALUES ('gabriel', 'senha123')")

# Inserindo o Catálogo Fixo de Animes (Os usuários vão escolher destes)
animes_iniciais = [
    ('Naruto', 'TV', 220),
    ('Baki', 'TV', 26),
    ('Jujutsu Kaisen', 'TV', 24),
    ('Kimi no Na wa', 'Filme', 1),
    ('One Piece', 'TV', 1100),
    ('Blue Lock', 'TV', 24),
    ('Attack on Titan', 'TV', 97),
    ('Demon Slayer', 'TV', 63),
    ('My Hero Academia', 'TV', 170),
    ('Death Note', 'TV', 37),
    ('Dragon Ball Super', 'TV', 131),
    ('Fullmetal Alchemist: Brotherhood', 'TV', 64),
    ('Hunter x Hunter (2011)', 'TV', 148),
    ('Steins Gate', 'TV', 24),
    ('Cowboy Bebop', 'TV', 26),
    ('Neon Genesis Evangelion', 'TV', 26),
    ('Vinland Saga', 'TV', 48),
    ('Mob Psycho 100', 'TV', 37),
    ('One Punch Man', 'TV', 24),
    ('Cyberpunk: Edgerunners', 'TV', 10),
    ('Code Geass', 'TV', 50),
    ('Haikyuu', 'TV', 85),
    ('Monster', 'TV', 74),
    ('Tengen Toppa Gurren Lagann', 'TV', 27),
    ('Violet Evergarden', 'TV', 13),
    ('Sousou no Frieren', 'TV', 28),
    ('Bleach', 'TV', 366),
    ('Chainsaw Man', 'TV', 12),
    ('Gintama', 'TV', 367),
    ('JoJo´s Bizarre Adventure', 'TV', 190),
    ('Koe no Katachi', 'Filme', 1)

]
cursor.executemany("INSERT OR IGNORE INTO animes (nome, tipo, total_eps) VALUES (?, ?, ?)", animes_iniciais)

conexao.commit()
conexao.close()

print("Banco recriado com sucesso!")
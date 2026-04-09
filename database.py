import sqlite3
from datetime import datetime

DATABASE = 'projeto.db'

def conectar():
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contatos_nutri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            whatsapp TEXT NOT NULL,
            objetivo TEXT NOT NULL,
            data_envio TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados pronto!")

def salvar_contato(nome, whatsapp, objetivo):
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        
        cursor.execute('''
            INSERT INTO contatos_nutri (nome, whatsapp, objetivo)
            VALUES (?, ?, ?)
        ''', (nome, whatsapp, objetivo))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar contato: {e}")
        return False

def listar_contatos(limite=100):
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nome, whatsapp, objetivo, data_envio 
            FROM contatos_nutri 
            ORDER BY data_envio DESC
            LIMIT ?
        ''', (limite,))
        
        contatos = cursor.fetchall()
        conn.close()
        
        return [dict(contato) for contato in contatos]
    except Exception as e:
        print(f"❌ Erro ao listar contatos: {e}")
        return []

def obter_estatisticas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM contatos_nutri')
        total = cursor.fetchone()['total']
        
        
        cursor.execute('''
            SELECT COUNT(*) as hoje 
            FROM contatos_nutri 
            WHERE DATE(data_envio) = DATE('now', 'localtime')
        ''')
        hoje = cursor.fetchone()['hoje']
        
        
        cursor.execute('''
            SELECT COUNT(*) as semana 
            FROM contatos_nutri 
            WHERE DATE(data_envio) >= DATE('now', 'localtime', '-7 days')
        ''')
        semana = cursor.fetchone()['semana']
        
        
        cursor.execute('''
            SELECT COUNT(*) as mes 
            FROM contatos_nutri 
            WHERE strftime('%Y-%m', data_envio) = strftime('%Y-%m', 'now', 'localtime')
        ''')
        mes = cursor.fetchone()['mes']
        
        conn.close()
        
        return {
            'total': total,
            'hoje': hoje,
            'semana': semana,
            'mes': mes
        }
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {e}")
        return None
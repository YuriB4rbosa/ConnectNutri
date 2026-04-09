from flask import render_template, request, jsonify, session, redirect, url_for
from database import salvar_contato, listar_contatos, obter_estatisticas
import os

SENHA_ADMIN = os.getenv('ADMIN_PASSWORD')

def configurar_rotas(app):
    
    @app.route('/')
    def index():
        
        return render_template('index.html')
    
    @app.route('/agendar', methods=['POST'])
    def agendar():
        
        try:
            nome = request.form.get('nome', '').strip()
            whatsapp = request.form.get('whatsapp', '').strip()
            objetivo = request.form.get('objetivo', '').strip()
            
            if not nome or not whatsapp or not objetivo:
                return jsonify({'success': False, 'message': 'Preencha todos os campos.'}), 400
            
            
            whatsapp_clean = ''.join(filter(str.isdigit, whatsapp))
            
            if len(whatsapp_clean) < 10 or len(whatsapp_clean) > 11:
                return jsonify({'success': False, 'message': 'WhatsApp inválido.'}), 400
            
            sucesso = salvar_contato(nome, whatsapp_clean, objetivo)
            
            if sucesso:
                return jsonify({
                    'success': True, 
                    'message': f'Olá {nome}! Agendamento registrado. Vamos conversar no WhatsApp!'
                })
            return jsonify({'success': False, 'message': 'Erro ao salvar dados.'}), 500
            
        except Exception as e:
            print(f"Erro: {str(e)}")
            return jsonify({'success': False, 'message': 'Erro interno.'}), 500

    

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        
        if request.method == 'POST':
            senha = request.form.get('senha')
            if senha == SENHA_ADMIN:
                session['logado'] = True
                session.permanent = True 
                return redirect(url_for('admin'))
            return render_template('login.html', erro="Senha incorreta!")
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        
        session.pop('logado', None)
        return redirect(url_for('login'))

    
    @app.route('/admin')
    def admin():
        
        if not session.get('logado'):
            return redirect(url_for('login'))
        return render_template('admin.html')

    @app.route('/admin/contatos')
    def listar_contatos_route():
        
        if not session.get('logado'):
            return jsonify({'error': 'Não autorizado'}), 401
        try:
            contatos = listar_contatos(100)
            return jsonify(contatos)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/admin/dashboard')
    def admin_dashboard():
        
        if not session.get('logado'):
            return jsonify({'error': 'Não autorizado'}), 401
        try:
            stats = obter_estatisticas()
            if stats:
                return jsonify({
                    'total_contatos': stats['total'],
                    'contatos_hoje': stats['hoje'],
                    'contatos_semana': stats['semana'],
                    'contatos_mes': stats['mes']
                })
            return jsonify({'error': 'Erro ao obter estatísticas'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
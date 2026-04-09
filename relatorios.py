from fpdf import FPDF
import sqlite3
from datetime import datetime

def gerar_relatorio_semanal():
    
    conn = sqlite3.connect("projeto.db") 
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("SELECT nome, whatsapp, objetivo, data_envio FROM contatos_nutri")
        contatos = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return
    finally:
        conn.close()

    if not contatos:
        print("Nenhum novo contato para o relatório.")
        return

    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16) 
    
    
    pdf.cell(0, 10, text="Relatório de Novos Pacientes - Nutrição", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=10)
    pdf.cell(0, 10, text=f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    
    for contato in contatos:
        
        nome, whats, objetivo, data = contato
        
        
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(27, 67, 50) 
        pdf.cell(0, 10, text=f"Paciente: {nome}", new_x="LMARGIN", new_y="NEXT")
        
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("helvetica", size=11)
        pdf.cell(0, 8, text=f"WhatsApp: {whats}", new_x="LMARGIN", new_y="NEXT")
        
        
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 8, text="Objetivo:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", size=11)
        pdf.multi_cell(0, 8, text=f"{objetivo}")
        
        
        pdf.cell(0, 8, text=f"Data de interesse: {data}", new_x="LMARGIN", new_y="NEXT")
        
        
        pdf.ln(5)
        pdf.cell(0, 0, border="T") 
        pdf.ln(5)

    
    nome_arquivo = f"relatorio_nutri_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf.output(nome_arquivo)
    print(f"✅ Relatório '{nome_arquivo}' gerado com sucesso!")

if __name__ == "__main__":
    gerar_relatorio_semanal()
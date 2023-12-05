import tkinter as tk
from tkinter import Tk, Toplevel, Label, Text, Scrollbar, messagebox, Button
import customtkinter
from CTkMessagebox import CTkMessagebox
import sqlite3

def criar_tabela():
    conexao = sqlite3.connect('imc_db.sqlite')
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            endereco TEXT,
            altura REAL,
            peso REAL,
            imc REAL,
            classificacao TEXT
        )
    ''')

    conexao.commit()
    conexao.close()

def salvar_no_banco(nome, endereco, altura, peso, imc, classificacao):
    conexao = sqlite3.connect('imc_db.sqlite')
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO imc (nome, endereco, altura, peso, imc, classificacao)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, endereco, altura, peso, imc, classificacao))

    conexao.commit()
    conexao.close()

def buscar_dados():
    conexao = sqlite3.connect('imc_db.sqlite')
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM imc')
    dados = cursor.fetchall()

    conexao.close()
    return dados

def calcular_imc():
    try:
        altura_str = entrada_alt.get().replace('.', '').replace(',', '')  # Remover ponto e vírgula
        altura = float(altura_str) / 100  # Converter altura para metros
        peso = float(entrada_peso.get())

        imc = peso / (altura ** 2)

        classificacao = ""

        if imc < 16:
            classificacao = "Desnutrição grave"
        elif imc < 16.9:
            classificacao = "Desnutrição moderada"
        elif imc < 18.5:
            classificacao = "Desnutrição leve"
        elif imc < 25:
            classificacao = "Normal"
        elif imc < 30:
            classificacao = "Sobrepeso"
        elif imc < 35:
            classificacao = "Pré-Obesidade"
        elif imc < 40:
            classificacao = "Obesidade Grau I"
        elif imc < 45:
            classificacao = "Obesidade Grau II"
        else:
            classificacao = "Obesidade Grau III (Mórbida)"

        nome = entrada_nome.get()
        endereco = entrada_end.get()

        resultado = f"Nome: {nome}\nEndereço: {endereco}\nIMC: {imc:.2f}\nClassificação: {classificacao}"
        resultado_label.configure(text=resultado)

        # Salvar no banco de dados
        salvar_no_banco(nome, endereco, altura, peso, imc, classificacao)

    except ValueError:
        resultado_label.configure(text="Erro: Insira valores válidos para altura e peso.")

def exibir_dados():
    
    dados = buscar_dados()
    if dados:
        # Se houver dados, criar uma nova janela para exibir
        nova_janela = customtkinter.CTk()
        nova_janela.title("Dados Consultados")
        nova_janela.geometry("500x400")
        nova_janela._set_appearance_mode("dark")

        resultado = "Dados encontrados:\n"
        for dado in dados:
            resultado += f"Nome: {dado[1]}\nEndereço: {dado[2]}\nIMC: {dado[5]:.2f}\nClassificação: {dado[6]}\n\n"

        # Usar o widget Text com barra de rolagem
        resultado_text = Text(nova_janela, wrap="word", width=50, height=10)
        resultado_text.pack(padx=10, pady=10)

        scrollbar = Scrollbar(nova_janela, command=resultado_text.yview)
        scrollbar.pack(side="right", fill="y")

        resultado_text.config(yscrollcommand=scrollbar.set)
        resultado_text.insert("1.0", resultado)
        resultado_text.config(state="disabled")  # Desabilita a edição

        # Adicionar um botão para limpar o banco de dados com o mesmo estilo
        botao_limpar_banco = customtkinter.CTkButton(nova_janela, text="Limpar Banco de Dados", command=limpar_banco, bg_color="#242424", fg_color="#263d76")
        botao_limpar_banco.pack(pady=10)

        # Iniciar o loop principal da nova interface gráfica
        nova_janela.mainloop()
    else:
        CTkMessagebox(title="Sem Dados", message="Nenhum dado encontrado.", fg_color="#242424", bg_color="#242424", text_color="white", button_color="#263d76", title_color="white")

def limpar_banco():
    msg = CTkMessagebox(title="Limpar Banco de Dados", message="Tem certeza que deseja limpar o banco de dados?", option_1="Sim", option_2="Não", icon="question", fg_color="#242424", bg_color="#242424", text_color="white", button_color="#263d76", title_color="white")
    resposta = msg.get()
    if resposta:
        conexao = sqlite3.connect('imc_db.sqlite')
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM imc')
        conexao.commit()
        conexao.close()
        CTkMessagebox(title="Limpeza Concluída", message="Banco de dados limpo com sucesso.", fg_color="#242424", bg_color="#242424", text_color="white", button_color="#263d76", title_color="white")

def limpar_resultado():
    resultado_label.configure(text="")

def sair():
    janela.destroy()

# Criar uma janela
janela = customtkinter.CTk()
janela.title("CALCULADORA DE IMC")
janela.geometry("650x250")
janela._set_appearance_mode("dark")
janela.resizable(False, False)

# Criar campos de entrada de texto
frame1 = customtkinter.CTkFrame(janela, fg_color="#242424", bg_color="#242424", )
frame1.grid(row=0, column=0, padx=10, pady=10, sticky='w')

label_nome = customtkinter.CTkLabel(frame1, text="NOME PACIENTE:", text_color="white")
label_nome.grid(row=0, column=0, sticky='w')

entrada_nome = customtkinter.CTkEntry(frame1, width=420, height=20)
entrada_nome.grid(row=0, column=1, sticky='w', padx=10)

frame2 = customtkinter.CTkFrame(janela, fg_color="#242424", bg_color="#242424")
frame2.grid(row=1, column=0, padx=10, pady=10, sticky='w')

label_end = customtkinter.CTkLabel(frame2, text="ENDEREÇO:(XXXXXX-XX)", text_color="white")
label_end.grid(row=1, column=0, sticky='w')

entrada_end = customtkinter.CTkEntry(frame2, width=378, height=20)
entrada_end.grid(row=1, column=1, sticky='w', padx=10)

frame3 = customtkinter.CTkFrame(janela, fg_color="#242424", bg_color="#242424")
frame3.grid(row=2, column=0, padx=10, pady=10, sticky='w')

label_alt = customtkinter.CTkLabel(frame3, text="ALTURA:(XXX)", text_color="white")
label_alt.grid(row=2, column=0, sticky='w')

entrada_alt = customtkinter.CTkEntry(frame3, width=190, height=20)
entrada_alt.grid(row=2, column=1, sticky='w', padx=10)

frame4 = customtkinter.CTkFrame(janela, fg_color="#242424", bg_color="#242424")
frame4.grid(row=3, column=0, padx=10, pady=10, sticky='w')

label_peso = customtkinter.CTkLabel(frame4, text="PESO:(XX)", text_color="white")
label_peso.grid(row=3, column=0, sticky='w')

entrada_peso = customtkinter.CTkEntry(frame4, width=210, height=20)
entrada_peso.grid(row=3, column=1, sticky='w', padx=10)

# Botões
botao_processar = customtkinter.CTkButton(janela, text="CALCULAR", bg_color="#242424", fg_color="#263d76", command=calcular_imc)
botao_processar.grid(row=4, column=0, sticky='w', padx=20, pady=15)

botao_limpar = customtkinter.CTkButton(janela, text="LIMPAR", bg_color="#242424", fg_color="#263d76", command=limpar_resultado)
botao_limpar.grid(row=4, column=0, sticky='w', padx=179, pady=15)

botao_exibir_dados = customtkinter.CTkButton(janela, text="EXIBIR DADOS", bg_color="#242424", fg_color="#263d76", command=exibir_dados)
botao_exibir_dados.grid(row=4, column=0, sticky='w', padx=340, pady=15)

botao_sair = customtkinter.CTkButton(janela, text="SAIR", bg_color="#242424", fg_color="#263d76", command=sair)
botao_sair.grid(row=4, column=0, sticky='n', pady=15, padx=500)

# Posicionando o Label diretamente onde o novo_frame estava
resultado_label = customtkinter.CTkLabel(janela, text="", text_color="black", width=310, height=60)
resultado_label.grid(row=0, column=0, rowspan=7, sticky="w", padx=320)

# Iniciar o loop principal da interface gráfica
janela.mainloop()

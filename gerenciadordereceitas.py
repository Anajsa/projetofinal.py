import flet as ft
import sqlite3

# Configuração do banco de dados SQLite
def setup_database():
    conn = sqlite3.connect("receitas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            foto TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função principal
def main(page: ft.Page):
    # Configuração da página
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Gerenciador de Receitas"
    page.bgcolor = "#FCE4EC"  # Fundo rosa claro
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO  # Permite rolar se o conteúdo for grande

    # Função para adicionar receita ao banco de dados
    def adicionar_receita(e):
        if not titulo_input.value or not descricao_input.value or not foto_input.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Todos os campos são obrigatórios!"),
                open=True,
            )
            page.update()
            return

        conn = sqlite3.connect("receitas.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO receitas (titulo, descricao, foto) VALUES (?, ?, ?)",
            (titulo_input.value, descricao_input.value, foto_input.value),
        )
        conn.commit()
        conn.close()

        # Limpar os campos após adicionar
        titulo_input.value = ""
        descricao_input.value = ""
        foto_input.value = ""
        carregar_receitas()  # Atualiza a lista automaticamente
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Receita adicionada com sucesso!"),
            open=True,
        )
        page.update()

    # Função para carregar receitas do banco de dados
    def carregar_receitas():
        conn = sqlite3.connect("receitas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT titulo, descricao, foto FROM receitas")
        receitas = cursor.fetchall()
        conn.close()

        lista_receitas.controls.clear()  # Limpa a lista antes de recarregar
        for receita in receitas:
            lista_receitas.controls.append(
                ft.Card(
                    content=ft.Column(
                        [
                            ft.Text(f"Título: {receita[0]}", color="#880E4F", weight=ft.FontWeight.BOLD, size=18),
                            ft.Text(f"Descrição: {receita[1]}", color="#6A1B9A", size=16),
                            ft.Image(
                                src=receita[2],
                                width=300,
                                height=200,
                                fit=ft.ImageFit.COVER,
                            ),
                        ],
                        spacing=10,
                    ),
                    elevation=5,
                    color="#F8BBD0",  # Fundo rosa mais escuro nos cartões
                )
            )
        page.update()

    # Entradas para os dados da receita
    titulo_input = ft.TextField(label="Título da Receita", color="#880E4F", width=300)
    descricao_input = ft.TextField(label="Descrição", color="#880E4F", width=300)
    foto_input = ft.TextField(label="URL da Foto", color="#880E4F", width=300)

    # Botão para adicionar receita
    adicionar_btn = ft.ElevatedButton(
        "Adicionar Receita",
        on_click=adicionar_receita,
        color="#AD1457",
        
        width=200,
    )

    # Lista de receitas exibidas
    lista_receitas = ft.Column(spacing=20)

    # Layout da página
    page.add(
        ft.Column(
            [
                ft.Text("Gerenciador de Receitas", size=28, weight=ft.FontWeight.BOLD, color="#880E4F"),
                titulo_input,
                descricao_input,
                foto_input,
                adicionar_btn,
                ft.Divider(height=20, thickness=1, color="#880E4F"),  # Linha separadora
                lista_receitas,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # Carregar receitas ao iniciar a aplicação
    carregar_receitas()

# Configura o banco de dados e inicia o app
setup_database()
ft.app(target=main)

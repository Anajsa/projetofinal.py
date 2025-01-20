import flet as ft

# Função principal para criar o aplicativo
def main(page: ft.Page):
    page.title = "Gerenciador de Receitas"
    page.bgcolor = "#FCE4EC"  # Cor de fundo rosa claro
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Lista de receitas (inicialmente vazia)
    receitas = []

    # Função para adicionar nova receita
    def adicionar_receita(e):
        receita = {
            "titulo": titulo_input.value,
            "descricao": descricao_input.value,
            "foto": foto_input.value,
        }
        receitas.append(receita)
        atualizar_lista()

        # Limpar os campos de entrada após adicionar
        titulo_input.value = ""
        descricao_input.value = ""
        foto_input.value = ""
        page.update()

    # Função para editar uma receita
    def editar_receita(index):
        receita = receitas[index]
        titulo_input.value = receita["titulo"]
        descricao_input.value = receita["descricao"]
        foto_input.value = receita["foto"]
        salvar_btn.text = "Salvar Edições"
        salvar_btn.on_click = lambda e: salvar_edicoes(index)
        page.update()

    # Função para salvar as edições feitas na receita
    def salvar_edicoes(index):
        receitas[index] = {
            "titulo": titulo_input.value,
            "descricao": descricao_input.value,
            "foto": foto_input.value,
        }
        atualizar_lista()

        # Limpar os campos de entrada após salvar
        titulo_input.value = ""
        descricao_input.value = ""
        foto_input.value = ""
        salvar_btn.text = "Adicionar Receita"
        salvar_btn.on_click = lambda e: adicionar_receita(e)
        page.update()

    # Função para atualizar a lista de receitas exibidas
    def atualizar_lista():
        lista_receitas.controls.clear()
        for index, receita in enumerate(receitas):
            lista_receitas.controls.append(
                ft.Card(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"Titulo: {receita['titulo']}", weight=ft.FontWeight.BOLD, color="#F06292"),
                            ft.Text(f"Descrição: {receita['descricao']}", color="#9C27B0"),
                            ft.Image(
                                src=receita["foto"],
                                width=300,
                                height=200,
                                fit=ft.ImageFit.COVER,
                            ),
                            ft.Row(
                                controls=[
                                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, i=index: editar_receita(i), icon_color="#F06292"),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=10,
                    ),
                    elevation=5,
                    bgcolor="#F8BBD0",  # Cor de fundo rosa para o cartão
                )
            )
        page.update()

    # Entradas de texto para adicionar/editar receitas
    titulo_input = ft.TextField(label="Título da Receita", width=300)
    descricao_input = ft.TextField(label="Descrição", width=300)
    foto_input = ft.TextField(label="URL da Foto", width=300)

    # Botões para adicionar e salvar
    salvar_btn = ft.ElevatedButton("Adicionar Receita", on_click=adicionar_receita, width=200, bgcolor="#F06292", color="white")

    # Lista de receitas exibida
    lista_receitas = ft.Column(
        spacing=20,
        controls=[],
    )

    # Layout do formulário e da lista
    page.add(
        ft.Column(
            controls=[
                titulo_input,
                descricao_input,
                foto_input,
                salvar_btn,
                lista_receitas,
            ],
            spacing=30,
        )
    )

# Executa o aplicativo
ft.app(target=main)

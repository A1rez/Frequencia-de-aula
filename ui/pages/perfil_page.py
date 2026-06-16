import flet as ft


def perfil_page(
    page,
    aluno,
    mostrar_lista_alunos,
):
    def voltar(e):
        mostrar_lista_alunos(page)

    return ft.Column(
        controls=[
            ft.Text(
                aluno["nome"],
                size=24,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Divider(),

            ft.Text(f"ID: {aluno['id']}"),

            ft.Text(
                f"Status: {'Ativo' if aluno['ativo'] else 'Inativo'}"
            ),

            ft.Divider(),

            ft.Text("Idade: Em desenvolvimento"),

            ft.Text("Faixa: Em desenvolvimento"),

            ft.Text("Graus: Em desenvolvimento"),

            ft.Text("Data da última graduação: Em desenvolvimento"),

            ft.Text("Frequência atual: Em desenvolvimento"),

            ft.Text("Elegível para graduação: Em desenvolvimento"),

            ft.Text("Observações: Em desenvolvimento"),

            ft.Divider(),

            ft.Button(
                "Exibir Histórico de Presenças",
                disabled=True,
            ),

            ft.Button(
                "Editar Cadastro",
                disabled=True,
            ),

            ft.Button(
                "Voltar",
                on_click=voltar,
            ),
        ],
        spacing=15,
    )
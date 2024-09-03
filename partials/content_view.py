"""Visualiza todos os treinos na pagina de view."""
from time import sleep
import flet as ft
from partials.content_save import save_pdf


class View(ft.UserControl):
    """Classe principal."""
    def __init__(self, file_json):
        super().__init__()
        self.file_json = file_json

    def container_content(self):
        """Garante todos os dados json em containers separados."""
        containers = []

        for day, trainings in self.file_json.items():
            training_text = []

            for training, reps in trainings.items():
                training_text.append(
                    ft.Text(
                        spans=[
                            ft.TextSpan(
                                text=f"{training.upper()} ",
                                style=ft.TextStyle(
                                    color=ft.colors.ON_PRIMARY,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                            ft.TextSpan(
                                text=f" {reps}",
                                style=ft.TextStyle(
                                    color=ft.colors.PRIMARY,
                                    weight=ft.FontWeight.W_900
                                ),
                            ),
                        ]
                    )
                )

            container_day = ft.Container(
                padding=ft.padding.all(10),
                content=ft.ResponsiveRow(
                    controls=[
                        ft.Text(
                            value=day,
                            weight=ft.FontWeight.W_900,
                            color=ft.colors.PRIMARY,
                        ),
                        *training_text,
                        ft.Divider(color=ft.colors.PRIMARY),
                    ]
                ),
            )
            containers.append(container_day)

        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            controls=containers)

    def verify_save(self):
        """Exibir aviso de salvamento."""
        self.avise.controls[2].visible = True
        self.avise.controls[2].col = 12
        self.avise.update()

        action = save_pdf()

        self.avise.controls[2].visible = False
        self.avise.controls[2].col = 0
        self.avise.update()

        if action:
            # Exibir botão de sucesso
            self.avise.controls[0].visible = True
            self.avise.controls[1].visible = False
            self.avise.controls[0].col = 12
            self.avise.controls[1].col = 0
        else:
            # Exibir botão de erro
            self.avise.controls[0].visible = False
            self.avise.controls[1].visible = True
            self.avise.controls[0].col = 0
            self.avise.controls[1].col = 12

        # Atualiza a interface para refletir as mudanças
        self.avise.update()

        # Aguarda 1 segundo
        sleep(2)

        # Esconder ambos os botões
        self.avise.controls[0].visible = False
        self.avise.controls[1].visible = False

        # Atualiza a interface novamente
        self.avise.update()

    def build(self):

        self.avise = ft.ResponsiveRow(
            col=12,
            controls=[
                ft.TextButton(
                    col=0,
                    icon=ft.icons.DOWNLOAD_DONE,
                    icon_color=ft.colors.GREEN,
                    text="PDF salvo",
                    style=ft.ButtonStyle(
                        color=ft.colors.GREEN,
                    ),
                    disabled=True,
                    visible=False,
                ),
                ft.TextButton(
                    col=0,
                    icon=ft.icons.CANCEL,
                    icon_color=ft.colors.RED,
                    text="Erro ao salvar",
                    style=ft.ButtonStyle(
                        color=ft.colors.RED,
                    ),
                    disabled=True,
                    visible=False,
                ),
                ft.Text(
                    col=0,
                    value="BAIXANDO ...",
                    style=ft.TextStyle(
                        color=ft.colors.PRIMARY,
                    ),
                    weight=ft.FontWeight.W_500,
                    visible=False,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        )

        return ft.Container(
            ft.ResponsiveRow(
                controls=[
                    self.container_content(),
                    ft.IconButton(
                        icon=ft.icons.DOWNLOAD,
                        tooltip="Salvar em PDF",
                        on_click=lambda e: self.verify_save(),
                    ),
                    self.avise,
                ]
            ),
            bgcolor=ft.colors.BACKGROUND,
            padding=ft.padding.all(10),
        )

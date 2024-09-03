"""Módulo principal da aplicação"""

import json
from typing import Dict
import flet as ft
from partials.content_home import Home
from partials.content_edit import Edit
from partials.content_view import View


class FileJson:
    """Classe para o arquivo JSON"""

    def __init__(self) -> None:
        # Define o caminho do arquivo JSON e carrega o conteúdo se o arquivo
        # existir
        self.file_path = "training.json"
        self.file_json: Dict[str, Dict] = {
            "SEGUNDA-FEIRA": {},
            "TERÇA-FEIRA": {},
            "QUARTA-FEIRA": {},
            "QUINTA-FEIRA": {},
            "SEXTA-FEIRA": {},
            "SÁBADO": {},
            "DOMINGO": {},
        }
        self.load_json()

    def load_json(self) -> None:
        """Carrega o JSON do arquivo, se existir, ou cria o arquivo
        com o conteúdo padrão"""
        try:
            with open(self.file_path, "r", encoding="utf8") as file:
                self.file_json = json.load(file)
        except FileNotFoundError:
            with open(self.file_path, mode="w", encoding="utf8") as file:
                json.dump(self.file_json, file, ensure_ascii=False, indent=4)

    @property
    def read_json(self) -> Dict[str, Dict]:
        """Retorna o arquivo json."""
        return self.file_json


class AppTheme:
    """Classe para aplicar tema."""

    def __init__(self, dark_mode=False):
        self.dark_mode = dark_mode
        self.update_theme()

    def update_theme(self):
        """Atualizar o tema."""
        if self.dark_mode:
            self.theme = ft.Theme(
                color_scheme=ft.ColorScheme(
                    primary=ft.colors.BLUE_400,
                    on_primary=ft.colors.WHITE,
                    background=ft.colors.BLACK12,
                    on_background=ft.colors.BLACK87,
                    surface=ft.colors.GREY_800,
                    on_surface=ft.colors.LIGHT_BLUE_50,
                )
            )
        else:
            self.theme = ft.Theme(
                color_scheme=ft.ColorScheme(
                    primary=ft.colors.AMBER,
                    on_primary=ft.colors.BLACK,
                    background=ft.colors.WHITE70,
                    on_background=ft.colors.GREY_500,
                    surface=ft.colors.GREY_100,
                    on_surface=ft.colors.BLACK,
                )
            )


class App:
    """Classe principal de redenrização"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Treino Fácil"
        self.app_theme = AppTheme(dark_mode=False)
        self.page.theme = self.app_theme.theme
        self.page.bgcolor = ft.colors.BACKGROUND
        self.page.window_width = 450
        self.page.window_height = 650
        self.page.window_always_on_top = True
        self.page.appbar = ft.AppBar(
            bgcolor=ft.colors.BLACK,
            leading=ft.IconButton(
                icon=ft.icons.HOME,
                on_click=lambda e: self.change_content(e),
                icon_color=ft.colors.PRIMARY,
            ),
            actions=[
                ft.TextButton(
                    text="Editar Treinos",
                    icon=ft.icons.EDIT_ATTRIBUTES,
                    on_click=lambda e: self.change_content(e),
                ),
                ft.TextButton(
                    text="Visualizar Treino",
                    icon=ft.icons.VIEW_COLUMN_OUTLINED,
                    on_click=lambda e: self.change_content(e),
                ),
                ft.IconButton(
                    icon=(
                        ft.icons.DARK_MODE
                        if not self.app_theme.dark_mode
                        else ft.icons.LIGHT_MODE
                    ),
                    on_click=lambda e: self.toggle_theme(e),
                ),
            ],
        )
        self.file_json = FileJson().read_json
        self.home = ft.Container(content=Home(file_json=self.file_json))
        self.main()

    def toggle_theme(self, e=None):
        """Função para mudar o tema."""
        self.app_theme.dark_mode = not self.app_theme.dark_mode
        self.app_theme.update_theme()
        self.page.theme = self.app_theme.theme
        self.page.appbar.actions[-1].icon = ft.icons.DARK_MODE if not self.app_theme.dark_mode else ft.icons.LIGHT_MODE  # type: ignore
        self.page.update()

    def change_content(self, e=None):
        """Função para mudar o conteúdo."""
        try:
            text = e.control.text.upper()  # type: ignore
        except AttributeError:
            text = e.control.icon.upper()  # type: ignore

        if text == "HOME":
            self.home.content = Home(self.file_json)
        elif text == "EDITAR TREINOS":
            self.home.content = Edit(self.file_json)
        elif text == "VISUALIZAR TREINO":
            self.home.content = View(self.file_json)

        self.page.update()

    def main(self):
        """Função principal."""
        self.layout = ft.Container(
            expand=True,
            bgcolor=ft.colors.BACKGROUND,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    self.home,
                    ft.ResponsiveRow(
                        col=12,
                        controls=[
                            ft.Text(
                                col=6,
                                value="© Todos os direitos reservados. Anderson Gabriel Pereira Cruz 2024.",
                                color=ft.colors.PRIMARY,
                            ),
                            ft.Row(
                                col=6,
                                controls=[
                                    ft.TextButton(
                                        col=6,
                                        text="andersong.pereiracruz@gmail.com",
                                        style=ft.ButtonStyle(
                                            color=ft.colors.PRIMARY,
                                        ),
                                        url="mailto:andersong.pereiracruz@gmail.com",
                                    ),
                                    ft.IconButton(
                                        content=ft.Image(
                                            src="icons/git_hub.png",
                                            height=20,
                                            color=ft.colors.PRIMARY,
                                        )
                                    ),
                                    ft.IconButton(
                                        content=ft.Image(
                                            src="icons/instagram.png",
                                            height=20,
                                            color=ft.colors.PRIMARY,
                                        )
                                    ),
                                ],
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
        )
        self.page.add(self.layout)


if __name__ == "__main__":
    ft.app(target=App, assets_dir="assets")

import flet as ft
from partials.content_home import Home
from partials.content_edit import Edit
from partials.content_view import View

class Dict:
    def __init__(self):
        self.training = {
            "SEGUNDA-FEIRA": {
                "SUPINO INCLINADO": "4x8",
                "PULL-UP": "4x8",
                "AGACHAMENTO": "4x10",
                "DESENVOLVIMENTO MILITAR": "4x8",
                "ABDOMINAL": "3x15"
            },
            "TERÇA-FEIRA": {
                "PESOS LIVRES": "4x8",
                "REMADA CURVADA": "4x10",
                "LEG PRESS": "4x12",
                "EXTENSÃO DE TRÍCEPS": "4x10",
                "CRUNCH": "3x20"
            },
            "QUARTA-FEIRA": {
                "BENCH PRESS": "4x8",
                "PULL-DOWN": "4x8",
                "AFUNDO": "4x10",
                "ROSCA DIRETA": "4x12",
                "ABDOMINAL INVERTIDO": "3x15"
            },
            "QUINTA-FEIRA": {
                "DEADLIFT": "4x8",
                "MACHINE ROW": "4x10",
                "LEG CURL": "4x12",
                "FLEXÃO DE BRAÇO": "4x8",
                "PLANK": "3x1min"
            },
            "SEXTA-FEIRA": {
                "PUSH PRESS": "4x8",
                "BARBELL CURL": "4x10",
                "GORDURA NO GLÚTEO": "4x12",
                "TRÍCEPS NA CORDA": "4x10",
                "ABDOMINAL OBLIQUO": "3x15"
            },
            "SÁBADO": {
                "SUPINO RETO": "4x8",
                "PULL-UP": "4x8",
                "AGACHAMENTO": "4x10",
                "FLEXÃO DE BRAÇO": "4x8",
                "ABDOMINAL BICICLETA": "3x20"
            },
            "DOMINGO": {}
        }

    @property
    def read_dict(self):
        return self.training

class AppTheme:
    def __init__(self, dark_mode=False):
        self.dark_mode = dark_mode
        self.update_theme()

    def update_theme(self):
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
                icon_color=ft.colors.PRIMARY
            ),
            actions=[
                ft.TextButton(
                    text="Editar Treinos",
                    icon=ft.icons.EDIT_ATTRIBUTES,
                    on_click=lambda e: self.change_content(e)
                ),
                ft.TextButton(
                    text="Visualizar Treino",
                    icon=ft.icons.VIEW_COLUMN_OUTLINED,
                    on_click=lambda e: self.change_content(e)
                ),
                ft.IconButton(
                    icon=ft.icons.DARK_MODE if not self.app_theme.dark_mode else ft.icons.LIGHT_MODE,
                    on_click=lambda e: self.toggle_theme(e)
                )
            ]

        )
        self.dict = Dict().read_dict
        self.home = ft.Container(
            content=Home(dict=self.dict)
        )
        self.main()

    def toggle_theme(self, e=None):
        self.app_theme.dark_mode = not self.app_theme.dark_mode
        self.app_theme.update_theme()
        self.page.theme = self.app_theme.theme
        self.page.appbar.actions[-1].icon = ft.icons.DARK_MODE if not self.app_theme.dark_mode else ft.icons.LIGHT_MODE
        self.page.update()

    def change_content(self, e=None):
        try:
            text = e.control.text.upper()
        except AttributeError:
            text = e.control.icon.upper()

        if text == "HOME":
            self.home.content = Home(self.dict)
        elif text == "EDITAR TREINOS":
            self.home.content = Edit(self.dict)
        elif text == "VISUALIZAR TREINO":
            self.home.content = View(self.dict)
        
        self.page.update()

    def main(self):

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
                                    color=ft.colors.PRIMARY,),                  
                            ft.Row(
                                col=6,
                                controls=[
                                    ft.TextButton(
                                        col=6,
                                        text="andersong.pereiracruz@gmail.com",
                                        style=ft.ButtonStyle(color=ft.colors.PRIMARY,),
                                        url="mailto:andersong.pereiracruz@gmail.com"
                                        ),
                                    ft.IconButton(
                                        content=ft.Image(src="icons/git_hub.png", height=20, color=ft.colors.PRIMARY,)
                                    ),
                                    ft.IconButton(
                                        content=ft.Image(src="icons/instagram.png", height=20, color=ft.colors.PRIMARY,)
                                    )
                                ]
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                ]
            )
        )
        self.page.add(self.layout)
        
if __name__ == "__main__":
    ft.app(target=App, assets_dir="assets")

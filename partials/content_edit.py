import flet as ft
from time import sleep
import json

class Edit(ft.UserControl):
    def __init__(self, file_json):
        super().__init__()
        self.file_json = file_json 
        self.frame = ft.Container() # Content a ser atualizado conforme o dropdown
        self.fields = [] # Armazenamento dos textos
        self.day = None

    def show_content(self, e):
        self.day = e.control.text

        self.style = ft.TextStyle(
            color=ft.colors.ON_PRIMARY,
            weight=ft.FontWeight.W_500,
            size=16,
        )
        self.label = ft.TextStyle(
            color=ft.colors.PRIMARY,
            weight=ft.FontWeight.W_900,
            size=12,
            
        )

        if self.day in self.file_json:
        
            self.fields = []

            for treino, repeticoes in self.file_json[self.day].items():
                text_field = ft.ResponsiveRow(
                    col=12,
                    controls=[
                        ft.TextField(
                            col={'xs': 9, 'md': 11},
                            value=f"{treino.title()}",
                            border=ft.InputBorder.UNDERLINE,
                            text_style=self.style,
                            label="Treino",
                            label_style=self.label,
                            selection_color=ft.colors.PRIMARY,
                            cursor_color=ft.colors.PRIMARY,
                        ),
                        ft.TextField(
                            col={'xs': 3, 'md': 1},
                            value=str(repeticoes),
                            border=ft.InputBorder.UNDERLINE,
                            text_style=self.style,
                            label="Repetições",
                            label_style=self.label,
                            selection_color=ft.colors.PRIMARY,
                            cursor_color=ft.colors.PRIMARY
                        )
                    ]
                )
                self.fields.append(text_field)

            self.frame.content = ft.Column(
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=self.fields  # Passa os campos para o frame
            )
            self.update()

    def save_json(self, e=None):
        try:
            if self.day:
                new_data = {} # Dict de novas informações
                for field in self.fields:
                    treino_field = field.controls[0]
                    repeticoes_field = field.controls[1]
                    treino = treino_field.value.strip().lower()
                    repeticoes = repeticoes_field.value.strip()

                    if not repeticoes:
                        repeticoes = "4x8"

                    if treino and repeticoes:
                        new_data[treino] = repeticoes

                self.file_json[self.day] = new_data

                self.buttons_alert.content.controls[0].visible = True
                self.buttons_alert.content.controls[1].visible = False

                # Salva o JSON atualizado
                with open("training.json", "w", encoding="utf8") as file:
                    json.dump(self.file_json, file, ensure_ascii=False, indent=4)

                self.buttons_alert.content.controls[0].visible = True
                self.buttons_alert.content.controls[1].visible = False

        except Exception as ex: 
                self.buttons_alert.content.controls[0].visible = False
                self.buttons_alert.content.controls[1].visible = True 

        finally:

            self.update()

            sleep(2)
            self.buttons_alert.content.controls[0].visible = False
            self.buttons_alert.content.controls[1].visible = False
            self.update() 

    def create_field(self, e=None):
        new_field = ft.ResponsiveRow(
            col=12,
            controls=[
                ft.TextField(
                    col={'xs': 9, 'md': 11},
                    value="",
                    border=ft.InputBorder.UNDERLINE,
                    text_style=self.style,
                    label="Treino",
                    label_style=self.label,
                    selection_color=ft.colors.PRIMARY,
                    cursor_color=ft.colors.ON_PRIMARY
                ),
                ft.TextField(
                    col={'xs': 3, 'md': 1},
                    value="",
                    border=ft.InputBorder.UNDERLINE,
                    text_style=self.style,
                    label="Repetições",
                    label_style=self.label,
                    selection_color=ft.colors.ON_PRIMARY,
                    cursor_color=ft.colors.ON_PRIMARY
                )
            ]
        )
        self.fields.append(new_field)

        self.frame.content = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=self.fields
        )
        self.update()

    def delete_fields(self, e=None):
        for field in self.fields:
            field.controls[0].value = ""
            field.controls[1].value = ""
            self.update()

    def build(self):

        self.buttons_alert = ft.Container(
                        content=ft.ResponsiveRow(
                            col=12,
                            controls=[
                                ft.TextButton(
                                    col=6,
                                    icon=ft.icons.UPLOAD,
                                    icon_color=ft.colors.GREEN,
                                    text="Sucesso ao salvar",
                                    style=ft.ButtonStyle(color=ft.colors.GREEN,),
                                    disabled=True,
                                    visible=False,
                                ),
                                ft.TextButton(
                                    col=6,
                                    icon=ft.icons.CANCEL,
                                    icon_color=ft.colors.RED,
                                    text="Error ao salvar",
                                    style=ft.ButtonStyle(color=ft.colors.RED,),
                                    disabled=True,
                                    visible=False
                                )
                            ]
                        )
                    )

        self.button_style = ft.ButtonStyle(
            color={
                ft.MaterialState.DEFAULT: ft.colors.PRIMARY,
                ft.MaterialState.HOVERED: ft.colors.ON_PRIMARY,
                ft.MaterialState.FOCUSED: ft.colors.ON_PRIMARY,
                ft.MaterialState.PRESSED: ft.colors.ON_PRIMARY,
                ft.MaterialState.SELECTED: ft.colors.ON_PRIMARY
            },
            bgcolor={
                ft.MaterialState.DEFAULT: ft.colors.BACKGROUND,
                ft.MaterialState.HOVERED: ft.colors.PRIMARY,
                ft.MaterialState.FOCUSED: ft.colors.PRIMARY,
                ft.MaterialState.PRESSED: ft.colors.PRIMARY,
                ft.MaterialState.SELECTED: ft.colors.PRIMARY
            },
            animation_duration=1000,
        )
        
        return ft.Container(
            margin=ft.margin.all(10),
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Dropdown(
                        options=[
                            ft.dropdown.Option(
                                text=days,
                                on_click=lambda e: self.show_content(e),
                            ) for days in self.file_json.keys()
                        ],
                        label="Dia",
                        bgcolor=ft.colors.ON_BACKGROUND,
                        label_style=ft.TextStyle(
                            color=ft.colors.PRIMARY,
                            weight=ft.FontWeight.BOLD,
                        ),
                        text_style=ft.TextStyle(
                            color=ft.colors.PRIMARY,
                            weight=ft.FontWeight.BOLD,
                        )
                    ),
                    self.buttons_alert,
                    self.frame,
                    ft.Divider(color=ft.colors.PRIMARY),
                    ft.ResponsiveRow(
                        controls=[
                            ft.IconButton(icon=ft.icons.SAVE, style=self.button_style, col=5, on_click=self.save_json),
                            ft.IconButton(icon=ft.icons.ADD, style=self.button_style, col=5, on_click=self.create_field),
                            ft.IconButton(icon=ft.icons.DELETE, style=self.button_style, col=2, on_click=self.delete_fields)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ],
            )
        )

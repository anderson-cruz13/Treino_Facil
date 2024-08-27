import flet as ft
from datetime import datetime


def week():
    day = datetime.now()

    day_week = {
        0: "SEGUNDA-FEIRA",
        1: "TERÇA-FEIRA",
        2: "QUARTA-FEIRA",
        3: "QUINTA-FEIRA",
        4: "SEXTA-FEIRA",
        5: "SÁBADO",
        6: "DOMINGO",
    }

    return day_week[day.weekday()]

class Home(ft.UserControl):
    def __init__(self, dict):
        super().__init__()
        self.dict = dict
        self.day = week()
    
    def training_day(self):
        texts_training = []

        for values in self.dict[self.day].items():
            texts_training.append(
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            text=f"{values[0].upper()} ",
                            style=ft.TextStyle(
                                color=ft.colors.ON_PRIMARY,
                                weight=ft.FontWeight.BOLD,
                            )
                        ),
                        ft.TextSpan(
                            text=f" {values[1]}",
                            style=ft.TextStyle(
                                color=ft.colors.PRIMARY,
                                weight=ft.FontWeight.W_900
                            )
                        )
                    ]
                )
            )
        

        training = ft.Column(
            controls=[
                *texts_training
            ]
        )

        return ft.Container(
            expand=True,
            bgcolor=ft.colors.BACKGROUND,
            margin=ft.margin.all(20),
            padding=ft.padding.all(10),
            opacity=0.7,
            content=ft.Column(
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value=self.day,
                        size=16,
                        color=ft.colors.PRIMARY,
                        weight=ft.FontWeight.W_900
                    ),
                    ft.Divider(color=ft.colors.SECONDARY),
                    training
                ]
            )
        )

    def build(self):
        return ft.Container(
            padding=10,
            expand=True,
            content=ft.Stack(
                alignment=ft.Alignment(0, -1),
                controls=[
                    self.training_day(),
                    ft.Image(
                        src="images/logo.png",
                        opacity=0.1,
                    ),
                ]
            )
        )
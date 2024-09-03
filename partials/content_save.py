"""Módulo que gerencia o salvamento dos treinos em PDF."""
from os import path, environ
from json import load
from platform import system
from fpdf import FPDF


class PDF(FPDF):
    """Classe principal."""
    def header(self):
        # Adicionar imagem ao lado do título
        self.image("assets/icon.png", x=10, y=5, w=20)

        # Adicionar título
        self.set_font(family="Arial", style="B", size=18)
        self.cell(w=30)  # Espaço para a imagem
        self.cell(w=0, h=10, txt="Treino", border=0, align="L")
        self.ln(10)  # Espaço pós cabeçalho

        # Linha
        self.set_xy(x=10, y=20)
        self.set_line_width(width=1)
        self.cell(w=0, h=0, txt="", border="T", align="C")
        self.ln(10)  # Adiciona espaço após a linha

    def chapter_title(self, title: str) -> None:
        """Função para gerar o título do PDF."""
        self.set_font(family="Arial", style="B", size=14)
        self.cell(w=0, h=10, txt=title, border=1, align="C")
        self.ln(15)

    def chapter_body(self, body: list) -> None:
        """Função que gera o corpo."""
        self.set_font(family="Arial", style="", size=12)
        for exercise, rep in body:
            self.cell(w=90, h=6, txt=f"{exercise.upper()} ", ln=0)
            self.set_font(
                family="Arial", style="B", size=12
            )  # Texto em negrito para repetições
            self.cell(w=0, h=6, txt=rep, ln=1)
            self.set_font(
                family="Arial", style="", size=12
            )  # Volta ao estilo normal para o próximo exercício
        self.ln()


def save_pdf() -> bool:
    """Salva o PDF."""
    # Criar PDF e adicionar conteúdo
    pdf = PDF()
    pdf.add_page()

    with open(file="training.json", mode="r", encoding="utf8") as file:
        training = load(file)

    for day, trainings in training.items():
        if trainings:
            pdf.chapter_title(day)
            body = [(exercise, rep) for exercise, rep in trainings.items()]
            pdf.chapter_body(body=body)

    # Verifica se o sistema é Android
    if system() == "Linux" and "ANDROID_STORAGE" in environ:
        DOWNLOADS_PATH = "/storage/emulated/0/Download"
        PDF_FILE_PATH = path.join(DOWNLOADS_PATH, "treino.pdf")
    else:
        DESKTOP_PATH = path.join(path.expanduser("~"), "Desktop")
        PDF_FILE_PATH = path.join(DESKTOP_PATH, "treino.pdf")

    pdf.output(PDF_FILE_PATH)
    return True

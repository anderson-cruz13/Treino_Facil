from fpdf import FPDF
from os import path, environ
from platform import system

training = {
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

class PDF(FPDF):
    def header(self):
        # Adicionar imagem ao lado do título
        self.image('assets/icon.png', x=10, y=5, w=20) 
        
        # Adicionar título
        self.set_font(family="Arial", style='B', size=18)
        self.cell(w=30)  # Espaço para a imagem
        self.cell(w=0, h=10, txt='Treino padrão não modificado', border=0, align='L')
        self.ln(10)  # Espaço pós cabeçalho

        #Linha
        self.set_xy(x=10, y=20)  
        self.set_line_width(width=1)  
        self.cell(w=0, h=0, txt='', border='T', align='C')  
        self.ln(10)  # Adiciona espaço após a linha

    def chapter_title(self, title: str) -> None:
        self.set_font(family="Arial", style="B", size=14)
        self.cell(w=0, h=10, txt=title, border=1, align='C')
        self.ln(15)

    def chapter_body(self, body: list) -> None:
        self.set_font(family="Arial", style="", size=12)
        for exercise, rep in body:
            self.cell(w=90, h=6, txt=f"{exercise.upper()} ", ln=0)
            self.set_font(family="Arial", style="B", size=12)  # Texto em negrito para repetições
            self.cell(w=0, h=6, txt=rep, ln=1)
            self.set_font(family="Arial", style="", size=12)  # Volta ao estilo normal para o próximo exercício
        self.ln()

def save_pdf() -> bool:
    # Criar PDF e adicionar conteúdo
    pdf = PDF()
    pdf.add_page()

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


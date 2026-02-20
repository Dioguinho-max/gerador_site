from flask import Flask, render_template, request
import secrets
import string

app = Flask(__name__)

def gerar_senha(tamanho):
    letras = string.ascii_letters
    numeros = string.digits
    simbolos = string.punctuation

    # Garante pelo menos 1 letra, 1 número e 1 símbolo
    senha = [
        secrets.choice(letras),
        secrets.choice(numeros),
        secrets.choice(simbolos)
    ]

    todos = letras + numeros + simbolos

    for _ in range(tamanho - 3):
        senha.append(secrets.choice(todos))

    secrets.SystemRandom().shuffle(senha)
    return ''.join(senha)

def verificar_forca(senha):
    pontos = 0
    if len(senha) >= 8:
        pontos += 1
    if any(c.isdigit() for c in senha):
        pontos += 1
    if any(c in string.punctuation for c in senha):
        pontos += 1
    if any(c.isupper() for c in senha):
        pontos += 1

    niveis = ["Fraca ❌", "Média ⚠️", "Boa 👍", "Forte 🔥"]
    return niveis[pontos-1]

@app.route("/", methods=["GET", "POST"])
def index():
    senha = None
    forca = None

    if request.method == "POST":
        dificuldade = request.form["dificuldade"]

        # Define tamanho com base na dificuldade
        if dificuldade == "facil":
            tamanho = 6
        elif dificuldade == "media":
            tamanho = 10
        elif dificuldade == "dificil":
            tamanho = 14
        elif dificuldade == "muito_dificil":
            tamanho = 20
        else:
            tamanho = 10

        senha = gerar_senha(tamanho)
        forca = verificar_forca(senha)

    return render_template("index.html", senha=senha, forca=forca)

if __name__ == "__main__":
    app.run(debug=True)

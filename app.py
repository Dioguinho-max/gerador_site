from flask import Flask, render_template, request, send_file
import secrets
import string
import io
import urllib.parse

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
        tamanho = int(request.form["tamanho"])
        senha = gerar_senha(tamanho)
        forca = verificar_forca(senha)

    return render_template("index.html", senha=senha, forca=forca)

@app.route("/download")
def download():
    senha = request.args.get("senha")
    if not senha:
        return "Nenhuma senha para baixar!", 400

    # Cria arquivo em memória
    buffer = io.BytesIO()
    buffer.write(senha.encode("utf-8"))
    buffer.seek(0)

    # Encode no nome do arquivo para não quebrar com caracteres especiais
    filename = urllib.parse.quote("senha.txt")

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(debug=True)
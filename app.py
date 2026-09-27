   from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Curso Correto do G & LJ</title>
    </head>
    <body>
        <h1>Curso Correto do G & LJ</h1>
        <p>Bem-vindo ao nosso espaço de cursos técnicos.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
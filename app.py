from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "curso-correto-g-lj-change-this-key"
DB = "curso_correto.db"

COURSES = [
    ("Construção Civil", "Construção e Engenharia", "Fundamentos de construção, materiais, leitura de projetos e segurança."),
    ("Desenho Técnico", "Construção e Engenharia", "Leitura, interpretação e criação de desenhos técnicos."),
    ("Desenho e Projeto", "Construção e Engenharia", "Princípios de projeto, plantas e documentação técnica."),
    ("Topografia", "Construção e Engenharia", "Medição, representação e noções de levantamento de terrenos."),
    ("Arquitetura", "Construção e Engenharia", "Introdução ao projeto arquitetónico e organização de espaços."),
    ("Informática Básica", "Informática e Tecnologia", "Computador, internet, documentos, folhas de cálculo e segurança digital."),
    ("Programação", "Informática e Tecnologia", "Lógica de programação e desenvolvimento de aplicações."),
    ("Desenvolvimento Web", "Informática e Tecnologia", "HTML, CSS, JavaScript e fundamentos de aplicações web."),
    ("Redes de Computadores", "Informática e Tecnologia", "Conceitos de redes, equipamentos, endereçamento e configuração."),
    ("Cibersegurança", "Informática e Tecnologia", "Boas práticas de segurança, proteção de contas e dados."),
    ("Banco de Dados", "Informática e Tecnologia", "Modelação, SQL e organização de dados."),
    ("Design Gráfico", "Informática e Tecnologia", "Princípios de composição, tipografia e criação visual."),
    ("Eletricidade Geral", "Eletricidade e Eletrónica", "Fundamentos de circuitos, componentes e segurança elétrica."),
    ("Eletrónica", "Eletricidade e Eletrónica", "Componentes eletrónicos e princípios de circuitos."),
    ("Automação", "Eletricidade e Eletrónica", "Introdução ao controlo e automação de processos."),
    ("Energia Solar", "Eletricidade e Eletrónica", "Fundamentos de sistemas fotovoltaicos e eficiência energética."),
    ("Mecânica Automóvel", "Mecânica", "Fundamentos de manutenção e sistemas de veículos."),
    ("Mecatrónica", "Mecânica", "Integração de mecânica, eletrónica e automação."),
    ("Soldadura", "Mecânica", "Fundamentos, segurança e técnicas de soldadura."),
    ("Contabilidade", "Administração e Negócios", "Princípios de contabilidade e organização financeira."),
    ("Gestão", "Administração e Negócios", "Fundamentos de gestão e organização."),
    ("Marketing", "Administração e Negócios", "Estratégias de comunicação, marca e divulgação."),
    ("Empreendedorismo", "Administração e Negócios", "Ideias, modelos de negócio e planeamento."),
    ("Enfermagem", "Saúde", "Fundamentos introdutórios e práticas de cuidados de saúde."),
    ("Farmácia", "Saúde", "Noções introdutórias sobre medicamentos e assistência farmacêutica."),
    ("Primeiros Socorros", "Saúde", "Resposta inicial e segura em situações de emergência."),
    ("Hotelaria", "Hotelaria e Serviços", "Fundamentos de atendimento e operações hoteleiras."),
    ("Turismo", "Hotelaria e Serviços", "Introdução ao turismo, atendimento e organização de serviços."),
    ("Cozinha e Pastelaria", "Hotelaria e Serviços", "Técnicas básicas, higiene e organização de cozinha."),
    ("Agricultura", "Outras Áreas", "Fundamentos de produção agrícola e boas práticas."),
    ("Segurança no Trabalho", "Outras Áreas", "Prevenção de riscos e cultura de segurança."),
]

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course TEXT NOT NULL,
        UNIQUE(user_id, course)
    )""")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    categories = sorted(set(c[1] for c in COURSES))
    return render_template("index.html", courses=COURSES, categories=categories)

@app.route("/cursos")
def courses():
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    result = COURSES
    if q:
        result = [c for c in result if q in c[0].lower() or q in c[1].lower()]
    if category:
        result = [c for c in result if c[1] == category]
    categories = sorted(set(c[1] for c in COURSES))
    return render_template("courses.html", courses=result, categories=categories, q=q, selected=category)

@app.route("/curso/<name>")
def course_detail(name):
    course = next((c for c in COURSES if c[0] == name), None)
    if not course:
        return "Curso não encontrado", 404
    return render_template("course.html", course=course)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        if not name or not email or len(password) < 6:
            flash("Preencha todos os campos. A senha deve ter pelo menos 6 caracteres.")
            return redirect(url_for("register"))
        try:
            conn = db()
            conn.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",
                         (name, email, generate_password_hash(password)))
            conn.commit()
            conn.close()
            flash("Conta criada com sucesso. Agora podes entrar.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Este email já está registado.")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        conn = db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
          conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Login efetuado com sucesso.")
            return redirect(url_for("home"))

        flash("Email ou senha incorretos.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sessão terminada.")
    return redirect(url_for("home"))


@app.route("/inscrever/<name>", methods=["POST"])
def enroll(name):
    if "user_id" not in session:
        flash("Entra na tua conta para te inscreveres no curso.")
        return redirect(url_for("login"))

    course = next((c for c in COURSES if c[0] == name), None)

    if not course:
        return "Curso não encontrado", 404

    conn = db()
    conn.execute(
        "INSERT OR IGNORE INTO enrollments(user_id, course) VALUES(?, ?)",
        (session["user_id"], course[0])
    )
    conn.commit()
    conn.close()

    flash("Inscrição realizada com sucesso!")
    return redirect(url_for("course_detail", name=name))


@app.route("/meus-cursos")
def my_courses():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = db()
    enrollments = conn.execute(
        "SELECT course FROM enrollments WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("my_courses.html", enrollments=enrollments)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)     
from flask import Flask, request, render_template, redirect, session, url_for
import sqlite3
import bleach
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session


# Crear app Flask y configurar sesión segura
app = Flask(__name__)
app.config['SECRET_KEY'] = 'una_clave_secreta_segura'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


# Crear tabla de usuarios si no existe
with sqlite3.connect("users.db") as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 🛡 Sanitización contra XSS
        name = bleach.clean(request.form.get("name"))
        email = bleach.clean(request.form.get("email"))
        password = request.form.get("password")

        # Validación
        if not all([name, email, password]):
            errores = ["Todos los campos son requeridos"]
            return render_template("register.html", errores=errores, name=name, email=email, password=password)


        # 🔐 Hasheo seguro de contraseña
        hashed_pw = generate_password_hash(password)

        try:
            with sqlite3.connect("users.db") as conn:
                # ✅ Consulta parametrizada contra SQL Injection
                conn.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name_pw, email_pw, hashed_pw)
                )
                conn.commit()
                return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "El correo ya está registrado", 400

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = bleach.clean(request.form.get("email"))
        password = request.form.get("password")

        with sqlite3.connect("users.db") as conn:
            user = conn.execute("SELECT id, password FROM users WHERE email = ?", (email,)).fetchone()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]  # ✅ Sesión segura con ID de usuario
            return redirect(url_for("dashboard"))

        return "Credenciales inválidas", 401

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return "Bienvenido a tu panel protegido"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)


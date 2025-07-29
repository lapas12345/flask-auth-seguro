# 🛡️ Aplicación Flask Segura

Este proyecto es una aplicación web sencilla desarrollada con Flask que permite el **registro**, **inicio de sesión** y el acceso a una **página protegida**. Además, incorpora medidas básicas de seguridad para prevenir ataques comunes como **inyección SQL**, **XSS** y mal manejo de contraseñas o sesiones.

---

## 🚀 Funcionalidades

- Registro de usuario con nombre, correo y contraseña.
- Inicio de sesión con verificación de credenciales.
- Página protegida accesible solo a usuarios autenticados.
- Cierre de sesión.
- Creación automática de la base de datos `users.db` si no existe.

---

## 🔐 Medidas de seguridad implementadas

| Tipo de amenaza       | Protección usada                                      | Librería |
|-----------------------|--------------------------------------------------------|----------|
| Inyección SQL         | Uso de **consultas parametrizadas** (`?`)              | sqlite3  |
| XSS (Cross-Site Scripting) | Sanitización de entradas del usuario con `bleach.clean()` | bleach   |
| Robo o fuga de contraseñas | Hasheo con `generate_password_hash()`               | werkzeug |
| Hijacking de sesión   | Sesiones protegidas con `Flask-Session` y `SECRET_KEY` | flask-session |

---

## ⚙️ Requisitos

- Python 3.8+
- Flask
- Flask-Session
- Bleach
- Werkzeug

Instalación de dependencias:

```bash
python -m pip install flask flask-session bleach

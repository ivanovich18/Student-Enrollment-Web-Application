from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///students.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/deregister", methods=["POST"])
def deregister():

    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM records WHERE id_number = ?", id)
    return redirect("/table")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        id_number = request.form.get("id_number")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birthday = request.form.get("birthday")
        gender = request.form.getlist("gender")
        student_type = request.form.getlist("type")
        address = request.form.get("address")
        department = request.form.getlist("department")
        program = request.form.get("program")

        if not id_number or not first_name or not last_name or not birthday or not gender or not student_type or not address or not department or not program:
            return redirect("/")

        db.execute("INSERT INTO records (id_number, first_name, last_name, birthday, gender, student_type, address, department, program) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   id_number, first_name, last_name, birthday, gender, student_type, address, department, program)

        return redirect("/")

    else:
        return render_template("index.html")


@app.route("/table", methods=["GET", "POST"])
def table():
    if request.method == "GET":
        records = db.execute("SELECT * FROM records")
        return render_template("table.html", records=records)

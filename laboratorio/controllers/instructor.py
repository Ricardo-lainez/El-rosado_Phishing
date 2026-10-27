from flask import Blueprint, abort, current_app, render_template, request

instructor = Blueprint("instructor", __name__)


@instructor.get("/instructor")
@instructor.get("/admin")
def dashboard():
    if request.remote_addr not in ("127.0.0.1", "::1"):
        abort(403)
    rows, totals = current_app.extensions["eventos"].dashboard()
    beneficios_rows, beneficios_total = current_app.extensions["eventos"].dashboard_beneficios()
    return render_template("instructor.html", rows=rows, totals=totals,
                           beneficios_rows=beneficios_rows, beneficios_total=beneficios_total)


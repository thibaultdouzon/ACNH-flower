from app import app

from flask import render_template, request

@app.route("/", methods=["GET"])
def index():
    flower_types = [
        {"name": "Cosmos"},
        {"name": "Roses"},
        ]
    
    flower_colors = [
        {"name": "Red"},
        {"name": "Green"},
    ]
    
    return render_template("form.html", title="Home", flower_types=flower_types, flower_colors=flower_colors)

@app.route("/results", methods=["POST"])
def result_page():
    form = request.form
    
    tgt_type = form["tgt_type"]
    tgt_color = form["tgt_color"]
    seed = True if "seed" in form else False
    island = True if "island" in form else False
    
    return f"{tgt_type=} {tgt_color=} {seed=} {island=}"







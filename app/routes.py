from app import app

from flask import render_template

@app.route("/")

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









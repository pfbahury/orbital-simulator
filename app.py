from flask import Flask, jsonify, render_template
import numpy as np
from orbita import calcular_orbita, AU

app = Flask(__name__)


@app.route("/")
def index():
    # vai carregar um template com o espaço pro gráfico
    return render_template("index.html")

@app.route("/orbita")
def orbita():
    a = 17.8 * AU
    e = 0.967
    x, y = calcular_orbita(a, e, n_points=400, theta0=3)

    data = {
        "a": a,
        "e": e,
        "frames": [{"x": x[i], "y": y[i]} for i in range(len(x))]
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

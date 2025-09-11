from flask import Flask, jsonify, render_template, request
import numpy as np
from orbita import calcular_orbita, AU, M_S

app = Flask(__name__)


@app.route("/")
def index():
    # vai carregar um template com o espaço pro gráfico
    return render_template("index.html")

@app.route("/orbita")
def orbita():
    try:
        # Pega os parâmetros da query string
        massa = request.args.get("massaCorporal", type=float, default=M_S)
        e = request.args.get("excentricidade", type=float, default=0.967)
        a = request.args.get("semieixo", type=float, default=17.8) * AU
        theta0 = request.args.get("angulo", type=float, default=0)
        n_points = request.args.get("numPontos", type=int, default=300)

        # Calcula a órbita
        x, y = calcular_orbita(a, e, theta0, n_points)

        data = {
            "massa": massa,
            "a": a,
            "e": e,
            "theta0": theta0,
            "frames": [{"x": x[i], "y": y[i]} for i in range(len(x))]
        }
        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 400

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, render_template, request
import numpy as np
from orbita import calcular_orbita, AU, M_S, calcular_velocidades
import webbrowser
import threading
import time
import sys
import os

app = Flask(__name__)

# Fix for PyInstaller to find templates and static files
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/orbita")
def orbita():
    try:
        massa = request.args.get("massaCorporal", type=float, default=M_S)
        e = request.args.get("excentricidade", type=float, default=0.967)
        a = request.args.get("semieixo", type=float, default=17.8) * AU
        theta0 = request.args.get("angulo", type=float, default=0)
        n_points = request.args.get("numPontos", type=int, default=300)
        
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

@app.route("/velocidades")
def velocidades():
    try:
        massa = request.args.get("massaCorporal", type=float, default=1.99e30)
        e = request.args.get("excentricidade", type=float, default=0.967)
        a = request.args.get("semieixo", type=float, default=17.8) * AU
        
        resultado = calcular_velocidades(massa, a, e)
        resposta = {
            "tipo": resultado["tipo"],
            "v_perielio_kms": resultado["v_perielio"] / 1000,
            "r_perielio_km": resultado["r_perielio"] / 1000
        }
        if resultado["tipo"] == "eliptica":
            resposta["v_afelio_kms"] = resultado["v_afelio"] / 1000
            resposta["r_afelio_km"] = resultado["r_afelio"] / 1000
        return jsonify(resposta)
    except Exception as err:
        return jsonify({"error": str(err)}), 400

if __name__ == "__main__":
    port = 5000
    url = f"http://localhost:{port}"
   
    print("="*40)
    print("🚀 Iniciando Flask App")
    print(f"📍 {url}")
    print("🌐 Abrindo navegador...")
    print("="*40)
   
    timer = threading.Timer(1.5, lambda: webbrowser.open(url))
    timer.daemon = True
    timer.start()
   
    # IMPORTANT: use_reloader=False for PyInstaller
    app.run(debug=False, port=port, use_reloader=False)
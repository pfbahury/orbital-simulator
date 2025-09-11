import numpy as np
import json
from scipy.constants import G

M_S = 1.99e30  # Massa do Sol (kg)
AU = 1.496e11  # Unidade Astronômica (m)
G = 6.67430e-11  # Constante gravitacional

def calcular_orbita(a, e, theta0=0, n_points=300):
    if e >= 1:
        theta_max = np.arccos(-1/e) * 0.95
        theta = np.linspace(-theta_max, theta_max, n_points)
    else:
        theta = np.linspace(0, 2*np.pi, n_points)

    p = a * (1 - e**2) if e < 1 else a * (e**2 - 1)
    r = p / (1 + e * np.cos(theta - theta0))

    valid = np.isfinite(r) & (r < 1e16)
    r = r[valid]
    theta = theta[valid]

    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x.tolist(), y.tolist()

def exportar_orbita_json(a, e, n_points=300, filepath="orbita.json"):
    x, y = calcular_orbita(a, e, n_points)
    
    data = {
        "a": a,
        "e": e,
        "n_points": n_points,
        "frames": [{"x": x[i], "y": y[i]} for i in range(len(x))]
    }

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Dados exportados para {filepath}")
    return data



def calcular_velocidades(massa_central: float, semi_eixo_maior: float, excentricidade: float):
    if excentricidade < 1:
        r_peri = semi_eixo_maior * (1 - excentricidade)
        v_peri = np.sqrt(G * massa_central * (2/r_peri - 1/semi_eixo_maior))
        r_afelio = semi_eixo_maior * (1 + excentricidade)
        v_afelio = np.sqrt(G * massa_central * (2/r_afelio - 1/semi_eixo_maior))
        return {
            "tipo": "eliptica",
            "v_perielio": v_peri,
            "v_afelio": v_afelio,
            "r_perielio": r_peri,
            "r_afelio": r_afelio
        }

    elif excentricidade == 1:
        p = semi_eixo_maior * (1 - excentricidade**2)
        r_peri = p / 2
        v_peri = np.sqrt(2 * G * massa_central / r_peri)
        return {
            "tipo": "parabolica",
            "v_perielio": v_peri,
            "r_perielio": r_peri
        }

    else:
        r_peri = semi_eixo_maior * (excentricidade - 1)
        v_peri = np.sqrt(G * massa_central * (2/r_peri + 1/semi_eixo_maior))
        return {
            "tipo": "hiperbolica",
            "v_perielio": v_peri,
            "r_perielio": r_peri
        }
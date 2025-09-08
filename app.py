import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import G
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from PIL import Image, ImageTk
import os

# Constantes
M_S = 1.99e30  # Massa do Sol (kg)
AU = 1.496e11  # Unidade Astronômica (m)

class GravitationalSimulator:
    def __init__(self, root):
        """
        Inicializa o simulador com parâmetros padrões e interface gráfica.
        """
        self.root = root
        self.root.title("SIMULADOR ORBITAL")
        self.root.geometry("1000x700")

        # Variáveis de entrada configuráveis pelo usuário
        self.massa_central = tk.DoubleVar(value=M_S)
        self.excentricidade = tk.DoubleVar(value=0.967)  # Cometa Halley
        self.semi_eixo_maior = tk.DoubleVar(value=17.8)  # a para Halley (em AU)
        self.theta0 = tk.DoubleVar(value=0)  # Ângulo do periélio (rad)
        self.passos = tk.IntVar(value=1000)

        self.ani = None  # objeto da animação
        self.bg_image = None  # Para armazenar a imagem de fundo
        self.x_points = []  # Para armazenar os pontos x da órbita
        self.y_points = []  # Para armazenar os pontos y da órbita
        self.animation_running = False  # Estado da animação

        self.create_widgets()

    def create_widgets(self):
        """
        Cria os elementos da interface gráfica do usuário (GUI).
        """
        # ---------- TÍTULO CENTRALIZADO ----------
        title_label = ttk.Label(self.root, text="SIMULADOR ORBITAL", 
                               font=("Arial", 20, "bold"), 
                               foreground="darkblue")
        title_label.pack(pady=20)
        
        # ---------- FRAME PRINCIPAL DE ENTRADA ----------
        input_frame = ttk.LabelFrame(self.root, text="PARÂMETROS DE ENTRADA")
        input_frame.pack(fill="x", padx=20, pady=10)

        # Carregar e definir imagem de fundo FIXA
        try:
            # Caminho para a imagem - usando raw string (r antes das aspas) para evitar problemas com \
            image_path = r"C:\Users\thiag\OneDrive\Desktop\Código Python\background_orbital.png"
            
            # Verifica se o arquivo existe
            if os.path.exists(image_path):
                self.load_background_image(input_frame, image_path)
            else:
                # Se não encontrar, tenta um caminho alternativo
                alternative_path = r"background_orbital.png"  # Tenta no diretório atual
                if os.path.exists(alternative_path):
                    self.load_background_image(input_frame, alternative_path)
                else:
                    print("Imagem de fundo não encontrada. Continuando sem imagem.")
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo: {e}")
            # Continua sem imagem de fundo se houver erro

        # Estilo para fontes maiores
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"))
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TEntry", font=("Arial", 10))

        # Opções rápidas para massa
        self.mass_options = {
            "Sol": 1.99e30,
            "Terra": 5.97e24,
            "Lua": 7.35e22,
            "Outro": None
        }

        # Combobox para selecionar massa
        ttk.Label(input_frame, text="MASSA DO CORPO CENTRAL:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.massa_choice = ttk.Combobox(input_frame, values=list(self.mass_options.keys()), state="readonly", font=("Arial", 10))
        self.massa_choice.set("Sol")  # valor inicial
        self.massa_choice.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.massa_choice.bind("<<ComboboxSelected>>", self.update_mass_entry)

        # Campo extra para digitar massa (aparece só se escolher "Outro")
        self.massa_entry = ttk.Entry(input_frame, textvariable=self.massa_central, font=("Arial", 10))
        self.massa_entry.grid(row=0, column=2, padx=10, pady=5)
        self.massa_entry.grid_remove()  # escondido por padrão

        # Demais entradas
        entradas = [
            ("EXCENTRICIDADE:", self.excentricidade),
            ("SEMI-EIXO MAIOR (m):", self.semi_eixo_maior),
            ("ÂNGULO DO PERIELIO (rad):", self.theta0),
            ("NÚMERO DE PONTOS:", self.passos),
        ]

        for i, (label, var) in enumerate(entradas, start=1):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            ttk.Entry(input_frame, textvariable=var, font=("Arial", 10)).grid(row=i, column=1, padx=10, pady=5, sticky="w")

        # Expandir colunas
        for col in range(3):
            input_frame.grid_columnconfigure(col, weight=1)

        # ---------- FRAME DOS BOTÕES ----------
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Simular Órbita", command=self.simular_orbita).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(button_frame, text="Calcular Velocidades", command=self.calcular_velocidades).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(button_frame, text="Salvar Imagem", command=self.salvar_imagem).grid(row=0, column=2, padx=10, pady=5)
        ttk.Button(button_frame, text="Pausar/Continuar", command=self.toggle_animation).grid(row=0, column=3, padx=10, pady=5)

        # ---------- ÁREA DO GRÁFICO ----------
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_background_image(self, frame, image_path):
        """
        Carrega e define uma imagem de fundo FIXA para o frame especificado.
        """
        try:
            # Carrega a imagem usando PIL
            image = Image.open(image_path)
            
            # Redimensiona a imagem para caber no frame
            image = image.resize((800, 200), Image.Resampling.LANCZOS)
            
            # Converte para formato compatível com Tkinter
            self.bg_image = ImageTk.PhotoImage(image)
            
            # Cria um label com a imagem e coloca no frame
            bg_label = tk.Label(frame, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Garante que a imagem fique atrás dos outros widgets
            bg_label.lower()
            
            print(f"Imagem de fundo carregada com sucesso: {image_path}")
        except Exception as e:
            print(f"Erro ao carregar a imagem de fundo: {e}")

    def update_mass_entry(self, event):
        """
        Atualiza a entrada de massa com base na escolha do usuário.
        """
        choice = self.massa_choice.get()
        if choice == "Outro":
            self.massa_entry.grid()  # mostra o campo extra
        else:
            self.massa_entry.grid_remove()  # esconde o campo
            self.massa_central.set(self.mass_options[choice])

    def simular_orbita(self):
        """
        Calcula os pontos da trajetória orbital e inicia a animação.
        """
        e = self.excentricidade.get()
        a = self.semi_eixo_maior.get()  # Agora em metros
        theta0 = self.theta0.get()
        n_points = self.passos.get()

        # Para órbitas hiperbólicas, precisamos limitar o ângulo
        if e >= 1:
            theta_max = np.arccos(-1/e) * 0.95  # Limita para evitar divisão por zero
            theta = np.linspace(-theta_max, theta_max, n_points)
        else:
            theta = np.linspace(0, 2 * np.pi, n_points)

        p = a * (1 - e**2) if e < 1 else a * (e**2 - 1)
        r = p / (1 + e * np.cos(theta - theta0))
        
        # Remove valores infinitos ou muito grandes
        valid_indices = np.isfinite(r) & (r < 1e16)
        r = r[valid_indices]
        theta = theta[valid_indices]
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Armazena os pontos para a animação
        self.x_points = x
        self.y_points = y

        self.animar_orbita(x, y, e)

    def calcular_velocidades(self):
        """
        Calcula e exibe as velocidades no periélio e afélio.
        """
        e = self.excentricidade.get()
        a = self.semi_eixo_maior.get()  # Agora em metros
        M = self.massa_central.get()

        if e < 1:
            r_peri = a * (1 - e)
            v_peri = np.sqrt(G * M * (2/r_peri - 1/a))
            r_afelio = a * (1 + e)
            v_afelio = np.sqrt(G * M * (2/r_afelio - 1/a))
            messagebox.showinfo("Velocidades Orbitais", 
                               f"Velocidade no Periélio: {v_peri/1000:.2f} km/s\n"
                               f"Velocidade no Afélio: {v_afelio/1000:.2f} km/s\n"
                               f"Distância no Periélio: {r_peri:.2e} m\n"
                               f"Distância no Afélio: {r_afelio:.2e} m")
        elif e == 1:
            p = a * (1 - e**2)
            r_peri = p / 2
            v_peri = np.sqrt(2 * G * M / r_peri)
            messagebox.showinfo("Velocidade de Escape", 
                               f"Velocidade no Periélio (escape): {v_peri/1000:.2f} km/s\n"
                               f"Distância no Periélio: {r_peri:.2e} m")
        else:
            r_peri = a * (e - 1)
            v_peri = np.sqrt(G * M * (2/r_peri + 1/a))
            messagebox.showinfo("Velocidade Hiperbólica", 
                               f"Velocidade no Periélio: {v_peri/1000:.2f} km/s\n"
                               f"Distância no Periélio: {r_peri:.2e} m")

    def animar_orbita(self, x, y, e):
        """
        Cria uma animação da trajetória orbital com ponto em movimento.
        """
        # Para a animação atual se existir
        if self.ani:
            self.ani.event_source.stop()
        
        self.ax.clear()
        
        # Calcula limites para melhor visualização
        max_range = max(np.max(np.abs(x)), np.max(np.abs(y))) * 1.1
        
        # Desenha a órbita
        self.ax.plot(x, y, label=f"Órbita (e={e:.3f})", color="lightblue", alpha=0.7, zorder=1)
        
        # Desenha o corpo central
        self.ax.scatter([0], [0], color="yellow", s=300, label="Corpo Central", zorder=2, edgecolors="orange")
        
        # Prepara o ponto do cometa
        self.ponto, = self.ax.plot([], [], 'ro', label="Cometa", markersize=10, zorder=4, markeredgecolor='darkred')
        
        # Prepara a trilha do cometa
        self.trilha, = self.ax.plot([], [], 'r-', alpha=0.5, linewidth=2, zorder=3)

        # Configurações do gráfico
        self.ax.set_xlabel("Distância (m)")
        self.ax.set_ylabel("Distância (m)")
        self.ax.set_title("ANIMAÇÃO ORBITAL")
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlim(-max_range, max_range)
        self.ax.set_ylim(-max_range, max_range)
        self.ax.set_aspect('equal')
        
        # Formata os eixos para usar notação científica para números grandes
        self.ax.ticklabel_format(style='scientific', scilimits=(-2, 6))
        self.ax.xaxis.get_offset_text().set_fontsize(10)
        self.ax.yaxis.get_offset_text().set_fontsize(10)

        # Inicia a animação
        self.animation_running = True
        
        # Cria a animação
        self.ani = animation.FuncAnimation(
            self.fig, 
            self.update_animation, 
            frames=len(x), 
            interval=30, 
            repeat=True,
            blit=True
        )
        
        # Atualiza o canvas
        self.canvas.draw()

    def update_animation(self, frame):
        """
        Atualiza a animação frame a frame.
        """
        if not self.animation_running:
            return self.ponto, self.trilha
            
        # Atualiza a posição do cometa
        self.ponto.set_data([self.x_points[frame]], [self.y_points[frame]])
        
        # Atualiza a trilha (mostra apenas os últimos 50 pontos)
        trail_length = 50
        start_idx = max(0, frame - trail_length)
        self.trilha.set_data(self.x_points[start_idx:frame+1], self.y_points[start_idx:frame+1])
        
        return self.ponto, self.trilha

    def toggle_animation(self):
        """
        Pausa ou continua a animação.
        """
        if not self.ani:
            return
            
        self.animation_running = not self.animation_running
        if self.animation_running:
            self.ani.event_source.start()
        else:
            self.ani.event_source.stop()

    def salvar_imagem(self):
        """
        Salva a imagem do gráfico atual em um arquivo.
        """
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Salvar imagem como"
        )
        if filepath:
            self.fig.savefig(filepath, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Sucesso", f"Imagem salva em {filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GravitationalSimulator(root)
    root.mainloop()
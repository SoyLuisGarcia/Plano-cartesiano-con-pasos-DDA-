import tkinter as tk
from tkinter import ttk, messagebox
import math

# --- CONFIGURACIÓN GENERAL MEJORADA ---
PLANO_SIZE = 300
CANVAS_SIZE = 600  # Reducido para mejor ajuste
MARGEN = 40  # Margen reducido
AREA_UTIL = CANVAS_SIZE - 2 * MARGEN
SCALE = AREA_UTIL / PLANO_SIZE

# PALETA DE COLORES MEJORADA
DARK_BG = "#1E1E2E"
ACCENT_COLOR = "#7E6CA8"
SECONDARY_COLOR = "#4A90E2"
SUCCESS_COLOR = "#27AE60"
WARNING_COLOR = "#F39C12"
CANVAS_BG = "#FFFFFF"
GRID_COLOR = "#E8F4F8"
LINE_COLOR = "#3498DB"
TRIANGLE_FILL = "#E1F0FA"
TEXT_COLOR = "#2C3E50"
PANEL_BG = "#2D3748"

FONT_MONO = ("Consolas", 10)
FONT_TITLE = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)

def clamp_int(s):
    return int(s)

def scale_point(x, y):
    sx = MARGEN + x * SCALE
    sy = CANVAS_SIZE - (MARGEN + y * SCALE)
    return sx, sy

def dda_points(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    points = []
    if steps == 0:
        return [(round(x1), round(y1))]
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    return points

def classify_slope(dx, dy):
    if dx == 0:
        return None, "Vertical (dx=0)"
    m = dy / dx
    if m > 1:
        tipo = "m > 1 (inclinación pronunciada)"
    elif m < -1:
        tipo = "m < -1 (inclinación negativa pronunciada)"
    elif 0 < m < 1:
        tipo = "0 < m < 1 (inclinación suave)"
    elif -1 < m < 0:
        tipo = "-1 < m < 0 (suave negativa)"
    elif m == 0:
        tipo = "Horizontal (m=0)"
    else:
        tipo = "m = ±1 (45°)"
    return m, tipo

def calcular_angulo(dx, dy):
    if dx == 0:
        return 90
    ang = abs(math.degrees(math.atan(dy / dx)))
    return round(ang, 2)

def determinar_cuadrante(dx, dy):
    if dx > 0 and dy > 0:
        return "I (Arriba-Derecha)"
    elif dx < 0 and dy > 0:
        return "II (Arriba-Izquierda)"
    elif dx < 0 and dy < 0:
        return "III (Abajo-Izquierda)"
    elif dx > 0 and dy < 0:
        return "IV (Abajo-Derecha)"
    else:
        return "Eje (sin cuadrante definido)"

class DDATool:
    def __init__(self, root):
        self.root = root
        root.title("🔺 Herramienta DDA - Algoritmo de Línea y Triángulos")
        root.config(bg=DARK_BG)
        
        # Configurar estilo ttk
        self.setup_styles()

        main = ttk.Frame(root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # --- Canvas con diseño mejorado ---
        canvas_frame = ttk.LabelFrame(main, text="🎯 Plano Cartesiano (0-300)", padding=6)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        # Frame para el canvas con borde
        canvas_container = ttk.Frame(canvas_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_container, width=CANVAS_SIZE, height=CANVAS_SIZE, 
                               bg=CANVAS_BG, highlightthickness=1, highlightbackground="#CCCCCC")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # --- Panel de control mejorado ---
        control = ttk.Frame(main, width=320)
        control.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(8, 0))

        # --- Sección de coordenadas con diseño mejorado ---
        coords_frame = ttk.LabelFrame(control, text="📍 Coordenadas (0-300)", padding=8)
        coords_frame.pack(fill=tk.X, pady=(0, 8))

        # Crear entradas separadas para cada coordenada
        coords_grid = ttk.Frame(coords_frame)
        coords_grid.pack(fill=tk.X)

        # Punto A
        ttk.Label(coords_grid, text="Punto A:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=4)
        ttk.Label(coords_grid, text="X:").grid(row=0, column=1, sticky="e", padx=(8, 2))
        self.ax = ttk.Entry(coords_grid, width=6, font=("Consolas", 10))
        self.ax.grid(row=0, column=2, sticky="w", padx=(0, 8))
        self.ax.insert(0, "20")
        
        ttk.Label(coords_grid, text="Y:").grid(row=0, column=3, sticky="e", padx=(8, 2))
        self.ay = ttk.Entry(coords_grid, width=6, font=("Consolas", 10))
        self.ay.grid(row=0, column=4, sticky="w")
        self.ay.insert(0, "25")

        # Punto B
        ttk.Label(coords_grid, text="Punto B:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", pady=4)
        ttk.Label(coords_grid, text="X:").grid(row=1, column=1, sticky="e", padx=(8, 2))
        self.bx = ttk.Entry(coords_grid, width=6, font=("Consolas", 10))
        self.bx.grid(row=1, column=2, sticky="w", padx=(0, 8))
        self.bx.insert(0, "10")
        
        ttk.Label(coords_grid, text="Y:").grid(row=1, column=3, sticky="e", padx=(8, 2))
        self.by = ttk.Entry(coords_grid, width=6, font=("Consolas", 10))
        self.by.grid(row=1, column=4, sticky="w")
        self.by.insert(0, "40")

        # Punto C
        ttk.Label(coords_grid, text="Punto C:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", pady=4)
        ttk.Label(coords_grid, text="X:").grid(row=2, column=1, sticky="e", padx=(8, 2))
        self.cx = ttk.Entry(coords_grid, width=6, font=("Consolas", 10))
        self.cx.grid(row=2, column=2, sticky="w", padx=(0, 8))
        self.cx.insert(0, "0")
        
        ttk.Label(coords_grid, text="Y:").grid(row=2, column=3, sticky="e", padx=(8, 2))
        self.cy = ttk.Entry(coords_grid, width=6, font=("Consolas", 10))
        self.cy.grid(row=2, column=4, sticky="w")
        self.cy.insert(0, "0")

        # --- Modos de dibujo con iconos ---
        mode_frame = ttk.LabelFrame(control, text="🎨 Modo de Dibujo", padding=8)
        mode_frame.pack(fill=tk.X, pady=(0, 8))

        self.draw_mode = tk.StringVar(value="line")
        ttk.Radiobutton(mode_frame, text="📏 Línea (A-B)", variable=self.draw_mode, 
                       value="line").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(mode_frame, text="🔺 Triángulo (A,B,C)", variable=self.draw_mode, 
                       value="triangle").pack(anchor=tk.W, pady=2)

        # --- Botones con colores y iconos ---
        button_frame = ttk.LabelFrame(control, text="⚡ Acciones", padding=8)
        button_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Button(button_frame, text="🖊️ Dibujar (Algoritmo DDA)", 
                  command=self.on_draw, style="Accent.TButton").pack(fill=tk.X, pady=2)
        
        ttk.Button(button_frame, text="🔺 Dibujar Triángulo Completo", 
                  command=self.on_draw_triangle, style="Secondary.TButton").pack(fill=tk.X, pady=2)
        
        ttk.Button(button_frame, text="📊 Ver Tablas DDA", 
                  command=self.show_tables, style="Info.TButton").pack(fill=tk.X, pady=2)
        
        ttk.Button(button_frame, text="🗑️ Borrar Todo", 
                  command=self.clear_all, style="Warning.TButton").pack(fill=tk.X, pady=2)

        # --- Panel de información mejorado ---
        info_frame = ttk.LabelFrame(control, text="📊 Información del Algoritmo DDA", padding=6)
        info_frame.pack(fill=tk.BOTH, expand=True)

        # Frame con scroll para la información
        info_container = ttk.Frame(info_frame)
        info_container.pack(fill=tk.BOTH, expand=True)

        # Text widget con mejor formato
        self.info_text = tk.Text(info_container, height=16, width=38, 
                                font=("Consolas", 9), bg="#F8F9FA", fg=TEXT_COLOR,
                                relief="flat", padx=8, pady=8, wrap=tk.WORD)
        
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(info_container, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.last_segments = {}
        self.draw_axes()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configurar colores para los estilos
        style.configure("TFrame", background=DARK_BG)
        style.configure("TLabelFrame", background=DARK_BG, foreground="white", font=FONT_TITLE)
        style.configure("TLabelFrame.Label", background=DARK_BG, foreground="white")
        style.configure("TLabel", background=DARK_BG, foreground="white", font=FONT_NORMAL)
        style.configure("TRadiobutton", background=DARK_BG, foreground="orange", font=FONT_NORMAL)
        style.configure("TButton", font=FONT_NORMAL)
        
        # Botones con colores específicos - SIN HOVER
        style.configure("Accent.TButton", background=ACCENT_COLOR, foreground="white")
        style.map("Accent.TButton", 
                 background=[('active', ACCENT_COLOR), ('pressed', ACCENT_COLOR)])
        
        style.configure("Secondary.TButton", background=SECONDARY_COLOR, foreground="white")
        style.map("Secondary.TButton", 
                 background=[('active', SECONDARY_COLOR), ('pressed', SECONDARY_COLOR)])
        
        style.configure("Info.TButton", background="#17A2B8", foreground="white")
        style.map("Info.TButton", 
                 background=[('active', "#17A2B8"), ('pressed', "#17A2B8")])
        
        style.configure("Warning.TButton", background=WARNING_COLOR, foreground="white")
        style.map("Warning.TButton", 
                 background=[('active', WARNING_COLOR), ('pressed', WARNING_COLOR)])
        
        # Radiobuttons acentuados
        style.configure("Accent.TRadiobutton", background=DARK_BG, foreground="white")
        
        # Entradas de texto
        style.configure("TEntry", fieldbackground="white", foreground=TEXT_COLOR)

    def draw_axes(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill=CANVAS_BG, outline="")
        
        # Dibujar grid más compacto
        for i in range(0, PLANO_SIZE + 1, 10):
            x = MARGEN + i * SCALE
            y = CANVAS_SIZE - (MARGEN + i * SCALE)
            if i % 50 == 0:  # Líneas más gruesas cada 50 unidades
                self.canvas.create_line(x, MARGEN, x, CANVAS_SIZE - MARGEN, fill=GRID_COLOR, width=1.5)
                self.canvas.create_line(MARGEN, y, CANVAS_SIZE - MARGEN, y, fill=GRID_COLOR, width=1.5)
            else:
                self.canvas.create_line(x, MARGEN, x, CANVAS_SIZE - MARGEN, fill=GRID_COLOR, width=0.5)
                self.canvas.create_line(MARGEN, y, CANVAS_SIZE - MARGEN, y, fill=GRID_COLOR, width=0.5)
        
        # Dibujar ejes principales
        self.canvas.create_line(MARGEN, CANVAS_SIZE - MARGEN, CANVAS_SIZE - MARGEN, CANVAS_SIZE - MARGEN, 
                               width=2, fill="#2C3E50")
        self.canvas.create_line(MARGEN, MARGEN, MARGEN, CANVAS_SIZE - MARGEN, 
                               width=2, fill="#2C3E50")

        # Etiquetas del eje X (abajo)
        for i in range(0, PLANO_SIZE + 1, 50):
            x = MARGEN + i * SCALE
            # Etiquetas del eje X (abajo)
            self.canvas.create_text(x, CANVAS_SIZE - MARGEN + 15, text=str(i), 
                                   font=("Consolas", 8, "bold"), fill="#2C3E50")
            # Etiquetas del eje X (arriba)
            self.canvas.create_text(x, MARGEN - 15, text=str(i), 
                                   font=("Consolas", 8, "bold"), fill="#2C3E50")

        # Etiquetas del eje Y (izquierda y derecha)
        for i in range(0, PLANO_SIZE + 1, 50):
            y = CANVAS_SIZE - (MARGEN + i * SCALE)
            # Etiquetas del eje Y (izquierda)
            self.canvas.create_text(MARGEN - 18, y, text=str(i), 
                                   font=("Consolas", 8, "bold"), fill="#2C3E50")
            # Etiquetas del eje Y (derecha)
            self.canvas.create_text(CANVAS_SIZE - MARGEN + 18, y, text=str(i), 
                                   font=("Consolas", 8, "bold"), fill="#2C3E50")

        # Etiquetas X, Y en los extremos
        self.canvas.create_text(CANVAS_SIZE - MARGEN + 25, CANVAS_SIZE - MARGEN - 10, 
                               text="X", font=("Arial", 12, "bold"), fill="#2C3E50")
        self.canvas.create_text(CANVAS_SIZE - MARGEN + 25, MARGEN - 10, 
                               text="X", font=("Arial", 12, "bold"), fill="#2C3E50")
        self.canvas.create_text(MARGEN - 15, MARGEN - 15, text="Y", 
                               font=("Arial", 12, "bold"), fill="#2C3E50")
        self.canvas.create_text(CANVAS_SIZE - MARGEN + 15, MARGEN - 15, text="Y", 
                               font=("Arial", 12, "bold"), fill="#2C3E50")

        # Dibujar bordes del área útil
        self.canvas.create_rectangle(MARGEN, MARGEN, CANVAS_SIZE - MARGEN, CANVAS_SIZE - MARGEN,
                                   outline="#CCCCCC", width=1)

    def read_points(self):
        return (
            (clamp_int(self.ax.get()), clamp_int(self.ay.get())),
            (clamp_int(self.bx.get()), clamp_int(self.by.get())),
            (clamp_int(self.cx.get()), clamp_int(self.cy.get()))
        )

    def on_draw(self):
        try:
            A, B, C = self.read_points()
        except ValueError:
            messagebox.showerror("Error", "❌ Por favor ingresa valores numéricos válidos en todas las coordenadas.")
            return
        self.draw_axes()
        self.last_segments.clear()
        self.info_text.delete("1.0", tk.END)

        if self.draw_mode.get() == "line":
            self.draw_segment(A, B, "A-B")
            self.show_point_labels([A, B])
        else:
            self.on_draw_triangle()

    def on_draw_triangle(self):
        try:
            A, B, C = self.read_points()
        except ValueError:
            messagebox.showerror("Error", "❌ Por favor ingresa valores numéricos válidos en todas las coordenadas.")
            return
        self.draw_axes()
        self.last_segments.clear()
        self.draw_segment(A, B, "A-B")
        self.draw_segment(B, C, "B-C")
        self.draw_segment(C, A, "C-A")
        self.fill_triangle(A, B, C)
        self.show_triangle_angles(A, B, C)
        self.show_point_labels([A, B, C])

    def draw_segment(self, P1, P2, name):
        (x1, y1), (x2, y2) = P1, P2
        
        # Verificar que los puntos estén dentro del rango visible
        if not (0 <= x1 <= PLANO_SIZE and 0 <= y1 <= PLANO_SIZE and 
                0 <= x2 <= PLANO_SIZE and 0 <= y2 <= PLANO_SIZE):
            messagebox.showwarning("Advertencia", 
                                 f"⚠️ Algunos puntos están fuera del rango visible (0-300).\n"
                                 f"Ajusta las coordenadas para ver la figura completa.")
        
        pts = dda_points(x1, y1, x2, y2)
        
        # Dibujar puntos del algoritmo DDA
        for (px, py) in pts:
            if 0 <= px <= PLANO_SIZE and 0 <= py <= PLANO_SIZE:  # Solo dibujar puntos visibles
                sx, sy = scale_point(px, py)
                self.canvas.create_oval(sx - 2, sy - 2, sx + 2, sy + 2, 
                                      fill=LINE_COLOR, outline=LINE_COLOR, width=1)

        # Dibujar línea que conecta los puntos
        sx1, sy1 = scale_point(x1, y1)
        sx2, sy2 = scale_point(x2, y2)
        self.canvas.create_line(sx1, sy1, sx2, sy2, fill=LINE_COLOR, width=2)

        dx, dy = x2 - x1, y2 - y1
        m, tipo = classify_slope(dx, dy)
        angulo = calcular_angulo(dx, dy)
        cuadrante = determinar_cuadrante(dx, dy)

        self.last_segments[name] = {"puntos": pts, "pendiente": m, "tipo": tipo}

        # Mostrar información con formato mejorado
        self.info_text.insert(tk.END, f"📏 **Segmento {name}**\n", "title")
        self.info_text.insert(tk.END, f"   Punto Inicial: ({x1}, {y1})\n")
        self.info_text.insert(tk.END, f"   Punto Final: ({x2}, {y2})\n")
        self.info_text.insert(tk.END, f"   ΔX = {dx:>4} | ΔY = {dy:>4}\n")
        
        if m is not None:
            self.info_text.insert(tk.END, f"   Pendiente (m) = {m:.4f}\n")
        self.info_text.insert(tk.END, f"   Tipo: {tipo}\n")
        self.info_text.insert(tk.END, f"   Ángulo = {angulo}°\n")
        self.info_text.insert(tk.END, f"   Cuadrante: {cuadrante}\n")
        self.info_text.insert(tk.END, f"   Puntos calculados: {len(pts)}\n")
        self.info_text.insert(tk.END, "─" * 35 + "\n\n")

        # Configurar tags para formato
        self.info_text.tag_configure("title", foreground=ACCENT_COLOR, font=("Consolas", 9, "bold"))

    def fill_triangle(self, A, B, C, color=TRIANGLE_FILL):
        coords = []
        for (x, y) in (A, B, C):
            sx, sy = scale_point(x, y)
            coords.extend([sx, sy])
        self.canvas.create_polygon(coords, fill=color, outline=ACCENT_COLOR, width=2)

    def show_point_labels(self, points):
        colors = [ACCENT_COLOR, SECONDARY_COLOR, SUCCESS_COLOR]
        for i, (x, y) in enumerate(points):
            if 0 <= x <= PLANO_SIZE and 0 <= y <= PLANO_SIZE:  # Solo mostrar etiquetas visibles
                sx, sy = scale_point(x, y)
                point_name = ["A", "B", "C"][i]
                # Dibujar punto
                self.canvas.create_oval(sx - 4, sy - 4, sx + 4, sy + 4, 
                                      fill=colors[i], outline="white", width=1)
                # Etiqueta
                self.canvas.create_text(sx + 18, sy - 12, text=f"{point_name}({x},{y})", 
                                       fill=colors[i], font=("Consolas", 9, "bold"),
                                       anchor="w")

    def show_triangle_angles(self, A, B, C):
        def dist(P, Q): return math.hypot(Q[0] - P[0], Q[1] - P[1])
        a = dist(B, C); b = dist(A, C); c = dist(A, B)
        
        # Calcular ángulos con verificación de triángulo válido
        try:
            Aang = math.degrees(math.acos(max(-1, min(1, (b**2 + c**2 - a**2) / (2*b*c)))))
            Bang = math.degrees(math.acos(max(-1, min(1, (a**2 + c**2 - b**2) / (2*a*c)))))
            Cang = 180 - (Aang + Bang)
            
            self.info_text.insert(tk.END, "🔺 **Ángulos del Triángulo**\n", "title")
            self.info_text.insert(tk.END, f"   ∠A = {Aang:.2f}°\n")
            self.info_text.insert(tk.END, f"   ∠B = {Bang:.2f}°\n")
            self.info_text.insert(tk.END, f"   ∠C = {Cang:.2f}°\n")
            self.info_text.insert(tk.END, f"   Suma: {Aang + Bang + Cang:.1f}°\n")
            
            # Determinar tipo de triángulo
            if Aang < 90 and Bang < 90 and Cang < 90:
                tipo = "Acutángulo"
            elif Aang == 90 or Bang == 90 or Cang == 90:
                tipo = "Rectángulo"
            else:
                tipo = "Obtusángulo"
            self.info_text.insert(tk.END, f"   Tipo: {tipo}\n")
            
        except (ValueError, ZeroDivisionError):
            self.info_text.insert(tk.END, "⚠️  No se pueden calcular ángulos (puntos colineales)\n")
        
        self.info_text.insert(tk.END, "─" * 35 + "\n\n")

    def show_tables(self):
        if not self.last_segments:
            messagebox.showinfo("Información", "📊 Dibuja primero algún segmento o triángulo para ver las tablas DDA.")
            return
        
        top = tk.Toplevel(self.root)
        top.title("📋 Tablas Detalladas - Algoritmo DDA")
        top.geometry("500x350")
        top.configure(bg=DARK_BG)
        
        nb = ttk.Notebook(top)
        nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        for name, data in self.last_segments.items():
            frame = ttk.Frame(nb)
            nb.add(frame, text=name)
            
            # Frame para la tabla con scroll
            table_frame = ttk.Frame(frame)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
            
            # Crear tabla
            table = ttk.Treeview(table_frame, columns=("paso", "x", "y"), show="headings", height=12)
            table.heading("paso", text="Paso")
            table.heading("x", text="Coordenada X")
            table.heading("y", text="Coordenada Y")
            table.column("paso", width=60, anchor="center")
            table.column("x", width=100, anchor="center")
            table.column("y", width=100, anchor="center")
            
            # Scrollbar para la tabla
            scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
            table.configure(yscrollcommand=scrollbar.set)
            
            table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Insertar datos
            for i, (x, y) in enumerate(data["puntos"]):
                table.insert("", tk.END, values=(i, x, y))

    def clear_all(self):
        self.canvas.delete("all")
        self.draw_axes()
        self.info_text.delete("1.0", tk.END)
        self.last_segments.clear()
        # Limpiar TODAS las coordenadas - VERSIÓN QUE LAS DEJA VACÍAS
        entries = [self.ax, self.ay, self.bx, self.by, self.cx, self.cy]
        
        for entry in entries:
            entry.delete(0, tk.END) 

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x650")  # Ventana más compacta
    app = DDATool(root)
    root.mainloop()
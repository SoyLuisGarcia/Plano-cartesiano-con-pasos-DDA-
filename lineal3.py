import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

# --- CONFIGURACIÓN DE TEMAS ---

DARK_THEME = {
    "bg_root": "#2E2E2E",      
    "bg_frame": "#3C3C3C",     
    "fg_text": "#DEDEDE",      
    "bg_canvas": "#FAFAFA",    
    "fg_canvas_text": "black", 
    "bg_entry": "#454545",
    "bg_entry_focus": "#555555",
    "accent_color": "#007ACC"
}

LIGHT_THEME = {
    "bg_root": "#F0F0F0",       
    "bg_frame": "#FFFFFF",      
    "fg_text": "#333333",       
    "bg_canvas": "#FFFFFF",
    "fg_canvas_text": "black",
    "bg_entry": "#E0E0E0",
    "bg_entry_focus": "#CCCCCC",
    "accent_color": "#28A745"
}

# --- Variables Globales ---
CANVAS_VIEWPORT_WIDTH = 700
CANVAS_VIEWPORT_HEIGHT = 700
PLANO_WIDTH = 1600
PLANO_HEIGHT = 1600
color_linea_rgb = "#0000FF" 
zoom_factor = 0.75 
current_theme = "dark" 

FONT_BODY = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 10)
FONT_TITLE = ("Segoe UI", 12, "bold")

# Variable para guardar los resultados del último DDA
ultimo_resultado_dda = ""

# --- Funciones ---

def dda(x1, y1, x2, y2, color, pixel_size=1):
    """Algoritmo DDA para dibujar una línea en el canvas con tamaño de píxel."""
    global ultimo_resultado_dda
    dx = x2 - x1
    dy = y2 - y1
    
    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        x_inc = 0.0
        y_inc = 0.0
    else:
        x_inc = dx / steps
        y_inc = dy / steps

    x_inc_display = round(x_inc, 2)
    y_inc_display = round(y_inc, 2)
    
    resultado = f"--- Algoritmo DDA ---\n\n"
    resultado += f"Punto A: ({x1}, {y1})\n"
    resultado += f"Punto B: ({x2}, {y2})\n"
    resultado += f"dx = {dx}, dy = {dy}\n"
    resultado += f"Pasos = {steps}\n"
    resultado += f"Incrementos: x_inc={x_inc_display}, y_inc={y_inc_display}\n\n"
    
    x, y = float(x1), float(y1) 
    cx_plano, cy_plano = PLANO_WIDTH // 2, PLANO_HEIGHT // 2
    
    for i in range(steps + 1):
        px = round(x)
        py = round(y)
        
        canvas.create_oval(px + cx_plano, -py + cy_plano, 
                           px + pixel_size + cx_plano, -py + pixel_size + cy_plano, 
                           fill=color, outline=color)
        
        resultado += f"Paso {i}: ({px}, {py})\n"
        x += x_inc
        y += y_inc
    
    resultado += "--------------------------------------\n"
    
    font_style = ("Arial", 10, "bold")
    canvas.create_text(x1 + cx_plano + 5, -y1 + cy_plano - 5, 
                       text=f"A({x1}, {y1})", anchor=tk.SW, font=font_style, fill="blue")
    
    canvas.create_text(x2 + cx_plano + 5, -y2 + cy_plano - 5, 
                       text=f"B({x2}, {y2})", anchor=tk.SW, font=font_style, fill="red")

    ultimo_resultado_dda = resultado


def dibujar_ejes():
    """Dibuja el plano cartesiano con cuadrícula y etiquetas."""
    canvas.delete(tk.ALL) 
    
    cx, cy = PLANO_WIDTH // 2, PLANO_HEIGHT // 2
    intervalo_fino = 10  
    intervalo_grueso = 100 

    theme = DARK_THEME if current_theme == "dark" else LIGHT_THEME
    line_color = "#E0E0E0" if current_theme == "dark" else "#D0D0D0"
    
    for i in range(-cx, cx + 1, intervalo_fino):
        if i != 0:
            canvas.create_line(cx + i, 0, cx + i, PLANO_HEIGHT, fill=line_color, tags="axes", dash=(1, 2))
        
    for j in range(-cy, cy + 1, intervalo_fino):
        if j != 0:
            canvas.create_line(0, cy - j, PLANO_WIDTH, cy - j, fill=line_color, tags="axes", dash=(1, 2))

    axis_color = "gray" if current_theme == "dark" else "#888888"
    canvas.create_line(cx, 0, cx, PLANO_HEIGHT, fill=axis_color, tags="axes", width=2)  
    canvas.create_line(0, cy, PLANO_WIDTH, cy, fill=axis_color, tags="axes", width=2)  
    
    label_color = theme['fg_canvas_text']
    for i in range(-cx, cx + 1, intervalo_grueso):
        if i != 0:
            canvas.create_line(cx + i, cy - 5, cx + i, cy + 5, fill=axis_color, tags="axes")
            canvas.create_text(cx + i, cy + 20, text=str(i), fill=label_color, font=FONT_BODY, tags="axes")

    for j in range(-cy, cy + 1, intervalo_grueso):
        if j != 0:
            canvas.create_line(cx - 5, cy - j, cx + 5, cy - j, fill=axis_color, tags="axes")
            canvas.create_text(cx - 20, cy - j, text=str(j), fill=label_color, font=FONT_BODY, tags="axes")

    canvas.create_text(cx + 25, cy + 25, text="(0,0)", fill=label_color, font=FONT_TITLE, tags="axes")
    aplicar_zoom()


def seleccionar_color():
    global color_linea_rgb
    color_code = colorchooser.askcolor(title="Seleccionar Color de la Línea")
    if color_code:
        color_linea_rgb = color_code[1] 
        btn_color.config(bg=color_linea_rgb)
        lbl_color_display.config(bg=color_linea_rgb)
        
        r, g, b = color_code[0]
        entry_rojo.delete(0, tk.END)
        entry_rojo.insert(0, str(int(r)))
        entry_verde.delete(0, tk.END)
        entry_verde.insert(0, str(int(g)))
        entry_azul.delete(0, tk.END)
        entry_azul.insert(0, str(int(b)))


def dibujar_linea():
    canvas.delete(tk.ALL)
    dibujar_ejes() 
    
    try:
        x1 = int(entry_x1.get() or 0)
        y1 = int(entry_y1.get() or 0)
        x2 = int(entry_x2.get() or 0)
        y2 = int(entry_y2.get() or 0)
        
        pixel_size = int(entry_pixel_size.get() or 1)
        pixel_size = max(1, pixel_size) 
        
        rojo = int(entry_rojo.get() or 0)
        verde = int(entry_verde.get() or 0)
        azul = int(entry_azul.get() or 0)
        
        rojo = max(0, min(255, rojo))
        verde = max(0, min(255, verde))
        azul = max(0, min(255, azul))
        
        color = f'#{rojo:02x}{verde:02x}{azul:02x}'
        
    except ValueError:
        return 
    
    dda(x1, y1, x2, y2, color, pixel_size)


def aplicar_zoom():
    global zoom_factor
    canvas.scale(tk.ALL, 0, 0, zoom_factor, zoom_factor)
    canvas.config(scrollregion=(0, 0, PLANO_WIDTH * zoom_factor, PLANO_HEIGHT * zoom_factor))
    
    center_x = PLANO_WIDTH / 2
    center_y = PLANO_HEIGHT / 2
    
    target_x = (center_x * zoom_factor) - (CANVAS_VIEWPORT_WIDTH / 2)
    target_y = (center_y * zoom_factor) - (CANVAS_VIEWPORT_HEIGHT / 2)
    
    fraction_x = target_x / (PLANO_WIDTH * zoom_factor)
    fraction_y = target_y / (PLANO_HEIGHT * zoom_factor)
    
    canvas.xview_moveto(fraction_x)
    canvas.yview_moveto(fraction_y)


def zoom_in():
    global zoom_factor
    if zoom_factor < 2.0: 
        zoom_factor += 0.25
        dibujar_linea() 

def zoom_out():
    global zoom_factor
    if zoom_factor > 0.25: 
        zoom_factor -= 0.25
        dibujar_linea()


def alternar_tema():
    global current_theme
    if current_theme == "dark":
        current_theme = "light"
        theme = LIGHT_THEME
        btn_theme_toggle.config(text="Modo Oscuro")
    else:
        current_theme = "dark"
        theme = DARK_THEME
        btn_theme_toggle.config(text="Modo Claro")

    root.config(bg=theme["bg_root"])
    canvas.config(bg=theme["bg_canvas"])
    
    style.configure('.', background=theme["bg_root"], foreground=theme["fg_text"])
    style.configure('TFrame', background=theme["bg_frame"])
    style.configure('TLabelFrame', background=theme["bg_frame"], foreground=theme["fg_text"])
    style.configure('TLabel', background=theme["bg_frame"], foreground=theme["fg_text"])
    style.configure('TEntry', fieldbackground=theme["bg_entry"], foreground=theme["fg_text"])
    style.map('TEntry', fieldbackground=[('focus', theme["bg_entry_focus"])])
    style.configure('Accent.TButton', background=theme["accent_color"])
    style.map('Accent.TButton', background=[('active', theme["accent_color"])])
    dibujar_linea()


# --- Nueva función: mostrar resultados del DDA ---
def mostrar_resultados_dda():
    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title("Resultados del Algoritmo DDA")
    ventana_resultados.geometry("600x500")
    
    text_res = tk.Text(ventana_resultados, 
                       wrap=tk.WORD, 
                       font=FONT_MONO, 
                       bg="#FFFFFF", 
                       fg="#000000")
    text_res.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_res.insert(tk.END, ultimo_resultado_dda if ultimo_resultado_dda else "Primero dibuja una línea con el botón DIBUJAR.")
    text_res.config(state=tk.DISABLED)
    
    scrollbar_res = ttk.Scrollbar(text_res, command=text_res.yview)
    text_res.config(yscrollcommand=scrollbar_res.set)
    scrollbar_res.pack(side=tk.RIGHT, fill=tk.Y)


# --- Configuración de la Ventana Principal ---
root = tk.Tk()
root.title("Algoritmo DDA y Plano Cartesiano con Scroll y Zoom")
root.config(bg=DARK_THEME["bg_root"]) 

style = ttk.Style()
style.theme_use('clam') 
style.configure('.', background=DARK_THEME["bg_root"], foreground=DARK_THEME["fg_text"], font=FONT_BODY)
style.configure('TFrame', background=DARK_THEME["bg_frame"], borderwidth=0)
style.configure('TLabelFrame', background=DARK_THEME["bg_frame"], foreground=DARK_THEME["fg_text"], font=FONT_TITLE) 
style.configure('TLabel', background=DARK_THEME["bg_frame"], foreground=DARK_THEME["fg_text"], font=FONT_BODY)
style.configure('TEntry', fieldbackground=DARK_THEME["bg_entry"], foreground=DARK_THEME["fg_text"], borderwidth=0)
style.map('TEntry', fieldbackground=[('focus', DARK_THEME["bg_entry_focus"])])
style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'), padding=10,
                background=DARK_THEME["accent_color"], foreground='white', relief='flat') 
style.map('Accent.TButton', background=[('active', '#0090FF'), ('!active', DARK_THEME["accent_color"])],
          foreground=[('active', 'white'), ('!active', 'white')])

# --- Contenedor Principal ---
main_frame = ttk.Frame(root, padding="10", style='TFrame')
main_frame.pack(fill=tk.BOTH, expand=True)

# --- Controles (Derecha) ---
control_frame = ttk.Frame(main_frame, padding="10", style='TFrame')
control_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

btn_theme_toggle = ttk.Button(control_frame, text="Modo Claro", command=alternar_tema, style='Accent.TButton', cursor="hand2")
btn_theme_toggle.pack(pady=10, fill=tk.X)
ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)

coords_frame = ttk.LabelFrame(control_frame, text="1. Coordenadas de Línea", padding="10")
coords_frame.pack(fill=tk.X, pady=10)

labels_coords = ["A (X1):", "A (Y1):", "B (X2):", "B (Y2):"]
entries = {}

for i, label_text in enumerate(labels_coords):
    row = i // 2
    col = i % 2
    label = ttk.Label(coords_frame, text=label_text, width=6)
    label.grid(row=row, column=col*2, padx=5, pady=5, sticky=tk.W)
    entry = ttk.Entry(coords_frame, width=8) 
    entry.grid(row=row, column=col*2 + 1, padx=5, pady=5, sticky=tk.E)
    entry.insert(0, "90" if i == 0 else "100" if i == 1 else "-600" if i == 2 else "200") 
    entries[label_text] = entry

entry_x1, entry_y1 = entries["A (X1):"], entries["A (Y1):"]
entry_x2, entry_y2 = entries["B (X2):"], entries["B (Y2):"]

ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)

settings_frame = ttk.LabelFrame(control_frame, text="2. Configuración de Vista", padding="10")
settings_frame.pack(fill=tk.X, pady=10)

lbl_pixel_size = ttk.Label(settings_frame, text="Tamaño del Píxel (1-5):")
lbl_pixel_size.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_pixel_size = ttk.Entry(settings_frame, width=5) 
entry_pixel_size.insert(0, "2")
entry_pixel_size.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

lbl_zoom = ttk.Label(settings_frame, text="Zoom:")
lbl_zoom.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

zoom_frame = ttk.Frame(settings_frame)
zoom_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

btn_zoom_in = ttk.Button(zoom_frame, text="➕", command=zoom_in, width=2, cursor="hand2")
btn_zoom_in.pack(side=tk.LEFT, padx=(0, 5))

btn_zoom_out = ttk.Button(zoom_frame, text="➖", command=zoom_out, width=2, cursor="hand2")
btn_zoom_out.pack(side=tk.LEFT)

ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)

color_frame = ttk.LabelFrame(control_frame, text="3. Configuración de Color (RGB)", padding="10")
color_frame.pack(fill=tk.X, pady=10)

lbl_color_display = tk.Label(color_frame, text="Color Actual", bg=color_linea_rgb, fg="white", font=FONT_TITLE, relief=tk.FLAT, bd=0)
lbl_color_display.grid(row=0, column=0, columnspan=2, sticky=tk.EW, pady=(0, 5), padx=5, ipady=5)

btn_color = tk.Button(color_frame, text="Seleccionar Color", command=seleccionar_color, bg=color_linea_rgb, fg="white", relief=tk.FLAT, font=FONT_BODY, cursor="hand2")
btn_color.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(5, 10), padx=5) 

labels_rgb = ["Rojo:", "Verde:", "Azul:"]
entries_rgb = {}

for i, label_text in enumerate(labels_rgb):
    label = ttk.Label(color_frame, text=label_text)
    label.grid(row=i+2, column=0, padx=5, pady=2, sticky=tk.W) 
    entry = ttk.Entry(color_frame, width=8) 
    entry.grid(row=i+2, column=1, padx=5, pady=2, sticky=tk.E)
    entries_rgb[label_text] = entry

entry_rojo, entry_verde, entry_azul = entries_rgb["Rojo:"], entries_rgb["Verde:"], entries_rgb["Azul:"]
entry_rojo.insert(0, "0")
entry_verde.insert(0, "0")
entry_azul.insert(0, "255")

dibujar_btn = ttk.Button(control_frame, text="DIBUJAR LÍNEA DDA", command=dibujar_linea, style='Accent.TButton', cursor="hand2")
dibujar_btn.pack(pady=(20, 10), fill=tk.X)

btn_dda = ttk.Button(control_frame, text="DDA", command=mostrar_resultados_dda, style='Accent.TButton', cursor="hand2")
btn_dda.pack(pady=(5, 10), fill=tk.X)

# --- Canvas ---
canvas_container = ttk.LabelFrame(main_frame, text="Plano Cartesiano con Scroll", padding="5")
canvas_container.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(canvas_container, bg=DARK_THEME["bg_canvas"], width=CANVAS_VIEWPORT_WIDTH, height=CANVAS_VIEWPORT_HEIGHT)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_x = ttk.Scrollbar(canvas_container, orient="horizontal", command=canvas.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
scrollbar_y = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

dibujar_ejes()

root.mainloop()
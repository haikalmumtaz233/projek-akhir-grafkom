import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog
from PIL import Image, ImageDraw, ImageGrab
import math

# Fungsi untuk algoritma DDA
def dda_line(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps
    x = x1
    y = y1
    for i in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_increment
        y += y_increment
    return points

# Fungsi untuk algoritma midpoint circle
def midpoint_circle(x0, y0, radius):
    points = []
    x = radius
    y = 0
    p = 1 - radius

    while x >= y:
        points.append((x0 + x, y0 + y))
        points.append((x0 + y, y0 + x))
        points.append((x0 - y, y0 + x))
        points.append((x0 - x, y0 + y))
        points.append((x0 - x, y0 - y))
        points.append((x0 - y, y0 - x))
        points.append((x0 + y, y0 - x))
        points.append((x0 + x, y0 - y))
        y += 1
        if p <= 0:
            p = p + 2 * y + 1
        else:
            x -= 1
            p = p + 2 * y - 2 * x + 1
    return points

# Fungsi untuk algoritma midpoint ellipse
def midpoint_ellipse(rx, ry, xc, yc):
    points = []
    x = 0
    y = ry
    p1 = ry**2 - rx**2 * ry + 0.25 * rx**2
    while 2 * ry**2 * x <= 2 * rx**2 * y:
        points.append((xc + x, yc + y))
        points.append((xc - x, yc + y))
        points.append((xc + x, yc - y))
        points.append((xc - x, yc - y))
        if p1 < 0:
            x += 1
            p1 = p1 + 2 * ry**2 * x + ry**2
        else:
            x += 1
            y -= 1
            p1 = p1 + 2 * ry**2 * x - 2 * rx**2 * y + ry**2

    p2 = ry**2 * (x + 0.5)**2 + rx**2 * (y - 1)**2 - rx**2 * ry**2
    while y >= 0:
        points.append((xc + x, yc + y))
        points.append((xc - x, yc + y))
        points.append((xc + x, yc - y))
        points.append((xc - x, yc - y))
        if p2 > 0:
            y -= 1
            p2 = p2 - 2 * rx**2 * y + rx**2
        else:
            y -= 1
            x += 1
            p2 = p2 + 2 * ry**2 * x - 2 * rx**2 * y + rx**2
    return points

# Fungsi untuk algoritma boundary-fill
def boundary_fill(x, y, fill_color, boundary_color):
    current_color = canvas.gettags(canvas.find_closest(x, y))
    if current_color != boundary_color and current_color != fill_color:
        canvas.create_oval(x, y, x+1, y+1, outline=fill_color, fill=fill_color, tags=fill_color)
        boundary_fill(x + 1, y, fill_color, boundary_color)
        boundary_fill(x - 1, y, fill_color, boundary_color)
        boundary_fill(x, y + 1, fill_color, boundary_color)
        boundary_fill(x, y - 1, fill_color, boundary_color)

# Fungsi untuk menyimpan gambar
def save_image():
    canvas_x = canvas.winfo_rootx() + canvas.winfo_x()
    canvas_y = canvas.winfo_rooty() + canvas.winfo_y()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    I = ImageGrab.grab(bbox=(canvas_x, canvas_y, canvas_x + canvas_width, canvas_y + canvas_height))
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if filename:
        I.save(filename)

# Fungsi untuk menggambar lingkaran
def draw_circle(event):
    x, y = event.x, event.y
    radius = int(radius_entry.get())
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline=color, fill=fill_color, width=thickness)

# Fungsi untuk menggambar elips
def draw_ellipse(event):
    x, y = event.x, event.y
    rx = int(radius_entry.get())
    ry = int(radius_entry.get()) // 2
    canvas.create_oval(x - rx, y - ry, x + rx, y + ry, outline=color, fill=fill_color, width=thickness)

# Fungsi untuk menggambar garis saat drag
def start_line(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def draw_line(event):
    global start_x, start_y
    points = dda_line(start_x, start_y, event.x, event.y)
    for point in points:
        canvas.create_oval(point[0], point[1], point[0] + thickness, point[1] + thickness, fill=color)
    start_x, start_y = event.x, event.y

# Fungsi untuk boundary fill
def fill(event):
    x, y = event.x, event.y
    boundary_fill(x, y, fill_color, boundary_color)

# Fungsi untuk mengubah warna
def change_color():
    global color
    color = colorchooser.askcolor()[1]

# Fungsi untuk mengubah warna fill
def change_fill_color():
    global fill_color
    fill_color = colorchooser.askcolor()[1]

# Fungsi untuk mengubah ketebalan
def change_thickness(value):
    global thickness
    thickness = int(value)

# Fungsi untuk menghapus canvas
def clear_canvas():
    canvas.delete("all")

# Fungsi untuk mengubah mode gambar
def set_mode(event=None):
    global mode
    mode = shape_var.get()
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if mode == "Circle":
        canvas.bind("<Button-1>", draw_circle)
    elif mode == "Line":
        canvas.bind("<Button-1>", start_line)
        canvas.bind("<B1-Motion>", draw_line)
    elif mode == "Ellipse":
        canvas.bind("<Button-1>", draw_ellipse)

# Fungsi untuk transformasi
def apply_transform():
    transform_type = transform_var.get()
    if transform_type == "Translate":
        dx = simpledialog.askinteger("Input", "Enter translation distance for x:")
        dy = simpledialog.askinteger("Input", "Enter translation distance for y:")
        if dx is not None and dy is not None:
            for item in canvas.find_all():
                canvas.move(item, dx, dy)
    elif transform_type == "Rotate":
        angle = simpledialog.askfloat("Input", "Enter rotation angle (degrees):")
        if angle is not None:
            angle_rad = math.radians(angle)
            for item in canvas.find_all():
                coords = canvas.coords(item)
                if coords:
                    cx = (coords[0] + coords[2]) / 2
                    cy = (coords[1] + coords[3]) / 2
                    new_coords = []
                    for i in range(0, len(coords), 2):
                        x = coords[i] - cx
                        y = coords[i + 1] - cy
                        new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad) + cx
                        new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad) + cy
                        new_coords.extend([new_x, new_y])
                    canvas.coords(item, *new_coords)
    elif transform_type == "Scale":
        sx = simpledialog.askfloat("Input", "Enter scale factor for x:")
        sy = simpledialog.askfloat("Input", "Enter scale factor for y:")
        if sx is not None and sy is not None:
            for item in canvas.find_all():
                coords = canvas.coords(item)
                if coords:
                    cx = (coords[0] + coords[2]) / 2
                    cy = (coords[1] + coords[3]) / 2
                    new_coords = []
                    for i in range(0, len(coords), 2):
                        x = coords[i] - cx
                        y = coords[i + 1] - cy
                        new_x = x * sx + cx
                        new_y = y * sy + cy
                        new_coords.extend([new_x, new_y])
                    canvas.coords(item, *new_coords)

# Inisialisasi Tkinter
root = tk.Tk()
root.title("Paint Program - Grafika Komputer")

# Frame untuk kontrol bentuk, transform, clear, dan save
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Dropdown untuk memilih bentuk
shape_var = tk.StringVar(root)
shape_var.set("Circle")
shape_menu = tk.OptionMenu(top_frame, shape_var, "Circle", "Line", "Ellipse", command=set_mode)
shape_menu.grid(row=0, column=0, padx=5, pady=5)

# Dropdown untuk memilih jenis transformasi
transform_var = tk.StringVar(root)
transform_var.set("Translate")
transform_menu = tk.OptionMenu(top_frame, transform_var, "Translate", "Rotate", "Scale")
transform_menu.grid(row=0, column=1, padx=5, pady=5)

# Tombol untuk menerapkan transformasi
transform_button = tk.Button(top_frame, text="Apply Transform", command=apply_transform)
transform_button.grid(row=0, column=2, padx=5, pady=5)

# Tombol untuk membersihkan canvas
clear_button = tk.Button(top_frame, text="Clear", command=clear_canvas)
clear_button.grid(row=0, column=3, padx=5, pady=5)

# Tombol untuk menyimpan gambar
save_button = tk.Button(top_frame, text="Save", command=save_image)
save_button.grid(row=0, column=4, padx=5, pady=5)

# Frame untuk kontrol warna, fill, dan radius
control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Tombol untuk mengganti warna
color_button = tk.Button(control_frame, text="Choose Color", command=change_color)
color_button.grid(row=0, column=0, padx=5, pady=5)

# Tombol untuk mengganti warna fill
fill_color_button = tk.Button(control_frame, text="Choose Fill Color", command=change_fill_color)
fill_color_button.grid(row=0, column=1, padx=5, pady=5)

# Label dan Entry untuk radius lingkaran dan elips
radius_label = tk.Label(control_frame, text="Radius:")
radius_label.grid(row=0, column=2, padx=5, pady=5)

radius_entry = tk.Entry(control_frame, width=5)
radius_entry.grid(row=0, column=3, padx=5, pady=5)
radius_entry.insert(0, "50")

# Slider untuk ketebalan garis
thickness_slider = tk.Scale(control_frame, from_=1, to_=10, orient=tk.HORIZONTAL, label="Thickness", command=change_thickness)
thickness_slider.grid(row=0, column=4, padx=5, pady=5)

# Canvas untuk menggambar
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Variabel global
color = "black"
fill_color = "white"
boundary_color = "black"
thickness = 1
mode = "circle"  # Default mode

# Mengatur mode default
set_mode()

# Menjalankan Tkinter
root.mainloop()
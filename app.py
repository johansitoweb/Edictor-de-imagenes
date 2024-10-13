import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageDraw

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes")
        self.root.configure(bg='black')

        self.image_label = tk.Label(root, bg='black')
        self.image_label.pack()

        self.canvas = tk.Canvas(root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.btn_frame = tk.Frame(root, bg='black')
        self.btn_frame.pack(side=tk.TOP, fill=tk.X)

        # Cambiar pack() por grid() para organizar los botones
        self.btn_open = tk.Button(self.btn_frame, text="Abrir Imagen", command=self.open_image, bg='gray')
        self.btn_open.grid(row=0, column=0, padx=5, pady=5)

        self.btn_gray = tk.Button(self.btn_frame, text="Escala de Grises", command=self.convert_to_gray, bg='gray')
        self.btn_gray.grid(row=0, column=1, padx=5, pady=5)

        self.btn_brightness = tk.Button(self.btn_frame, text="Ajustar Brillo", command=self.adjust_brightness, bg='gray')
        self.btn_brightness.grid(row=0, column=2, padx=5, pady=5)

        self.btn_contrast = tk.Button(self.btn_frame, text="Ajustar Contraste", command=self.adjust_contrast, bg='gray')
        self.btn_contrast.grid(row=0, column=3, padx=5, pady=5)

        self.btn_rotate = tk.Button(self.btn_frame, text="Rotar Imagen", command=self.rotate_image, bg='gray')
        self.btn_rotate.grid(row=0, column=4, padx=5, pady=5)

        self.btn_draw_rectangle = tk.Button(self.btn_frame, text="Agregar Rectángulo", command=self.add_rectangle, bg='gray')
        self.btn_draw_rectangle.grid(row=0, column=5, padx=5, pady=5)

        self.btn_add_text = tk.Button(self.btn_frame, text="Agregar Texto", command=self.add_text, bg='gray')
        self.btn_add_text.grid(row=0, column=6, padx=5, pady=5)

        self.btn_undo = tk.Button(self.btn_frame, text="Deshacer", command=self.undo, bg='gray')
        self.btn_undo.grid(row=0, column=7, padx=5, pady=5)

        self.btn_zoom_in = tk.Button(self.btn_frame, text="Zoom In", command=self.zoom_in, bg='gray')
        self.btn_zoom_in.grid(row=0, column=8, padx=5, pady=5)

        self.btn_zoom_out = tk.Button(self.btn_frame, text="Zoom Out", command=self.zoom_out, bg='gray')
        self.btn_zoom_out.grid(row=0, column=9, padx=5, pady=5)

        self.btn_save = tk.Button(self.btn_frame, text="Guardar Imagen", command=self.save_image, bg='gray')
        self.btn_save.grid(row=0, column=10, padx=5, pady=5)

        self.image = None
        self.history = []
        self.zoom_level = 1.0

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.history.append(self.image.copy())
            self.display_image(self.image)

    def display_image(self, img):
        img = img.resize((int(img.width * self.zoom_level), int(img.height * self.zoom_level)))
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)
        self.image_label.image = self.tk_image

    def convert_to_gray(self):
        if self.image:
            gray_image = ImageOps.grayscale(self.image)
            self.history.append(self.image.copy())
            self.display_image(gray_image)
            self.image = gray_image

    def adjust_brightness(self):
        if self.image:
            factor = simpledialog.askfloat("Ajustar Brillo", "Factor de brillo (1.0 es original):", minvalue=0.0)
            if factor is not None:
                enhancer = ImageEnhance.Brightness(self.image)
                bright_image = enhancer.enhance(factor)
                self.history.append(self.image.copy())
                self.display_image(bright_image)
                self.image = bright_image

    def adjust_contrast(self):
        if self.image:
            factor = simpledialog.askfloat("Ajustar Contraste", "Factor de contraste (1.0 es original):", minvalue=0.0)
            if factor is not None:
                enhancer = ImageEnhance.Contrast(self.image)
                contrast_image = enhancer.enhance(factor)
                self.history.append(self.image.copy())
                self.display_image(contrast_image)
                self.image = contrast_image

    def rotate_image(self):
        if self.image:
            angle = simpledialog.askfloat("Rotar Imagen", "Ángulo de rotación (grados):")
            if angle is not None:
                rotated_image = self.image.rotate(angle)
                self.history.append(self.image.copy())
                self.display_image(rotated_image)
                self.image = rotated_image

    def add_rectangle(self):
        if self.image:
            x1 = simpledialog.askinteger("Rectángulo", "Coordenada X1:")
            y1 = simpledialog.askinteger("Rectángulo", "Coordenada Y1:")
            x2 = simpledialog.askinteger("Rectángulo", "Coordenada X2:")
            y2 = simpledialog.askinteger("Rectángulo", "Coordenada Y2:")
            if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
                draw = ImageDraw.Draw(self.image)
                draw.rectangle([x1, y1, x2, y2], outline="white", width=3)
                self.history.append(self.image.copy())
                self.display_image(self.image)

    def add_text(self):
        if self.image:
            text = simpledialog.askstring("Agregar Texto", "Texto a agregar:")
            x = simpledialog.askinteger("Posición X", "Coordenada X:")
            y = simpledialog.askinteger("Posición Y", "Coordenada Y:")
            color = colorchooser.askcolor(title="Elige un color")[1]
            if text and x is not None and y is not None and color:
                draw = ImageDraw.Draw(self.image)
                draw.text((x, y), text, fill=color)
                self.history.append(self.image.copy())
                self.display_image(self.image)

    def undo(self):
        if len(self.history) > 1:
            self.history.pop()  # Eliminar la última imagen
            self.image = self.history[-1]  # Volver a la anterior
            self.display_image(self.image)

    def zoom_in(self):
        self.zoom_level *= 1.2
        if self.image:
            self.display_image(self.image)

    def zoom_out(self):
        self.zoom_level /= 1.2
        if self.image:
            self.display_image(self.image)

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                       filetypes=[("PNG files", "*.png"),
                                                                  ("JPEG files", "*.jpg"),
                                                                  ("BMP files", "*.bmp")])
            if file_path:
                self.image.save(file_path)
                messagebox.showinfo("Éxito", "Imagen guardada correctamente.")

if __name__ == "__main__":
    root = tk.Tk()
    editor = ImageEditor(root)
    root.mainloop()

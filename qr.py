import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from fpdf import FPDF

def generar_qr_link():
    link = entry_link.get()
    if link:
        qr = qrcode.make(link)
        mostrar_qr(qr)
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un enlace.")

def generar_qr_datos():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    telefono = entry_telefono.get()
    correo = entry_correo.get()

    if nombre and apellido and telefono and correo:
        datos = f"Nombre: {nombre}\nApellido: {apellido}\nTeléfono: {telefono}\nCorreo: {correo}"
        qr = qrcode.make(datos)
        mostrar_qr(qr)
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

def mostrar_qr(qr):
    qr.save("codigo_qr.png")  # Guarda el QR como PNG
    img = Image.open("codigo_qr.png")
    img_tk = ImageTk.PhotoImage(img)
    
    label_qr.config(image=img_tk)
    label_qr.image = img_tk  # Mantener una referencia a la imagen

def descargar_qr():
    try:
        with open("codigo_qr.png", "rb") as f:
            pass  # Aquí puedes implementar la lógica para descargar el archivo si es necesario
        messagebox.showinfo("Descargar", "Código QR guardado como 'codigo_qr.png'.")
    except FileNotFoundError:
        messagebox.showwarning("Advertencia", "No hay código QR generado para descargar.")
        
def abrir_ventana_imagenes():
    ventana_imagenes = ttk.Toplevel(root)
    ventana_imagenes.title("Subir Imágenes")

    label_imagen = ttk.Label(ventana_imagenes, text="Subir imagen JPG o PNG:")
    label_imagen.pack(pady=10)

    btn_subir = ttk.Button(ventana_imagenes, text="Subir Imagen", command=subir_imagen)
    btn_subir.pack(pady=5)

    btn_convertir = ttk.Button(ventana_imagenes, text="Convertir a PDF", command=convertir_a_pdf)
    btn_convertir.pack(pady=5)

def subir_imagen():
    global imagen_subida
    archivo = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if archivo:
        imagen_subida = Image.open(archivo)
        messagebox.showinfo("Imagen Cargada", "Imagen cargada exitosamente.")

def convertir_a_pdf():
    if 'imagen_subida' in globals():
        pdf = FPDF()
        pdf.add_page()
        
        # Guardar la imagen temporalmente para agregarla al PDF
        imagen_subida.save("imagen_temp.jpg")
        pdf.image("imagen_temp.jpg", x=10, y=10, w=190)  # Ajusta el tamaño según sea necesario
        pdf.output("imagen_convertida.pdf")
        
        messagebox.showinfo("Conversión Completa", "La imagen ha sido convertida a PDF como 'imagen_convertida.pdf'.")
    else:
        messagebox.showwarning("Advertencia", "No hay ninguna imagen cargada para convertir.")

# Crear la ventana principal
root = ttk.Window(themename='cyborg')  # Use ttk.Window for ttkbootstrap themes    
root.title("Generador de Códigos QR")

# Cargar la imagen usando PIL
#imagen = Image.open("./ceo.jpg")
#imagen = imagen.resize((50, 50), Image.LANCZOS)  # Usar Lanczos para redimensionar
#imagen_tk = ImageTk.PhotoImage(imagen)

# Crear un widget Label para mostrar la imagen
#label = ttk.Label(root, image=imagen_tk)
#label.pack()


# Sección para generar QR a partir de un enlace
frame_link = ttk.Frame(root)
frame_link.pack(pady=10)

label_link = ttk.Label(frame_link, text="Ingrese un enlace:")
label_link.pack(side=tk.LEFT)

entry_link = ttk.Entry(frame_link, width=40)
entry_link.pack(side=tk.LEFT)

btn_generar_link = ttk.Button(frame_link, text="Generar QR", command=generar_qr_link)
btn_generar_link.pack(side=tk.LEFT)

# Sección para generar QR a partir de datos personales
frame_datos = ttk.Frame(root)
frame_datos.pack(pady=10)

label_nombre = ttk.Label(frame_datos, text="Nombre:")
label_nombre.grid(row=0, column=0)
entry_nombre = ttk.Entry(frame_datos)
entry_nombre.grid(row=0, column=1)

label_apellido = ttk.Label(frame_datos, text="Apellido:")
label_apellido.grid(row=1, column=0)
entry_apellido = ttk.Entry(frame_datos)
entry_apellido.grid(row=1, column=1)

label_telefono = ttk.Label(frame_datos, text="Teléfono:")
label_telefono.grid(row=2, column=0)
entry_telefono = ttk.Entry(frame_datos)
entry_telefono.grid(row=2, column=1)

label_correo = ttk.Label(frame_datos, text="Correo:")
label_correo.grid(row=3, column=0)
entry_correo = ttk.Entry(frame_datos)
entry_correo.grid(row=3, column=1)

btn_generar_datos = ttk.Button(frame_datos, text="Generar QR", command=generar_qr_datos)
btn_generar_datos.grid(row=4, columnspan=2)

# Sección para mostrar el código QR
label_qr = ttk.Label(root)
label_qr.pack(pady=10)

# Botón para descargar el QR
btn_descargar = ttk.Button(root, text="Descargar QR", command=descargar_qr)
btn_descargar.pack(pady=10)

# Botón para abrir la ventana de imágenes
btn_imagenes = ttk.Button(root, text="Abrir Ventana de Imágenes", command=abrir_ventana_imagenes)
btn_imagenes.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
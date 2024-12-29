import os
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from rembg import remove

def process_images(image_paths, output_folder, progress_callback):
    total_images = len(image_paths)
    for index, image_path in enumerate(image_paths, start=1):
        try:
            with open(image_path, "rb") as file:
                input_image = file.read()
                output_image = remove(input_image)

            image_name = os.path.basename(image_path)
            output_path = os.path.join(output_folder, f"no_bg_{image_name}")

            with open(output_path, "wb") as file:
                file.write(output_image)
        except Exception as e:
            print(f"Erro ao processar {image_path}: {e}")
        finally:
            progress_callback(index, total_images)

def select_images():
    file_paths = ctk.filedialog.askopenfilenames(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
    if file_paths:
        image_paths_entry.delete(0, ctk.END)
        image_paths_entry.insert(0, "; ".join(file_paths))

def select_output_folder():
    folder_path = ctk.filedialog.askdirectory()
    if folder_path:
        output_folder_entry.delete(0, ctk.END)
        output_folder_entry.insert(0, folder_path)

def update_progress(current, total):
    progress_bar.set(current / total)
    progress_label.configure(text=f"Processando {current}/{total} imagens")
    root.update_idletasks()

def start_processing():
    image_paths = image_paths_entry.get().split("; ")
    output_folder = output_folder_entry.get()

    if not image_paths or not output_folder:
        CTkMessagebox(title="Erro", message="Selecione as imagens e a pasta de saída.", icon="cancel", option_1="Fechar")
        return

    try:
        progress_bar.set(0)
        progress_label.configure(text="Iniciando...")
        root.update_idletasks()
        process_images(image_paths, output_folder, update_progress)
        CTkMessagebox(title="Sucesso", message="Imagens processadas com sucesso!", icon="check", option_1="Fechar")
    except Exception as e:
        CTkMessagebox(title="Erro", message=f"Erro ao processar imagens: {e}", icon="cancel", option_1="Fechar")
    finally:
        progress_bar.set(0)
        progress_label.configure(text="")

def center_window_to_display(screen: ctk, width: int, height: int):
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * screen._get_window_scaling())
    y = int(((screen_height/2) - (height/1.5)) * screen._get_window_scaling())
    return f"{width}x{height}+{x}+{y}"

# Configuração da interface
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Remover Fundo de Imagens")
root.geometry(center_window_to_display(root, 400, 500))
root.resizable(False, False)

# Cabeçalho
header_label = ctk.CTkLabel(root, text="Remover Fundo de Imagens", font=("Arial", 24, "bold"))
header_label.pack(pady=20)

# Seleção de imagens
frame_images = ctk.CTkFrame(root)
frame_images.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(frame_images, text="Selecione as imagens:", font=("Arial", 16)).pack(anchor="w", pady=5, padx=10)
image_paths_entry = ctk.CTkEntry(frame_images, placeholder_text="Caminho das imagens...", width=600)
image_paths_entry.pack(pady=5, padx=10)
ctk.CTkButton(frame_images, text="Escolher Imagens", command=select_images).pack(pady=5)

# Seleção da pasta de saída
frame_output = ctk.CTkFrame(root)
frame_output.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(frame_output, text="Selecione a pasta de saída:", font=("Arial", 16)).pack(anchor="w", pady=5, padx=10)
output_folder_entry = ctk.CTkEntry(frame_output, placeholder_text="Caminho da pasta de saída...", width=600)
output_folder_entry.pack(pady=5, padx=10)
ctk.CTkButton(frame_output, text="Escolher Pasta", command=select_output_folder).pack(pady=5)

# Barra de progresso
frame_progress = ctk.CTkFrame(root)
frame_progress.pack(pady=10, padx=20, fill="x")

progress_bar = ctk.CTkProgressBar(frame_progress)
progress_bar.pack(pady=10, fill='x', padx=10)
progress_bar.set(0)
progress_label = ctk.CTkLabel(frame_progress, text="", font=("Arial", 14))
progress_label.pack(pady=5)

# Botão de iniciar
start_button = ctk.CTkButton(root, text="Iniciar", command=start_processing, fg_color="green", hover_color="darkgreen", font=("Arial", 16))
start_button.pack(pady=20)

# Inicializa o programa
root.mainloop()
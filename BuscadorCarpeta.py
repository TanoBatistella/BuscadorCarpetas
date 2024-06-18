import os
import re

def print_complete_project_structure(project_path):
    print("Estructura completa del Proyecto:\n")
    ignored_folders = {'node_modules', 'venv', '__pycache__', '.git', 'dist', 'build'}

    for root, dirs, files in os.walk(project_path):
        # Filtra carpetas innecesarias
        dirs[:] = [d for d in dirs if d not in ignored_folders]

        # Calcula el nivel de indentación
        level = root.replace(project_path, '').count(os.sep)
        indent = ' ' * 4 * (level)

        # Imprime la carpeta actual
        print(f"{indent}- {os.path.basename(root)}/")

        # Calcula el nivel de indentación para los archivos
        subindent = ' ' * 4 * (level + 1)

        # Imprime los archivos dentro de la carpeta actual
        for file_name in files:
            file_path = os.path.join(root, file_name)
            print(f"{subindent}- {file_name}")

    file_needed = input("\n¿Qué archivo necesita? Ingrese el nombre: ")
    file_paths = []
    for root, _, files in os.walk(project_path):
        for file_name in files:
            if file_name == file_needed:
                file_paths.append(os.path.join(root, file_name))
    if len(file_paths) == 1:
        print(f"\nArchivo encontrado: {file_paths[0]}")
        with open(file_paths[0], 'r', encoding='utf-8') as file:
            print("\nContenido del archivo:")
            print(file.read())
    elif len(file_paths) > 1:
        print("\nSe encontraron múltiples archivos con el mismo nombre:")
        for i, file_path in enumerate(file_paths, start=1):
            print(f"{i}. {os.path.relpath(file_path, project_path)}")
        selection = int(input("Seleccione el número del archivo deseado: ")) - 1
        print(f"\nArchivo seleccionado: {file_paths[selection]}")
        with open(file_paths[selection], 'r', encoding='utf-8') as file:
            print("\nContenido del archivo:")
            print(file.read())
    else:
        print(f"\nNo se encontró ningún archivo con el nombre '{file_needed}'.")

def search_folder(project_path, folder_name):
    folder_found = False
    for root, dirs, files in os.walk(project_path):
        if folder_name in dirs:
            folder_path = os.path.join(root, folder_name)
            folder_found = True
            print(f"Carpeta encontrada: {os.path.relpath(folder_path, project_path)}\n")
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    print(f"  - {file_name}")
            break
    if not folder_found:
        print(f"No se encontró la carpeta: {folder_name}")

def search_keyword(project_path, keyword):
    keyword_found = False
    source_code_extensions = ['.js', '.jsx', '.py', '.java']  # Archivos al cual considerar
    ignored_folders = ['node_modules', 'venv']  # Carpetas cúal ignorar

    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in ignored_folders]

        for file_name in files:
            if os.path.splitext(file_name)[1] in source_code_extensions:
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        for line_number, line in enumerate(lines, start=1):
                            if re.search(r'\b{}\b'.format(re.escape(keyword)), line, re.IGNORECASE):
                                if not keyword_found:
                                    print(f"Resultados para la palabra clave '{keyword}':\n")
                                    keyword_found = True
                                print(f"Archivo: {os.path.relpath(file_path, project_path)}, Línea {line_number}:")
                                print(line.strip())
                                print()
                except (UnicodeDecodeError, IsADirectoryError, PermissionError) as e:
                    continue
                except Exception as e:
                    print(f"Error al abrir el archivo {file_path}: {e}")
                    continue
    if not keyword_found:
        print(f"No se encontró la palabra clave: {keyword}")

def print_summary_project_structure(project_path):
    ignored_folders = {'node_modules', 'venv', '__pycache__', '.git', 'dist', 'build'}
    print("Estructura resumida del Proyecto:\n")
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in ignored_folders]
        level = root.replace(project_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}- {os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for dir_name in dirs:
            print(f"{subindent}- {dir_name}/")

if __name__ == "__main__":
    project_path = "C:/Users/tano_.DESKTOP-B9N0NPL/Desktop/CIMAURBANO"
    if os.path.exists(project_path):
        option = input("¿Qué desea hacer? (proyecto completo/proyecto resumido/buscar carpeta/palabra clave): ")
        if option.lower() == "proyecto completo":
            print_complete_project_structure(project_path)
        elif option.lower() == "proyecto resumido":
            print_summary_project_structure(project_path)
        elif option.lower() == "buscar carpeta":
            folder_name = input("Ingrese el nombre de la carpeta que desea buscar: ")
            search_folder(project_path, folder_name)
        elif option.lower() == "palabra clave":
            keyword = input("Ingrese la palabra clave que desea buscar: ")
            search_keyword(project_path, keyword)
        else:
            print("Opción no válida.")
    else:
        print("La ruta del proyecto no es válida.")

def split_file(file_path, chunk_size):
    try:
        with open(file_path, 'rb') as file:
            chunk_number = 0
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break  # Fin del archivo
                output_file_name = f"chunk_{chunk_number}.bin"
                with open(output_file_name, 'wb') as output_file:
                    output_file.write(chunk)
                print(f"Fragmento {chunk_number} guardado en {output_file_name}")
                chunk_number += 1
    except FileNotFoundError:
        print(f"El archivo '{file_path}' no existe.")
      
def merge_chunks(input_directory, output_file):
    try:
        with open(output_file, 'wb') as output:
            chunk_number = 0
            while True:
                chunk_file = f"{input_directory}/chunk_{chunk_number}.bin"
                try:
                    with open(chunk_file, 'rb') as chunk:
                        output.write(chunk.read())
                        print(f"Fragmento {chunk_number} agregado al archivo")
                        chunk_number += 1
                except FileNotFoundError:
                    break  # No hay más fragmentos
    except Exception as e:
        print(f"Error al reensamblar los fragmentos: {e}")
      

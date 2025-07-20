from PIL import Image
import os

# --- CONFIGURACAO ---
# Define a pasta onde estao suas imagens originais
input_folder = "in"

# Define a pasta onde as imagens cortadas serao salvas
output_folder = "out"

# Cria a pasta de saida se ela nao existir
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Pasta '{output_folder}' criada com sucesso.")

files = os.listdir(input_folder)

print(f"\nIniciando o processo em {len(files)} arquivos...")

for filename in files:
    # Checa se o arquivo e uma imagem PNG
    if filename.lower().endswith(('.png')):
        
        # Cria o caminho completo para o arquivo de entrada e saida
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        try:
            # Abre a imagem
            img = Image.open(input_path)
            
            # Converte para RGBA para garantir que a transparencia seja lida corretamente
            img = img.convert("RGBA")
            
            # Pega a "bounding box" (caixa delimitadora) dos pixels que nao sao transparentes
            bbox = img.getbbox()
            
            # Se uma bounding box foi encontrada (a imagem nao esta totalmente vazia)
            if bbox:
                # Corta a imagem usando a bounding box
                img_cortada = img.crop(bbox)
                
                # Salva a nova imagem cortada
                img_cortada.save(output_path)
                print(f" - '{filename}' cortado e salvo com sucesso.")
            else:
                print(f" - ATENCAO: '{filename}' parece estar vazia e foi ignorada.")

        except Exception as e:
            print(f" - ERRO ao processar '{filename}': {e}")

print("\nProcesso concluido! Verifique a pasta 'images_cortadas'.")
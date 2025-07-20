from PIL import Image

idle_path = "Walk.png" # Caminho do arquivo da imagem
output_folder = "./crop_tool/in"
sprite_sheet = Image.open(idle_path)

num_frames = 8 # Número de frames na imagem (ajuste se necessário)
frame_width = sprite_sheet.width // num_frames
frame_height = sprite_sheet.height

for i in range(num_frames):
    box = (i * frame_width, 0, (i + 1) * frame_width, frame_height)
    frame = sprite_sheet.crop(box)
    frame.save(f"{output_folder}enemy_walk_left_{i}.png") #Alterar nome de saida

print("Frames salvos com sucesso!")

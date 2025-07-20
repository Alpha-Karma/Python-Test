import pgzrun
from pgzero.actor import Actor
from pgzero.builtins import music, sounds, keys, images
from pygame import Rect
import random
import time
import math

# --- Constantes do Mundo e da Câmera ---
WIDTH = 800
HEIGHT = 500
GROUND_Y = 450
WORLD_WIDTH = 2400
MENU = 'menu'
PLAYING = 'playing'
EXIT = 'exit'

# --- Variáveis Globais ---
DEBUG_MODE = False
game_state = MENU
game_won = False
game_lost = False
sound_enabled = True
start_time = 0
camera_x = 0

# --- Controles e Botões ---
keys_held = {"left": False, "right": False, "jump": False}
menu_buttons = {
    "start": Rect(300, 150, 200, 50),
    "sound": Rect(300, 220, 200, 50),
    "exit": Rect(300, 290, 200, 50)
}
restart_button = Rect(300, 200, 200, 50)

# --- Inicialização dos Fundos (Backgrounds) ---
sky = Actor("background_sky.jpg")

def check_circle_collision(circle1, circle2):
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance < (r1 + r2)

# --- Classes dos Personagens ---
class Hero:
    def __init__(self, pos):
        self.world_x, self.y = pos
        self.vy = 0
        self.on_ground = False
        self.frame = 0
        self.frame_timer = 0
        self.facing_right = True
        self.was_moving = False
        self.idle_frames = [f"hero_idle_{i}" for i in range(9)]
        self.walk_frames_right = [f"hero_walk_right_{i}" for i in range(5)]
        self.walk_frames_left = [f"hero_walk_left_{i}" for i in range(5)]
        self.sprite = Actor(self.idle_frames[0], pos=(self.world_x, self.y))

    def update(self):
        moving = False
        if keys_held["left"]:
            self.world_x -= 3
            moving = True
            self.facing_right = False
        elif keys_held["right"]:
            self.world_x += 3
            moving = True
            self.facing_right = True

        if moving != self.was_moving:
            self.frame = 0
            self.frame_timer = 0

        if keys_held["jump"] and self.on_ground:
            self.vy = -8
            self.on_ground = False
            if sound_enabled:
                sounds.jump.play()

        self.vy += 0.4
        self.y += self.vy

        expected_y = (GROUND_Y - self.sprite.height / 2) + 8
        if self.y > expected_y:
            self.y = expected_y
            self.vy = 0
            self.on_ground = True

        # Escolhe a lista de frames correta
        if moving:
            frames = self.walk_frames_right if self.facing_right else self.walk_frames_left
        else:
            frames = self.idle_frames

        # Animação
        self.frame_timer += 1
        if self.frame_timer >= 6:
            self.frame = (self.frame + 1) % len(frames)
            self.frame_timer = 0

        self.sprite.image = frames[self.frame]
        self.sprite.pos = (self.world_x, self.y)
        self.was_moving = moving

    def draw(self, camera_x):
        self.sprite.x = self.world_x - camera_x
        self.sprite.draw()

    def get_hitbox_circle(self):
        return (self.world_x, self.sprite.bottom - 30, 15)

    def draw_hitbox_circle(self, screen, camera_x):
        x, y, r = self.get_hitbox_circle()
        screen.draw.filled_circle((x - camera_x, y), r, 'red')

class Enemy:
    def __init__(self, pos):
        self.world_x, self.y = pos
        self.vx = random.choice([-1, 1])
        self.patrol_limit_left = self.world_x - 150
        self.patrol_limit_right = self.world_x + 150
        self.frame = 0
        self.frame_timer = 0

        self.frames_right = [f"enemy_walk_{i}" for i in range(8)]
        self.frames_left = [f"enemy_walk_left_{i}" for i in range(8)]
        self.current_frames = self.frames_right if self.vx > 0 else self.frames_left

        self.sprite = Actor(self.current_frames[0], pos=pos)

    def update(self):
        self.world_x += self.vx
        if self.world_x < self.patrol_limit_left or self.world_x > self.patrol_limit_right:
            self.vx *= -1
            self.current_frames = self.frames_right if self.vx > 0 else self.frames_left
            self.frame = 0

        self.frame_timer += 1
        if self.frame_timer >= 8:
            self.frame = (self.frame + 1) % len(self.current_frames)
            self.frame_timer = 0

        self.sprite.image = self.current_frames[self.frame]
        self.sprite.pos = (self.world_x, self.y)

    def draw(self, camera_x):
        self.sprite.x = self.world_x - camera_x
        self.sprite.draw()

    def get_hitbox_circle(self):
        return (self.world_x, self.sprite.bottom - 40, 20)

    def draw_hitbox_circle(self, screen, camera_x):
        x, y, r = self.get_hitbox_circle()
        screen.draw.filled_circle((x - camera_x, y), r, 'orange')

class Princess:
    def __init__(self, pos):
        self.world_x, self.y = pos
        self.rescued = False
        self.idle_frames = [f"princess_idle_{i}" for i in range(9)]
        self.frame = 0
        self.frame_timer = 0
        self.sprite = Actor(self.idle_frames[0], pos=pos)

    def update(self, hero_hitbox_circle):
        if not self.rescued:
            if check_circle_collision(self.get_hitbox_circle(), hero_hitbox_circle):
                self.rescued = True
                if sound_enabled:
                    sounds.rescue.play()
            
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame = (self.frame + 1) % len(self.idle_frames)
                self.frame_timer = 0
                self.sprite.image = self.idle_frames[self.frame]
        self.sprite.pos = (self.world_x, self.y)

    def draw(self, camera_x):
        self.sprite.x = self.world_x - camera_x
        self.sprite.draw()
            
    def draw_hitbox_circle(self, screen, camera_x):
        x, y, r = self.get_hitbox_circle()
        screen.draw.filled_circle((x - camera_x, y), r, 'green')
    
    def get_hitbox_circle(self):
        return (self.world_x, self.sprite.centery, self.sprite.width / 2)


# --- Funções de Inicialização ---
def init_characters():
    global hero, enemies, princess
    
    temp_hero_sprite = Actor("hero_idle_0")
    hero_y = (GROUND_Y - temp_hero_sprite.height / 2) + 8
    hero = Hero((200, hero_y))

    temp_enemy_sprite = Actor("enemy_walk_0")
    enemy_y = (GROUND_Y - temp_enemy_sprite.height / 2) + 8
    enemies = [Enemy((800, enemy_y)), Enemy((1500, enemy_y))]
    
    temp_princess_sprite = Actor("princess_idle_0")
    princess_y = (GROUND_Y - temp_princess_sprite.height / 2) + 4
    princess = Princess((WORLD_WIDTH - 150, princess_y))

init_characters()

# --- Funções Auxiliares ---
def toggle_music():
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        music.play("bgm")
    else:
        music.stop()

def draw_menu(screen):
    screen.draw.text("MEDIEVAL QUEST", center=(400, 80), fontsize=48, color="gold")
    for label, rect in menu_buttons.items():
        screen.draw.filled_rect(rect, "darkblue")
        screen.draw.text(label.upper(), center=rect.center, fontsize=32, color="white")

def handle_menu_click(pos):
    global game_state, start_time
    if menu_buttons["start"].collidepoint(pos):
        game_state = PLAYING
        start_time = time.time()
        if sound_enabled:
            music.play("bgm")
    elif menu_buttons["sound"].collidepoint(pos):
        toggle_music()
    elif menu_buttons["exit"].collidepoint(pos):
        exit()


# --- Loop Principal ---
def update():
    global game_won, game_lost, camera_x
    if game_state == PLAYING and not (game_won or game_lost):
        hero.update()
        for enemy in enemies:
            enemy.update()
        
        princess.update(hero.get_hitbox_circle())

        for enemy in enemies:
            if check_circle_collision(hero.get_hitbox_circle(), enemy.get_hitbox_circle()):
                game_lost = True
                if sound_enabled:
                    sounds.hit.play()

        if princess.rescued:
            game_won = True

        # CONTROLE DA CÂMERA
        camera_x = hero.world_x - WIDTH / 2
        camera_x = max(0, camera_x)
        camera_x = min(WORLD_WIDTH - WIDTH, camera_x)

def draw():
    screen.clear()
    
    if game_state == MENU:
        draw_menu(screen)
        
    elif game_state == PLAYING:
        # 1. Céu fixo
        sky.center = (WIDTH / 2, HEIGHT / 2)
        sky.draw()

        # 2. Montanhas com parallax
        try:
            parallax_factor = 0.2
            tile_width = images.background_mountains.get_width()
            parallax_offset = camera_x * parallax_factor
            start_x = -(parallax_offset % tile_width)
            num_tiles = (WIDTH // tile_width) + 2
            y_pos_montanha = GROUND_Y - images.background_mountains.get_height() + 80

            for i in range(num_tiles):
                screen.blit("background_mountains", (start_x + i * tile_width, y_pos_montanha))
        except AttributeError:
            # Este bloco só executa se a imagem "background_mountains.png" não for encontrada
            pass

        # 3. Chão com rolagem
        try:
            tile_width = images.tile_ground.get_width()
            start_x = -(camera_x % tile_width)
            num_tiles = (WIDTH // tile_width) + 2
            for i in range(num_tiles):
                screen.blit("tile_ground", (start_x + i * tile_width, GROUND_Y))
        except AttributeError:
            screen.draw.filled_rect(Rect(0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y), (80, 50, 20))

        # 4. Personagens e objetos
        hero.draw(camera_x)
        for enemy in enemies:
            enemy.draw(camera_x)
        princess.draw(camera_x)

        # 5. Hitboxes (se ativado)
        if DEBUG_MODE:
            hero.draw_hitbox_circle(screen, camera_x)
            for enemy in enemies:
                enemy.draw_hitbox_circle(screen, camera_x)
            if not princess.rescued:
                princess.draw_hitbox_circle(screen, camera_x)

        # 6. Interface
        if not (game_won or game_lost):
            elapsed = int(time.time() - start_time)
            screen.draw.text(f"Time: {elapsed}s", topleft=(10, 10), fontsize=30, color="white")

        if game_won:
            screen.draw.text("YOU RESCUED THE PRINCESS!", center=(WIDTH // 2, 100), fontsize=40, color="gold")
            screen.draw.filled_rect(restart_button, "darkred")
            screen.draw.text("RESTART", center=restart_button.center, fontsize=30, color="white")
        elif game_lost:
            screen.draw.text("YOU DIED!", center=(WIDTH // 2, 100), fontsize=40, color="red")
            screen.draw.filled_rect(restart_button, "darkred")
            screen.draw.text("RESTART", center=restart_button.center, fontsize=30, color="white")


def on_mouse_down(pos):
    global game_state, game_won, game_lost, start_time
    if game_state == MENU:
        handle_menu_click(pos)
    elif game_state == PLAYING and (game_won or game_lost):
        if restart_button.collidepoint(pos):
            game_won = False
            game_lost = False
            init_characters()
            start_time = time.time()

def on_key_down(key):
    if key == keys.LEFT:
        keys_held["left"] = True
    elif key == keys.RIGHT:
        keys_held["right"] = True
    elif key == keys.SPACE:
        keys_held["jump"] = True

def on_key_up(key):
    if key == keys.LEFT:
        keys_held["left"] = False
    elif key == keys.RIGHT:
        keys_held["right"] = False
    elif key == keys.SPACE:
        keys_held["jump"] = False

pgzrun.go()
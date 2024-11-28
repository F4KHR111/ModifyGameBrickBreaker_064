# R. Muhammad Fakhri Wirdiyan
# NIM 20230140073
# TAMBAHAN
# 1.Menampilakn menu select level
# 2.Jika Bola Memantul 2 Kali, mengeluarkan tambahan 1 bola di bola yang terpantul
# 3.Membuat Papan Pantulan secara acak di area brick
# 4.Membuat 10 Balok secara acak, jika pecah akan mengeluarkan 5 bola (balok yang memiliki angka 5)
# 5.Membuat menu pause (jika menekan tombol "ESC" ketika game dimainkan)
# 6.Memperbaiki tampilan permainan
# command untuk install game nya yaitu buka terminal di vscode kemudian ketikan "pip install pygame" dan tekan enter, kemudian masukkan kembali "python3 -m pip install pygame" kemudian tekan enter kembali


import pygame
import random
import time
import sys

# Start the game
pygame.init()

size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Brick Breaker Game")

# Colors
GREEN = (28, 252, 106)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (252, 3, 152)
ORANGE = (252, 170, 28)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)

BRICK_COLORS = {
    1: ORANGE,    # Level 1: Oranye
    2: (135, 206, 250),  # Level 2: Biru Muda (Sky Blue)
    3: (128, 0, 128)     # Level 3: Ungu
}

# Ball class to store position and movement for each ball
class Ball:
    def __init__(self, x, y, speed_multiplier=1):
        self.rect = pygame.Rect(x, y, 10, 10)  # Posisi bola
        self.speed_x = random.choice([1, -1]) * random.randint(2, 4) * speed_multiplier
        self.speed_y = random.choice([1, -1]) * random.randint(2, 4) * speed_multiplier
        self.radius = 5  # Ukuran bola (lingkaran)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self):
        # Menggambar bola sebagai lingkaran
        pygame.draw.circle(screen, WHITE, self.rect.center, self.radius)

# Brick class to add attributes to each brick (such as special and value)
class Brick:
    def __init__(self, x, y, special=False, value=1):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.special = special
        self.value = value

# Pause Menu Function
def pause_menu():
    pause_font = pygame.font.Font(None, 74)
    option_font = pygame.font.Font(None, 48)
    
    # Pause title
    pause_text = pause_font.render("PAUSED", True, WHITE)
    pause_rect = pause_text.get_rect(center=(size[0]//2, 150))
    
    # Options
    exit_text = option_font.render("Quit Game", True, WHITE)
    level_text = option_font.render("Return to Level Select", True, WHITE)
    
    exit_rect = exit_text.get_rect(center=(size[0]//2, 300))
    level_rect = level_text.get_rect(center=(size[0]//2, 400))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Resume game
                    return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
                elif level_rect.collidepoint(mouse_pos):
                    return 'level_select'
        
        # Darken the screen
        s = pygame.Surface(size)
        s.set_alpha(128)
        s.fill(BLACK)
        screen.blit(s, (0,0))
        
        # Draw pause elements
        screen.blit(pause_text, pause_rect)
        screen.blit(exit_text, exit_rect)
        screen.blit(level_text, level_rect)
        
        # Highlight options on hover
        mouse_pos = pygame.mouse.get_pos()
        if exit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, DARK_BLUE, exit_rect, 3)
        if level_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, DARK_BLUE, level_rect, 3)
        
        pygame.display.flip()

# Function to create a new game state
def create_game(level):
    speed_multiplier = 1
    if level == 2:
        speed_multiplier = 2
    elif level == 3:
        speed_multiplier = 3

    floor = pygame.Rect(250, 550, 100, 10)
    ball = Ball(floor.x + floor.width // 2 - 5, floor.y - 10, speed_multiplier)
    score = 0

    # Create initial bricks
    bricks = [Brick(x * 20, y * 20) for y in range(10) for x in range(30)]
    
    # Add random bumpers
    bumpers = []
    for i in range(10):
        bumper_width = 50
        bumper_height = 10
        x = random.randint(0, 550)
        y = random.randint(100, 390)
        bumpers.append(pygame.Rect(x, y, bumper_width, bumper_height))
    
    balls = [ball]
    
    # Add special bricks
    special_bricks = random.sample(bricks, 10)
    for brick in special_bricks:
        brick.special = True
        brick.value = 5

    return floor, balls, score, bricks, bumpers, special_bricks, speed_multiplier

# Function to select level
def select_level():
    pygame.init()
    
    # Screen setup
    size = (600, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Brick Breaker - Level Select")
    
    # Colors
    BACKGROUND = (20, 20, 40)  # Deep blue-dark background
    BUTTON_COLORS = {
        'normal': (52, 152, 219),     # Soft blue
        'hover': (41, 128, 185),       # Darker blue
        'text': (255, 255, 255),       # White text
        'shadow': (44, 62, 80)         # Dark shadow
    }
    
    # Fonts
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 48)
    subtitle_font = pygame.font.Font(None, 36)
    
    # Create button class for interactive elements
    class Button:
        def __init__(self, x, y, width, height, text, level):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.level = level
            self.is_hovered = False
        
        def draw(self, surface):
            # Shadow effect
            shadow_rect = self.rect.move(5, 5)
            pygame.draw.rect(surface, BUTTON_COLORS['shadow'], shadow_rect, border_radius=10)
            
            # Button color changes on hover
            color = BUTTON_COLORS['hover'] if self.is_hovered else BUTTON_COLORS['normal']
            pygame.draw.rect(surface, color, self.rect, border_radius=10)
            
            # Text rendering
            text_surf = button_font.render(self.text, True, BUTTON_COLORS['text'])
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
        
        def handle_event(self, event):
            if event.type == pygame.MOUSEMOTION:
                self.is_hovered = self.rect.collidepoint(event.pos)
    
    # Create level buttons
    buttons = [
        Button(100, 250, 400, 70, "Level 1: Normal Speed", 1),
        Button(100, 350, 400, 70, "Level 2: 2x Challenge", 2),
        Button(100, 450, 400, 70, "Level 3: Ultimate Test", 3)
    ]
    
    # Quit button
    quit_button = Button(200, 550, 200, 50, "Quit Game", None)
    
    # Background stars
    stars = [(pygame.math.Vector2(
        (x * 100 + random.randint(-50, 50)) % 600, 
        (y * 100 + random.randint(-50, 50)) % 600
    ), random.randint(1, 3)) for x in range(6) for y in range(6)]
    
    clock = pygame.time.Clock()
    
    while True:
        screen.fill(BACKGROUND)
        
        # Draw twinkling stars
        for star_pos, size in stars:
            pygame.draw.circle(screen, (255, 255, 255), 
                               (int(star_pos.x), int(star_pos.y)), 
                               size, size)
        
        # Title
        title = title_font.render("BRICK BREAKER", True, (255, 255, 255))
        title_rect = title.get_rect(center=(300, 100))
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = subtitle_font.render("Choose Your Challenge", True, (200, 200, 255))
        subtitle_rect = subtitle.get_rect(center=(300, 170))
        screen.blit(subtitle, subtitle_rect)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for button in buttons + [quit_button]:
                button.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        return button.level
                
                if quit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        # Draw buttons
        for button in buttons:
            button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)


# Ask for player name
def ask_ready():
    font = pygame.font.Font(None, 48)
    yes_button = pygame.Rect(150, 300, 120, 50)
    no_button = pygame.Rect(330, 300, 120, 50)
    clock = pygame.time.Clock()

    while True:
        draw_background()

        # Draw the question text
        question_text = font.render("Are you ready?", True, WHITE)
        question_rect = question_text.get_rect(center=(size[0] // 2, 200))
        screen.blit(question_text, question_rect)

        # Draw the buttons
        pygame.draw.rect(screen, GREEN, yes_button)
        pygame.draw.rect(screen, RED, no_button)

        # Add text to the buttons
        yes_text = font.render("Yes", True, BLACK)
        no_text = font.render("No", True, BLACK)
        screen.blit(yes_text, yes_button.move(30, 10))
        screen.blit(no_text, no_button.move(30, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button.collidepoint(mouse_pos):
                    return True  # Start the game
                elif no_button.collidepoint(mouse_pos):
                    return False  # Return to level select

        pygame.display.flip()
        clock.tick(30)

def draw_background():
    screen.fill((20, 20, 40))  # Background color (dark blue)
    stars = [(pygame.Vector2(random.randint(0, 800), random.randint(0, 600)), random.randint(1, 3)) for _ in range(50)]
    # Simulate moving stars
    for star_pos, size in stars:
        pygame.draw.circle(screen, (255, 255, 255), 
                           (int(star_pos.x), int(star_pos.y)), 
                           size, size)
        star_pos.y += 0.5  # Move stars down
        if star_pos.y > 600:
            star_pos.y = random.randint(-50, 0)

def draw_bumpers(bumpers):
    for bumper in bumpers:
        pygame.draw.rect(screen, GRAY, bumper)

def draw_brick(bricks, font, level):
    for brick in bricks:
        # Pilih warna berdasarkan level
        color = PINK if brick.special else BRICK_COLORS[level]
        pygame.draw.rect(screen, color, brick.rect)
        
        # Jika brick spesial, tampilkan nilai pada brick
        if brick.special:
            value_text = font.render(str(brick.value), True, BLACK)
            text_rect = value_text.get_rect(center=brick.rect.center)
            screen.blit(value_text, text_rect)

# Ubah fungsi run_game untuk memastikan brick ditambahkan setiap 10 - 5 detik dengan tingkatan level berbeda
def run_game():
    level = select_level()
    if level is None:
        return  # User keluar dari permainan
    is_ready = ask_ready()
    if not is_ready:
        return
    
    floor, balls, score, bricks, bumpers, special_bricks, speed_multiplier = create_game(level)

    bricks_broken = 0
    last_brick_time = time.time()  # Waktu terakhir baris brick ditambahkan

    # Font untuk rendering nilai pada brick
    brick_font = pygame.font.Font(None, 12)

    # Tentukan interval penambahan brick berdasarkan level
    if level == 1:
        brick_interval = 10  # Level 1, tambahkan setiap 10 detik
    elif level == 2:
        brick_interval = 7  # Level 2, tambahkan setiap 7 detik
    elif level == 3:
        brick_interval = 5  # Level 3, tambahkan setiap 5 detik

    while True:
        current_time = time.time()

        # Tambahkan baris brick berdasarkan interval waktu yang sudah ditentukan
        if current_time - last_brick_time >= brick_interval:
            new_row = [Brick(x * 20, 0, special=random.random() < 0.2, value=5 if random.random() < 0.2 else 1)
                       for x in range(30)]
            for brick in bricks:
                brick.rect.y += 20  # Geser brick yang sudah ada ke bawah
            bricks.extend(new_row)  # Tambahkan baris baru di atas
            last_brick_time = current_time  # Reset waktu penambahan baris brick

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_result = pause_menu()
                    if pause_result == 'level_select':
                        return  # Kembali ke pemilihan level

        screen.fill(BLACK)
        pygame.draw.rect(screen, PINK, floor)

        font = pygame.font.Font(None, 24)
        text = font.render(f"CURRENT SCORE: {score} (Level {level})", 1, WHITE)
        screen.blit(text, (10, 570))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and floor.x < 500:
            floor.x += 13.5
        if keys[pygame.K_LEFT] and floor.x > 0:
            floor.x -= 13.5

        # Gambar bricks dan bumpers
        draw_brick(bricks, brick_font, level)
        draw_bumpers(bumpers)

        for ball in balls:
            ball.move()

            if ball.rect.x > 590 or ball.rect.x < 0:
                ball.speed_x = -ball.speed_x
            if ball.rect.y <= 3:
                ball.speed_y = -ball.speed_y
            if floor.collidepoint(ball.rect.x, ball.rect.y):
                ball.speed_y = -ball.speed_y

            for bumper in bumpers:
                if bumper.collidepoint(ball.rect.x, ball.rect.y):
                    ball.speed_y = -ball.speed_y

            ball.draw()

            hit_bricks = []
            for brick in bricks:
                if brick.rect.collidepoint(ball.rect.x, ball.rect.y):
                    hit_bricks.append(brick)
                    ball.speed_x = -ball.speed_x
                    ball.speed_y = -ball.speed_y
                    score += brick.value
                    bricks_broken += 1

                    if brick.special:
                        for _ in range(5):
                            new_ball = Ball(ball.rect.x, ball.rect.y, speed_multiplier)
                            balls.append(new_ball)

            for brick in hit_bricks:
                bricks.remove(brick)

            if bricks_broken >= 2:
                new_ball = Ball(balls[0].rect.x, balls[0].rect.y, speed_multiplier)
                balls.append(new_ball)
                bricks_broken = 0

            balls = [ball for ball in balls if ball.rect.y < 600]

            if not balls:
                font_lost = pygame.font.Font(None, 74)
                text_lost = font_lost.render("YOU LOST!", 1, RED)
                screen.blit(text_lost, (150, 300))
                pygame.display.flip()
                pygame.time.delay(3000)
                return

            if not bricks:
                font_won = pygame.font.Font(None, 48)
                text_won = font_won.render("YOU WON THE GAME", 1, GREEN)
                text_rect = text_won.get_rect(center=(size[0] // 2, size[1] // 2))
                screen.blit(text_won, text_rect)
                pygame.display.flip()
                pygame.time.delay(3000)
                return

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Main game loop
def main():
    while True:
        run_game()

# Start the game
if __name__ == "__main__":
    main()
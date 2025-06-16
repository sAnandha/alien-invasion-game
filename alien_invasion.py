import pygame
import sys
import random
import time
import os
import urllib.request
from pygame.locals import *

# Initialize pygame
pygame.init()

# Get the user's screen info for responsive design
screen_info = pygame.display.Info()
USER_SCREEN_WIDTH = screen_info.current_w
USER_SCREEN_HEIGHT = screen_info.current_h

# Set game dimensions based on screen size (responsive)
# Use 80% of screen size or fallback to standard size if detection fails
try:
    SCREEN_WIDTH = min(int(USER_SCREEN_WIDTH * 0.8), 1600)
    SCREEN_HEIGHT = min(int(USER_SCREEN_HEIGHT * 0.8), 900)
except:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

# Scale factor for responsive elements (based on reference resolution of 800x600)
SCALE_X = SCREEN_WIDTH / 800
SCALE_Y = SCREEN_HEIGHT / 600

# Function to scale values based on screen size
def scale_value(value, is_horizontal=True):
    return int(value * (SCALE_X if is_horizontal else SCALE_Y))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
BRIGHT_YELLOW = (255, 255, 0)
NEON_PINK = (255, 20, 147)
DEEP_BLUE = (0, 0, 100)

# Game states
MENU = 0
GAME = 1
GAME_OVER = 2
VICTORY = 3

# Create images directory if it doesn't exist
if not os.path.exists('game_images'):
    os.makedirs('game_images')

# Function to download images
def download_image(url, filename):
    if not os.path.exists(f'game_images/{filename}'):
        try:
            urllib.request.urlretrieve(url, f'game_images/{filename}')
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")
            return False
    return True

# Download necessary images
image_urls = {
    'spaceship': 'https://raw.githubusercontent.com/clear-code-projects/Space-invaders/main/graphics/player.png',
    'alien1': 'https://raw.githubusercontent.com/clear-code-projects/Space-invaders/main/graphics/red.png',
    'alien2': 'https://raw.githubusercontent.com/clear-code-projects/Space-invaders/main/graphics/green.png',
    'alien3': 'https://raw.githubusercontent.com/clear-code-projects/Space-invaders/main/graphics/yellow.png',
    'bullet': 'https://cdn-icons-png.flaticon.com/512/5610/5610944.png',
    'background': 'https://img.freepik.com/premium-vector/space-game-background-neon-night-alien-landscape_107791-1624.jpg',
    'powerup': 'https://raw.githubusercontent.com/clear-code-projects/Space-invaders/main/graphics/extra.png',
    'heart_powerup': 'https://cdn-icons-png.flaticon.com/512/833/833472.png'
}

for name, url in image_urls.items():
    download_image(url, f"{name}.png")

class Game:
    def __init__(self):
        # Create a responsive window that can be resized
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Alien Invasion')
        self.clock = pygame.time.Clock()
        
        # Load custom gaming font
        self.load_fonts()
        
        # Game variables
        self.state = MENU
        self.score = 0
        self.high_score = self.load_high_score()
        self.lives = 3
        self.max_lives = 3  # Maximum number of lives
        self.target_score = 250  # Player wins when reaching this score
        
        # Load images
        self.load_images()
        
        # Create player
        self.player = Player(self.player_img)
        
        # Create enemy group
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        # Menu selection
        self.menu_selection = 0
        self.menu_options = ["New Game", "High Score", "Exit"]
        
        # Background
        self.background = self.load_background()
        self.menu_background = self.load_menu_background()
        
        # Handle window resize events
        self.last_window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        
    def load_fonts(self):
        """Load custom gaming fonts or use system fonts as fallback"""
        try:
            # Try to download a gaming font if not already downloaded
            font_url = "https://github.com/google/fonts/raw/main/ofl/pressstart2p/PressStart2P-Regular.ttf"
            if not os.path.exists('game_images/game_font.ttf'):
                try:
                    urllib.request.urlretrieve(font_url, 'game_images/game_font.ttf')
                    print("Downloaded game font")
                except Exception as e:
                    print(f"Failed to download font: {e}")
            
            # Load the custom font if available
            if os.path.exists('game_images/game_font.ttf'):
                base_size = scale_value(16, False)
                self.font_large = pygame.font.Font('game_images/game_font.ttf', base_size * 2)
                self.font_medium = pygame.font.Font('game_images/game_font.ttf', base_size)
                self.font_small = pygame.font.Font('game_images/game_font.ttf', int(base_size * 0.75))
            else:
                raise FileNotFoundError("Custom font not found")
        except:
            # Fallback to system fonts
            self.font_large = pygame.font.SysFont('Arial', scale_value(48, False))
            self.font_medium = pygame.font.SysFont('Arial', scale_value(36, False))
            self.font_small = pygame.font.SysFont('Arial', scale_value(24, False))
            
    def load_menu_background(self):
        """Create a custom space background for the menu"""
        # Create a custom space background
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill(BLACK)
        
        # Create a responsive starfield with more stars for menu
        star_count = int((SCREEN_WIDTH * SCREEN_HEIGHT) / 1500)  # More stars for menu
        for _ in range(star_count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randint(1, 4)
            color = random.choice([WHITE, CYAN, BRIGHT_YELLOW])
            pygame.draw.circle(bg, color, (x, y), radius)
            
        # Add some nebula-like effects
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randint(50, 150)
            color = random.choice([(20, 0, 40, 50), (0, 20, 40, 50), (40, 0, 20, 50)])
            
            # Create a surface with per-pixel alpha
            nebula = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(nebula, color, (radius, radius), radius)
            bg.blit(nebula, (x-radius, y-radius))
            
        # Add a planet
        planet_radius = scale_value(80)
        planet_x = SCREEN_WIDTH - planet_radius - scale_value(50)
        planet_y = scale_value(100, False)
        
        # Draw planet
        planet = pygame.Surface((planet_radius*2, planet_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(planet, (150, 100, 50), (planet_radius, planet_radius), planet_radius)
        
        # Add some details to the planet
        for _ in range(15):
            detail_x = random.randint(0, planet_radius*2)
            detail_y = random.randint(0, planet_radius*2)
            detail_radius = random.randint(5, 15)
            distance = ((detail_x - planet_radius)**2 + (detail_y - planet_radius)**2)**0.5
            if distance < planet_radius:
                pygame.draw.circle(planet, (120, 80, 40), (detail_x, detail_y), detail_radius)
        
        bg.blit(planet, (planet_x - planet_radius, planet_y - planet_radius))
        
        return bg
        
        # Game variables
        self.state = MENU
        self.score = 0
        self.high_score = self.load_high_score()
        self.lives = 3
        self.target_score = 200  # Player wins when reaching this score
        
        # Load images
        self.load_images()
        
        # Create player
        self.player = Player(self.player_img)
        
        # Create enemy group
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        # Menu selection
        self.menu_selection = 0
        self.menu_options = ["New Game", "High Score", "Exit"]
        
        # Background
        self.background = self.load_background()
        
        # Handle window resize events
        self.last_window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        
    def handle_resize(self, new_width, new_height):
        """Handle window resize events to make the game responsive"""
        global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y
        
        # Update screen dimensions
        SCREEN_WIDTH = max(new_width, 400)  # Minimum width
        SCREEN_HEIGHT = max(new_height, 300)  # Minimum height
        
        # Update scale factors
        SCALE_X = SCREEN_WIDTH / 800
        SCALE_Y = SCREEN_HEIGHT / 600
        
        # Update the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        
        # Reload backgrounds to fit new dimensions
        self.background = self.load_background()
        self.menu_background = self.load_menu_background()
        
        # Update font sizes
        self.load_fonts()
        
        # Reset player position
        self.player.rect.centerx = SCREEN_WIDTH // 2
        self.player.rect.bottom = SCREEN_HEIGHT - scale_value(10, False)
        
    def load_background(self):
        try:
            bg = pygame.image.load('game_images/background.png').convert()
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            return bg
        except:
            # Fallback to a simple background
            bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            bg.fill(BLACK)
            
            # Create a responsive starfield
            star_count = int((SCREEN_WIDTH * SCREEN_HEIGHT) / 5000)  # Adjust star density based on screen size
            for _ in range(star_count):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                radius = random.randint(1, 3)
                pygame.draw.circle(bg, WHITE, (x, y), radius)
            return bg
        
    def load_images(self):
        # Load player image (spaceship)
        try:
            self.player_img = pygame.image.load('game_images/spaceship.png').convert_alpha()
            self.player_img = pygame.transform.scale(self.player_img, (scale_value(50), scale_value(50, False)))
        except:
            self.player_img = pygame.Surface((scale_value(50), scale_value(50, False)), pygame.SRCALPHA)
            pygame.draw.polygon(self.player_img, BLUE, [(scale_value(25), 0), (0, scale_value(50, False)), (scale_value(50), scale_value(50, False))])
        
        # Load enemy images (aliens)
        enemy_size = (scale_value(40), scale_value(40, False))
        try:
            self.enemy_img_10 = pygame.image.load('game_images/alien1.png').convert_alpha()
            self.enemy_img_10 = pygame.transform.scale(self.enemy_img_10, enemy_size)
            
            self.enemy_img_30 = pygame.image.load('game_images/alien2.png').convert_alpha()
            self.enemy_img_30 = pygame.transform.scale(self.enemy_img_30, enemy_size)
            
            self.enemy_img_50 = pygame.image.load('game_images/alien3.png').convert_alpha()
            self.enemy_img_50 = pygame.transform.scale(self.enemy_img_50, enemy_size)
        except:
            self.enemy_img_10 = pygame.Surface(enemy_size, pygame.SRCALPHA)
            pygame.draw.circle(self.enemy_img_10, GREEN, (enemy_size[0]//2, enemy_size[1]//2), enemy_size[0]//2)
            
            self.enemy_img_30 = pygame.Surface(enemy_size, pygame.SRCALPHA)
            pygame.draw.circle(self.enemy_img_30, RED, (enemy_size[0]//2, enemy_size[1]//2), enemy_size[0]//2)
            
            self.enemy_img_50 = pygame.Surface(enemy_size, pygame.SRCALPHA)
            pygame.draw.circle(self.enemy_img_50, BLUE, (enemy_size[0]//2, enemy_size[1]//2), enemy_size[0]//2)
        
        # Load bullet image
        bullet_size = (scale_value(10), scale_value(20, False))
        try:
            self.bullet_img = pygame.image.load('game_images/bullet.png').convert_alpha()
            self.bullet_img = pygame.transform.scale(self.bullet_img, bullet_size)
        except:
            self.bullet_img = pygame.Surface(bullet_size, pygame.SRCALPHA)
            pygame.draw.rect(self.bullet_img, RED, (0, 0, bullet_size[0], bullet_size[1]))
        
        # Load powerup images
        powerup_size = (scale_value(30), scale_value(30, False))
        try:
            self.powerup_img = pygame.image.load('game_images/powerup.png').convert_alpha()
            self.powerup_img = pygame.transform.scale(self.powerup_img, powerup_size)
            
            self.heart_powerup_img = pygame.image.load('game_images/heart_powerup.png').convert_alpha()
            self.heart_powerup_img = pygame.transform.scale(self.heart_powerup_img, powerup_size)
        except:
            self.powerup_img = pygame.Surface(powerup_size, pygame.SRCALPHA)
            pygame.draw.rect(self.powerup_img, CYAN, (0, 0, powerup_size[0], powerup_size[1]))
            
            self.heart_powerup_img = pygame.Surface(powerup_size, pygame.SRCALPHA)
            pygame.draw.circle(self.heart_powerup_img, RED, (powerup_size[0]//2, powerup_size[1]//2), powerup_size[0]//2)
            
        # Create heart images for lives
        heart_size = scale_value(20)
        self.heart_full = pygame.Surface((heart_size, heart_size), pygame.SRCALPHA)
        self.heart_empty = pygame.Surface((heart_size, heart_size), pygame.SRCALPHA)
        
        # Draw heart shape - scale the points based on screen size
        points = []
        base_points = [(10, 0), (13, 3), (16, 5), (18, 8), (19, 12), 
                      (18, 15), (16, 17), (13, 19), (10, 20), 
                      (7, 19), (4, 17), (2, 15), (1, 12), 
                      (2, 8), (4, 5), (7, 3)]
                      
        for x, y in base_points:
            points.append((int(x * heart_size / 20), int(y * heart_size / 20)))
        
        # Full heart (red)
        pygame.draw.polygon(self.heart_full, RED, points)
        
        # Empty heart (outline only)
        pygame.draw.polygon(self.heart_empty, RED, points, 1)
        
    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
        except:
            return 0
            
    def save_high_score(self):
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))
            
    def spawn_enemies(self):
        # Clear existing enemies
        self.enemies.empty()
        
        # Spawn enemies with different point values
        for _ in range(5):  # 10-point enemies
            enemy = Enemy(self.enemy_img_10, 10)
            self.enemies.add(enemy)
            
        for _ in range(3):  # 30-point enemies
            enemy = Enemy(self.enemy_img_30, 30)
            self.enemies.add(enemy)
            
        for _ in range(2):  # 50-point enemies
            enemy = Enemy(self.enemy_img_50, 50)
            self.enemies.add(enemy)
            
    def spawn_powerup(self):
        if random.random() < 0.01:  # 1% chance to spawn a powerup
            powerup_type = random.choice(["speed", "rapid_fire", "heart"])
            
            if powerup_type == "heart":
                powerup = PowerUp(self.heart_powerup_img, "heart")
            else:
                powerup = PowerUp(self.powerup_img, powerup_type)
                
            self.powerups.add(powerup)
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            # Handle window resize events
            elif event.type == VIDEORESIZE:
                self.handle_resize(event.w, event.h)
                
            if self.state == MENU:
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
                    elif event.key == K_DOWN:
                        self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
                    elif event.key == K_RETURN:
                        if self.menu_selection == 0:  # New Game
                            self.state = GAME
                            self.score = 0
                            self.lives = 3
                            self.player.reset()
                            self.spawn_enemies()
                        elif self.menu_selection == 1:  # High Score
                            pass  # Just display high score on menu
                        elif self.menu_selection == 2:  # Exit
                            pygame.quit()
                            sys.exit()
            
            elif self.state == GAME:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.player.shoot(self.bullets, self.bullet_img)
                        
            elif self.state == GAME_OVER or self.state == VICTORY:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.state = MENU
                    
    def update(self):
        if self.state == GAME:
            # Update player
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            
            # Update bullets
            self.bullets.update()
            
            # Update enemies
            self.enemies.update()
            
            # Update powerups
            self.powerups.update()
            self.spawn_powerup()
            
            # Check for bullet-enemy collisions
            hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
            for hit in hits:
                for enemy in hits[hit]:
                    self.score += enemy.points
                
            # Check for player-enemy collisions
            if pygame.sprite.spritecollide(self.player, self.enemies, True):
                self.lives -= 1
                if self.lives <= 0:
                    self.state = GAME_OVER
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
                        
            # Check for player-powerup collisions
            powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
            for powerup in powerup_hits:
                if powerup.powerup_type == "speed":
                    self.player.speed_boost()
                elif powerup.powerup_type == "rapid_fire":
                    self.player.rapid_fire()
                elif powerup.powerup_type == "heart" and self.lives < self.max_lives:
                    self.lives += 1
                    
            # Check if player reached target score
            if self.score >= self.target_score:
                self.state = VICTORY
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                    
            # Spawn new enemies if all are defeated
            if len(self.enemies) == 0:
                self.spawn_enemies()
                
    def draw(self):
        # Draw appropriate background based on game state
        if self.state == MENU:
            self.screen.blit(self.menu_background, (0, 0))
            
            # Draw title with glow effect
            y_offset = scale_value(100, False)
            title_shadow = self.font_large.render("ALIEN INVASION", True, DEEP_BLUE)
            title = self.font_large.render("ALIEN INVASION", True, BRIGHT_YELLOW)
            
            # Draw shadow slightly offset for glow effect
            self.screen.blit(title_shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 2, y_offset + 2))
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, y_offset))
            
            # Draw menu options with better colors
            for i, option in enumerate(self.menu_options):
                if i == self.menu_selection:
                    # Selected option gets a highlight effect
                    glow = self.font_medium.render(option, True, NEON_PINK)
                    text = self.font_medium.render(option, True, BRIGHT_YELLOW)
                    # Draw a rectangle behind selected option
                    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, scale_value(280 + i * 60, False)))
                    pygame.draw.rect(self.screen, (50, 0, 50, 128), 
                                    text_rect.inflate(scale_value(20), scale_value(10, False)), 
                                    border_radius=scale_value(5))
                else:
                    glow = None
                    text = self.font_medium.render(option, True, CYAN)
                
                # Center the text
                text_x = SCREEN_WIDTH//2 - text.get_width()//2
                text_y = scale_value(280 + i * 60, False)
                
                # Draw glow effect for selected item
                if glow:
                    self.screen.blit(glow, (text_x + 1, text_y + 1))
                
                self.screen.blit(text, (text_x, text_y))
                
            # Draw high score
            high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, BRIGHT_YELLOW)
            self.screen.blit(high_score_text, (SCREEN_WIDTH//2 - high_score_text.get_width()//2, SCREEN_HEIGHT - scale_value(50, False)))
            
        elif self.state == GAME:
            # Draw game background
            self.screen.blit(self.background, (0, 0))
            
            # Draw player
            self.screen.blit(self.player.image, self.player.rect)
            
            # Draw bullets
            self.bullets.draw(self.screen)
            
            # Draw enemies
            self.enemies.draw(self.screen)
            
            # Draw powerups
            self.powerups.draw(self.screen)
            
            # Draw HUD
            score_text = self.font_small.render(f"Score: {self.score} / {self.target_score}", True, BRIGHT_YELLOW)
            self.screen.blit(score_text, (scale_value(10), scale_value(10, False)))
            
            # Draw lives as hearts - only show 3 hearts max
            for i in range(self.max_lives):  # Maximum 3 hearts
                if i < self.lives:
                    self.screen.blit(self.heart_full, (scale_value(10 + i * 25), scale_value(40, False)))
                else:
                    self.screen.blit(self.heart_empty, (scale_value(10 + i * 25), scale_value(40, False)))
            
        elif self.state == GAME_OVER:
            # Draw game background
            self.screen.blit(self.background, (0, 0))
            
            game_over_text = self.font_large.render("GAME OVER", True, RED)
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - scale_value(100, False)))
            
            score_text = self.font_medium.render(f"Final Score: {self.score}", True, CYAN)
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
            
            continue_text = self.font_small.render("Press ENTER to continue", True, WHITE)
            self.screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + scale_value(100, False)))
            
        elif self.state == VICTORY:
            # Draw game background
            self.screen.blit(self.background, (0, 0))
            
            victory_text = self.font_large.render("VICTORY!", True, BRIGHT_YELLOW)
            self.screen.blit(victory_text, (SCREEN_WIDTH//2 - victory_text.get_width()//2, SCREEN_HEIGHT//2 - scale_value(100, False)))
            
            score_text = self.font_medium.render(f"Final Score: {self.score}", True, CYAN)
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
            
            continue_text = self.font_small.render("Press ENTER to continue", True, WHITE)
            self.screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + scale_value(100, False)))
            
        pygame.display.flip()
        
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - scale_value(10, False)
        self.speed = scale_value(5)  # Scale speed based on screen width
        self.normal_speed = scale_value(5)
        self.cooldown = 0
        self.normal_cooldown = 20
        self.rapid_fire_timer = 0
        self.speed_boost_timer = 0
        
    def update(self, keys):
        # Movement
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            
        # Cooldown for shooting
        if self.cooldown > 0:
            self.cooldown -= 1
            
        # Handle power-up timers
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer == 0:
                self.cooldown = self.normal_cooldown
                
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0:
                self.speed = self.normal_speed
                
    def shoot(self, bullets_group, bullet_img):
        if self.cooldown == 0:
            bullet = Bullet(bullet_img, self.rect.centerx, self.rect.top)
            bullets_group.add(bullet)
            self.cooldown = 5 if self.rapid_fire_timer > 0 else self.normal_cooldown
            
    def reset(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - scale_value(10, False)
        self.speed = self.normal_speed
        self.cooldown = 0
        self.rapid_fire_timer = 0
        self.speed_boost_timer = 0
        
    def rapid_fire(self):
        self.rapid_fire_timer = 300  # 5 seconds at 60 FPS
        self.cooldown = 5
        
    def speed_boost(self):
        self.speed_boost_timer = 300  # 5 seconds at 60 FPS
        self.speed = self.normal_speed * 2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, points):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-scale_value(100, False), -scale_value(40, False))
        self.points = points
        
        # Set speed based on points (higher points = faster enemies)
        # Scale speed based on screen height
        base_speed = 0
        if points == 10:
            base_speed = 2
        elif points == 30:
            base_speed = 3
        else:  # 50 points
            base_speed = 4
            
        self.speed = scale_value(base_speed, False)
        
    def update(self):
        self.rect.y += self.speed
        
        # If enemy goes off screen, reset position
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-scale_value(100, False), -scale_value(40, False))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -scale_value(10, False)  # Scale speed based on screen height
        
    def update(self):
        self.rect.y += self.speed
        
        # Remove bullet if it goes off screen
        if self.rect.bottom < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image, powerup_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = scale_value(3, False)  # Scale speed based on screen height
        self.powerup_type = powerup_type
        
    def update(self):
        self.rect.y += self.speed
        
        # Remove powerup if it goes off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

if __name__ == "__main__":
    game = Game()
    game.run()

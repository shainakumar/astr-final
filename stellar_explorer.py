import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stellar Explorer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.SysFont("Arial", 16)

# Load placeholder images (you should replace these with real sprites later)
player_img = pygame.Surface((50, 50))
player_img.fill(WHITE)

star_img = pygame.Surface((20, 20))
star_img.fill(RED)

hazard_img = pygame.Surface((25, 25))
hazard_img.fill(YELLOW)

# HR Diagram Overlay (static visual placeholder for now)
hr_diagram = pygame.Surface((300, 200))
hr_diagram.fill(GRAY)
hr_pos = (WIDTH - 320, 20)

# Weighted star types for realism
STAR_TYPES = [
    ("Main Sequence", 0.4),
    ("Red Giant", 0.1),
    ("Blue Giant", 0.05),
    ("Red Supergiant", 0.05),
    ("Blue Supergiant", 0.02),
    ("White Dwarf", 0.1),
    ("Brown Dwarf", 0.05),
    ("Subgiant", 0.05),
    ("Neutron Star", 0.01),
    ("Protostar", 0.12),
    ("The Sun", 0.05),
]

def weighted_star_type():
    choices, weights = zip(*STAR_TYPES)
    return random.choices(choices, weights)[0]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Star class
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = star_img.copy()
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.star_type = weighted_star_type()
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Hazard class
class Hazard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = hazard_img.copy()
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.hazard_type = random.choice(["Black Hole", "Pulsar", "Quasar", "Supernova"])
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Card popup
class Popup:
    def __init__(self, text):
        self.text = text
        self.active = True
        self.timer = 180  # display for 3 seconds

    def draw(self, surface):
        if self.active:
            box = pygame.Surface((300, 100))
            box.fill((250, 250, 210))
            pygame.draw.rect(box, BLACK, box.get_rect(), 2)
            lines = self.text.split('\n')
            for i, line in enumerate(lines):
                rendered = font.render(line, True, BLACK)
                box.blit(rendered, (10, 10 + 20 * i))
            surface.blit(box, (20, HEIGHT - 120))
            self.timer -= 1
            if self.timer <= 0:
                self.active = False

# Groups and setup
player = Player()
all_sprites = pygame.sprite.Group()
stars = pygame.sprite.Group()
hazards = pygame.sprite.Group()
all_sprites.add(player)

# Game state
collected_cards = []
popup = None

def reset_player():
    player.rect.center = (WIDTH // 2, HEIGHT // 2)

def spawn_star():
    star = Star()
    all_sprites.add(star)
    stars.add(star)

def spawn_hazard():
    hazard = Hazard()
    all_sprites.add(hazard)
    hazards.add(hazard)

# Game loop
clock = pygame.time.Clock()
running = True
spawn_timer = 0
hazard_timer = 0

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(keys)
    stars.update()
    hazards.update()

    spawn_timer += 1
    hazard_timer += 1

    if spawn_timer > 60:
        spawn_star()
        spawn_timer = 0

    if hazard_timer > 300:
        spawn_hazard()
        hazard_timer = 0

    # Collision detection with stars
    hits = pygame.sprite.spritecollide(player, stars, True)
    for hit in hits:
        collected_cards.append(hit.star_type)
        popup = Popup(f"You discovered a {hit.star_type} star!\nAdded to HR Diagram and Cards.")

    # Collision detection with hazards
    dangers = pygame.sprite.spritecollide(player, hazards, False)
    if dangers:
        popup = Popup(f"Danger! You hit a {dangers[0].hazard_type}!\nTeleporting to safe zone.")
        reset_player()

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)
    screen.blit(hr_diagram, hr_pos)

    if popup:
        popup.draw(screen)
        if not popup.active:
            popup = None

    # Display collected cards
    y_offset = 240
    for card in collected_cards[-5:]:
        label = font.render(f"Card: {card}", True, WHITE)
        screen.blit(label, (hr_pos[0], hr_pos[1] + y_offset))
        y_offset += 20

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

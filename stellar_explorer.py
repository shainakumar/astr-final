import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stellar Explorer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# --- Concept and Special Cards ---
LOWER_RARITY_CARDS = {
    "Wien’s Law": "Hotter objects emit shorter wavelengths (appear bluer). λmax = b/T.",
    "Doppler Shift": "Motion changes wave frequency: toward=higher, away=lower.",
    "Diffraction Limit": "Resolution limit of telescopes: d=λ/(2NA).",
    "Brightness-Luminosity-Distance": "Brightness depends on both intrinsic luminosity and distance.",
    "Distance-Parallax": "Parallax inversely relates to distance: farther stars shift less.",
    "Escape Velocity": "Speed needed to escape a body's gravity.",
    "Hubble’s Law": "Further galaxies recede faster: universe is expanding.",
    "Kepler’s Laws": "Planets orbit elliptically; orbit time² ∝ distance³."
}

HIGHER_RARITY_CARDS = {
    "Sirius (Star)": "Binary: Sirius A (blue-white giant) + Sirius B (white dwarf). 6.8 ly away.",
    "Betelgeuse (Star)": "Red supergiant. 15 solar masses. 14000x sun's luminosity. 642.5 ly away.",
    "Aldebaran (Star)": "Orange giant in Taurus. 1.7 solar masses. 425x sun's luminosity.",
    "Crab Pulsar (Star)": "Neutron star in Crab Nebula. 1.4 solar masses. Spinning rapidly.",
    "Rigel (Star)": "Blue supergiant. 18 solar masses. 870 ly away. Very bright.",
    "Messier 13 (Cluster)": "Globular cluster of ~100K stars in Hercules. 11.6 billion years old.",
    "Messier 45 (Pleiades)": "Open cluster of hot blue stars. 100 million years old. In Taurus.",
    "Messier 44 (Beehive)": "Open cluster in Cancer. 600 million years old. Blue-white stars.",
    "47 Tucanae (Cluster)": "Dense globular cluster in Tucana. Over 500K stars.",
    "Andromeda Galaxy": "Nearest major galaxy. 1 trillion stars. 2.5 million ly away.",
    "Milky Way Galaxy": "Our galaxy! 100B stars, barred spiral. 13.6 billion years old.",
    "M87 Galaxy": "Supergiant elliptical galaxy. 53M ly away. Huge black hole center.",
    "Barnard’s Galaxy": "Dwarf irregular galaxy. Young hot blue stars."
}

# Player's collections
collected_stars = []
collected_concepts = []
collected_specials = []

# Fonts
font = pygame.font.SysFont("Arial", 16)

# Load placeholder images
player_img = pygame.Surface((50, 50))
player_img.fill(WHITE)

star_img = pygame.Surface((20, 20))
star_img.fill((255, 100, 100))

hazard_img = pygame.Surface((25, 25))
hazard_img.fill(YELLOW)

# HR Diagram (smaller, clean)
hr_diagram = pygame.Surface((300, 250))
hr_diagram.fill(GRAY)
hr_pos = (WIDTH - 320, 20)

# Star types
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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed

class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = star_img.copy()
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.star_type = weighted_star_type()
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 3)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

class Hazard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = hazard_img.copy()
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.hazard_type = random.choice(["Black Hole", "Pulsar", "Quasar", "Supernova"])
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 3)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

class Popup:
    def __init__(self, text):
        self.text = text
        self.active = True
        self.timer = 300
        self.font = pygame.font.SysFont("Arial", 16)

    def draw(self, surface):
        if self.active:
            box = pygame.Surface((400, 180))
            box.fill((250, 250, 210))
            pygame.draw.rect(box, BLACK, box.get_rect(), 2)
            lines = self.wrap_text(self.text, self.font, 380)
            for i, line in enumerate(lines):
                rendered = self.font.render(line, True, BLACK)
                box.blit(rendered, (10, 10 + 20 * i))
            surface.blit(box, (WIDTH//2 - 200, HEIGHT - 200))
            self.timer -= 1
            if self.timer <= 0:
                self.active = False

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)
        return lines

# HR star properties
HR_PROPERTIES = {
    "Main Sequence": (6000, 1),
    "Red Giant": (4000, 1000),
    "Blue Giant": (10000, 10000),
    "Red Supergiant": (3500, 100000),
    "Blue Supergiant": (20000, 100000),
    "White Dwarf": (10000, 0.001),
    "Brown Dwarf": (2500, 0.0001),
    "Subgiant": (5000, 10),
    "Neutron Star": (1000000, 0.01),
    "Protostar": (3000, 0.01),
    "The Sun": (5800, 1),
}

def plot_star_on_hr(surface, star_type):
    if star_type not in HR_PROPERTIES:
        return
    temp, lum = HR_PROPERTIES[star_type]
    temp_min, temp_max = 2000, 40000
    x = int(280 * (math.log10(temp_max) - math.log10(temp)) / (math.log10(temp_max) - math.log10(temp_min))) + 10
    lum_min, lum_max = 0.0001, 100000
    y = int(230 * (math.log10(lum_max) - math.log10(lum)) / (math.log10(lum_max) - math.log10(lum_min))) + 10
    pygame.draw.circle(surface, WHITE, (x, y), 4)

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

# Groups
player = Player()
all_sprites = pygame.sprite.Group(player)
stars = pygame.sprite.Group()
hazards = pygame.sprite.Group()

# Game state
popup = None
clock = pygame.time.Clock()
running = True
spawn_timer = 0
hazard_timer = 0

# Game Loop
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

    if spawn_timer > 40:
        spawn_star()
        spawn_timer = 0
    if hazard_timer > 200:
        spawn_hazard()
        hazard_timer = 0

    hits = pygame.sprite.spritecollide(player, stars, True)
    for hit in hits:
        star_name = hit.star_type
        if star_name not in collected_stars:
            collected_stars.append(star_name)
            popup = Popup(f"You discovered {star_name}!\nAdded to HR Diagram.")
            plot_star_on_hr(hr_diagram, star_name)

        if random.random() < 0.2:
            concept = random.choice(list(LOWER_RARITY_CARDS.keys()))
            if concept not in collected_concepts:
                collected_concepts.append(concept)
                popup = Popup(f"Concept Card Unlocked:\n{concept}\n{LOWER_RARITY_CARDS[concept]}")

        if random.random() < 0.05:
            special = random.choice(list(HIGHER_RARITY_CARDS.keys()))
            if special not in collected_specials:
                collected_specials.append(special)
                popup = Popup(f"Special Card Found:\n{special}\n{HIGHER_RARITY_CARDS[special]}")

    dangers = pygame.sprite.spritecollide(player, hazards, False)
    if dangers:
        popup = Popup(f"Careful! You hit a {dangers[0].hazard_type}!\nTeleporting to safety.")
        reset_player()

    # Drawing
    screen.fill(BLACK)
    all_sprites.draw(screen)
    screen.blit(hr_diagram, hr_pos)

    # Draw Progress Bars (top left)
    concept_total = len(LOWER_RARITY_CARDS)
    special_total = len(HIGHER_RARITY_CARDS)
    concept_unlocked = len(collected_concepts)
    special_unlocked = len(collected_specials)

    screen.blit(font.render("Concept Cards", True, WHITE), (20, 20))
    pygame.draw.rect(screen, WHITE, (20, 40, 200, 10), 2)
    pygame.draw.rect(screen, BLUE, (20, 40, int((concept_unlocked/concept_total)*200), 10))

    screen.blit(font.render("Special Cards", True, WHITE), (20, 70))
    pygame.draw.rect(screen, WHITE, (20, 90, 200, 10), 2)
    pygame.draw.rect(screen, YELLOW, (20, 90, int((special_unlocked/special_total)*200), 10))

    # Draw Collected Cards (small list)
    y_offset = 130
    for card in (collected_concepts + collected_specials)[-6:]:
        label = font.render(card, True, WHITE)
        screen.blit(label, (20, y_offset))
        y_offset += 20

    if popup:
        popup.draw(screen)
        if not popup.active:
            popup = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

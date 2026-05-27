import pygame
import random

# display initializing
pygame.init()
screen_into = pygame.display.Info()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geo Game")
icon = pygame.image.load("sprites/page_icon.png")
pygame.display.set_icon(icon)

class Buttons:
    """Represents buttons logic"""
    buttons = []
    def __init__(self, center_position, pasive_image, active_image, scale, function):
        """Initialize the button with position, image, image after click, the scale of the image and their function"""
        self.image = pasive_image
        self.active_image = active_image
        self.scale = scale
        self.function = function
        self.position = center_position
        self.rect = pygame.transform.scale_by(self.image , scale).get_rect(center=center_position)
        Buttons.buttons.append(self)
        self.active = False
        self.hovered = False

    def draw(self):
        """Function to draw the buttons"""
        current_scale = self.scale + (int(self.hovered) * 0.25)
        if self.active:
            screen.blit(pygame.transform.scale_by(self.active_image, current_scale),
                        pygame.transform.scale_by(self.active_image , current_scale).get_rect(center=self.position))
        else:
            screen.blit(pygame.transform.scale_by(self.image , current_scale),
                        pygame.transform.scale_by(self.image , current_scale).get_rect(center=self.position))

# buttons functions
def answer_entering():
    """The 'Enter' button function"""
    global apos, bpos, cpos, result, user_text, coin, score
    if user_text and int(user_text) == result:
        apos, bpos, cpos, result = triangle_create(300)
        print(result)
        Cute_cat.new_cat()
        coin = Coin()
        Coin.animation = True
        score += 1
    user_text = ""

class Cute_cat:
    """Represents a cat animation"""
    animation = False
    def __init__(self, position, target_pos):
        """Initialize the cat with a given position and a target position"""
        self.image = pygame.image.load("sprites\cute cat.png")
        self.target_pos = pygame.math.Vector2(target_pos)
        self.pos = pygame.math.Vector2(position)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        self.full_distance = self.pos.distance_to(self.target_pos)
        self.speed = 10

    def update(self):
        """Function to update the position of the cat for the movement animation"""
        if self.pos.distance_to(self.target_pos) < self.speed:
            Cute_cat.animation = False

        direction = (self.target_pos - self.pos).normalize()
        self.pos += direction * self.speed
        self.rect.center = int(self.pos.x), int(self.pos.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    @staticmethod
    def new_cat():
        """Static method to create a new cat animation with random coordinates"""
        global cat
        Cute_cat.animation = True

        if random.getrandbits(1):
            position = (random.randint(0, WIDTH), HEIGHT * random.getrandbits(1))
        else:
            position = (WIDTH * random.getrandbits(1), random.randint(0, HEIGHT))

        cat = Cute_cat(position, (WIDTH - position[0], HEIGHT - position[1]))

class Coin:
    animation = False
    def __init__(self):
        self.distance = 10
        self.image = pygame.image.load("sprites/coin.png")
        self.image = pygame.transform.scale_by(self.image, 0.4)
        self.rect = self.image.get_rect(center=piggy_rect.center)

    def update(self):
        self.rect = self.image.get_rect(center=(piggy_rect.centerx, piggy_rect.centery - self.distance))
        self.distance += 2.5

        if self.distance >= 75:
            self.animation = False
        else:
            screen.blit(self.image, self.rect)

# fonts
main_font = pygame.font.SysFont("Arial", 20)
robotic_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 32)
user_text = ""
score_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 24)

# background
background_img = pygame.image.load("sprites/unicron background.jpg").convert()
background_rect = background_img.get_rect(topleft = (0,0))
background2_rect = background_img.get_rect(topleft = (500,0))

# scoring
with open("score.txt", "r") as score_file:
    score = int(score_file.read())
piggy_image = pygame.image.load("sprites/piggy.png").convert_alpha()
piggy_image = pygame.transform.scale_by(piggy_image, 0.35)
piggy_rect = piggy_image.get_rect(center=(450,420))

# triangles screen
triangles_screen_rect = pygame.Rect((100, 60), (300, 310))
triangles_screen = pygame.Surface((triangles_screen_rect.width, triangles_screen_rect.height))
# triangles screen background
graph_img = pygame.image.load("sprites\graph.png").convert_alpha()
scaled_graph_img = pygame.transform.scale(graph_img, (triangles_screen_rect.width, triangles_screen_rect.height))
# triangles screen ouline
graph_outline_img = pygame.image.load("sprites\graph background.png").convert_alpha()
scaled_graph_outline_img = pygame.transform.scale(graph_outline_img, (triangles_screen_rect.width + 20, triangles_screen_rect.height + 20))
graph_outline_rect = scaled_graph_outline_img.get_rect(center=triangles_screen_rect.center)

# answer entering field
entering_field_img = pygame.image.load("sprites\entering field.png").convert_alpha()
entering_field_img = pygame.transform.scale_by(entering_field_img, 5)
entering_field_rect = entering_field_img.get_rect(center=(250,415))

# buttons
Buttons((250,473),
        pygame.image.load("sprites\enter button.png").convert_alpha(),
        pygame.image.load("sprites\enter button active.png").convert_alpha(),
        5, answer_entering)

def background_animation():
    """Function for the background movement animation"""
    global background_rect, background2_rect
    if background_rect.right <= 0: background_rect.left = 500
    if background2_rect.right <= 0: background2_rect.left = 500
    background_rect.left -= 1
    background2_rect.left -= 1

def triangle_create(screen_size):
    """Function to create a new triagle on the screen"""
    a = (random.choice(range((screen_size // 20), screen_size, (screen_size // 20))), random.choice(range((screen_size // 20), screen_size, (screen_size // 20))))
    b = (a[0], random.choice(list(range((screen_size // 20), a[1], (screen_size // 20))) + list(range(a[1] + (screen_size // 20), screen_size, (screen_size // 20)))))
    c = (random.choice(list(range((screen_size // 20), a[0], (screen_size // 20))) + list(range(a[0] + (screen_size // 20), screen_size, (screen_size // 20)))), a[1])

    return a, b, c, (b[1] // (screen_size // 20) - a[1] // (screen_size // 20)) ** 2 + (c[0] // (screen_size // 20) - a[0] // (screen_size // 20)) ** 2

apos, bpos, cpos, result = triangle_create(300)
print(result)

def to_coordinadtes(pos):
    """Function to translate the triangle position on the screen into graph positions"""
    return (pos[0] - 150) // 15, (pos[1] - 150) // -15

def cat_movement():
    """Function for the right answers animation"""
    pass

clock = pygame.time.Clock()

# the main loop
running = True
while running:
    # events
    for event in pygame.event.get():
        # quiting the game loop
        if event.type == pygame.QUIT:
            with open("score.txt", "w") as score_file:
                score_file.write(str(score))
            running = False
            # checking for mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in Buttons.buttons:
                button.active = False
        # disabling the event handling while the cat animation is going
        if not Cute_cat.animation:
            # checking for pressed buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in Buttons.buttons:
                    if button.rect.collidepoint(event.pos):
                        button.function()
                        button.active = True
            # checking for player input
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    answer_entering()
                elif event.unicode in "1234567890" and len(user_text) < 3:
                    user_text += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
            # checking for mouse movement
            elif event.type == pygame.MOUSEMOTION:
                for button in Buttons.buttons:
                    button.hovered = button.rect.collidepoint(event.pos)


    # background
    background_animation()
    screen.blit(background_img,background_rect)
    screen.blit(background_img,background2_rect)
    # score coin animation
    if Coin.animation:
        coin.update()
    # score
    screen.blit(piggy_image, piggy_rect)
    score_surf = score_font.render(str(score), True, (255, 255, 0))
    score_rect = score_surf.get_rect(center=(piggy_rect.center[0],
                                                      piggy_rect.center[1] + (piggy_rect.height / 2) + 10 + (score_surf.get_height() / 2)))
    screen.blit(score_surf, score_rect)

    # triangle drawing background
    screen.blit(triangles_screen, (triangles_screen_rect.x, triangles_screen_rect.y))
    triangles_screen.blit(scaled_graph_img, (0, 0))
    screen.blit(scaled_graph_outline_img, graph_outline_rect)
    # draw triangle
    pygame.draw.line(triangles_screen, (0, 0, 0), apos, bpos, width=3)
    pygame.draw.line(triangles_screen, (0, 0, 0), bpos, cpos, width=3)
    pygame.draw.line(triangles_screen, (0, 0, 0), cpos, apos, width=3)
    # draw buttons
    for button in Buttons.buttons:
        button.draw()
    # entering field
    screen.blit(entering_field_img, entering_field_rect)
    player_answer_surface = robotic_font.render(user_text, True, (255, 255, 0))
    screen.blit(player_answer_surface, player_answer_surface.get_rect(center=(292.5, 417.5)))
    # draw coordinates
    coordinates_surface = main_font.render("a = {}, b = {}, c = {}".format(*[to_coordinadtes(pos) for pos in [apos, bpos, cpos]]), True, (255, 255, 0))
    coordinates_surface_rect = coordinates_surface.get_rect(center=(250,25))
    coordinates_surface_background = pygame.transform.scale(pygame.image.load("sprites/buttons background.png").convert_alpha(),
                                                            (coordinates_surface_rect.width + 25, coordinates_surface_rect.height + 18))
    coordinates_surface_background_rect = coordinates_surface_background.get_rect(center=coordinates_surface_rect.center)
    screen.blit(coordinates_surface_background, coordinates_surface_background_rect)
    screen.blit(coordinates_surface, coordinates_surface_rect)
    # cute cat celebrating animation
    if Cute_cat.animation:
        cat.update()
        cat.draw(screen)

    # the fps and update of the screen
    clock.tick(60)
    pygame.display.update()

pygame.quit()


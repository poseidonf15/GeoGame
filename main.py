import pygame
import random

# display initializing
pygame.init()
screen_into = pygame.display.Info()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Buttons:
    buttons = []
    def __init__(self, center_position, pasive_image, active_image, scale, function):
        self.image = pygame.transform.scale_by(pasive_image, scale)
        self.active_image = pygame.transform.scale_by(active_image, scale)
        self.function = function
        self.rect = self.image.get_rect(center=center_position)
        Buttons.buttons.append(self)
        self.active = False

    @staticmethod
    def draw():
        for button in Buttons.buttons:
            if not button.active:
                screen.blit(button.image, button.rect)
            else:
                screen.blit(button.active_image, button.rect)

def answer_entering():
    global apos, bpos, cpos, result, user_text
    if user_text and int(user_text) == result:
        apos, bpos, cpos, result = triangle_create(300)
    user_text = ""

# fonts
main_font = pygame.font.SysFont("Arial", 20)
robotic_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 32)
user_text = ""

# background
background_img = pygame.image.load("sprites/unicron background.jpg").convert()
background_rect = background_img.get_rect(topleft = (0,0))
background2_rect = background_img.get_rect(topleft = (500,0))

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
    global background_rect, background2_rect
    if background_rect.right <= 0: background_rect.left = 500
    if background2_rect.right <= 0: background2_rect.left = 500
    background_rect.left -= 1
    background2_rect.left -= 1

def triangle_create(screen_size):
    a = (random.choice(range((screen_size // 20), screen_size, (screen_size // 20))), random.choice(range((screen_size // 20), screen_size, (screen_size // 20))))
    b = (a[0], random.choice(list(range((screen_size // 20), a[1], (screen_size // 20))) + list(range(a[1] + (screen_size // 20), screen_size, (screen_size // 20)))))
    c = (random.choice(list(range((screen_size // 20), a[0], (screen_size // 20))) + list(range(a[0] + (screen_size // 20), screen_size, (screen_size // 20)))), a[1])

    return a, b, c, (b[1] // (screen_size // 20) - a[1] // (screen_size // 20)) ** 2 + (c[0] // (screen_size // 20) - a[0] // (screen_size // 20)) ** 2

apos, bpos, cpos, result = triangle_create(300)
print(result)

def to_coordinadtes(pos):
    return (pos[0] - 150) // 15, (pos[1] - 150) // -15

clock = pygame.time.Clock()

# the main loop
running = True
while running:
    # events
    for event in pygame.event.get():
        # quiting the game loop
        if event.type == pygame.QUIT:
            running = False
        # checking for pressed buttons
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in Buttons.buttons:
                if button.rect.collidepoint(event.pos):
                    button.function()
                    button.active = True
        # checking for mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in Buttons.buttons:
                button.active = False
        # checking for player input
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                answer_entering()
            elif event.unicode in "1234567890" and len(user_text) < 3:
                user_text += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]

    # background
    background_animation()
    screen.blit(background_img,background_rect)
    screen.blit(background_img,background2_rect)
    # triangle drawing background
    screen.blit(triangles_screen, (triangles_screen_rect.x, triangles_screen_rect.y))
    triangles_screen.blit(scaled_graph_img, (0, 0))
    screen.blit(scaled_graph_outline_img, graph_outline_rect)
    # draw triangle
    pygame.draw.line(triangles_screen, (0, 0, 0), apos, bpos, width=3)
    pygame.draw.line(triangles_screen, (0, 0, 0), bpos, cpos, width=3)
    pygame.draw.line(triangles_screen, (0, 0, 0), cpos, apos, width=3)
    # draw buttons
    Buttons.draw()
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

    # the fps and update of the screen
    clock.tick(60)
    pygame.display.update()

pygame.quit()


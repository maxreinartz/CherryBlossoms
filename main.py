import pygame, random, math, tkinter
from datetime import datetime
from screeninfo import get_monitors
from tkinter import filedialog

def get_screen_size():
    for m in get_monitors():
        if m.is_primary:
            return m.width, m.height
        
def select_image():
    root = tkinter.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp')])  # Show the file dialog
    return file_path

screen_width, screen_height = get_screen_size()

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
text = False

infoObject = pygame.display.Info()
Modified_SCREEN_WIDTH = (screen_width/800)
Modified_SCREEN_HEIGHT = (screen_width/600)

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
clock = pygame.time.Clock()
pygame.display.set_caption('Cherry Blossoms')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
paused = False
time_scale = 1.0
firework_mode = 1
FPS = 60

controls = [
    'Esc: Quit',
    'Period: Show/Hide Text',
    'S: Screenshot',
    'P: Pause',
    'N: Fireworks Mode Down',
    'M: Fireworks Mode Up',
    'LBracket: FPS Down',
    'RBracket: FPS Up',
    'Up: Add 50',
    'Down: Remove 50',
    'Left: Slow Down',
    'Right: Speed Up',
    'Click: Add White',
    'Middle Click: Firework',
    'Right Click: Push Away',
]

controls.sort(key=len, reverse=True)
controls_x = 10
controls_y = 10

color_presets = [
    [(200, 255), (0, 100), (0, 100)], # red
    [(200, 255), (100, 200), (0, 50)], # orange
    [(200, 255), (200, 255), (0, 100)], # yellow
    [(0, 100), (200, 255), (0, 100)], # green
    [(0, 100), (200, 255), (200, 255)], # blue
    [(100, 200), (0, 100), (200, 255)], # purple
]

pattern_presets = [
    [  # USA pattern
        [(200, 255), (0, 100), (0, 100)],  # red
        [(200, 255), (200, 255), (200, 255)],  # white
        [(0, 100), (0, 100), (200, 255)],  # blue
    ],
    [  # Japan pattern
        [(200, 255), (0, 100), (0, 100)],  # red
        [(200, 255), (200, 255), (200, 255)],  # white
    ],
    [  # Germany pattern
        [(0, 100), (0, 100), (0, 100)],  # black
        [(200, 255), (0, 100), (0, 100)],  # red
        [(200, 255), (200, 255), (0, 100)], # yellow
    ],
    [   # Creeper pattern
        [(0, 100), (0, 100), (0, 100)],  # black
        [(0, 100), (200, 255), (0, 100)],  # green 
    ],
    [   # Rainbow pattern
        [(200, 255), (0, 100), (0, 100)],  # red
        [(200, 255), (100, 200), (0, 50)],  # orange
        [(200, 255), (200, 255), (0, 100)],  # yellow
        [(0, 100), (200, 255), (0, 100)],  # green
        [(0, 100), (200, 255), (200, 255)],  # blue
        [(100, 200), (0, 100), (200, 255)],  # purple
    ],
    [   # Penguin pattern
        [(200, 255), (200, 255), (200, 255)],  # white
        [(0, 100), (0, 100), (0, 100)],  # black
    ],
    [   # Cool Colors pattern
        [(0, 100), (200, 255), (200, 255)],  # cyan
        [(100, 200), (0, 100), (200, 255)],  # purple
    ],
    [   # Warm Colors pattern
        [(200, 255), (0, 100), (0, 100)],  # red
        [(200, 255), (200, 255), (0, 100)],  # yellow
        [(0, 100), (200, 255), (0, 100)],  # green
    ]
]

class CherryBlossom:
    def __init__(self):
        self.reset()
        self.radius = random.randint(1, 3)
        self.isPink = True
        self.trail = []

    def reset(self):
        self.x = random.uniform(-100, screen_width)
        self.y = random.uniform(-screen_height, -10)
        self.speed = random.uniform(0.4 * Modified_SCREEN_HEIGHT, 0.8 * Modified_SCREEN_HEIGHT)
        self.speed_x = random.uniform(0.8 * Modified_SCREEN_WIDTH, 2 * Modified_SCREEN_WIDTH)
        self.color = (random.randint(200, 255), random.randint(100, 192), random.randint(180, 203))

    def update(self, dt):
        self.y += self.speed * dt
        self.x += self.speed_x * dt
        if not self.isPink:
            if self.y > screen_height or self.x > screen_width:
                cherry_blossoms.remove(self)
        elif self.y > screen_height:
            self.reset()
        elif self.x > screen_width:
            self.x = 0

    def push_away(self, mouse_pos):
        dx, dy = self.x - mouse_pos[0], self.y - mouse_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance < 150:
            push_force = 150 / distance
            self.x += dx / distance * push_force
            self.y += dy / distance * push_force

    def draw(self, screen):
        if len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                factor = i / len(self.trail)
                color = int(self.color[0] * factor), int(self.color[1] * factor), int(self.color[2] * factor)
                pygame.draw.line(screen, color, self.trail[i-1], self.trail[i], 2)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class WhiteCherryBlossom(CherryBlossom):
    def __init__(self):
        self.isPink = False
        self.trail = []
        self.reset()

    def reset(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.speed = random.uniform(0.4 * Modified_SCREEN_HEIGHT, 0.8 * Modified_SCREEN_HEIGHT)
        self.speed_x = random.uniform(0.8 * Modified_SCREEN_WIDTH, 2 * Modified_SCREEN_WIDTH)
        self.color = random.choice([(255, 255, 255), (211, 211, 211)])
        self.radius = random.randint(1, 3)

    def update(self, dt):
        self.y += self.speed * dt
        self.x += self.speed_x * dt
        if self.y > screen_height or self.x > screen_width:
          cherry_blossoms.remove(self)

class Firework(CherryBlossom):
    def __init__(self, color):
        self.isPink = False
        self.trail = []
        self.reset(color)
    
    def reset(self, color):
        angle = random.uniform(0, 2 * math.pi)
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.speed = random.uniform(0.01 * Modified_SCREEN_HEIGHT, 1.5 * Modified_SCREEN_HEIGHT) * math.cos(angle)
        self.speed_x = random.uniform(1 * Modified_SCREEN_WIDTH, 2 * Modified_SCREEN_WIDTH) * math.sin(angle)
        self.color = (random.randint(color[0][0], color[0][1]), random.randint(color[1][0], color[1][1]), random.randint(color[2][0], color[2][1]))
        self.radius = random.randint(1, 3)

    def update(self, dt):
        self.speed += 0.1 * dt
        self.y += self.speed * dt
        self.x += self.speed_x * dt
        if self.y > screen_height + 100 or self.x > screen_width:
          cherry_blossoms.remove(self)
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)

def create_cherry_blossoms_from_image(image_path, scale_factor=0.5, step=5):
    image_surface = pygame.image.load(image_path)
    width, height = image_surface.get_size()
    image_surface = pygame.transform.scale(image_surface, (int(width * scale_factor), int(height * scale_factor)))
    image_array = pygame.surfarray.array3d(image_surface)
    alpha_array = pygame.surfarray.array_alpha(image_surface)
    cherry_blossoms = []
    for y in range(0, image_array.shape[1], step):
        for x in range(0, image_array.shape[0], step):
            if alpha_array[x, y] > 0:
                cherry_blossom = CherryBlossom()
                cherry_blossom.x = x - width // 4
                cherry_blossom.y = y - height // 4
                cherry_blossom.color = image_array[x, y]
                cherry_blossom.isPink = False
                cherry_blossoms.append(cherry_blossom)
    return cherry_blossoms

cherry_blossoms = [CherryBlossom() for _ in range(700)]
fireworks = []

running = True
while running:
    dt = clock.tick(FPS) / 16.0 # 16 keeps the delta time at 1.0
    dt *= time_scale

    pink_cherry_blossoms = [cherry_blossom for cherry_blossom in cherry_blossoms if cherry_blossom.isPink]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                for _ in range(50):
                    cherry_blossoms.append(CherryBlossom())
            elif event.key == pygame.K_DOWN:
                for _ in range(50):
                    for i in range(len(cherry_blossoms) - 1, -1, -1):
                        if cherry_blossoms[i].isPink:
                            del cherry_blossoms[i]
                            break
            elif event.key == pygame.K_LEFT:
                time_scale -= 0.1
                if time_scale < 0.1:
                    time_scale = 0.1
            elif event.key == pygame.K_RIGHT:
                time_scale += 0.1
            elif event.key == pygame.K_PERIOD:
                text = not text
            elif event.key == pygame.K_s:
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                pygame.image.save(screen, f'screenshot_{timestamp}.png')
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_LEFTBRACKET:
                FPS -= 15
                if FPS < 15:
                    FPS = 15
            elif event.key == pygame.K_RIGHTBRACKET:
                FPS += 15
            elif event.key == pygame.K_m:
                firework_mode += 1
                if firework_mode > 2:
                    firework_mode = 2
            elif event.key == pygame.K_n:
                firework_mode -= 1
                if firework_mode < 1:
                    firework_mode = 1
            elif event.key == pygame.K_l:
                x, y = pygame.mouse.get_pos()
                image_path = select_image()
                if image_path:
                    new_cherry_blossoms = create_cherry_blossoms_from_image(image_path)
                    for cherry_blossom in new_cherry_blossoms:
                        cherry_blossom.x += x
                        cherry_blossom.y += y
                    cherry_blossoms.extend(new_cherry_blossoms)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            if(firework_mode == 1):
                color_preset = random.choice(color_presets)
                for _ in range(int(round(len(pink_cherry_blossoms) / 2, 0))):
                    cherry_blossoms.append(Firework(color_preset))
            elif(firework_mode == 2):
                pattern_preset = random.choice(pattern_presets)
                for _ in range(int(round(len(pink_cherry_blossoms) / 2, 0))):
                    color_preset = random.choice(pattern_preset)
                    cherry_blossoms.append(Firework(color_preset))
    if pygame.mouse.get_pressed()[0]:
        for _ in range(int(round(len(pink_cherry_blossoms) / 100, 0))):
            cherry_blossoms.append(WhiteCherryBlossom())
    elif pygame.mouse.get_pressed()[2]:
        mouse_pos = pygame.mouse.get_pos()
        for cherry_blossom in cherry_blossoms:
            cherry_blossom.push_away(mouse_pos)

    if not paused:
        for cherry_blossom in cherry_blossoms[:]:
            cherry_blossom.update(dt)

    screen.fill((0, 0, 0))
    for cherry_blossom in cherry_blossoms:
        cherry_blossom.draw(screen)

    fps = clock.get_fps()

    fps_text = font.render("FPS: {:.2f}".format(fps), True, (255, 255, 255))
    dt_text = font.render("Delta Time: {:.2f}".format(dt), True, (255, 255, 255))
    firework_text = font.render("Firework Mode: {}".format(firework_mode), True, (255, 255, 255))
    scale_text = font.render("Time Scale: {:.2f}".format(time_scale), True, (255, 255, 255))
    pink_count_text = font.render('Pink Count: {}'.format(len(pink_cherry_blossoms)), False, (255, 255, 255))
    count_text = font.render('Count: {}'.format(len(cherry_blossoms)), False, (255, 255, 255))

    if(text):
        controls_y = 10
        for control in controls:
            control_text = font.render(control, True, (255, 255, 255))
            screen.blit(control_text, (controls_x, controls_y))
            controls_y += control_text.get_height() + 10
        screen.blit(firework_text, (screen_width - firework_text.get_width() - 10, 10))
        screen.blit(dt_text, (screen_width - dt_text.get_width() - 10, 40))
        screen.blit(scale_text, (screen_width - scale_text.get_width() - 10, 70))
        screen.blit(pink_count_text, (screen_width - pink_count_text.get_width() - 10, 100))
        screen.blit(count_text, (screen_width - count_text.get_width() - 10, 130))
        screen.blit(fps_text, (screen_width - fps_text.get_width() - 10, 160))

    pygame.display.flip()

pygame.quit()
import pygame, random, math
from datetime import datetime
from screeninfo import get_monitors

def get_screen_size():
    for m in get_monitors():
        if m.is_primary:
            return m.width, m.height

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
      if self.y > screen_height:
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
    def __init__(self):
        self.isPink = False
        self.trail = []
        self.reset()
    
    def reset(self):
        angle = random.uniform(0, 2 * math.pi)
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.speed = random.uniform(0.01 * Modified_SCREEN_HEIGHT, 1.5 * Modified_SCREEN_HEIGHT) * math.cos(angle)
        self.speed_x = random.uniform(1 * Modified_SCREEN_WIDTH, 2 * Modified_SCREEN_WIDTH) * math.sin(angle)
        self.color = (random.randint(200, 255), random.randint(100, 200), random.randint(0, 50))
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

cherry_blossoms = [CherryBlossom() for _ in range(700)]
fireworks = []

running = True
while running:
    dt = clock.tick(60) / 16.0 # 16 keeps the delta time at 1.0
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
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            for _ in range(int(round(len(pink_cherry_blossoms) / 2, 0))):
                cherry_blossoms.append(Firework())
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
    scale_text = font.render("Time Scale: {:.2f}".format(time_scale), True, (255, 255, 255))
    pink_count_text = font.render('Pink Count: {}'.format(len(pink_cherry_blossoms)), False, (255, 255, 255))
    count_text = font.render('Count: {}'.format(len(cherry_blossoms)), False, (255, 255, 255))
    controls_text = font.render('Period: Show/Hide Text, S: Screenshot, P: Pause, Up: Add 50, Down: Remove 50, Left: Slow Down, Right: Speed Up, Click: Add White, Middle Click: Firework, Right Click: Push Away', False, (255, 255, 255))

    if(text):
        screen.blit(controls_text, (screen_width - controls_text.get_width(), 0))
        screen.blit(dt_text, (screen_width - dt_text.get_width(), 30))
        screen.blit(scale_text, (screen_width - scale_text.get_width(), 60))
        screen.blit(pink_count_text, (screen_width - pink_count_text.get_width(), 90))
        screen.blit(count_text, (screen_width - count_text.get_width(), 120))
        screen.blit(fps_text, (screen_width - fps_text.get_width(), 150))

    pygame.display.flip()

pygame.quit()
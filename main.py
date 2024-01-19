import pygame, random, math
from datetime import datetime

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
text = False

infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w + 100
SCREEN_HEIGHT = infoObject.current_h + 100
Modified_SCREEN_WIDTH = (SCREEN_WIDTH/800)
Modified_SCREEN_HEIGHT = (SCREEN_HEIGHT/600)

screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption('Cherry Blossoms')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

class CherryBlossom:
    def __init__(self):
        self.reset()
        self.radius = random.randint(1, 3)
        self.isPink = True

    def reset(self):
        self.x = random.uniform(-100, SCREEN_WIDTH)
        self.y = random.uniform(-SCREEN_HEIGHT, -10)
        self.speed = random.uniform(0.4 * Modified_SCREEN_HEIGHT, 0.8 * Modified_SCREEN_HEIGHT)
        self.speed_x = random.uniform(0.8 * Modified_SCREEN_WIDTH, 2 * Modified_SCREEN_WIDTH)
        self.color = (random.randint(200, 255), random.randint(100, 192), random.randint(180, 203))

    def update(self):
      self.y += self.speed
      self.x += self.speed_x
      if self.y > SCREEN_HEIGHT:
          self.reset()
      elif self.x > SCREEN_WIDTH:
          self.x = 0

    def push_away(self, mouse_pos):
        dx, dy = self.x - mouse_pos[0], self.y - mouse_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance < 50:
            self.x += dx / distance * 10
            self.y += dy / distance * 10

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class WhiteCherryBlossom(CherryBlossom):
    def __init__(self):
        self.isPink = False
        self.reset()

    def reset(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.speed = random.uniform(0.4 * Modified_SCREEN_HEIGHT, 0.8 * Modified_SCREEN_HEIGHT)
        self.speed_x = random.uniform(0.8 * Modified_SCREEN_WIDTH, 2 * Modified_SCREEN_WIDTH)
        self.color = random.choice([(255, 255, 255), (211, 211, 211)])
        self.radius = random.randint(1, 3)

    def update(self):
        self.y += self.speed
        self.x += self.speed_x
        if self.y > SCREEN_HEIGHT or self.x > SCREEN_WIDTH:
          cherry_blossoms.remove(self)

cherry_blossoms = [CherryBlossom() for _ in range(700)]

running = True
while running:
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
            elif event.key == pygame.K_PERIOD:
                text = not text
            elif event.key == pygame.K_s:
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                pygame.image.save(screen, f'screenshot_{timestamp}.png')
    if pygame.mouse.get_pressed()[0]:
        for _ in range(int(round(len(pink_cherry_blossoms) / 100, 0))):
            cherry_blossoms.append(WhiteCherryBlossom())  
    elif pygame.mouse.get_pressed()[2]:
        mouse_pos = pygame.mouse.get_pos()
        for cherry_blossom in cherry_blossoms:
            cherry_blossom.push_away(mouse_pos)

    for cherry_blossom in cherry_blossoms[:]:
        cherry_blossom.update()

    screen.fill((0, 0, 0))
    for cherry_blossom in cherry_blossoms:
        cherry_blossom.draw(screen)

    fps = clock.get_fps()

    fps_text = font.render("FPS: {:.2f}".format(fps), True, (255, 255, 255))
    pink_count_text = font.render('Pink Count: {}'.format(len(pink_cherry_blossoms)), False, (255, 255, 255))
    count_text = font.render('Count: {}'.format(len(cherry_blossoms)), False, (255, 255, 255))
    controls_text = font.render('Period: Show/Hide Text, S: Screenshot, Up: Add 50, Down: Remove 50, Click: Add White, Right Click: Push Away', False, (255, 255, 255))

    if(text):
        screen.blit(controls_text, (SCREEN_WIDTH - 50 - controls_text.get_width(), 0))
        screen.blit(pink_count_text, (SCREEN_WIDTH - 50 - pink_count_text.get_width(), 50))
        screen.blit(count_text, (SCREEN_WIDTH - 50 - count_text.get_width(), 100))
        screen.blit(fps_text, (SCREEN_WIDTH - 50 - fps_text.get_width(), 150))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
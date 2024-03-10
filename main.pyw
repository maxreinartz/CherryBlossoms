import pygame, random, math, tkinter, requests, os, logging, zipfile, shutil
from datetime import datetime
from screeninfo import get_monitors
from tkinter import filedialog

# ! Most of this may not work on any other OS than Windows

# Gets appdata folder
# TODO: Make this work on other OS
appdata = os.getenv('APPDATA')

# Define the directory and file for logging
log_dir = os.path.join(appdata, 'CherryBlossoms')
log_file = os.path.join(log_dir, 'cherryblossoms.log')

# Check if the directory exists, if not, create it
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Check if the file exists, if not, create it
if not os.path.isfile(log_file):
    with open(log_file, 'a'):
        pass

# Sets up logging
logging.basicConfig(
    filename=os.path.join(appdata, 'CherryBlossoms', 'cherryblossoms.log'),
    level=logging.INFO,
    format='CherryBlossoms - %(levelname)s: %(message)s'
)
date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
logging.info(f'=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-={date}=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

version = 6
# Set to False to disable updates
updates = False

# Checks for updates
def check_for_updates():
    logging.info(f"Version: {version}")
    
    try:
        # Get latest version from GitHub
        response = requests.get('https://raw.githubusercontent.com/Creeper76/CherryBlossoms/main/version.txt')
        # Write the latest version to a variable
        latest_version = response.text.strip()
        os.makedirs(os.path.join(appdata, 'CherryBlossoms'), exist_ok=True)
        # Open the version file and write the current version to it
        with open(os.path.join(appdata, 'CherryBlossoms', 'version.txt'), 'wb') as f:
            f.write(str(version).encode())
        # Open the version file and read the current version from it
        # ? This may not be necessary
        with open(os.path.join(appdata, 'CherryBlossoms', 'version.txt'), 'r') as f:
            current_version = f.read().strip()
        # Compare the latest version to the current version
        if latest_version > current_version:
            logging.info(f'Update available! You\'re Version: {current_version}; Latest Version: {latest_version}')
            logging.info('Downloading update...')
            # Download the update zip file from GitHub
            response = requests.get('https://github.com/creeper76/cherryblossoms/archive/refs/heads/main.zip')
            with open(os.path.join(appdata, 'CherryBlossoms', f'cherryblossoms_update_{latest_version}.zip'), 'wb') as f:
                f.write(response.content)

            # Extract the files from the zip file
            files_to_extract = ['CherryBlossoms-main/main.pyw', 'CherryBlossoms-main/LICENSE', 'CherryBlossoms-main/icon.png']
            with zipfile.ZipFile(os.path.join(appdata, 'CherryBlossoms', f'cherryblossoms_update_{latest_version}.zip'), 'r') as zip_ref:
                for file in files_to_extract:
                    try:
                        data = zip_ref.read(file)
                        with open(os.path.join(appdata, 'CherryBlossoms', os.path.basename(file)), 'wb') as f:
                            f.write(data)
                    except KeyError:
                        logging.error(f'The file {file} is not in the zip file')
            
            # Remove the zip file
            os.remove(os.path.join(appdata, 'CherryBlossoms', f'cherryblossoms_update_{latest_version}.zip'))

            # Copy the files to the current directory
            shutil.copy(os.path.join(appdata, 'CherryBlossoms', 'main.pyw'), os.getcwd())
        else:
            logging.info('You\'re up to date!')
    except Exception as e:
        logging.error('Something went wrong while updating :(')
        logging.error(e)

# Check for updates
if updates:
    check_for_updates()

# Gets the screen size
def get_screen_size():
    for m in get_monitors():
        if m.is_primary:
            return m.width, m.height
        
# Opens a file dialog to select an image
def select_image():
    logging.info('Opened select image prompt.')
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp')])
    return file_path

# Get the screen size
screen_width, screen_height = get_screen_size()

# Initialize pygame
pygame.init()
pygame.font.init()
# Best font ever
font = pygame.font.SysFont('Comic Sans MS', 20)
text = False

# Set the screen size
infoObject = pygame.display.Info()
Modified_SCREEN_WIDTH = (screen_width/800)
Modified_SCREEN_HEIGHT = (screen_width/600)

# Set the screen size
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
# Set clock variable
clock = pygame.time.Clock()
# Set the window title
pygame.display.set_caption('Cherry Blossoms')

# Set the icon
try:
    icon = pygame.image.load(os.path.join(appdata, 'CherryBlossoms/icon.png'))
    pygame.display.set_icon(icon)
except:
    # If the icon is not found, download it
    logging.warning('Icon not found, downloading...')
    url = 'https://raw.githubusercontent.com/Creeper76/CherryBlossoms/main/icon.png'
    try:
        response = requests.get(url)
        os.makedirs(os.path.join(appdata, 'CherryBlossoms'), exist_ok=True)
        with open(os.path.join(appdata, 'CherryBlossoms', 'icon.png'), 'wb') as f:
            f.write(response.content)
    except:
        logging.error('Request failed! (are you connected to the internet?)')
        logging.info('Skipping...')
    try:
        icon = pygame.image.load(os.path.join(appdata, 'CherryBlossoms', 'icon.png'))
        pygame.display.set_icon(icon)
        logging.info('Icon downloaded successfully!')
    except Exception as e:
        logging.error('Failed to download icon, skipping...')
        logging.error('Error: {}'.format(e))

# Set the variables
paused = False
time_scale = 1.0
firework_mode = 1
# Set the frames per second
FPS = 60

# List of controls
controls = [
    'Esc/Space: Quit',
    'Period: Show/Hide Text',
    'S: Screenshot',
    'P: Pause',
    'N: Fireworks Mode Down',
    'M: Fireworks Mode Up',
    'L: Load Image',
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

# Sort the controls by length
controls.sort(key=len, reverse=True)
controls_x = 10
controls_y = 10

# Set the color presets
color_presets = [
    [(200, 255), (0, 100), (0, 100)], # red
    [(200, 255), (100, 200), (0, 50)], # orange
    [(200, 255), (200, 255), (0, 100)], # yellow
    [(0, 100), (200, 255), (0, 100)], # green
    [(0, 100), (200, 255), (200, 255)], # blue
    [(100, 200), (0, 100), (200, 255)], # purple
]

# Set the pattern presets
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
    ],
    [   # Pastel Colors pattern
        [(200, 255), (100, 200), (100, 200)],  # pink
        [(200, 255), (200, 255), (100, 200)],  # yellow
        [(100, 200), (200, 255), (200, 255)],  # cyan
        [(100, 200), (100, 200), (200, 255)],  # blue

    ],
    [   # Dark Colors pattern
        [(0, 100), (0, 100), (0, 100)],  # black
        [(100, 200), (100, 200), (100, 200)],  # gray
    ],
    [   # Light Colors pattern
        [(200, 255), (200, 255), (200, 255)],  # white
        [(100, 200), (100, 200), (100, 200)],  # gray
    ]
]

# Set the cherry blossom class
class CherryBlossom:
    def __init__(self):
        self.reset()
        # Set the size of the cherry blossom
        self.radius = random.randint(1, 3)
        # Specify if it's pink. This is used to determine if the cherry blossom should be removed when it goes off screen
        self.isPink = True
        # Set the trail. This is used to draw the trail of the fireworks; ignore it for cherry blossoms
        self.trail = []

    def reset(self):
        # Set the x and y position of the cherry blossom
        self.x = random.uniform(-100, screen_width)
        self.y = random.uniform(-screen_height, -10)
        # Set the speed of the cherry blossom
        self.speed = random.uniform(0.4 * Modified_SCREEN_HEIGHT, 0.8 * Modified_SCREEN_HEIGHT)
        self.speed_x = random.uniform(0.8 * Modified_SCREEN_WIDTH, 2 * Modified_SCREEN_WIDTH)
        # Set the color of the cherry blossom
        self.color = (random.randint(200, 255), random.randint(100, 192), random.randint(180, 203))

    def update(self, dt):
        # Update the position of the cherry blossom
        self.y += self.speed * dt
        self.x += self.speed_x * dt
        # Remove the not-pink cherry blossoms if they goes off screen
        if not self.isPink:
            if self.y > screen_height or self.x > screen_width:
                cherry_blossoms.remove(self)
        # Run this if it is a pink cherry blossom
        elif self.y > screen_height:
            self.reset()
        elif self.x > screen_width:
            self.x = 0

    # Right click to push away code
    def push_away(self, mouse_pos):
        # Get the distance between the mouse and the cherry blossom
        dx, dy = self.x - mouse_pos[0], self.y - mouse_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        # If the distance is greater than 0, push the cherry blossom away. This is to prevent division by zero
        if distance > 0:
            if distance < 150:
                push_force = 150 / distance
                self.x += dx / distance * push_force
                self.y += dy / distance * push_force

    # Draw the cherry blossom to the screen
    def draw(self, screen):
        # Draw the trail. Only used for fireworks
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
    def __init__(self, color, x, y):
        self.isPink = False
        self.trail = []
        self.reset(color, x, y)
    
    def reset(self, color, x, y):
        angle = random.uniform(0, 2 * math.pi)
        self.x = x
        self.y = y
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
    
    if(random.randint(1, 50) * dt == 1):
        PosX = random.randint(50, screen_width - 50)
        PosY = random.randint(150, screen_height - 200)
        ColorPresent = random.choice(color_presets)
        for _ in range(int(round(len(pink_cherry_blossoms) / 2, 0))):
            cherry_blossoms.append(Firework(ColorPresent, PosX, PosY))

    pink_cherry_blossoms = [cherry_blossom for cherry_blossom in cherry_blossoms if cherry_blossom.isPink]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
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
                    cherry_blossoms.append(Firework(color_preset, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            elif(firework_mode == 2):
                pattern_preset = random.choice(pattern_presets)
                for _ in range(int(round(len(pink_cherry_blossoms) / 2, 0))):
                    color_preset = random.choice(pattern_preset)
                    cherry_blossoms.append(Firework(color_preset, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
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

    if(fps < 15):
        logging.warning('FPS is below 15!')

    fps_text = font.render("FPS: {:.2f}".format(fps), True, (255, 255, 255))
    dt_text = font.render("Delta Time: {:.2f}".format(dt), True, (255, 255, 255))
    firework_text = font.render("Firework Mode: {}".format(firework_mode), True, (255, 255, 255))
    scale_text = font.render("Time Scale: {:.2f}".format(time_scale), True, (255, 255, 255))
    pink_count_text = font.render('Pink Count: {}'.format(len(pink_cherry_blossoms)), False, (255, 255, 255))
    count_text = font.render('Count: {}'.format(len(cherry_blossoms)), False, (255, 255, 255))
    mouse_pos_text = font.render('Mouse Pos: {}'.format(pygame.mouse.get_pos()), False, (255, 255, 255))
    # You can't remove or modify the following two lines
    made_with_love = font.render("Made with love by Creeper76 ", True, (255, 255, 255))
    heart = font.render("<3", True, (255, 105, 180))

    if(text):
        controls_y = 10
        for control in controls:
            control_text = font.render(control, True, (255, 255, 255))
            screen.blit(control_text, (controls_x, controls_y))
            controls_y += control_text.get_height() + 10
        TEXT_PADDING = 10
        TEXT_HEIGHT = 30
        TEXT_START_HEIGHT = 10

        screen.blit(mouse_pos_text, (screen_width - mouse_pos_text.get_width() - TEXT_PADDING, TEXT_START_HEIGHT + 0*TEXT_HEIGHT))
        screen.blit(firework_text, (screen_width - firework_text.get_width() - TEXT_PADDING, TEXT_START_HEIGHT + 1*TEXT_HEIGHT))
        screen.blit(dt_text, (screen_width - dt_text.get_width() - TEXT_PADDING, TEXT_START_HEIGHT + 2*TEXT_HEIGHT))
        screen.blit(scale_text, (screen_width - scale_text.get_width() - TEXT_PADDING, TEXT_START_HEIGHT + 3*TEXT_HEIGHT))
        screen.blit(pink_count_text, (screen_width - pink_count_text.get_width() - TEXT_PADDING, TEXT_START_HEIGHT + 4*TEXT_HEIGHT))
        screen.blit(count_text, (screen_width - count_text.get_width() - TEXT_PADDING, TEXT_START_HEIGHT + 5*TEXT_HEIGHT))
        screen.blit(fps_text, (screen_width - fps_text.get_width() - TEXT_PADDING, TEXT_START_HEIGHT + 6*TEXT_HEIGHT))
        # You can't remove or modify the following two lines
        screen.blit(made_with_love, (screen_width - made_with_love.get_width() - heart.get_width() - 10, screen_height - made_with_love.get_height() - 10))
        screen.blit(heart, (screen_width - heart.get_width() - 10, screen_height - heart.get_height() - 10))

    pygame.display.flip()

pygame.quit()
import sys
import os
import random
import pygame
from pygame import mixer
from button import Button

"""Game made by people with limited and basic knowledge on coding, PLZ no hate, THANKS FOR PLAYING <3"""

mixer.init() #command to add sounds
mixer.music.load("music/Background_music.mp3") #Background sound uploading
background_music_volume = 0.5  #variable for Background sound volume
mixer.music.set_volume(background_music_volume) #setting Background sound volume
mixer.music.play(-1) #playing Background Sound

#Sound effects uploading
Purple_SFX = mixer.Sound("music/bouncing_sound.wav") #need to change and place
Yellow_SFX = mixer.Sound("music/angelic_choir_sound.wav")
Freeze_SFX = mixer.Sound("music/freezing_sound.wav")
Winning_SFX = mixer.Sound("music/mario_item_sound.wav")
volume_SFX=1 #variable for sound effects volume

#Player Colours
Player_1_Blue = (0, 108, 191)  #player
Player_2_Red = (186, 41, 75) #player
#Trail Colours
Blue_Trail = (69, 156, 224, 100) #trail
Red_Trail = (237, 93, 127, 100) #trail

#Arena colours
GREEN = (138, 171, 124)
GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
#Effect Colours
PURPLE = (150, 0, 150)
YELLOW = (255, 212, 75)
LIGHT_BLUISH_WHITE = (173, 216, 230)
PeachPuff = (255, 218, 185)

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info() 
screen_width,screen_height = info.current_w,info.current_h
window_width,window_height = screen_width-10,screen_height-50
SCREEN = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Menu")

Arene_s = (window_width//3)*2
Arene_Ss = (810*Arene_s)//2020
DEFAULT_IMAGE_SIZE = (Arene_s, Arene_Ss)
DEFAULT_IMAGE_SISE = (window_width,window_height)
QUIT_Y = window_height*0.9
OPTION_Y = QUIT_Y - 125
Arene_X = window_width//6

#image uploading
Arene = pygame.image.load("assets/Arene_btn.png")
Arene = pygame.transform.scale(Arene, DEFAULT_IMAGE_SIZE)
Background_Image = pygame.image.load("assets/Background.png")
Background_Image = pygame.transform.scale(Background_Image, DEFAULT_IMAGE_SISE)
Side_Bar_Image = pygame.image.load("assets/side_bar.png")
Rules_Image = pygame.image.load("assets/rulerer.png")
Rules_Image = pygame.transform.scale(Rules_Image, (1920, 1080))
frost_image = pygame.image.load("assets/frost.png")


PIXEL_SIZE = 25
GRID_SIZE = 20
ARENA_WIDTH, ARENA_HEIGHT = PIXEL_SIZE * GRID_SIZE, PIXEL_SIZE * GRID_SIZE
arena_x_offset = (screen_width - ARENA_WIDTH) // 2
arena_y_offset = (screen_height - ARENA_HEIGHT) // 2

player_blue = {"x": 1, "y": 1, "score": 0}
player_red = {"x": 18, "y": 18, "score": 0}
grid = [["green" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
grid[1][1] = "gray"
grid[18][18] = "gray"

wall_count = 5
wall_chance = 0.05
total_walls = 0
max_wall = 60

purple_spawn_count = 2
yellow_spawn_timer = 4
FROST = 0
frost_spawn_interval = 4
PEACH_spawn_interval = 10
clock = pygame.time.Clock()

def options():
    global volume_SFX
    global background_music_volume
    global wall_count
    global max_wall
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("MENU / OPTIONS", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(window_width//2,window_height*0.1))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        RER_TEXT = get_font(45).render(str(wall_count), True, "Black")
        RER_RECT = RER_TEXT.get_rect(center=(window_width//2+350,window_height*0.6))
        SCREEN.blit(RER_TEXT, RER_RECT)
        
        REeR_TEXT = get_font(45).render("Walls per round: ", True, "Black")
        REeR_RECT = REeR_TEXT.get_rect(center=(window_width//2-30,window_height*0.6))
        SCREEN.blit(REeR_TEXT, REeR_RECT)
        
        RER_TEXT = get_font(45).render(str(max_wall), True, "Black")
        RER_RECT = RER_TEXT.get_rect(center=(window_width//2+225,window_height*0.8))
        SCREEN.blit(RER_TEXT, RER_RECT)
        
        REeR_TEXT = get_font(45).render("Max walls: ", True, "Black")
        REeR_RECT = REeR_TEXT.get_rect(center=(window_width//2-30,window_height*0.8))
        SCREEN.blit(REeR_TEXT, REeR_RECT)
        
        Backgroundmus_TEXT = get_font(45).render("Background", True, "Black")
        Backgroundmus_RECT = Backgroundmus_TEXT.get_rect(center=(window_width//2,window_height*0.2))
        SCREEN.blit(Backgroundmus_TEXT, Backgroundmus_RECT)
        
        SFXX_TEXT = get_font(45).render("Sound Effects", True, "Black")
        SFXX_RECT = SFXX_TEXT.get_rect(center=(window_width//2,window_height*0.4))
        SCREEN.blit(SFXX_TEXT, SFXX_RECT)

        OPTIONS_BACK = Button(image=None, pos=(window_width//2,QUIT_Y), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        PLUS_BUTTON_ONE = Button(image=pygame.image.load("assets/plus.png"), pos=(window_width*3//4,window_height*0.2), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        MINUS_BUTTON_ONE = Button(image=pygame.image.load("assets/minus.png"), pos=(window_width//4,window_height*0.2), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        PLUS_BUTTON_TWO = Button(image=pygame.image.load("assets/plus.png"), pos=(window_width*3//4,window_height*0.4), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        MINUS_BUTTON_TWO = Button(image=pygame.image.load("assets/minus.png"), pos=(window_width//4,window_height*0.4), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        PLUS_BUTTON_THREE = Button(image=pygame.image.load("assets/plus.png"), pos=(window_width*3//4,window_height*0.6), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        MINUS_BUTTON_THREE = Button(image=pygame.image.load("assets/minus.png"), pos=(window_width//4,window_height*0.6), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        PLUS_BUTTON_four = Button(image=pygame.image.load("assets/plus.png"), pos=(window_width*3//4,window_height*0.8), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        MINUS_BUTTON_four = Button(image=pygame.image.load("assets/minus.png"), pos=(window_width//4,window_height*0.8), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        
        for button in [PLUS_BUTTON_ONE, MINUS_BUTTON_ONE, PLUS_BUTTON_TWO, MINUS_BUTTON_TWO, PLUS_BUTTON_THREE, MINUS_BUTTON_THREE, PLUS_BUTTON_four, MINUS_BUTTON_four]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)
        
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if PLUS_BUTTON_ONE.checkForInput(OPTIONS_MOUSE_POS):
                    background_music_volume = min(background_music_volume + 0.1, 1.0)
                    set_background_music_volume(background_music_volume)
                    print("hi")
                if MINUS_BUTTON_ONE.checkForInput(OPTIONS_MOUSE_POS):
                    background_music_volume = max(background_music_volume - 0.1, 0.0)
                    set_background_music_volume(background_music_volume)
                    print("bye")
                if PLUS_BUTTON_TWO.checkForInput(OPTIONS_MOUSE_POS):
                    volume_SFX = min(volume_SFX + 0.1, 1.0)
                    print(f"Volume increased to {volume_SFX:.1f}")
                    set_sound_effect_volume(volume_SFX)
                    print("hii")
                if MINUS_BUTTON_TWO.checkForInput(OPTIONS_MOUSE_POS):
                    volume_SFX = max(volume_SFX - 0.1, 0.0)
                    print(f"Volume decreased to {volume_SFX:.1f}")
                    set_sound_effect_volume(volume_SFX)
                    print("byee")
                if PLUS_BUTTON_THREE.checkForInput(OPTIONS_MOUSE_POS):
                    wall_count += 1
                    if wall_count > 10:
                        wall_count = 10
                    print("hiii")
                if MINUS_BUTTON_THREE.checkForInput(OPTIONS_MOUSE_POS):
                    wall_count -= 1
                    if wall_count < 3:
                        wall_count = 3
                    print("byeee")
                if PLUS_BUTTON_four.checkForInput(OPTIONS_MOUSE_POS):
                    max_wall += 3
                    if max_wall > 99:
                        max_wall = 99
                    print("hiiii")
                if MINUS_BUTTON_four.checkForInput(OPTIONS_MOUSE_POS):
                    max_wall -= 3
                    if max_wall < 12:
                        max_wall = 12
                    print("byeeee")
                set_sound_effect_volume(volume_SFX)   

        pygame.display.update()

def draw_arena():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = GREEN
            if grid[y][x] == "gray":
                color = GRAY
            elif grid[y][x] == "black":
                color = BLACK
            elif grid[y][x] == "blue":
                color = Blue_Trail
            elif grid[y][x] == "red":
                color = Red_Trail
            elif grid[y][x] == "purple":
                color = PURPLE
            elif grid[y][x] == "yellow":
                color = YELLOW
            elif grid[y][x] == "frost":
                color = LIGHT_BLUISH_WHITE
            elif grid[y][x] == "PeachPuff":
                color = PeachPuff

            if (x, y) == (player_blue["x"], player_blue["y"]):
                color = Player_1_Blue
            elif (x, y) == (player_red["x"], player_red["y"]):
                color = Player_2_Red

            rect_x = arena_x_offset + x * PIXEL_SIZE
            rect_y = arena_y_offset + y * PIXEL_SIZE
            pygame.draw.rect(SCREEN, color, (rect_x, rect_y, PIXEL_SIZE, PIXEL_SIZE))

def frost_animation(target_player):
    global FROST
    global target_x
    global target_y
    FROST = 1
    if target_player == player_red:
        target_x = 1370
        target_y = OPTION_Y - 280
    else:
        target_x = 95
        target_y = OPTION_Y - 280
    pygame.display.flip()

def spawn_energy():
    global rounds
    for _ in range(purple_spawn_count):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[y][x] == "green":
            grid[y][x] = "purple"

    if rounds % yellow_spawn_timer == 0:
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if grid[y][x] == "green":
                grid[y][x] = "yellow"
                break

    if rounds % frost_spawn_interval == 0:
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if grid[y][x] == "green":
                grid[y][x] = "frost"
                break
            
    if rounds % PEACH_spawn_interval == 0:
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if grid[y][x] == "green":
                grid[y][x] = "PeachPuff"
                break

def spawn_walls():
    global wall_count
    global total_walls
    global max_wall
    """Spawns a fixed number of walls."""
    walls_spawned = 0
    if total_walls < max_wall:
        while walls_spawned < wall_count:
            y = random.randint(0, GRID_SIZE - 1)
            x = random.randint(0, GRID_SIZE - 1)
            if grid[y][x] == "green":
                grid[y][x] = "gray"
                walls_spawned += 1
                total_walls += 1


def move_player(player, dx, dy, trail_color, player_color, opponent):
    """Moves the player on the grid with logic for frost effect."""
    global rounds
    
    nx, ny = player["x"] + dx, player["y"] + dy

    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] not in ("gray"):
        grid[player["y"]][player["x"]] = trail_color
        
        if grid[ny][nx] == "frost":
            Freeze_SFX.play()
            frost_animation(opponent)
            grid[ny][nx] = trail_color
            player["x"], player["y"] = nx, ny
            return True
            
        player["x"], player["y"] = nx, ny

        if grid[ny][nx] == "purple":
            for i in range(max(0, ny - 1), min(GRID_SIZE, ny + 2)):
                for j in range(max(0, nx - 1), min(GRID_SIZE, nx + 2)):
                    if grid[i][j] not in ("black", "gray"):
                        grid[i][j] = trail_color
        elif grid[ny][nx] == "yellow":
            Yellow_SFX.play()
            for i in range(max(0, ny - 2), min(GRID_SIZE, ny + 3)):
                for j in range(max(0, nx - 2), min(GRID_SIZE, nx + 3)):
                    if grid[i][j] not in ("black", "gray"):
                        grid[i][j] = trail_color
                        
        elif grid[ny][nx] == "PeachPuff":
            rounds += 6
        
        return False

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def play():
    global rounds
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.fill("black")
        
        PLAY_TEXT = get_font(45).render("How many rounds?", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(window_width//2, window_height*0.2))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(window_width//2, window_height*0.9), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        twenty_rounds = Button(image=pygame.image.load("assets/20wings.png"), pos=(window_width*3//4,window_height*0.5), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        fifty_rounds = Button(image=pygame.image.load("assets/50crown.png"), pos=(window_width*0.47,window_height*0.5), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        hundred_rounds = Button(image=pygame.image.load("assets/100castle.png"), pos=(window_width*1//4,window_height*0.48), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        RULES_BUTTON = Button(image=pygame.image.load("assets/Rules.png"), pos=(window_width*0.5,window_height*0.75), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [twenty_rounds, fifty_rounds, hundred_rounds, RULES_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if twenty_rounds.checkForInput(PLAY_MOUSE_POS):
                    rounds = 20
                    game()
                if fifty_rounds.checkForInput(PLAY_MOUSE_POS):
                    rounds = 50
                    game()
                if hundred_rounds.checkForInput(PLAY_MOUSE_POS):
                    rounds = 100
                    game()
                if RULES_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    RULES()

        pygame.display.update()

def game():
    global rounds
    global FROST
    global target_x
    global target_y
    global grid
    grid = [["green" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    grid[1][1] = "gray"  # Blue player's starting position
    grid[18][18] = "gray"  # Red player's starting position

    global player_blue, player_red
    player_blue = {"x": 1, "y": 1, "score": 0}  # Blue starts in top-left corner
    player_red = {"x": 18, "y": 18, "score": 0}  # Red starts in bottom-right corner

    spawn_energy()
    
    is_blue_turn = True

    Up_Dub_Blu_BUTTON = Button(image=pygame.image.load("assets/arrows/player2-dubarrow-up.png"), 
                                pos=(window_width // 6, OPTION_Y - 250), text_input=" ", 
                                font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    left_Dub_Blu_BUTTON = Button(image=pygame.image.load("assets/arrows/player2-dubarrow-left.png"), 
                                  pos=(window_width // 18, OPTION_Y - 50), text_input=" ", 
                                  font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    right_Dub_Blu_BUTTON = Button(image=pygame.image.load("assets/arrows/player2-dubarrow-right.png"), 
                                   pos=((window_width // 4) + 50, OPTION_Y - 50), text_input=" ", 
                                   font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    down_Dub_Blu_BUTTON = Button(image=pygame.image.load("assets/arrows/player2-dubarrow-down.png"), 
                                  pos=(window_width // 6, OPTION_Y + 150), text_input=" ", 
                                  font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    Up_Blu_BUTTON = Button(image=pygame.image.load("assets/arrows/player2-arrow-up.png"), 
                            pos=(window_width // 6, OPTION_Y - 150), text_input=" ", 
                            font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    left_Blu_BUTTON = Button(image=pygame.image.load("assets/arrows/player2-arrow-left.png"), 
                              pos=(window_width // 6 - 108, OPTION_Y - 50), text_input=" ", 
                              font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    right_Blu_BUTTON = Button(image=pygame.image.load("assets/arrows/player2-arrow-right.png"), 
                               pos=(window_width // 4 - 52, OPTION_Y - 50), text_input=" ", 
                               font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    down_Blu_BUTTON = Button(image=pygame.image.load("assets/arrows/player2-arrow-down.png"), 
                              pos=(window_width // 6, OPTION_Y + 50), text_input=" ", 
                              font=get_font(75), base_color="#24d19a", hovering_color="Blue")

    Up_Dub_red_BUTTON = Button(image=pygame.image.load("assets/arrows/player1-dubarrow-up.png"), 
                                pos=(window_width // 6 + 500 + 755 + 20, OPTION_Y - 250), text_input=" ", 
                                font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    left_Dub_red_BUTTON = Button(image=pygame.image.load("assets/arrows/player1-dubarrow-left.png"), 
                                  pos=(window_width // 18 + 500 + 755 + 20, OPTION_Y - 50), text_input=" ", 
                                  font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    right_Dub_red_BUTTON = Button(image=pygame.image.load("assets/arrows/player1-dubarrow-right.png"), 
                                   pos=((window_width // 4) + 50 + 500 + 755 + 20, OPTION_Y - 50), text_input=" ", 
                                   font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    down_Dub_red_BUTTON = Button(image=pygame.image.load("assets/arrows/player1-dubarrow-down.png"), 
                                  pos=(window_width // 6 + 500 + 755 + 20, OPTION_Y + 150), text_input=" ", 
                                  font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    Up_red_BUTTON = Button(image=pygame.image.load("assets/arrows/player1-arrow-up.png"), 
                            pos=(window_width // 6 + 500 + 755 + 20, OPTION_Y - 150), text_input=" ", 
                            font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    left_red_BUTTON = Button(image=pygame.image.load("assets/arrows/player1-arrow-left.png"), 
                              pos=(window_width // 6 + 500 - 108 + 755 + 20, OPTION_Y - 50), text_input=" ", 
                              font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    right_red_BUTTON = Button(image=pygame.image.load("assets/arrows/player1-arrow-right.png"), 
                               pos=(window_width // 4 - 52 + 500 + 755 + 20, OPTION_Y - 50), text_input=" ", 
                               font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    down_red_BUTTON = Button(image=pygame.image.load("assets/arrows/player1-arrow-down.png"), 
                              pos=(window_width // 6 + 500 + 755 + 20, OPTION_Y + 50), text_input=" ", 
                              font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    
    while rounds > 0:
        if is_blue_turn:
            SCREEN.fill(Player_1_Blue)
        elif not is_blue_turn:
            SCREEN.fill(Player_2_Red)
        SCREEN.blit(Side_Bar_Image, (-10, 0))
        SCREEN.blit(Side_Bar_Image, (1235, 0))
        draw_arena()
        
        blue_scorez = sum(row.count("blue") for row in grid)
        red_scorez = sum(row.count("red") for row in grid)
        
        bluez_text = get_font(30).render(f"Points: {blue_scorez}", True, "royalblue3")
        SCREEN.blit(bluez_text, (50, 40))
        redz_text = get_font(30).render(f"Points: {red_scorez}", True, "red3")
        SCREEN.blit(redz_text, (1275, 40))
        
        rounds_text = get_font(30).render(f"Rounds Left: {rounds}", True, "White")
        SCREEN.blit(rounds_text, (720, 20))

        turn_text = "Blue's Turn" if is_blue_turn else "Red's Turn"
        turn_display = get_font(30).render(turn_text, True, "lightskyblue" if is_blue_turn else "lightcoral")
        SCREEN.blit(turn_display, (720, 60))

        for button in [
            Up_Dub_Blu_BUTTON, left_Dub_Blu_BUTTON, right_Dub_Blu_BUTTON, down_Dub_Blu_BUTTON,
            Up_Blu_BUTTON, left_Blu_BUTTON, right_Blu_BUTTON, down_Blu_BUTTON,
            Up_Dub_red_BUTTON, left_Dub_red_BUTTON, right_Dub_red_BUTTON, down_Dub_red_BUTTON,
            Up_red_BUTTON, left_red_BUTTON, right_red_BUTTON, down_red_BUTTON
        ]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)
        
        if FROST == 1:
            SCREEN.blit(frost_image, (target_x, target_y))

        valid_input = False
        frost_effect = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_blue_turn:
                    if Up_Blu_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 0, -1, "blue", Player_1_Blue, player_red)
                        valid_input = True
                    if down_Blu_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 0, 1, "blue", Player_1_Blue, player_red)
                        valid_input = True
                    if left_Blu_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, -1, 0, "blue", Player_1_Blue, player_red)
                        valid_input = True
                    if right_Blu_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 1, 0, "blue", Player_1_Blue, player_red)
                        valid_input = True
                    if Up_Dub_Blu_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 0, -2, "blue", Player_1_Blue, player_red)
                        valid_input = True
                    if down_Dub_Blu_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 0, 2, "blue", Player_1_Blue, player_red)
                        valid_input = True
                    if left_Dub_Blu_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, -2, 0, "blue", Player_1_Blue, player_red)
                        valid_input = True
                    if right_Dub_Blu_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 2, 0, "blue", Player_1_Blue, player_red)
                        valid_input = True

                elif not is_blue_turn:
                    if Up_red_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 0, -1, "red", Player_2_Red, player_blue)
                        valid_input = True
                    if down_red_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 0, 1, "red", Player_2_Red, player_blue)
                        valid_input = True
                    if left_red_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, -1, 0, "red", Player_2_Red, player_blue)
                        valid_input = True
                    if right_red_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 1, 0, "red", Player_2_Red, player_blue)
                        valid_input = True
                    if Up_Dub_red_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 0, -2, "red", Player_2_Red, player_blue)
                        valid_input = True
                    if down_Dub_red_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 0, 2, "red", Player_2_Red, player_blue)
                        valid_input = True
                    if left_Dub_red_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, -2, 0, "red", Player_2_Red, player_blue)
                        valid_input = True
                    if right_Dub_red_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 2, 0, "red", Player_2_Red, player_blue)
                        valid_input = True

        if valid_input:
            rounds -= 1
            if not frost_effect:
                is_blue_turn = not is_blue_turn

            if rounds % 2 == 0:
                spawn_walls()
                spawn_energy()

        pygame.display.flip()
        clock.tick(30)

    player_blue["score"] = sum(row.count("blue") for row in grid)
    player_red["score"] = sum(row.count("red") for row in grid)
    winner = "Blue" if player_blue["score"] > player_red["score"] else "Red"
    display_winner(winner, player_blue["score"], player_red["score"])
    
def display_winner(winner, blue_score, red_score):
    Winning_SFX.play()
    while True:
        SCREEN.fill((0, 0, 0))

        # Display winner text
        winner_text = get_font(60).render(f"{winner} Wins!", True, "Yellow")
        winner_rect = winner_text.get_rect(center=(screen_width // 2, screen_height // 3))
        SCREEN.blit(winner_text, winner_rect)

        # Display scores
        blue_score_text = get_font(40).render(f"Blue Score: {blue_score}", True, "cornflower blue")
        red_score_text = get_font(40).render(f"Red Score: {red_score}", True, "firebrick3")
        blue_score_rect = blue_score_text.get_rect(center=(screen_width // 2, screen_height // 2))
        red_score_rect = red_score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        SCREEN.blit(blue_score_text, blue_score_rect)
        SCREEN.blit(red_score_text, red_score_rect)

        menu_button = Button(image=None, pos=(screen_width // 3, screen_height * 3 // 4), 
                             text_input="MAIN MENU", font=get_font(50), base_color="White", hovering_color="Green")
        quit_button = Button(image=None, pos=(screen_width * 2 // 3, screen_height * 3 // 4), 
                             text_input="QUIT", font=get_font(50), base_color="White", hovering_color="Red")

        for button in [menu_button, quit_button]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkForInput(pygame.mouse.get_pos()):
                    main_menu()
                if quit_button.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


def set_sound_effect_volume(volume_SFX):
    """Set the volume for all sound effects."""
    Yellow_SFX.set_volume(volume_SFX)
    Purple_SFX.set_volume(volume_SFX)
    Freeze_SFX.set_volume(volume_SFX)
    Winning_SFX.set_volume(volume_SFX)
    
def set_background_music_volume(volume):
    mixer.music.set_volume(volume)
    print(f"Background music volume set to {volume:.1f}")

def main_menu():
    while True:
        SCREEN.blit(Background_Image, (0, 0))
        SCREEN.blit(Arene, (Arene_X, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        MENU_TEXT = get_font(100).render(" ", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
       
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(window_width//2,OPTION_Y-125), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(window_width//2,OPTION_Y), 
                            text_input="  ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(window_width//2,QUIT_Y), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()
        
def RULES():
    while True:
        SCREEN.fill("white")
        RULES_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(Rules_Image, (0, -50))
        
        back_BUTTON = Button(image=None, pos=(window_width//2, window_height*0.9), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        for button in [back_BUTTON]:
            button.changeColor(RULES_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_BUTTON.checkForInput(RULES_MOUSE_POS):
                    play()
                    
        pygame.display.update()

main_menu()

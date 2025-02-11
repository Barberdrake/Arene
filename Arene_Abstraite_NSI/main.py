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

Error_Sound = mixer.Sound("music/error_sound.wav")
Error_Sound.set_volume(1.0)

#Sound effects uploading
Purple_SFX = mixer.Sound("music/squeak_sound.wav") 
Yellow_SFX = mixer.Sound("music/angelic_choir_sound.wav")
Freeze_SFX = mixer.Sound("music/freezing_sound.wav")
Peach_Puff_SFX = mixer.Sound("music/thingly_sound.wav")
Winning_SFX = mixer.Sound("music/yay_sound.wav")
volume_SFX = 1 #variable for sound effects volume

#Player Colours
Player1_Blue = (0, 108, 191)  #player 1's colour
Player2_Red = (186, 41, 75) #player 2's colour
#Trail Colours
Blue_Trail = (69, 156, 224, 100) #trail colour for player 1
Red_Trail = (237, 93, 127, 100) #trail colour for player 2

BLACK = (0, 0, 0) #button colours
GRAY = (50, 50, 50) #wall color
GREEN = (138, 171, 124) #background of the arena
PURPLE = (150, 0, 150) #3x3 effect, purple colour
YELLOW = (255, 212, 75) #5x5 effect, yellow colour
LIGHT_BLUISH_WHITE = (173, 216, 230) #frost effect colour
PEACH = (255, 218, 185) #add rounds effect, peach colour

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info() 
screen_width,screen_height = info.current_w,info.current_h
print("screen_width",screen_width,"screen_height",screen_height)
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
Rules_Image = pygame.transform.scale(Rules_Image, (screen_width-screen_width*0.1, screen_height-screen_height*0.1))
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

purple_spawn_interval = 2
yellow_spawn_interval = 4
FROST = 0
frost_spawn_interval = 4
peach_spawn_interval = 10
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

        #TEXT for the Wall Count per Round Option
        Wall_Count_TEXT = get_font(45).render(str(wall_count), True, "Black")
        Wall_Count_RECT = Wall_Count_TEXT.get_rect(center=(window_width//2+350,window_height*0.6))
        SCREEN.blit(Wall_Count_TEXT, Wall_Count_RECT)
        
        Walls_Rounds_TEXT = get_font(45).render("Walls per round: ", True, "Black")
        Walls_Rounds_RECT = Walls_Rounds_TEXT.get_rect(center=(window_width//2-30,window_height*0.6))
        SCREEN.blit(Walls_Rounds_TEXT, Walls_Rounds_RECT)

        
        #TEXT for the Max Walls per Round
        Wall_MaxNumber_TEXT = get_font(45).render(str(max_wall), True, "Black")
        Wall_MaxNumber_RECT = Wall_MaxNumber_TEXT.get_rect(center=(window_width//2+225,window_height*0.8))
        SCREEN.blit(Wall_MaxNumber_TEXT, Wall_MaxNumber_RECT)
        
        Walls_Max_TEXT = get_font(45).render("Max walls: ", True, "Black")
        Walls_Max_RECT = Walls_Max_TEXT.get_rect(center=(window_width//2-30,window_height*0.8))
        SCREEN.blit(Walls_Max_TEXT, Walls_Max_RECT)

        #TEXT for Background Sound Volume Options
        Background_TEXT = get_font(45).render(f"Background : {background_music_volume:.1f}", True, "Black")
        Background_RECT = Background_TEXT.get_rect(center=(window_width//2,window_height*0.2))
        SCREEN.blit(Background_TEXT, Background_RECT)

        #TEXT for Sound effects Volume Options
        SFX_TEXT = get_font(45).render(f"SFX Volume : {volume_SFX:.1f}", True, "Black")
        SFX_RECT = SFX_TEXT.get_rect(center=(window_width//2,window_height*0.4))
        SCREEN.blit(SFX_TEXT, SFX_RECT)

        OPTIONS_BACK = Button(image=None, pos=(window_width//2,QUIT_Y), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        PLUS_BUTTON_Background = Button(image=pygame.image.load("assets/plus.png"), pos=(window_width*3//4,window_height*0.2), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        MINUS_BUTTON_Background = Button(image=pygame.image.load("assets/minus.png"), pos=(window_width//4,window_height*0.2), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        PLUS_BUTTON_SFX = Button(image=pygame.image.load("assets/plus.png"), pos=(window_width*3//4,window_height*0.4), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        MINUS_BUTTON_SFX = Button(image=pygame.image.load("assets/minus.png"), pos=(window_width//4,window_height*0.4), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        PLUS_BUTTON_Wall_Count = Button(image=pygame.image.load("assets/plus.png"), pos=(window_width*3//4,window_height*0.6), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        MINUS_BUTTON_Wall_Count = Button(image=pygame.image.load("assets/minus.png"), pos=(window_width//4,window_height*0.6), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        PLUS_BUTTON_Max_Wall = Button(image=pygame.image.load("assets/plus.png"), pos=(window_width*3//4,window_height*0.8), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        MINUS_BUTTON_Max_Wall = Button(image=pygame.image.load("assets/minus.png"), pos=(window_width//4,window_height*0.8), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        
        for button in [PLUS_BUTTON_Background, MINUS_BUTTON_Background, PLUS_BUTTON_SFX, MINUS_BUTTON_SFX, PLUS_BUTTON_Wall_Count, MINUS_BUTTON_Wall_Count, PLUS_BUTTON_Max_Wall, MINUS_BUTTON_Max_Wall]:
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
                    
                if PLUS_BUTTON_Background.checkForInput(OPTIONS_MOUSE_POS):
                    if background_music_volume == 1.0:
                        Error_Sound.play()
                    background_music_volume = min(background_music_volume + 0.1, 1.0)
                    set_background_music_volume(background_music_volume)
                if MINUS_BUTTON_Background.checkForInput(OPTIONS_MOUSE_POS):
                    if background_music_volume == 0.0:
                        Error_Sound.play()
                    background_music_volume = max(background_music_volume - 0.1, 0.0)
                    set_background_music_volume(background_music_volume)
                    
                if PLUS_BUTTON_SFX.checkForInput(OPTIONS_MOUSE_POS):
                    if volume_SFX == 1.0:
                        Error_Sound.play()
                    volume_SFX = min(volume_SFX + 0.1, 1.0)
                    set_sound_effect_volume(volume_SFX)
                    print(f"Volume increased to {volume_SFX:.1f}")
                    print("hii")
                if MINUS_BUTTON_SFX.checkForInput(OPTIONS_MOUSE_POS):
                    if volume_SFX == 0.0:
                        Error_Sound.play()
                    volume_SFX = max(volume_SFX - 0.1, 0.0)
                    set_sound_effect_volume(volume_SFX)
                    print(f"Volume decreased to {volume_SFX:.1f}")
                    print("byee")
                    
                if PLUS_BUTTON_Wall_Count.checkForInput(OPTIONS_MOUSE_POS):
                    wall_count += 1
                    if wall_count > 10:
                        wall_count = 10
                        Error_Sound.play()
                if MINUS_BUTTON_Wall_Count.checkForInput(OPTIONS_MOUSE_POS):
                    wall_count -= 1
                    if wall_count < 3:
                        wall_count = 3
                        Error_Sound.play()
                        
                if PLUS_BUTTON_Max_Wall.checkForInput(OPTIONS_MOUSE_POS):
                    max_wall += 3
                    if max_wall > 99:
                        max_wall = 99
                        Error_Sound.play()
                if MINUS_BUTTON_Max_Wall.checkForInput(OPTIONS_MOUSE_POS):
                    max_wall -= 3
                    if max_wall < 12:
                        max_wall = 12
                        Error_Sound.play()
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
            elif grid[y][x] == "peach":
                color = PEACH

            if (x, y) == (player_blue["x"], player_blue["y"]):
                color = Player1_Blue
            elif (x, y) == (player_red["x"], player_red["y"]):
                color = Player2_Red

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
    for _ in range(purple_spawn_interval):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[y][x] == "green":
            grid[y][x] = "purple"

    if rounds % yellow_spawn_interval == 0:
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
            
    if rounds % peach_spawn_interval == 0:
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if grid[y][x] == "green":
                grid[y][x] = "peach"
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
            Purple_SFX.play(2)
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
                        
        elif grid[ny][nx] == "peach":
            Peach_Puff_SFX.play()
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

        BACK_Play_Button = Button(image=None, pos=(window_width//2, window_height*0.9), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        Twenty_Rounds_Button = Button(image=pygame.image.load("assets/20wings.png"), pos=(window_width*3//4,window_height*0.5), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        Fifty_Rounds_Button = Button(image=pygame.image.load("assets/50crown.png"), pos=(window_width*0.47,window_height*0.5), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        Hundred_Rounds_Button = Button(image=pygame.image.load("assets/100castle.png"), pos=(window_width*1//4,window_height*0.48), 
                            text_input=" ", font=get_font(75), base_color="#24d19a", hovering_color="Blue")
        RULES_Button = Button(image=pygame.image.load("assets/Rules.png"), pos=(window_width*0.5,window_height*0.75), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [Twenty_Rounds_Button, Fifty_Rounds_Button, Hundred_Rounds_Button, RULES_Button]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        BACK_Play_Button.changeColor(PLAY_MOUSE_POS)
        BACK_Play_Button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_Play_Button.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if Twenty_Rounds_Button.checkForInput(PLAY_MOUSE_POS):
                    rounds = 20
                    game()
                if Fifty_Rounds_Button.checkForInput(PLAY_MOUSE_POS):
                    rounds = 50
                    game()
                if Hundred_Rounds_Button.checkForInput(PLAY_MOUSE_POS):
                    rounds = 100
                    game()
                if RULES_Button.checkForInput(PLAY_MOUSE_POS):
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
    
    Player1_turn = True #is it Player 1's turn = True

    UP_2x_Blue_Button = Button(image=pygame.image.load("assets/arrows/player2-dubarrow-up.png"), 
                                pos=(window_width // 6, OPTION_Y - 250), text_input=" ", 
                                font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    LEFT_2x_Blue_Button = Button(image=pygame.image.load("assets/arrows/player2-dubarrow-left.png"), 
                                  pos=(window_width // 18, OPTION_Y - 50), text_input=" ", 
                                  font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    RIGHT_2x_Blue_Button = Button(image=pygame.image.load("assets/arrows/player2-dubarrow-right.png"), 
                                   pos=((window_width // 4) + 50, OPTION_Y - 50), text_input=" ", 
                                   font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    DOWN_2x_Blue_Button = Button(image=pygame.image.load("assets/arrows/player2-dubarrow-down.png"), 
                                  pos=(window_width // 6, OPTION_Y + 150), text_input=" ", 
                                  font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    UP_Blue_Button = Button(image=pygame.image.load("assets/arrows/player2-arrow-up.png"), 
                            pos=(window_width // 6, OPTION_Y - 150), text_input=" ", 
                            font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    LEFT_Blue_Button = Button(image=pygame.image.load("assets/arrows/player2-arrow-left.png"), 
                              pos=(window_width // 6 - 108, OPTION_Y - 50), text_input=" ", 
                              font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    RIGHT_Blue_Button = Button(image=pygame.image.load("assets/arrows/player2-arrow-right.png"), 
                               pos=(window_width // 4 - 52, OPTION_Y - 50), text_input=" ", 
                               font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    DOWN_Blue_Button = Button(image=pygame.image.load("assets/arrows/player2-arrow-down.png"), 
                              pos=(window_width // 6, OPTION_Y + 50), text_input=" ", 
                              font=get_font(75), base_color="#24d19a", hovering_color="Blue")

    UP_2x_Red_Button = Button(image=pygame.image.load("assets/arrows/player1-dubarrow-up.png"), 
                                pos=(window_width // 6 + 500 + 755 + 20, OPTION_Y - 250), text_input=" ", 
                                font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    LEFT_2x_Red_Button = Button(image=pygame.image.load("assets/arrows/player1-dubarrow-left.png"), 
                                  pos=(window_width // 18 + 500 + 755 + 20, OPTION_Y - 50), text_input=" ", 
                                  font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    RIGHT_2x_Red_Button = Button(image=pygame.image.load("assets/arrows/player1-dubarrow-right.png"), 
                                   pos=((window_width // 4) + 50 + 500 + 755 + 20, OPTION_Y - 50), text_input=" ", 
                                   font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    DOWN_2x_Red_Button = Button(image=pygame.image.load("assets/arrows/player1-dubarrow-down.png"), 
                                  pos=(window_width // 6 + 500 + 755 + 20, OPTION_Y + 150), text_input=" ", 
                                  font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    UP_Red_Button = Button(image=pygame.image.load("assets/arrows/player1-arrow-up.png"), 
                            pos=(window_width // 6 + 500 + 755 + 20, OPTION_Y - 150), text_input=" ", 
                            font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    LEFT_Red_Button = Button(image=pygame.image.load("assets/arrows/player1-arrow-left.png"), 
                              pos=(window_width // 6 + 500 - 108 + 755 + 20, OPTION_Y - 50), text_input=" ", 
                              font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    RIGHT_Red_Button = Button(image=pygame.image.load("assets/arrows/player1-arrow-right.png"), 
                               pos=(window_width // 4 - 52 + 500 + 755 + 20, OPTION_Y - 50), text_input=" ", 
                               font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    DOWN_Red_Button = Button(image=pygame.image.load("assets/arrows/player1-arrow-down.png"), 
                              pos=(window_width // 6 + 500 + 755 + 20, OPTION_Y + 50), text_input=" ", 
                              font=get_font(75), base_color="#24d19a", hovering_color="Blue")
    
    while rounds > 0:
        if Player1_turn:
            SCREEN.fill(Player1_Blue)
        elif not Player1_turn:
            SCREEN.fill(Player2_Red)
        SCREEN.blit(Side_Bar_Image, (-10, 0))
        SCREEN.blit(Side_Bar_Image, (1235, 0))
        draw_arena()
        
        Player1_Scores = sum(row.count("blue") for row in grid)
        Player2_Scores = sum(row.count("red") for row in grid)
        
        Blue_Text = get_font(30).render(f"Points: {Player1_Scores}", True, "royalblue3")
        SCREEN.blit(Blue_Text, (50, 40))
        Red_Text = get_font(30).render(f"Points: {Player2_Scores}", True, "red3")
        SCREEN.blit(Red_Text, (1275, 40))
        
        Rounds_Text = get_font(30).render(f"Rounds Left: {rounds}", True, "White")
        SCREEN.blit(Rounds_Text, (720, 20))

        Turn_Text = "Blue's Turn" if Player1_turn else "Red's Turn"
        Turn_Display = get_font(30).render(Turn_Text, True, "lightskyblue" if Player1_turn else "lightcoral")
        SCREEN.blit(Turn_Display, (720, 60))

        for button in [
            UP_2x_Blue_Button, LEFT_2x_Blue_Button, RIGHT_2x_Blue_Button, DOWN_2x_Blue_Button,
            UP_Blue_Button, LEFT_Blue_Button, RIGHT_Blue_Button, DOWN_Blue_Button,
            UP_2x_Red_Button, LEFT_2x_Red_Button, RIGHT_2x_Red_Button, DOWN_2x_Red_Button,
            UP_Red_Button, LEFT_Red_Button, RIGHT_Red_Button, DOWN_Red_Button
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
                if Player1_turn:
                    if UP_Blue_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 0, -1, "blue", Player1_Blue, player_red)
                        valid_input = True
                    if DOWN_Blue_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 0, 1, "blue", Player1_Blue, player_red)
                        valid_input = True
                    if LEFT_Blue_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, -1, 0, "blue", Player1_Blue, player_red)
                        valid_input = True
                    if RIGHT_Blue_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 1, 0, "blue", Player1_Blue, player_red)
                        valid_input = True
                    if UP_2x_Blue_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 0, -2, "blue", Player1_Blue, player_red)
                        valid_input = True
                    if DOWN_2x_Blue_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 0, 2, "blue", Player1_Blue, player_red)
                        valid_input = True
                    if LEFT_2x_Blue_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, -2, 0, "blue", Player1_Blue, player_red)
                        valid_input = True
                    if RIGHT_2x_Blue_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_blue, 2, 0, "blue", Player1_Blue, player_red)
                        valid_input = True

                elif not Player1_turn:
                    if UP_Red_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 0, -1, "red", Player2_Red, player_blue)
                        valid_input = True
                    if DOWN_Red_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 0, 1, "red", Player2_Red, player_blue)
                        valid_input = True
                    if LEFT_Red_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, -1, 0, "red", Player2_Red, player_blue)
                        valid_input = True
                    if RIGHT_Red_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 1, 0, "red", Player2_Red, player_blue)
                        valid_input = True
                    if UP_2x_Red_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 0, -2, "red", Player2_Red, player_blue)
                        valid_input = True
                    if DOWN_2x_Red_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 0, 2, "red", Player2_Red, player_blue)
                        valid_input = True
                    if LEFT_2x_Red_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, -2, 0, "red", Player2_Red, player_blue)
                        valid_input = True
                    if RIGHT_2x_Red_Button.checkForInput(pygame.mouse.get_pos()):
                        FROST = 0
                        frost_effect = move_player(player_red, 2, 0, "red", Player2_Red, player_blue)
                        valid_input = True

        if valid_input:
            rounds -= 1
            if not frost_effect:
                Player1_turn = not Player1_turn

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
    Peach_Puff_SFX.set_volume(volume_SFX)
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
        SCREEN.blit(Rules_Image, (int(screen_width/25), int(screen_height/215)))
        
        back_BUTTON = Button(image=None, pos=(window_width*0.825, window_height*0.85), 
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

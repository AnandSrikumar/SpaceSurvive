import math
import Sprites
import pygame
from Segments import PlayerSegment
from Segments import Background
from EnemyRandom import RandomInit
import sys

WHITE = (255, 255, 255)
RED = (255, 0, 0)
pygame.init()
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = pygame.display.get_surface().get_size()

player_x, player_y = w / 2, h / 2
player_w, player_h = 0, 0
game_start = True
angle = 0
bullet_cool, cooling_time = pygame.USEREVENT + 1, 100
slope = 0
fire = True
dx = 0
bullet_list = []
mouse_pressed = False
right, left, up, down, shift = False, False, False, False, False
movement_speed = 20
background_x, background_y, background_x2, background_y2 = 0, 0, w, h
slope_e, dx_e = 0, 0
enemy_prepare = RandomInit(w, h)
end_sound, end_sound_time = pygame.USEREVENT+1, 100
can_play_sound = True
enemy_coming, coming_time = pygame.USEREVENT+2, 600
invincible_event, invincible_time = pygame.USEREVENT+3, 1000
enemy_bullet_event, enemy_bullet = pygame.USEREVENT+4, 100
enemy_shoot, shoot_time = pygame.USEREVENT+5, 50
can_enemy_load = True
can_enemy_fire = True
can_enemy_come = True
can_enemy_add = False
enemy_list = []
player_health = 100
player_max_health = 100
invincible = False
bul_wid, bul_hie = 150, 50
game_fin = False
score = 0
explosions = []
explosion_limit = 11
levels = [[5, 4], [8, 5], [10, 7]]
curr_level = 0
max_level = 2
enemy_bullets = []
boss = False
music_loaded = True
music = [Sprites.music, Sprites.boss_music]
music_index = 0
platformer = True
stage_x = -1500
stage_y = -1000
max_stage_x = 75000
max_stage_y = 75000
player_sprite = 0
bullet_sprite = 0


def event_handling():
    global mouse_pressed, fire, can_enemy_come, invincible, can_play_sound
    global can_enemy_fire, can_enemy_load
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
                sys.exit()

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
            # pygame.mouse.set_visible(False)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
        if event.type == bullet_cool:
            fire = True

        if event.type == enemy_coming:
            can_enemy_come = True

        if event.type == invincible_event:
            invincible = False

        if event.type == end_sound:
            can_play_sound = True
        if event.type == enemy_bullet_event:
            can_enemy_load = True
        if event.type == enemy_bullet:
            can_enemy_fire = True


def prepare_to_fire():
    global bullet_list, fire, can_play_sound
    if mouse_pressed and fire:
        bullet_list.append([player_x, player_y, slope, angle, dx])
        pygame.time.set_timer(bullet_cool, cooling_time)
        fire = False
        if can_play_sound:
            play_sound(Sprites.bullet_sound)
            can_play_sound = False


def load_enemy_bullet(x, y, ang, e_slope, p1, p2):
    global can_enemy_fire, can_enemy_load, enemy_bullets
    if can_enemy_load:

        enemy_bullets.append([x, y, e_slope, ang, (p1-p2)])
        can_enemy_load = False
        pygame.time.set_timer(enemy_bullet_event, enemy_bullet)


def calc_angle():
    global angle, slope, dx
    if game_start:
        points2 = pygame.mouse.get_pos()
        dx = points2[0] - player_x
        dy = points2[1] - player_y
        if dx != 0:
            slope = dy / dx
        angle = math.atan2(dy, dx)
        angle = math.degrees(-angle) + 90


def draw_sprites():
    global player_w, player_h, player_sprite
    calc_angle()
    segment = PlayerSegment(player_x, player_y, Sprites.player[player_sprite], angle1=angle, rotate=True)
    display_surface.blit(segment.image, segment.rect)
    player_sprite += 1
    player_w = segment.width
    player_h = segment.height
    if invincible:
        #pygame.draw.rect(display_surface, WHITE, (player_x-player_w/2, player_y-player_h/2, player_w, player_h), 1)
        pygame.draw.circle(display_surface, RED, (int(player_x), int(player_y)), player_w//2, 1)
    #pygame.display.update(segment.rect)
    if player_sprite == len(Sprites.player):
        player_sprite = 0


def draw_bullet(all_bullets, fire_bullet=Sprites.sample_bullet2, width=150, height=50, speed_x=30, speed_y=30):
    remove_list = []
    x_speed = speed_x
    y_speed = speed_y
    for bullets in all_bullets:
        if len(bullets) > 1:

            segment2 = PlayerSegment(bullets[0], bullets[1], fire_bullet, rotate=True,
                                 angle1=bullets[3], wid=width, hie=height)
            display_surface.blit(segment2.image, segment2.rect)
            #pygame.display.update(segment2.rect)
            y_speed = bullets[2] * x_speed
            if bullets[2] > 1:
                y_speed = speed_y
                x_speed = y_speed/bullets[2]

            elif bullets[2] < -1:
                y_speed = -speed_y
                x_speed = y_speed / bullets[2]

            if bullets[4] > 0:
                bullets[0] += x_speed
                bullets[1] += y_speed
            else:
                bullets[0] -= x_speed
                bullets[1] -= y_speed
            if bullets[0] > w or bullets[0]+segment2.width < 0 or bullets[1]+segment2.height < 0 or bullets[1] > h:
                remove_list.append(bullets)
    for rem in remove_list:
        all_bullets.remove(rem)


def movements():
    global player_x, player_y, player_w, player_h, movement_speed

    if shift:
        movement_speed = 20

    elif not shift:
        movement_speed = 10
    if not platformer:
        if right:
            if player_x + player_w/2 < w:
                player_x += movement_speed
        if left:
            if player_x - player_w/2 > 0:
                player_x -= movement_speed
        if up:
            if player_y - player_h/2 > 0:
                player_y -= movement_speed
        if down:
            if player_y + player_h/2 < h:
                player_y += movement_speed
    else:
        if right:
            if player_x + player_w/2 < w*0.75:
                player_x += movement_speed
        if left:
            if player_x - player_w/2 > w*0.25:
                player_x -= movement_speed
        if up:
            if player_y - player_h/2 > h*0.25:
                player_y -= movement_speed
        if down:
            if player_y + player_h/2 < h*0.75:
                player_y += movement_speed


def controls(key):
    global right, left, up, down, shift
    if key[pygame.K_d]:
        right = True
        left = False

    if key[pygame.K_a]:
        left = True
        right = False

    if key[pygame.K_w]:
        up = True
        down = False

    if key[pygame.K_s]:
        down = True
        up = False

    if key[pygame.K_RSHIFT] or key[pygame.K_LSHIFT]:
        shift = True


def controls_released(key):
    global right, left, up, down, shift
    if not key[pygame.K_d]:
        right = False

    if not key[pygame.K_a]:
        left = False

    if not key[pygame.K_w]:
        up = False

    if not key[pygame.K_s]:
        down = False

    if not (key[pygame.K_RSHIFT] or key[pygame.K_LSHIFT]):
        shift = False


def draw_background():
    if platformer:
        space1 = Background(background_x, background_y, Sprites.spacedark, wid=w, hie=w)
        display_surface.blit(space1.image, space1.rect)

    else:
        space1 = Background(background_x, background_y, Sprites.spacedark, wid=w, hie=h)
        display_surface.blit(space1.image, space1.rect)


def move_background():
    global background_x, background_y, background_x2, background_y2

    if player_x + player_w/2 >= w*0.7 and right:
        background_x -= movement_speed

    if player_x - player_w/2 <= w*0.25 and left:
        background_x += movement_speed

    if player_y + player_h/2 >= 0.7*h and down:
        background_y -= movement_speed

    if player_y - player_h/2 <= h*0.25 and up:
        background_y += movement_speed

    if background_x < -w:
        background_x = w

    if background_x > w:
        background_x = -w

    if background_y < -h:
        background_y = h

    if background_y > h:
        background_y = -h


def drawing_enemy():
    if platformer:
        draw_enemy_platform()
    else:
        draw_enemy()


def draw_enemy():
    global enemy_list, can_enemy_come, can_enemy_add, player_health, levels, curr_level, boss, music_loaded, music_index
    rem_list = []
    if levels[curr_level][1] == 0:
        if curr_level < max_level and not boss:
            curr_level += 1
    enem_len = levels[curr_level][0]
    if can_enemy_come and len(enemy_list) < enem_len and can_enemy_add and not boss:
        e_list = enemy_prepare.get_random_enemy(player_x, player_y)
        enemy_list.append(e_list)
        pygame.time.set_timer(enemy_coming, coming_time)
        can_enemy_come = False

    if len(enemy_list) == 0 and not can_enemy_add and not game_fin and not boss:
        can_enemy_add = True
        if player_health + 45 >= 100:
            player_health = 100
        else:
            player_health += 45
        levels[curr_level][1] -= 1
        if levels[curr_level][1] == 0:
            boss = True
            e_list = enemy_prepare.get_random_enemy(player_x, player_y, 1)
            enemy_list.append(e_list)
            music_loaded = True
            music_index = 1

    if boss:
        if len(enemy_list) == 0:
            boss = False
            if player_health+60 >= 100:
                player_health = 100
            else:
                player_health += 60
            music_loaded = True
            music_index = 0

    if len(enemy_list) == enem_len and can_enemy_add:
        can_enemy_add = False

    for enem_list in enemy_list:
        angle_e = calculate_player_pos(enem_list[0], enem_list[1])
        enem_seg = PlayerSegment(angle_e[1], angle_e[2], Sprites.ships[enem_list[5]], angle1=angle_e[0], rotate=True, wid=enem_list[8], hie=enem_list[9])
        display_surface.blit(enem_seg.image, enem_seg.rect)
        #pygame.display.update(enem_seg.rect)
        move_enemy(enem_list)
        if boss:
            load_enemy_bullet(angle_e[1], angle_e[2], angle_e[0], enem_list[2], player_x, enem_list[0])
        collision_detection(enem_seg.rect)
        collision_detection_bullet(enem_seg.rect, enem_list)
        if enem_list[0] < -100:
            rem_list.append(enem_list)

    for rem in rem_list:
        enemy_list.remove(rem)


def draw_enemy_platform():
    pass


def collision_detection_bullet(en_rect, e_list):
    global bullet_list, score, explosions
    for bullet in bullet_list:
        bul_rect = pygame.Rect(bullet[0]-bul_wid/6, bullet[1]-bul_hie/6, bul_wid/6, bul_hie/6)
        if type(bul_rect) == pygame.Rect and bul_rect.colliderect(en_rect):
            e_list[6] -= 25
            bullet[0] = -2000
            pygame.draw.circle(display_surface, RED, (en_rect[0]+en_rect[2]//2, en_rect[1]+en_rect[3]//2), en_rect[2]//2, 1)

    if e_list[6] < 0:
        explosions.append([en_rect[0], en_rect[1], 0, 125, Sprites.blasts])
        play_sound(Sprites.explosion_sound)
        e_list[0] = -200
        e_list[2] = 0
        score += e_list[7]


def collision_detection_player():
    global enemy_bullets, player_x, player_health
    rem = []
    player_rect = pygame.Rect(player_x-player_w*0.75, player_y-player_h*0.75, player_w*0.75, player_h*0.75)
    for bull in enemy_bullets:
        bul_rect = pygame.Rect(bull[0]-bul_wid/4, bull[1]-bul_hie/4, bul_wid/4, bul_hie/4)
        if bul_rect.colliderect(player_rect):
            player_health -= 5
            bull[0] = -2000
            pygame.draw.circle(display_surface, RED, (int(player_x), int(player_y)), player_w//2, 1)
        if bull[0] < 0:
            rem.append(bull)
    for r in rem:
        enemy_bullets.remove(r)


def collision_detection(enemy_rect):
    global player_health, invincible, player_x
    player_rect = pygame.Rect(player_x-10, player_y-10, 10, 10)
    if enemy_rect.colliderect(player_rect):
        if not invincible:
            player_health -= 15
            pygame.time.set_timer(invincible_event, invincible_time)
            invincible = True


def draw_obstacles():
    if not platformer:
        return


def check_for_player_health():
    global player_x, player_health
    if player_health < 0:

        if not game_fin:
            explosions.append([player_x, player_y, 0, 125, Sprites.player_expl])
            play_sound(Sprites.explosion_sound2)
        player_x = -2000
        stop_game()
        game_over()


def draw_explosions():
    global explosions
    rem = []
    for explosion in explosions:

        exp = PlayerSegment(explosion[0], explosion[1], explosion[4][explosion[2]], wid=200, hie=200)
        if explosion[2] < len(explosion[4])-1:
            explosion[2] += 1
        explosion[3] -= 1
        display_surface.blit(exp.image, exp.rect)
        if explosion[3] < 0:
            rem.append(explosion)

    for re in rem:
        explosions.remove(re)


def stop_game():
    global left, right, up, down
    global game_fin
    left, right, up, down, game_fin = False, False, False, False, True


def move_enemy(e_list):
    x_speed = e_list[3]
    y_speed = e_list[2]*x_speed
    if e_list[2] > 1:
        y_speed = e_list[3]
        x_speed = y_speed / e_list[2]
    elif e_list[2] < -1:
        y_speed = -e_list[3]
        x_speed = y_speed / e_list[2]

    if e_list[4] < 0:
        e_list[0] -= x_speed
        e_list[1] -= y_speed
    else:
        e_list[0] += x_speed
        e_list[1] += y_speed

    if not 0 <= e_list[0] <= w:
        enemy_prepare.renew_pos(e_list,[player_x, player_y])
    if not 0 <= e_list[1] <= h:
        enemy_prepare.renew_pos(e_list,[player_x, player_y])


def calculate_player_pos(enem_x, enem_y):
    global slope_e, dx_e
    dx_e = player_x - enem_x
    dy = player_y - enem_y
    rad = math.atan2(dy, dx_e)
    angle_e = math.degrees(-rad)+90
    return [angle_e, enem_x, enem_y]


def draw_player_health():
    global player_health
    pygame.draw.rect(display_surface, WHITE, (w/2-50, h-40, player_max_health, 20), 5)
    pygame.draw.rect(display_surface, WHITE, (w/2-50, h-40, player_health, 20))
    #pygame.display.update(rect1)


def check_boss():
    if boss:
        write_text("BOSS", w-60, h-30)


def game_over():
    if game_fin:
        write_text("GAME OVER, WANT TO CONTINUE? Y or N", w/2-60, h/2, size=18)
        if pygame.key.get_pressed()[pygame.K_n]:
            pygame.quit()
            quit()
        elif pygame.key.get_pressed()[pygame.K_y]:
            reset()
        

def write_text(text, x, y, font_name='freesansbold.ttf', size=14, color=(255, 255, 255)):
    font = pygame.font.Font(font_name, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.topleft=(x, y)
    display_surface.blit(text, text_rect)
    #pygame.display.update(text_rect)


def reset():
    global player_x, player_y, player_health, can_enemy_add, can_enemy_come
    global enemy_list, invincible, game_fin, bullet_list
    global mouse_pressed, right, left, up, down, shift, fire, score, levels, curr_level
    mouse_pressed = False
    right, left, up, down, shift = False, False, False, False, False
    fire = True
    can_enemy_come = True
    can_enemy_add = False
    invincible = False
    game_fin = False
    enemy_list = []
    bullet_list = []
    player_x = w/2
    player_y = h/2
    player_health = 100
    score = 0
    levels = [[5, 4], [8, 5], [10, 7]]
    curr_level = 0


def play_music():
    if music_loaded:
        pygame.mixer.music.load(music[music_index])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)


def play_sound(sound):
    effect = pygame.mixer.Sound(sound)
    effect.play()
    if "click" in sound:
        effect.set_volume(0.2)
    else:
        effect.set_volume(1.0)
    pygame.time.set_timer(end_sound, end_sound_time)


def draw_score():
    write_text("SCORE: "+str(score), 20, h-20)


def update_bullet_sprite():
    global bullet_sprite
    bullet_sprite += 1
    if bullet_sprite >= len(Sprites.bullets):
        bullet_sprite = 0


def run_the_game():
    global music_loaded
    display_surface.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    event_handling()
    controls(keys)
    controls_released(keys)
    draw_background()
    drawing_enemy()
    play_music()
    if music_loaded:
        music_loaded = False
    movements()
    draw_sprites()
    prepare_to_fire()
    draw_bullet(bullet_list, Sprites.bullets[bullet_sprite], 30, 30, speed_x=100, speed_y=100)
    update_bullet_sprite()
    draw_bullet(enemy_bullets, speed_x=60, speed_y=60)
    draw_player_health()
    draw_score()
    draw_explosions()
    check_for_player_health()
    collision_detection_player()
    check_boss()
    if platformer:
        move_background()
    pygame.display.update()
    clock.tick(30)


while True:
    run_the_game()

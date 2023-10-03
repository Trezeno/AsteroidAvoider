import pygame
import random
import os

pygame.init()
pygame.font.init()
pygame.mixer.init() #TODO: Add sound effects

#Declaring constants
#Generic game settings
FPS = 60
SHIP_VEL = 3
MAX_SHIP_HEALTH = 5
BULLET_VEL = 5
AMMO_PACK_VEL = 3
HEALTH_PACK_VEL = 3
MAX_AMMO_PACKS = 1
WIN_WIDTH, WIN_HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Asteroid Avoider")
BLACK_COLOUR = (0, 0, 0)
WHITE_COLOUR = (255, 255, 255)
YELLOW_COLOUR = (255, 255, 0)
ORANGE_COLOUR = (255, 165, 0)
RED_COLOUR = (255, 0, 0)
MAX_BULLETS = 3
MAX_AMMO = 10
GAME_FONT = pygame.font.SysFont("Agency FB", 40)
END_GAME_FONT = pygame.font.SysFont("Agency FB", 70)
PAUSE_GAME_FONT = pygame.font.SysFont("Agency FB", 50)

#Other global variables
game_state = "menu"
game_score = 0
spaceship_health = 5
max_asteroids = 5
asteroids = []
asteroid_spawn_timer = 0
ammo_packs = []
spaceship_ammo = 10
spaceship_bullets = []
ammo_pack_score_threshold = 500
health_packs = []
health_pack_score_threshold = 1000

#Assets import
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 64, 64
ASTEROID_WIDTH, ASTEROID_HEIGHT = 96, 96
AMMO_PACK_WIDTH, AMMO_PACK_HEIGHT = 32, 32
HEALTH_PACK_WIDTH, HEALTH_PACK_HEIGHT = 32, 32
SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Spaceship.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIN_WIDTH, WIN_HEIGHT))

spaceship = pygame.Rect(WIN_WIDTH // 2 - SPACESHIP_WIDTH // 2, WIN_HEIGHT - 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

ASTEROID_1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Asteroid1.png")), (ASTEROID_WIDTH, ASTEROID_HEIGHT))
ASTEROID_2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Asteroid2.png")), (ASTEROID_WIDTH, ASTEROID_HEIGHT))
ASTEROID_3 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Asteroid3.png")), (ASTEROID_WIDTH, ASTEROID_HEIGHT))
ASTEROID_4 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Asteroid4.png")), (ASTEROID_WIDTH, ASTEROID_HEIGHT))
ASTEROID_LIST = [ASTEROID_1, ASTEROID_2, ASTEROID_3, ASTEROID_4]

AMMO_PACK = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Ammo_Pack.png")), (AMMO_PACK_WIDTH, AMMO_PACK_HEIGHT))
HEALTH_PACK = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Health_Pack.png")), (HEALTH_PACK_WIDTH, HEALTH_PACK_HEIGHT))
MISSILE = pygame.image.load(os.path.join("Assets", "Missile.png"))

#Functions for game
#This functions handles all spaceship movement
def handle_spaceship_movement(keys_pressed, spaceship):
  if keys_pressed[pygame.K_w] and spaceship.y - SHIP_VEL > 0: #Move ship up
    spaceship.y -= SHIP_VEL
  if keys_pressed[pygame.K_s] and spaceship.y + SHIP_VEL + SPACESHIP_HEIGHT < WIN_HEIGHT: #Move ship down
    spaceship.y += SHIP_VEL
  if keys_pressed[pygame.K_a] and spaceship.x - SHIP_VEL > 0: #Move ship left
    spaceship.x -= SHIP_VEL
  if keys_pressed[pygame.K_d] and spaceship.x + SHIP_VEL + SPACESHIP_WIDTH < WIN_WIDTH: #Move ship right
    spaceship.x += SHIP_VEL
  
#This function handles bullet collision with asteroids or screen edge
#This function also increases game score by 50 for successfully shooting and destroying an asteroid
def handle_bullets(bullets, asteroids):
  global game_score
  for bullet in bullets:
    bullet.y -= BULLET_VEL
    if bullet.y < -15:
      bullets.remove(bullet)
    for asteroid in asteroids:
      if bullet.colliderect(asteroid):
        bullets.remove(bullet)
        asteroids.remove(asteroid)
        game_score += 50

#This function checks if it is able to spawn a new asteroid, and does so if the check passes
#This function also varies the speed at which asteroids spawn as your game score increases
def check_and_spawn_new_asteroid():
  global asteroid_spawn_timer
  global game_score
  if len(asteroids) < max_asteroids and asteroid_spawn_timer == 60:
    random_x_coord = random.randint(0, WIN_WIDTH - ASTEROID_WIDTH)
    asteroid = pygame.Rect(random_x_coord, 0, ASTEROID_WIDTH, ASTEROID_HEIGHT)
    asteroids.append(asteroid)
  if asteroid_spawn_timer > 60:
    asteroid_spawn_timer = 0
  if game_score < 1000:
    asteroid_spawn_timer += 1
  elif game_score < 2000:
    asteroid_spawn_timer += 2
  else: 
    asteroid_spawn_timer += 3

#This function checks to see if an ammo pack should be spawned, and does so if the check passes
def check_and_spawn_ammo():
  global game_score
  global ammo_pack_score_threshold
  if game_score > ammo_pack_score_threshold and len(ammo_packs) < MAX_AMMO_PACKS:
    random_x_coord = random.randint(0, WIN_WIDTH - AMMO_PACK_WIDTH)
    ammo_pack = pygame.Rect(random_x_coord, 0, AMMO_PACK_WIDTH, AMMO_PACK_HEIGHT)
    ammo_packs.append(ammo_pack)
    ammo_pack_score_threshold += 500

#This function handles the falling movement of the ammo pack
#It also handles the collision with the spaceship or the screen edge
def handle_ammo_movement(spaceship, ammo_packs):
  global spaceship_ammo
  for ammo in ammo_packs:
    ammo.y += AMMO_PACK_VEL
    if ammo.colliderect(spaceship):
      ammo_packs.remove(ammo)
      spaceship_ammo = MAX_AMMO
    elif ammo.y > WIN_HEIGHT:
      ammo_packs.remove(ammo)

#This function checks to see if it should spawn a health pack, and does so if the check passes
def check_and_spawn_health():
  global game_score
  global health_pack_score_threshold
  if game_score > health_pack_score_threshold:
    random_x_coord = random.randint(0, WIN_WIDTH - HEALTH_PACK_WIDTH)
    health_pack = pygame.Rect(random_x_coord, 0, HEALTH_PACK_WIDTH, HEALTH_PACK_HEIGHT)
    health_packs.append(health_pack)
    health_pack_score_threshold += 1000

#This function handles the falling movement of the health pack
#This function also handles the collision with the spaceship or screen edge
def handle_health_movement(spaceship, health_packs):
  global spaceship_health
  for health in health_packs:
    health.y += HEALTH_PACK_VEL
    if health.colliderect(spaceship):
      health_packs.remove(health)
      if spaceship_health < MAX_SHIP_HEALTH:
        spaceship_health += 1
    elif health.y > WIN_HEIGHT:
      health_packs.remove(health)

#This function handles the falling movement of the asteroids
#It also alters the falling speed of the asteroid depending on current game score as well as maximum shown on screen
#This function also handles the collision with the spaceship or screen edge
def handle_asteroid_movement(asteroids, ship):
  global spaceship_health
  global game_score
  global max_asteroids
  if game_score < 500:
    asteroid_vel = 2
  elif game_score < 1000:
    asteroid_vel = 3
  elif game_score < 1500:
    asteroid_vel = 4
  elif game_score < 2000:
    asteroid_vel = 5
  elif game_score < 2500:
    max_asteroids = 7
    asteroid_vel = 7
  elif game_score < 3000:
    asteroid_vel = 8.5
  else:
    max_asteroids = 10
    asteroid_vel = 10
  for asteroid in asteroids:
    asteroid.y += asteroid_vel
    if asteroid.colliderect(ship):
      asteroids.remove(asteroid)
      spaceship_health -= 1
    elif asteroid.y > WIN_HEIGHT:
      asteroids.remove(asteroid)
      game_score += 10

#This function allows you to pause the game during play
def pause_game():
  global game_state
  pause_game_text = PAUSE_GAME_FONT.render("Game Paused!", 1, WHITE_COLOUR)
  pause_game_text_2 = PAUSE_GAME_FONT.render("Press 'Space' to continue", 1, WHITE_COLOUR)
  WIN.blit(pause_game_text, (WIN_WIDTH/2 - pause_game_text.get_width()/2, WIN_HEIGHT/2 - pause_game_text.get_height() - 50))
  WIN.blit(pause_game_text_2, (WIN_WIDTH/2 - pause_game_text_2.get_width()/2, WIN_HEIGHT/2 - pause_game_text_2.get_height()/2))
  pygame.display.update()
  while game_state == "paused":
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        game_state = "end"
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
          game_state = "running"

#This function handles the game over screen and displays your score
def end_screen_text(score):
  end_game_text = END_GAME_FONT.render("Game over! Thank you for playing!", 1, WHITE_COLOUR)
  end_game_text_2 = END_GAME_FONT.render(f"Final Score: {score}", 1, WHITE_COLOUR)
  WIN.blit(end_game_text, (WIN_WIDTH/2 - end_game_text.get_width()/2, WIN_HEIGHT/2 - end_game_text.get_height() - 50))
  WIN.blit(end_game_text_2, (WIN_WIDTH/2 - end_game_text_2.get_width()/2, WIN_HEIGHT/2 - end_game_text_2.get_height()/2))
  pygame.display.update()

#This function is the introduction menu to the game before the main game loop starts
def main_menu():
  global game_state
  menu_text_game_name = END_GAME_FONT.render("Asteroid Avoider", 1, WHITE_COLOUR)
  menu_text_game_info = GAME_FONT.render("Welcome to AA. The game is simple and controls are as follows:", 1, WHITE_COLOUR)
  menu_text_game_info_2 = GAME_FONT.render("Use 'WASD' to move your ship to avoid the asteroids.", 1, WHITE_COLOUR)
  menu_text_game_info_3 = GAME_FONT.render("Press 'SPACE' to shoot missiles from your ship to destroy asteroids.", 1, WHITE_COLOUR)
  menu_text_game_info_4 = GAME_FONT.render("Press 'ESC' or 'P' to pause the game at any time.", 1, WHITE_COLOUR)
  menu_text_game_info_5 = GAME_FONT.render("Shooting asteroids rewards 50 points, avoiding them awards 10 points.", 1, WHITE_COLOUR)
  menu_text_game_info_6 = GAME_FONT.render("Make sure to fly into any ammo or health packs you need!", 1, WHITE_COLOUR)
  menu_text_game_info_7 = GAME_FONT.render("That's all! Best of luck!", 1, WHITE_COLOUR)
  menu_text_game_info_8 = PAUSE_GAME_FONT.render("Press 'SPACE' to start the game.", 1, WHITE_COLOUR)
  WIN.blit(SPACE_BACKGROUND, (0, 0))
  WIN.blit(menu_text_game_name, (WIN_WIDTH/2 - menu_text_game_name.get_width()/2, 50))
  WIN.blit(menu_text_game_info, (WIN_WIDTH/2 - menu_text_game_info.get_width()/2, 175))
  WIN.blit(menu_text_game_info_2, (WIN_WIDTH/2 - menu_text_game_info_2.get_width()/2, 225))
  WIN.blit(menu_text_game_info_3, (WIN_WIDTH/2 - menu_text_game_info_3.get_width()/2, 275))
  WIN.blit(menu_text_game_info_4, (WIN_WIDTH/2 - menu_text_game_info_4.get_width()/2, 325))
  WIN.blit(menu_text_game_info_5, (WIN_WIDTH/2 - menu_text_game_info_5.get_width()/2, 375))
  WIN.blit(menu_text_game_info_6, (WIN_WIDTH/2 - menu_text_game_info_6.get_width()/2, 425))
  WIN.blit(menu_text_game_info_7, (WIN_WIDTH/2 - menu_text_game_info_7.get_width()/2, 475))
  WIN.blit(menu_text_game_info_8, (WIN_WIDTH/2 - menu_text_game_info_8.get_width()/2, 575))
  pygame.display.update()
  while game_state == "menu":
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        game_state = "end"
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          game_state = "running"
          main(spaceship)

#This function draws everything onto the game window for it to be visible and the game able to be played
def draw_game_window(ship, bullets, score, spaceship_ammo, spaceship_health, asteroids, ammo_packs, health_packs):
  global asteroid_spawn_timer

  WIN.blit(SPACE_BACKGROUND, (0, 0))
  WIN.blit(SPACESHIP, (ship.x, ship.y))

  score_text = GAME_FONT.render(f"Score: {score}", 1, WHITE_COLOUR)
  WIN.blit(score_text, (10, WIN_HEIGHT - score_text.get_height() -10))

  if spaceship_health > 3:
    health_text = GAME_FONT.render(f"Health: {spaceship_health}", 1, WHITE_COLOUR)
  elif spaceship_health == 3:
    health_text = GAME_FONT.render(f"Health: {spaceship_health}", 1, YELLOW_COLOUR)
  elif spaceship_health == 2:
    health_text = GAME_FONT.render(f"Health: {spaceship_health}", 1, ORANGE_COLOUR)
  else:
    health_text = GAME_FONT.render(f"Health: {spaceship_health}", 1, RED_COLOUR)

  WIN.blit(health_text, (WIN_WIDTH - health_text.get_width()-10, WIN_HEIGHT - health_text.get_height() - 10))

  if spaceship_ammo > 0:
    ammo_text = GAME_FONT.render(f"Ammo: {spaceship_ammo}", 1, WHITE_COLOUR)
  else:
    ammo_text = GAME_FONT.render(f"Ammo: {spaceship_ammo}", 1, RED_COLOUR)
  WIN.blit(ammo_text, (WIN_WIDTH//2 - ammo_text.get_width()//2, WIN_HEIGHT - ammo_text.get_height() - 10))
  
  for bullet in bullets:
    WIN.blit(MISSILE, (bullet.x, bullet.y))
    
  for ammo in ammo_packs:
    WIN.blit(AMMO_PACK, (ammo.x, ammo.y))

  for health in health_packs:
    WIN.blit(HEALTH_PACK, (health.x, health.y))

  for asteroid in asteroids:
    WIN.blit(ASTEROID_LIST[0], (asteroid.x, asteroid.y))

  pygame.display.update()

#Main game loop using all of the above functions
def main(spaceship):
  global game_score
  global spaceship_health
  global spaceship_ammo
  global spaceship_bullets
  global game_state

  if game_state == "menu":
    main_menu()

  clock = pygame.time.Clock()
  bullet_side = "left"

  while game_state == "running":
    clock.tick(FPS)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        game_state = "end"
        break

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and len(spaceship_bullets) < MAX_BULLETS and spaceship_ammo > 0:
          if bullet_side == "left":
            bullet = pygame.Rect((spaceship.x + 5), (spaceship.y + spaceship.height//2-18), 5, 10)
            bullet_side = "right"
          else:
            bullet = pygame.Rect((spaceship.x + spaceship.width-20), (spaceship.y + spaceship.height//2-18), 5, 10)
            bullet_side = "left"
          spaceship_bullets.append(bullet)
          spaceship_ammo -= 1

        if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
          game_state = "paused"

    if spaceship_health == 0:
      game_state = "end"
      end_screen_text(game_score)
      pygame.time.delay(5000)
      break

    keys_pressed = pygame.key.get_pressed()
    check_and_spawn_new_asteroid()
    check_and_spawn_ammo()
    check_and_spawn_health()
    handle_spaceship_movement(keys_pressed, spaceship)
    handle_bullets(spaceship_bullets, asteroids)
    handle_asteroid_movement(asteroids, spaceship)
    handle_ammo_movement(spaceship, ammo_packs)
    handle_health_movement(spaceship, health_packs)
    draw_game_window(spaceship, spaceship_bullets, game_score, spaceship_ammo, spaceship_health, asteroids, ammo_packs, health_packs)

  if game_state == "paused":
    pause_game()
  if game_state == "running":
    main(spaceship)
  else:
    game_state = "end"

  if game_state == "end":
    pygame.quit()

if __name__ == "__main__":
  main(spaceship)

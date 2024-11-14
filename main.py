import pygame
import json
import easygui
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score import Score
from speed_power_up import SpeedPowerUp

def save_high_score(score, player):
    high_score_data = {
        "high_score": {
            "score": score,
            "player": player
        }
    }
    with open('high_score.json', "w") as file:
        json.dump(high_score_data, file, indent=4)

def load_high_score():
    try:
        with open('high_score.json', "r") as file:
            high_score_data = json.load(file)
            high_score = high_score_data["high_score"]["score"]
            high_scorer = high_score_data["high_score"]["player"]
            return high_score, high_scorer
    except (FileNotFoundError, KeyError):
        return None, None

state = "active"
score_var = 0

def main():
    global player
    global state
    global score_var

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    SpeedPowerUp.containers = (powerups, drawable, updatable)
    Shot.containers = (updatable, drawable, shots)
    AsteroidField.containers = (updatable)
    Score.containers = (updatable, drawable)
    
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "#00CCCC")
    
    score = Score('freesansbold.ttf', 32)

    dt = 0

    HIGH_SCORE, HIGH_SCORER = load_high_score()

    def gameOverText():
        game_over_str = "GAME OVER!"
        gameover = Score('freesansbold.ttf', 64)
        game_over_text = gameover.render(game_over_str, True, "white", "black")
        game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(game_over_text, game_over_text_rect)

    def reset_game():
        global score_var
        global state
        
        score_var = 0
        screen.fill("black")
        for asteroid in asteroids:
            asteroid.kill()
        state = "active"
        AsteroidField.powerup_active = False
        AsteroidField.powerup_time = None
        player.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    def soft_reset():
        screen.fill("black")
        for asteroid in asteroids:
            asteroid.kill()
        
        player.is_speed_boosted = False
        player.speed_boost_time = pygame.time.get_ticks()
        player.shot_multiplier = 1
        player.colour = player.og_colour
        AsteroidField.powerup_active = False
        AsteroidField.powerup_time = None
        
        player.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        if state == "active":
            for elem in updatable:
                elem.update(dt)

            #collision checking
            #Power Ups
            for powerup in powerups:
                if powerup.is_colliding(player):
                    powerup.kill()
                    player.is_speed_boosted = True
                    player.speed_boost_time = pygame.time.get_ticks()
                    player.shot_multiplier = 0.25
                    player.colour = "yellow"
                    AsteroidField.powerup_active = False
            
            #Asteroids
            for asteroid in asteroids:
                if asteroid.is_colliding(player) and (player.lives == 1):
                    player.lives = 0
                    print(f"Your score was: {score_var}")
                    
                    if (HIGH_SCORE == None) or (score_var > HIGH_SCORE):
                        player_name = easygui.enterbox("High Score! Please enter your name:")
                        save_high_score(score_var, player_name)
                        print(f"High Score: {score_var} by {player_name}")
                    else:
                        print(f"High Score: {HIGH_SCORE} by {HIGH_SCORER}")
                        
                    state = "gameover"
                elif asteroid.is_colliding(player) and (player.lives > 0):
                    player.lives -= 1
                    soft_reset()
                
                for shot in shots:
                    if asteroid.is_colliding(shot):
                        shot.kill()
                        asteroid.split()
                        score_var += 1

            screen.fill("black")
            
            for elem in drawable:
                elem.draw(screen)
            
            #(high) score text
            score_str = f"Score: {score_var}"
            score_text = score.render(score_str, True, "white", None)
            high_score_str = f"High Score: {HIGH_SCORE}"
            high_score_text = score.render(high_score_str, True, "white", None)
            score_width, score_height = score.size(score_str)
            high_score_width, high_score_height = score.size(high_score_str)
            screen.blit(score_text, (SCREEN_WIDTH - score_width - 5, SCREEN_HEIGHT - score_height - 5))
            screen.blit(high_score_text,(SCREEN_WIDTH - high_score_width - 5, SCREEN_HEIGHT - score_height * 2  - 5)) 

            #Lives text
            lives_str = f"Lives: {player.lives}"
            lives_text = score.render(lives_str, True, "white", None)
            lives_width, lives_height = score.size(lives_str)
            screen.blit(lives_text, (5, SCREEN_HEIGHT - lives_height -5))
            

        #handle gameover screen
        elif state == "gameover":
            gameOverText()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or keys[pygame.K_RETURN]:
                player.reset_lives()
                reset_game()

        dt = (clock.tick(60)/1000)
        pygame.display.flip()

        


if __name__ == "__main__":
    main()
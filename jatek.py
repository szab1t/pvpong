import pygame
import random
#inicialiazalas
pygame.init()
pygame.display.set_caption("Szabog")
#ablak letrehozasa
screen_width = 800
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
base_fire_rate = 120
#hatter szine
background_color = (255, 218, 185)

fps = 144
#betutipus
font = pygame.font.Font(None,40)

szabi_wins = pygame.image.load("szabi_wins.png")
bogi_wins = pygame.image.load("bogi_wins.png")

bogi_wins = pygame.transform.smoothscale(bogi_wins,(screen_width,screen_height))
szabi_wins = pygame.transform.smoothscale(szabi_wins,(screen_width,screen_height))
#JATEKOS OSZTALY
class Player:
    def __init__(self,x,y,width,height,color):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color
        self.speed = 2
        self.bullets = []
        self.bullet_speed = 4
        self.fire_rate = base_fire_rate
        self.damage = 1
        self.hp = 3
        self.bullet_count = 1
    #billentyuzet kezeles PLAYER 1
    def handlekeys_p1(self):
        if self.fire_rate > 0:
            self.fire_rate -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y >0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < screen_height - self.rect.height:
            self.rect.y += self.speed
        #loves
        if keys[pygame.K_d] and self.fire_rate == 0:
                if self.bullet_count == 1:
                    bullet_rect = pygame.Rect(self.rect.centerx,self.rect.centery,20,20)
                    self.bullets.append(bullet_rect)
                    self.fire_rate = base_fire_rate
                elif self.bullet_count == 3:
                    for i in range(1,4):
                        pass
    #PLAYER 2
    def handlekeys_p2(self):
        if self.fire_rate > 0:
            self.fire_rate -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y >0:
            self.rect.y -= self.speed
        elif keys[pygame.K_DOWN] and self.rect.y < screen_height - self.rect.height:
            self.rect.y += self.speed
        elif keys[pygame.K_LEFT] and self.fire_rate == 0 and self.bullet_count == 1:
            bullet_rect = pygame.Rect(self.rect.centerx,self.rect.centery,20,20)
            self.bullets.append(bullet_rect)
            self.fire_rate = base_fire_rate
        
    #jatekos kirajzolasa
    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)

    #golyo kirajzoltatasa
    def draw_bullets_p1(self,surface,target):
        for bullet in self.bullets:
            bullet.x += self.bullet_speed
            pygame.draw.rect(surface,(255,0,0),bullet) 
            if bullet.x > screen_width:
                self.bullets.remove(bullet)
                continue
            if bullet.colliderect(target):
                target.hp -= 1
                self.bullets.remove(bullet)

    def draw_bullets_p2(self,surface, target):
        for bullet in self.bullets:
            bullet.x -= self.bullet_speed
            pygame.draw.rect(surface,(0,255,255),bullet) 
            if bullet.x < 0:
                self.bullets.remove(bullet)
                continue
            #eltalalas
            if bullet.colliderect(target):
                target.hp -= 1
                self.bullets.remove(bullet)

#BONUSZ OSZTALY
class Bonus:
    def __init__(self,effect,color,x,y,width,height):
        self.rect = pygame.Rect(x,y,width,height)
        self.effect = effect
        self.color = color
        
    def bondraw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)
            
    
    def apply(self,player):
        if self.effect == "heal":
            player.hp += 1
        elif self.effect == "speed":
            player.speed += 1
        elif self.effect == "multibullet":
            player.bullet_count = 3
        elif self.effect == "bulletspeed":
            player.bullet_speed += 1
        
#GOMB OSZTALY
class Button:
    def __init__(self):
        pass

#FO PROGRAM

def main():
    bonuszok = [Bonus("heal",(0,0,0),int(screen_width/2 - 30/2),0,30,30),
                Bonus("speed",(255,255,255),int(screen_width/2 - 30/2),0,30,30),
                Bonus("bulletspeed",(255,0,0),int(screen_width/2 - 30/2),0,30,30)]
    activebonus = None
    bonus_cooldown = fps*2
    #jatekos letrehozasa
    player = Player(25,50,25,100,(0,0,255))
    player2 = Player(screen_width-50,50,25,100,(255,0,0))
    clock = pygame.time.Clock()
    #display beallitasa, kileptetes
    running = True
    timing = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #hatter,fps beallitasa
        screen.fill(background_color)
        clock.tick(fps)
        bonus_cooldown -= 1
        #Playerek kirajzolasa
        player.draw(screen)
        player.handlekeys_p1()
        player2.draw(screen)
        player2.handlekeys_p2()
        player.draw_bullets_p1(screen,player2)
        player2.draw_bullets_p2(screen,player)

        #bonuszok
        if bonus_cooldown <= 0 and not activebonus:
            activebonus = random.choice(bonuszok)
            bonus_cooldown = fps*2
        if activebonus:
            activebonus.bondraw(screen)
            activebonus.rect.y += 1
            if activebonus.rect.y >= screen_height:
                activebonus.rect.y = 0
                activebonus = None
                bonus_cooldown = fps*2
        bonus_cooldown -= 1
        for bullet in player.bullets:
            if activebonus and bullet.colliderect(activebonus):
                activebonus.apply(player)
                activebonus.rect.y = 0
                activebonus = None
                bonus_cooldown = fps*2

        for bullet in player2.bullets:
            if activebonus and bullet.colliderect(activebonus):
                activebonus.apply(player2)
                activebonus.rect.y = 0
                activebonus = None
                bonus_cooldown = fps*2
        #player hp kiiratasa
        player1_hp = font.render(f"Szabi hp-ja: {player.hp}",True,(0,0,255),None)
        player2_hp = font.render(f"Bogi hp-ja: {player2.hp}",True,(0,0,255),None)
        screen.blit(player1_hp,(25,screen_height - 50))
        screen.blit(player2_hp,(screen_width-225,screen_height - 50))
        if player.hp == 0:
            screen.blit(bogi_wins,(0,0))
        if player2.hp == 0:
            screen.blit(szabi_wins,(0,0))
        pygame.display.flip()
        

    #kilepes
    pygame.quit()


if __name__ == "__main__":
    main()
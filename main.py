import random
import math
import time
import arcade

#-------------------------------------Enemy-------------------------------------
class Enemy(arcade.Sprite):
    def __init__(self , w , h ):
        super().__init__(':resources:images/space_shooter/playerShip2_orange.png')
        self.initial_speed = 2 #sorat avalie
        self.speed_increase = 0.1  # مقدار افزایش سرعت در هر بار به‌روزرسانی
        self.center_x = random.randint(0 , w)
        self.center_y = h
        self.angle = 180 #ro be paeen
        self.w = 45
        self.h = 45
        self.exploded = False
        self.explosion_image = arcade.load_texture('e:\Education\corses\python\code\Silver Spacecraft\pic\explosion.jpg')
    def update_speed(self):
        self.initial_speed = self.initial_speed + self.speed_increase
    def move(self):
        self.center_y -= self.initial_speed
    def hit_sound(self):
        arcade.play_sound(arcade.sound.Sound(":resources:sounds/explosion1.wav"))

#-------------------------------------Bullet-------------------------------------
class Bullet(arcade.Sprite):
    def __init__(self , host):
        super().__init__(':resources:images/space_shooter/laserRed01.png')
        self.speed = 6
        self.angle = host.angle #zavie
        self.center_x = host.center_x #mokhtasat
        self.center_y = host.center_y #mokhtasat
    def move(self):
        angle_rad = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)   
    def laser_sound(self):
        arcade.play_sound(arcade.sound.Sound(":resources:sounds/lose4.wav"), 0.3)

#-------------------------------------SpaceCraft-------------------------------------
class SpaceCraft(arcade.Sprite):
    def __init__(self , w , h):
        super().__init__(':resources:images/space_shooter/playerShip1_green.png')
        self.w = 40
        self.h = 40
        self.center_x = w // 2
        self.center_y = 48
        self.angle = 0 #zavie
        self.change_angle = 0  #mizan jabejaei zavie
        self.bullet_list = [] #list tirha
        self.speed = 5
        self.score = 0
        self.health = 3
    def rotate(self): #taqir zavie
        self.angle += self.change_angle * 4
    def fire(self):
       self.bullet_list.append(Bullet(self)) #tir jadid

#-------------------------------------Game-------------------------------------
class Game(arcade.Window):
    def __init__(self):
        self.w = 800
        self.h = 600
        super().__init__(self.w , self.h , 'Silver SpaceCraft')
        arcade.set_background_color(arcade.color.BLACK)
        self.background_image = arcade.load_texture(':resources:images/backgrounds/stars.png')
        self.me = SpaceCraft(self.w , self.h)
        self.enemy_list = []
        self.enemy = Enemy(self.w, self.h)
        self.start_time = time.time() #lahze shoro
        self.next_enemy_time = random.randint(2, 5)
        self.game_start_time = time.time()
        self.heart_image = arcade.load_texture('e:\Education\corses\python\code\Silver Spacecraft\pic\heart.jpg')
        self.heart_w = 30
        self.heart_h = 30
        self.heart_padding = 10
        self.hearts_start_x = self.heart_w -10
        self.hearts_start_y =self.heart_h - 10
        self.remaining_hearts = 3
    def on_draw(self):
        arcade.start_render()
        if self.me.health <= 0:
            arcade.draw_text("Game Over !!! ", self.w//2-200, self.h//2, arcade.color.RED_VIOLET, 20, width=400, align="center")
        else:
            arcade.draw_lrwh_rectangle_textured(0 , 0 , self.w , self.h , self.background_image)
            self.me.draw()
            for i in range(len(self.me.bullet_list)):
                self.me.bullet_list[i].draw() #rasm tir ha
            for i in range(len(self.enemy_list)):
                self.enemy_list[i].draw()
            if self.enemy.exploded:
                arcade.draw_texture_rectangle(self.enemy.center_x, self.enemy.center_y, self.enemy.w, self.enemy.h, self.enemy.explosion_image)
            for i in range(self.me.health):
                arcade.draw_text("Score: " + str(self.me.score), self.w-130, 10, arcade.color.LIGHT_PINK, 20, width=200)
            for i in range(self.remaining_hearts):
                x = self.hearts_start_x + (self.heart_w + self.heart_padding) * i
                y = self.hearts_start_y
                arcade.draw_texture_rectangle(x, y, self.heart_w, self.heart_h, self.heart_image)
            
    def on_key_press(self , key , modifiers):
        if key == arcade.key.RIGHT :
            self.me.change_angle = -1
        elif key == arcade.key.LEFT :
            self.me.change_angle = 1
        elif key == arcade.key.SPACE :
            self.me.fire()
            self.me.bullet_list[-1].laser_sound()
    def on_key_release(self, key, modifiers): 
        self.me.change_angle = 0
    def on_update(self , delta_time): # hame etefaqat bazi
        self.end_time = time.time()
        if self.end_time - self.start_time > self.next_enemy_time:
            self.next_enemy_time = random.randint(4, 6)
            self.enemy_list.append(Enemy(self.w , self.h ))
            self.enemy.update_speed()
            self.start_time = time.time()
        self.me.rotate()
        for i in range(len(self.me.bullet_list)):
            self.me.bullet_list[i].move()
        for i in range(len(self.enemy_list)):             
            self.enemy_list[i].move()
        for enemy in self.enemy_list:
            for bullet in self.me.bullet_list:
                if arcade.check_for_collision(bullet , enemy): #barkhord tir va doshmn
                    enemy.hit_sound()
                    self.me.bullet_list.remove(bullet)
                    enemy.exploded = True
                    self.enemy_list.remove(enemy)
                    self.me.score += 1
        for enemy in self.enemy_list:
            if enemy.center_y < 0:
                self.me.health -= 1
                self.remaining_hearts -= 1
                self.enemy_list.remove(enemy)
                if self.me.health <= 0:
                    self.remaining_hearts = 0
        for bullet in self.me.bullet_list:
            if bullet.center_y > self.height or bullet.center_x < 0 or bullet.center_x > self.width:
                self.me.bullet_list.remove(bullet)
        


game = Game()
arcade.run()
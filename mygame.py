import pyxel
import math

class Player:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.max_hp = 10
        self.hp = self.max_hp
        self.speed = 3
        self.atk = 1
        self.exp = 0
        self.level = 0

        self.damage_count = 0

    def move(self, app):
        if pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed * pyxel.cos(45)
            self.y -= self.speed * pyxel.sin(45)
        elif pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed * pyxel.cos(45)
            self.y -= self.speed * pyxel.sin(45)
        elif pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed * pyxel.cos(45)
            self.y += self.speed * pyxel.sin(45)
        elif pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed * pyxel.cos(45)
            self.y += self.speed * pyxel.sin(45)
        elif pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed

        if self.x < 0:
            self.x = 0
        if self.x > 800:
            self.x = 800
        if self.y < 0:
            self.y = 0
        if self.y > 800:
            self.y = 800

        if self.damage_count >= 0:
            self.damage_count -= 1
            self.speed = 4
        else: 
            self.speed = 3
            for enemy in app.enemies:
                if (enemy.x-26<self.x<enemy.x+26 and enemy.y-13<self.y<enemy.y+13) or (enemy.x-13<self.x<enemy.x+13 and enemy.y-26<self.y<enemy.y+26) or ((enemy.x-13-self.x)**2+(enemy.y-13-self.y)**2 < 13**2) or ((enemy.x+13-self.x)**2+(enemy.y-13-self.y)**2 < 13**2) or ((enemy.x-13-self.x)**2+(enemy.y+13-self.y)**2 < 13**2) or ((enemy.x+13-self.x)**2+(enemy.y+13-self.y)**2 < 13**2):
                    self.hp -= 1
                    self.damage_count = 60
                    if self.hp <= 0:
                        app.gameover_flag = True

        for exporb in app.exporbs:
            if math.sqrt((exporb.x - self.x)**2 + (exporb.y - self.y)**2) <= 13:
                self.exp += 1.5
                app.exporbs.remove(exporb)
                if self.exp >= 10:
                    self.exp -= 10
                    self.level += 1
                    self.atk = 1 + (self.level*0.5)

    def shot(self, app):
        if (pyxel.frame_count-app.start_time) % 30 == 0 and len(app.enemies) >= 1:
        # 最寄りの敵を探す
            nearest_distance = 1600
            for enemy in app.enemies:
                xdis = self.x-enemy.x
                ydis = self.y-enemy.y
                distance= math.sqrt(xdis**2 + ydis**2)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_enemy = enemy
                    
            # 撃つ
            app.balets.append(Balet(self, nearest_enemy))

    def draw(self):
        if self.damage_count <= 0 or pyxel.frame_count % 2 == 0:
            pyxel.circ(self.x, self.y, 15, 0)
            pyxel.circ(self.x, self.y, 13, 9)
        pyxel.rect(self.x-25, self.y-25, 50, 5, 14)
        pyxel.rect(self.x-25, self.y-25, 50*self.hp/self.max_hp, 5, 11)
        pyxel.rect(self.x-25, self.y-20, 50*self.exp/10, 3, 10)

class Enemy:
    def __init__(self):
        self.max_hp = 3
        self.hp = self.max_hp

        pos_seed = pyxel.rndi(0, 3200)
        if 0 <= pos_seed < 800:
            self.x = pos_seed
            self.y = 0
        elif 800 <= pos_seed < 1600:
            self.x = 0
            self.y = pos_seed - 800
        elif 1600 <= pos_seed < 2400:
            self.x = pos_seed - 1600 
            self.y = 800
        else:
            self.x = 800
            self.y = pos_seed - 2400

    def move(self, app):
        degree = pyxel.atan2(app.player.y - self.y, app.player.x - self.x)
        self.x += 3 * pyxel.cos(degree)
        self.y += 3 * pyxel.sin(degree)

        for balet in app.balets:
            if self.x-13 < balet.x < self.x+13 and self.y-13 < balet.y < self.y+13:
                app.balets.remove(balet)
                self.hp -= 1 * app.player.atk
                if self.hp <= 0:
                    app.enemies.remove(self)
                    app.exporbs.append(ExpOrb(self.x, self.y))
                    app.score += 1
                    

    def draw(self):
        pyxel.rect(self.x-15, self.y-15, 30, 30, 0)
        pyxel.rect(self.x-13, self.y-13, 26, 26, 2)
        pyxel.rect(self.x-20, self.y-25, 40, 5, 14)
        pyxel.rect(self.x-20, self.y-25, 40*self.hp/self.max_hp, 5, 11)

class Balet:
    def __init__(self, player, enemy):
        self.x = player.x
        self.y = player.y
        degree = pyxel.atan2(enemy.y - self.y, enemy.x - self.x)
        self.vx = pyxel.cos(degree)
        self.vy = pyxel.sin(degree)

    def move(self, app):
        self.x += 10 * self.vx
        self.y += 10 * self.vy
        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 800:
            app.balets.remove(self)

    def draw(self):
        pyxel.line(self.x + 3 * self.vx, self.y + 3 * self.vy, self.x - 3 * self.vx, self.y - 3 * self.vy, 1)
        pyxel.line(self.x + 2 * self.vx, self.y + 3 * self.vy, self.x - 4 * self.vx, self.y - 3 * self.vy, 1)
        pyxel.line(self.x + 4 * self.vx, self.y + 3 * self.vy, self.x - 2 * self.vx, self.y - 3 * self.vy, 1)
        pyxel.line(self.x + 3 * self.vx, self.y + 2 * self.vy, self.x - 3 * self.vx, self.y - 4 * self.vy, 1)
        pyxel.line(self.x + 3 * self.vx, self.y + 4 * self.vy, self.x - 3 * self.vx, self.y - 2 * self.vy, 1)

class ExpOrb:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        for i in range(7):
            pyxel.line(self.x-3+i/2, self.y+i, self.x+i/2, self.y-6+i, 10)


class App:
    def __init__(self):
        pyxel.init(800,800)
        self.start()
        self.score = 0
        pyxel.run(self.update, self.draw)

    def start(self):
        self.start_time = pyxel.frame_count

        self.gameover_flag = False
        self.player = Player()
        self.enemies = []
        self.balets = []
        self.exporbs = []

    def update(self):
        if self.gameover_flag:
            if pyxel.btnp(pyxel.KEY_R):
                self.start()
            else:    
                return

        self.player.move(self)
        self.player.shot(self)

        if (pyxel.frame_count-self.start_time) % 150 == 0:
            for i in range (3):
                self.enemies.append(Enemy())

        for enemy in self.enemies:
            enemy.move(self)

        for balet in self.balets:
            balet.move(self)

            
    def draw(self):
        if self.gameover_flag:
            pyxel.cls(7)
            pyxel.text(380, 400, "GAME OVER!!!", 0)
        else:
            pyxel.cls(7)
            for balet in self.balets:
                balet.draw()
            for exporb in self.exporbs:
                exporb.draw()    
            for enemy in self.enemies:
                enemy.draw()
            self.player.draw()
            pyxel.text(5, 5, "SCORE : " + str(self.score), 0)
            

            
App()
import pygame
import random
import math
import time

WIDTH, HEIGHT = 800, 560
FPS = 60
BG = (30,35,25)
HUD_H = 40
PLAYER_SPEED = 4
SPAWN_DISTANCE = 200
MAX_HP = 3
INVINCIBLE_FRAMES = 90
MAX_AMMO = 12
RELOAD_FRAMES = 2 * FPS
BARREL_COUNT = 4
EXPLOSION_RADIUS = 110
EXPLOSION_FRAMES = 20

class Zombie:
    SIZE = 30
    SPEED = 1.5
    HP = 3
    COLOR = (60, 140, 60)

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.color = self.COLOR
        self.hp = self.HP
        self.frame = 0
        self.x, self.y = float(x), float(y)
        self.speed = self.SPEED

    def update(self, player_pos):
        px, py = player_pos
        cx, cy = self.rect.center
        dx, dy = px-cx, py-cy
        dist = math.hypot(dx, dy)
        if dist:
            self.x += dx/dist*self.speed
            self.y += dy/dist*self.speed
            self.rect.x, self.rect.y = round(self.x), round(self.y)
        self.frame += 1

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        wobble_y = int(math.sin(self.frame*0.2)*3)
        draw_rect = self.rect.move(0, wobble_y)
        pygame.draw.rect(screen, self.color, draw_rect, border_radius=5)
        eye_r = max(2, round(self.SIZE * 0.13))
        for fx in (0.2, 0.6):
            ex = draw_rect.x + round(self.SIZE * fx)
            pygame.draw.circle(screen, (200,40,40), (ex, draw_rect.y + round(self.SIZE/3)), eye_r)


class FastZombie(Zombie):
    SIZE = 20
    SPEED = 2.8
    HP = 1
    COLOR = (200, 200, 60)


class TankZombie(Zombie):
    SIZE = 44
    SPEED = 0.8
    HP = 6
    COLOR = (110, 60, 130)


def pick_zombie_type(wave):
    fast_w = 0 if wave < 2 else min(0.15 + 0.05*(wave-2), 0.40)
    tank_w = 0 if wave < 3 else min(0.10 + 0.03*(wave-3), 0.25)
    return random.choices([Zombie, FastZombie, TankZombie],
                          weights=[1-fast_w-tank_w, fast_w, tank_w])[0]


def spawn_zombie(width, height, player_rect, wave=1):
    cls = pick_zombie_type(wave)
    size = cls.SIZE
    while True:
        x = random.randint(0, width-size)
        y = random.randint(HUD_H, height-size)
        rect = pygame.Rect(x, y, size, size)
        if math.hypot(rect.centerx-player_rect.centerx, rect.centery-player_rect.centery) > SPAWN_DISTANCE:
            return cls(x, y)

class Barrel:
    W, H = 26, 34

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.W, self.H)

    def draw(self, screen):
        pygame.draw.rect(screen, (170,60,40), self.rect, border_radius=4)
        for yy in (self.rect.y+8, self.rect.bottom-8):
            pygame.draw.line(screen, (230,200,60), (self.rect.x, yy), (self.rect.right-1, yy), 2)


def spawn_barrels(width, height, player_rect, count=BARREL_COUNT):
    barrels = []
    while len(barrels) < count:
        x = random.randint(20, width-Barrel.W-20)
        y = random.randint(HUD_H+20, height-Barrel.H-20)
        rect = pygame.Rect(x, y, Barrel.W, Barrel.H)
        if math.hypot(rect.centerx-player_rect.centerx, rect.centery-player_rect.centery) < 150:
            continue
        if any(rect.inflate(60,60).colliderect(b.rect) for b in barrels):
            continue
        barrels.append(Barrel(x, y))
    return barrels

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (60,160,220)
        self.bullets = []
        self.shoot_cooldown = 0
        self.hp = MAX_HP
        self.invincible = 0
        self.ammo = MAX_AMMO
        self.reload_timer = 0

    def move(self, keys, width, height):
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy = -PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy = PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = PLAYER_SPEED
        if dx and dy:
            dx, dy = round(dx*0.7071), round(dy*0.7071)
        self.rect.x = max(0, min(width-self.rect.width, self.rect.x+dx))
        self.rect.y = max(HUD_H, min(height-self.rect.height, self.rect.y+dy))

    def tick(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1
        if self.reload_timer > 0:
            self.reload_timer -= 1
            if self.reload_timer == 0:
                self.ammo = MAX_AMMO

    def start_reload(self):
        if self.reload_timer == 0 and self.ammo < MAX_AMMO:
            self.reload_timer = RELOAD_FRAMES

    def take_hit(self):
        if self.invincible > 0:
            return False
        self.hp -= 1
        self.invincible = INVINCIBLE_FRAMES
        return True

    def shoot(self, target_pos):
        if self.shoot_cooldown > 0 or self.reload_timer > 0 or self.ammo <= 0: return
        cx, cy = self.rect.center
        tx, ty = target_pos
        dx, dy = tx-cx, ty-cy
        dist = (dx**2+dy**2)**0.5
        if dist == 0: return
        vx, vy = dx/dist*10, dy/dist*10
        self.bullets.append([cx, cy, vx, vy])
        self.shoot_cooldown = 15
        self.ammo -= 1
        if self.ammo == 0:
            self.start_reload()

    def update_bullets(self, width, height):
        live = []
        for b in self.bullets:
            b[0] += b[2]; b[1] += b[3]
            if 0 <= b[0] <= width and HUD_H <= b[1] <= height:
                live.append(b)
        self.bullets = live

    def draw(self, screen):
        blink_off = self.invincible > 0 and (self.invincible // 5) % 2 == 0
        if not blink_off:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        for b in self.bullets:
            pygame.draw.circle(screen, (255,220,60), (int(b[0]), int(b[1])), 5)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Escape")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20)
        self.small_font = pygame.font.SysFont("monospace", 16)
        self.big_font = pygame.font.SysFont("monospace", 44, bold=True)
        self.reset()

    def reset(self):
        self.player = Player(WIDTH//2, HEIGHT//2)
        self.zombies = [spawn_zombie(WIDTH, HEIGHT, self.player.rect) for _ in range(4)]
        self.score = 0
        self.wave = 1
        self.bonus = 0
        self.kills = 0
        self.kills_to_next = 8
        self.game_over = False
        self.start_time = time.time()
        self.barrels = spawn_barrels(WIDTH, HEIGHT, self.player.rect)
        self.explosions = []

    def kill_zombie(self, z):
        if z in self.zombies:
            self.zombies.remove(z)
            self.kills += 1
            self.bonus += 10
    
    def explode(self, barrel):
        cx, cy = barrel.rect.center
        self.barrels.remove(barrel)
        self.explosions.append([cx, cy, 0])
        for z in self.zombies[:]:
            if math.hypot(z.rect.centerx-cx, z.rect.centery-cy) <= EXPLOSION_RADIUS:
                self.kill_zombie(z)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: self.reset()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                self.player.shoot(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q and not self.game_over:
                self.player.start_reload()
        return True

    def update(self):
        if self.game_over: return
        keys = pygame.key.get_pressed()
        self.player.move(keys, WIDTH, HEIGHT)
        self.player.tick()
        self.player.update_bullets(WIDTH, HEIGHT)
        
        for z in self.zombies:
            z.update(self.player.rect.center)

        for z in self.zombies[:]:
            for b in self.player.bullets[:]:
                if z.rect.collidepoint(int(b[0]), int(b[1])):
                    self.player.bullets.remove(b)
                    if z.hit():
                        self.kill_zombie(z)
                        break
        
        for barrel in self.barrels[:]:
            for b in self.player.bullets[:]:
                if barrel.rect.collidepoint(int(b[0]), int(b[1])):
                    self.player.bullets.remove(b)
                    self.explode(barrel)
                    break

        self.explosions = [[x, y, a+1] for x, y, a in self.explosions if a+1 < EXPLOSION_FRAMES]

        for z in self.zombies:
            if z.rect.colliderect(self.player.rect):
                if self.player.take_hit() and self.player.hp <= 0:
                    self.game_over = True
                break

        self.score = int(time.time() - self.start_time) + self.bonus

        if self.kills >= self.kills_to_next:
            self.kills = 0
            self.wave += 1
            self.kills_to_next = 8 + self.wave * 2
            for _ in range(self.wave + 3):
                self.zombies.append(spawn_zombie(WIDTH, HEIGHT, self.player.rect, self.wave))

    def draw(self):
        self.screen.fill(BG)
        for x in range(0, WIDTH, 60):
            pygame.draw.line(self.screen, (40,45,35), (x,HUD_H), (x,HEIGHT), 1)

        for y in range(HUD_H, HEIGHT, 60):
            pygame.draw.line(self.screen, (40,45,35), (0,y), (WIDTH,y), 1)

        for barrel in self.barrels: barrel.draw(self.screen)
        for z in self.zombies: z.draw(self.screen)
        for x, y, age in self.explosions:
            r = max(1, int(EXPLOSION_RADIUS * age / EXPLOSION_FRAMES))
            pygame.draw.circle(self.screen, (255,150,40), (x, y), r, 6)
        
        self.player.draw(self.screen)
        hud_bg = pygame.Rect(0, 0, WIDTH, 40)
        pygame.draw.rect(self.screen, (15,20,15), hud_bg)
        p = self.player
        ammo_txt = f"RELOAD {p.reload_timer/FPS:.1f}s" if p.reload_timer > 0 else f"Ammo {p.ammo}/{MAX_AMMO}"
        
        hud = self.font.render(
            f"Wave {self.wave}  Score {self.score}  Kills {self.kills}/{self.kills_to_next}  HP {self.player.hp}/{MAX_HP}  {ammo_txt}",
            True, (160,220,120))
        self.screen.blit(hud, (8, 10))
        hint = self.small_font.render("WASD move | Click shoot | Q reload | R restart", True, (110,140,90))
        self.screen.blit(hint, (8, HEIGHT-20))

        if self.game_over:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((0,0,0,160))
            self.screen.blit(ov, (0,0))
            m = self.big_font.render("DEVOURED!", True, (180,40,40))
            s = self.font.render(f"Wave {self.wave} | Score {self.score} | Press R", True, (200,200,200))
            self.screen.blit(m, (WIDTH//2-m.get_width()//2, HEIGHT//2-40))
            self.screen.blit(s, (WIDTH//2-s.get_width()//2, HEIGHT//2+20))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()

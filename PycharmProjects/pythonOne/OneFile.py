import pygame
import random

pygame.init()

# Đường dẫn tới các hình ảnh
SCREEN_IMAGE = r"BackGroud.jpg"
PerSon = r"Crab.png"
BULLET_IMAGE_PATH = r"ball.png"
COIN_IMAGE_PATH = r"CoinHB.png"
Obstacle_IMAGE1 = r"LongWeapon.png"
Obstacle_IMAGE2 = r"ShortWeapon.png"

enemy_images = [
    r"BlueBall.png",
    r"GreenBall.png",
    r"PinkBall.png",
    r"YellowBall.png"
]

# Thiết lập màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Thiết lập kích thước màn hình
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Đặt tên cho cửa sổ
pygame.display.set_caption("Đá thủ Tạo game :)")

# Tạo đồng hồ để kiểm soát FPS
clock = pygame.time.Clock()


# Lớp Máy Bay Địch
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, size, speed):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -10)
        self.speed_y = speed

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -10)
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)


# Lớp Đạn
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            self.kill()


# Lớp Đồng Xu (Coin)
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(COIN_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = 5  # Tốc độ di chuyển ban đầu của đồng xu
        self.bouncing = False  # Cờ để biết đồng xu đang nảy lên hay rơi xuống

    def update(self):
        # Nếu đồng xu đang rơi xuống
        if not self.bouncing:
            self.rect.y += self.speed_y
            if self.rect.y + self.rect.height >= SCREEN_HEIGHT:  # Khi chạm cạnh dưới
                self.bouncing = True  # Đổi hướng di chuyển
        else:
            self.rect.y -= self.speed_y  # Di chuyển lên
            if self.rect.y <= 0:  # Khi chạm cạnh trên
                self.bouncing = False  # Đổi hướng di chuyển lại xuống


# Lớp Chướng Ngại Vật (Obstacle)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = random.randint(35, 50)
        self.height = random.randint(100, 200)
        self.image_path = random.choice([Obstacle_IMAGE1, Obstacle_IMAGE2])
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -50)
        self.speed_y = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


# Lớp Máy Bay Người Chơi
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(PerSon).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 50))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        self.coins_collected = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def collect_coin(self, coins):
        collected = pygame.sprite.spritecollide(self, coins, True)
        self.coins_collected += len(collected)


# Quản lý kẻ địch
class EnemyManager:
    def __init__(self):
        self.enemies = pygame.sprite.Group()

    def create_enemies(self):
        enemy_data = [
            (enemy_images[0], (40, 20), 2),
            (enemy_images[1], (60, 30), 3),
            (enemy_images[2], (50, 40), 4),
            (enemy_images[3], (80, 50), 5)
        ]
        for image, size, speed in enemy_data:
            enemy = Enemy(image, size, speed)
            self.enemies.add(enemy)

    def update(self):
        self.enemies.update()

    def draw(self, screen):
        self.enemies.draw(screen)


# Game Over
def game_over():
    font = pygame.font.SysFont(None, 28)
    text = font.render("Game Over! Press R to Retry or Q to Quit", True, RED)
    screen.fill(BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False


# Hàm chính
def main_game():
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    enemy_manager = EnemyManager()
    enemy_manager.create_enemies()

    background_image = pygame.image.load(SCREEN_IMAGE).convert()
    obstacle_timer, enemy_timer = 0, pygame.time.get_ticks()

    running = True
    paused = False
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.add(Bullet(player.rect.centerx, player.rect.top))
                if event.key == pygame.K_c:
                    paused = not paused  # Chuyển trạng thái dừng hoặc tiếp tục trò chơi

        if not paused:
            if current_time - obstacle_timer > 2000:
                obstacles.add(Obstacle())
                obstacle_timer = current_time

            if current_time - enemy_timer > 1000:
                enemy_manager.create_enemies()
                enemy_timer = current_time

            all_sprites.update()
            bullets.update()
            coins.update()
            obstacles.update()
            enemy_manager.update()

            # Kiểm tra va chạm giữa người chơi và chướng ngại vật
            if pygame.sprite.spritecollide(player, obstacles, False):
                if game_over():
                    main_game()
                else:
                    running = False

            # Kiểm tra va chạm giữa đạn và kẻ địch
            for bullet in bullets:
                for enemy in pygame.sprite.spritecollide(bullet, enemy_manager.enemies, True):
                    bullet.kill()
                    for _ in range(random.randint(1, 3)):
                        coins.add(Coin(enemy.rect.centerx, enemy.rect.centery))

            # Người chơi thu thập đồng xu
            player.collect_coin(coins)

        # Vẽ màn hình và các thành phần game
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        bullets.draw(screen)
        coins.draw(screen)
        obstacles.draw(screen)
        enemy_manager.draw(screen)

        # Vẽ viền cho tất cả các sprite
        #for sprite in all_sprites:
           # pygame.draw.rect(screen, RED, sprite.rect, 2)
        #for sprite in bullets:
           # pygame.draw.rect(screen, (0, 255, 0), sprite.rect, 2)
        #for sprite in coins:
          #  pygame.draw.rect(screen, (255, 255, 0), sprite.rect, 2)
        #for sprite in obstacles:
           # pygame.draw.rect(screen, (0, 0, 255), sprite.rect, 2)
        #for sprite in enemy_manager.enemies:
           # pygame.draw.rect(screen, WHITE, sprite.rect, 2)

        # Hiển thị thông tin số lượng đồng xu
        font = pygame.font.SysFont(None, 36)
        screen.blit(font.render(f"Coins: {player.coins_collected}", True, WHITE), (10, 10))

        pygame.display.flip()
        clock.tick(60)


# Chạy game
main_game()
pygame.quit()

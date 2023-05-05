import pygame
import sys
import random

# ゲームウィンドウのサイズ
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GROUND_HEIGHT=50

# 色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
YELLOW= (200,200,0)
RED = (255, 0, 0)



def main(): 
    
    def show_start_screen():
        # 背景を白にする
        screen.fill(WHITE)
        
        # タイトルの表示
        title_text = font.render("Jumping Game", True, BLACK)
        title_rect = title_text.get_rect()
        title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        screen.blit(title_text, title_rect)
        
        # ルール説明の表示
        rule_text1 = font.render("スペースキー連打でジャンプ！", True, BLACK)
        rule_rect1 = rule_text1.get_rect()
        rule_rect1.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        screen.blit(rule_text1, rule_rect1)
        
        rule_text1_ = font.render(" Aで左移動 Dで右移動 ", True, BLACK)
        rule_rect1_ = rule_text1_.get_rect()
        rule_rect1_.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 +50)
        screen.blit(rule_text1_, rule_rect1_)
        
        rule_text2 = font.render("障害物に当たらないように進もう！", True, BLACK)
        rule_rect2 = rule_text2.get_rect()
        rule_rect2.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
        screen.blit(rule_text2, rule_rect2)
        
        # スタートの表示
        start_text = font.render(" S でスタート！", True, BLACK)
        start_rect = start_text.get_rect()
        start_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200)
        screen.blit(start_text, start_rect)
        
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        waiting = False
    
    # プレイヤークラス
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((30, 30))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.centerx = WINDOW_WIDTH // 2
            self.rect.bottom = WINDOW_HEIGHT - 50
            self.velocity = pygame.math.Vector2(0, 0)
            self.acceleration = pygame.math.Vector2(0, 0.5)
            self.jump_count = 0  # ジャンプ回数
            self.frame=0
            
            

        def update(self):
            
            self.frame = self.frame + 1
            
            # 重力を加速度に加える
            self.velocity += self.acceleration

            # プレイヤーの位置を移動する
            self.rect.move_ip(self.velocity.x, self.velocity.y)
            
            # 画面外に出た場合、画面内に戻す
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
            if self.rect.top < 0:
                self.rect.top = 0
                self.velocity.y = 0  # 上方向への速度を0にする

        def jump(self):
            # ジャンプする   
            self.velocity.y = -7
            jump_sound.play()  # ジャンプ効果音の再生

    # 地面クラス
    class Ground(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((50, 50))
            self.image.fill(BROWN)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    # 障害物クラス
    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((70, 70))
            self.image.fill(BROWN)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (x, y)
            
            # ランダムな高さを設定する
            height = random.randint(0, 500)
            self.rect.bottom = self.rect.bottom - height
            self.rect.left = self.rect.left + height // 2

    def clear_screen():
        screen.fill(BLACK)

    def show_message(message, size, color, x, y):
        font = pygame.font.Font(None, size)
        text = font.render(message, True, color)
        rect = text.get_rect()
        rect.center = (x, y)
        screen.blit(text, rect)
        pygame.display.update()
        
    def game_end():
        clear_screen()
        pygame.mixer.music.stop()  # BGMの停止
        game_over_sound.play()  # ゲームオーバー効果音の再生
        show_message("Game Over", 64, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        show_message(f"Score(frame): {int(player.frame)}", 32, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        show_message("Press SPACE to restart", 32, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    main()
    
    # Pygameを初期化する
    pygame.init()
    
    font = pygame.font.Font("JKG-L_3.ttf", 30)
    
    # BGMと効果音の読み込み
    pygame.mixer.music.load("bgm.mp3")  # BGM
    pygame.mixer.music.set_volume(0.01)  # 音量の設定
    jump_sound = pygame.mixer.Sound("jump.mp3")  # ジャンプ効果音
    jump_sound.set_volume(0.01)
    collision_sound = pygame.mixer.Sound("collision.mp3")  # 障害物衝突効果音
    collision_sound.set_volume(0.01)
    
    # ゲームオーバー時に再生する効果音
    game_over_sound = pygame.mixer.Sound("gameover.mp3")
    game_over_sound.set_volume(0.01)

    # ゲームウィンドウを作成する
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    show_start_screen()

    # プレイヤーオブジェクトを作成する
    player = Player()
    #player.distance=0

    # 地面オブジェクトを作成する
    ground_list = pygame.sprite.Group()
    for i in range(0, WINDOW_WIDTH, 50):
        ground = Ground(i, WINDOW_HEIGHT-50)
        ground_list.add(ground)

    # 障害物オブジェクトを作成する
    obstacle_list = pygame.sprite.Group()

    # スプライトグループを作成する
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(ground_list)
    clock = pygame.time.Clock()
    game_over = False
    while not game_over:
        
        # BGM再生
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
            
        # イベント処理
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        

        # キーの状態を取得する
        keys = pygame.key.get_pressed()
        
        # プレイヤーの移動処理
        if keys[pygame.K_a]:
            player.velocity.x = -5
        if keys[pygame.K_d]:
            player.velocity.x = 5
        if keys[pygame.K_SPACE]:
            player.jump()
            
        

        # 衝突判定
        if pygame.sprite.spritecollide(player, ground_list, False):
            player.velocity.y = 0
            player.rect.bottom = ground_list.sprites()[0].rect.top

        if pygame.sprite.spritecollide(player, obstacle_list, False):
            collision_sound.play()
            game_over = True

        # 画面を黒で塗りつぶす
        screen.fill(BLACK)

        # スプライトを更新する
        all_sprites.update()

        # スプライトを描画する
        all_sprites.draw(screen)

        # 障害物を生成する
        if len(obstacle_list) < 6:
            obstacle = Obstacle(WINDOW_WIDTH, WINDOW_HEIGHT-20)
            obstacle_list.add(obstacle)
            all_sprites.add(obstacle)

        # 障害物を移動する
        for obstacle in obstacle_list:
            obstacle.rect.x -= 8
            if obstacle.rect.right < 0:
                obstacle.kill()

        # 画面を更新する
        pygame.display.update()

        # ゲームのフレームレートを設定する
        clock.tick(60)
        

    game_end()


main()


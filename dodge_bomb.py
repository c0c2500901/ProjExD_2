import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:  #画面内にあるか
    return (
        0 <= obj_rct.left and obj_rct.right <= WIDTH,
        0 <= obj_rct.top and obj_rct.bottom <= HEIGHT
    )

def gameover(screen: pg.Surface) -> None:  # GameOver画面
    # 半透明の黒い画面
    black_screen = pg.Surface((WIDTH, HEIGHT))
    black_screen.fill((0, 0, 0))
    black_screen.set_alpha(180)

    # Game Overテキスト
    font = pg.font.Font(None, 100)
    gameover_text = font.render("Game Over", True, (255, 255, 255))
    gameover_rct = gameover_text.get_rect()
    gameover_rct.center = (WIDTH // 2, HEIGHT // 2)

    # こうかとん画像読み込みと縮小
    kk_img = pg.image.load("fig/8.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 0.9)

    # 左側のこうかとん（テキストの左側）
    kk_l_rct = kk_img.get_rect()
    kk_l_rct.centery = HEIGHT // 2
    kk_l_rct.right = gameover_rct.left - 20  # テキストの左端から20px左

    # 右側のこうかとん（左右反転してテキストの右側）
    kk_r_img = pg.transform.flip(kk_img, True, False)  # 左右反転
    kk_r_rct = kk_r_img.get_rect()
    kk_r_rct.centery = HEIGHT // 2
    kk_r_rct.left = gameover_rct.right + 20  # テキストの右端から20px右

    # 描画処理
    screen.blit(black_screen, (0, 0))
    screen.blit(gameover_text, gameover_rct)
    screen.blit(kk_img, kk_l_rct)      # 左側のこうかとん
    screen.blit(kk_r_img, kk_r_rct)    # 右側のこうかとん

    pg.display.update()
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    kk_img = pg.transform.rotozoom(
        pg.image.load("fig/3.png"), 0, 0.9
    )
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 練習問題2：爆弾を作成
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)

    bb_rct = bb_img.get_rect()
    bb_rct.center = (
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT)
    )

    vx = 5
    vy = 5

    clock = pg.time.Clock()
    tmr = 0

    # 練習問題1：移動量の辞書
    DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, 5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (5, 0)
    }

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        # 練習問題1：こうかとんの移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # 練習問題3：こうかとんが画面外に出ないようにする
        old_rct = kk_rct.copy()
        kk_rct.move_ip(sum_mv)

        if not all(check_bound(kk_rct)):
            kk_rct = old_rct

        # 練習問題2：爆弾を移動
        bb_rct.move_ip(vx, vy)

        # 練習問題3：爆弾を画面端で反射
        if not check_bound(bb_rct)[0]:
            vx *= -1

        if not check_bound(bb_rct)[1]:
            vy *= -1

        # GaneOverの表示
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return


        # 描画
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)

        pg.display.update()

        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
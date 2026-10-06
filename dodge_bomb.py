import math
import os
import random
import sys
import time

import pygame as pg


WIDTH, HEIGHT = 1100, 650

os.chdir(os.path.dirname(os.path.abspath(__file__)))



def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """画面内にあるか確認する。"""
    return (
        0 <= obj_rct.left and obj_rct.right <= WIDTH,
        0 <= obj_rct.top and obj_rct.bottom <= HEIGHT
    )



def gameover(screen: pg.Surface) -> None:
    """Gameover"""
    black_screen = pg.Surface((WIDTH, HEIGHT))
    black_screen.fill((0, 0, 0))
    black_screen.set_alpha(180)

    font = pg.font.Font(None, 100)
    gameover_text = font.render(
        "Game Over",
        True,
        (255, 255, 255)
    )

    gameover_rct = gameover_text.get_rect()
    gameover_rct.center = (WIDTH // 2, HEIGHT // 2)

    kk_img = pg.image.load("fig/8.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 0.9)

    kk_l_rct = kk_img.get_rect()
    kk_l_rct.centery = HEIGHT // 2
    kk_l_rct.right = gameover_rct.left - 20

    kk_r_img = pg.transform.flip(kk_img, True, False)

    kk_r_rct = kk_r_img.get_rect()
    kk_r_rct.centery = HEIGHT // 2
    kk_r_rct.left = gameover_rct.right + 20

    screen.blit(black_screen, (0, 0))
    screen.blit(gameover_text, gameover_rct)
    screen.blit(kk_img, kk_l_rct)
    screen.blit(kk_r_img, kk_r_rct)

    pg.display.update()
    time.sleep(5)


# こうかとんの移動方向に対応した画像を作成する
def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    base_img = pg.image.load("fig/3.png")

    kk_imgs = {}

    # 動かない
    kk_imgs[(0, 0)] = pg.transform.rotozoom(
        base_img, 0, 0.9
    )

    # 左
    kk_imgs[(-5, 0)] = pg.transform.rotozoom(
        base_img, 0, 0.9
    )

    # 右
    kk_imgs[(5, 0)] = pg.transform.flip(
        base_img, True, False
    )
    kk_imgs[(5, 0)] = pg.transform.rotozoom(
        kk_imgs[(5, 0)], 0, 0.9
    )

    # 上
    kk_imgs[(0, -5)] = pg.transform.rotozoom(
        base_img, -90, 0.9
    )

    # 下
    kk_imgs[(0, 5)] = pg.transform.rotozoom(
        base_img, 90, 0.9
    )

    # 左上
    kk_imgs[(-5, -5)] = pg.transform.rotozoom(
        base_img, -45, 0.9
    )

    # 右上
    kk_imgs[(5, -5)] = pg.transform.flip(
        pg.transform.rotozoom(base_img, -45, 0.9),
        True,
        False
    )

    # 左下
    kk_imgs[(-5, 5)] = pg.transform.rotozoom(
        base_img, 45, 0.9
    )

    # 右下
    kk_imgs[(5, 5)] = pg.transform.flip(
        pg.transform.rotozoom(base_img, 45, 0.9),
        True,
        False
    )

    return kk_imgs


# 爆弾からこうかとんへの移動方向を計算する
def calc_orientation(
    org: pg.Rect,
    dst: pg.Rect,
    current_xy: tuple[float, float]
) -> tuple[float, float]:

    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery

    distance = math.sqrt(dx ** 2 + dy ** 2)

    # こうかとんとの距離が300未満なら現在の方向を維持する
    if distance < 300:
        return current_xy

    # こうかとんの方向へ向かう速度を計算する
    speed = math.sqrt(50)

    return (
        dx / distance * speed,
        dy / distance * speed
    )


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img = pg.image.load("fig/pg_bg.jpg")

    # 追加機能3：方向別こうかとん画像
    kk_imgs = get_kk_imgs()

    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 追加機能2：爆弾の画像を10段階用意
    bb_imgs = []

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        bb_img.set_colorkey((0, 0, 0))

        pg.draw.circle(
            bb_img,
            (255, 0, 0),
            (10 * r, 10 * r),
            10 * r
        )

        bb_imgs.append(bb_img)

    # 追加機能2：爆弾の加速度
    bb_accs = [a for a in range(1, 11)]

    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()

    bb_rct.center = (
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT)
    )

    vx = 5.0
    vy = 5.0

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

        # こうかとんの移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # 追加機能3：移動方向に応じて画像を変更
        kk_img = kk_imgs[tuple(sum_mv)]

        # 画像変更時も中心位置を維持
        center = kk_rct.center
        kk_rct = kk_img.get_rect()
        kk_rct.center = center

        # こうかとんが画面外に出ないようにする
        old_rct = kk_rct.copy()

        kk_rct.move_ip(sum_mv)

        if not all(check_bound(kk_rct)):
            kk_rct = old_rct

        # 追加機能2：時間経過で爆弾を大きく・速くする
        stage = min(tmr // 500, 9)

        bb_img = bb_imgs[stage]

        center = bb_rct.center
        bb_rct.size = bb_img.get_size()
        bb_rct.center = center

        # 追加機能4：爆弾をこうかとんに向かわせる
        vx, vy = calc_orientation(
            bb_rct,
            kk_rct,
            (vx, vy)
        )

        avx = vx * bb_accs[stage]
        avy = vy * bb_accs[stage]

        bb_rct.move_ip(avx, avy)

        # 爆弾を画面端で反射
        if not check_bound(bb_rct)[0]:
            vx *= -1

            if bb_rct.left < 0:
                bb_rct.left = 0

            if bb_rct.right > WIDTH:
                bb_rct.right = WIDTH

        if not check_bound(bb_rct)[1]:
            vy *= -1

            if bb_rct.top < 0:
                bb_rct.top = 0

            if bb_rct.bottom > HEIGHT:
                bb_rct.bottom = HEIGHT

        # Game Over
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
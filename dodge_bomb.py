import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    物体が画面内に収まっているか確認する。
    """
    return (
        0 <= obj_rct.left and obj_rct.right <= WIDTH,
        0 <= obj_rct.top and obj_rct.bottom <= HEIGHT
    )


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

        # 練習問題4：こうかとんと爆弾が衝突したら終了
        if kk_rct.colliderect(bb_rct):
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
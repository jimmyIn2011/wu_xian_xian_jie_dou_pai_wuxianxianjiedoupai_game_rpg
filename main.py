import pygame as pg
import random as rd


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2][1]
    left = [x for x in arr if x[1] < pivot]
    middle = [x for x in arr if x[1] == pivot]
    right = [x for x in arr if x[1] > pivot]
    return quick_sort(left) + middle + quick_sort(right)


class ShabbyAI:
    def __init__(self, human_cards, ai_cards):
        self.human_cards = human_cards.copy()
        self.ai_cards = ai_cards.copy()

    def optimal_ai_move(self, human_card):
        winning_cards = [c for c in self.ai_cards if c[1] > human_card[1]]
        if winning_cards:
            best_card = rd.choice(winning_cards)
        else:
            best_card = rd.choice(self.ai_cards)
        self.ai_cards.remove(best_card)
        return best_card

    def check_game_over(self):
        return [not self.human_cards or not self.ai_cards, 2 if not self.human_cards else 1]


def get_g():
    with open("./settings.none", 'r') as file:
        return int(file.readline().strip())


def get_bi():
    with open("./settings.none", 'r') as file:
        return int(file.readlines()[1])


def get_qh():
    with open("./settings.none", 'r') as file:
        return [int(sb) for sb in (file.readlines()[2:])]


def upd_g():
    with open("./settings.none", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if lines:
        lines[0] = str(gs) + '\n'
    with open("./settings.none", 'w', encoding='utf-8') as f:
        f.writelines(lines)


def upd_bi():
    with open("./settings.none", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if lines:
        lines[1] = str(money) + '\n'
    with open("./settings.none", 'w', encoding='utf-8') as f:
        f.writelines(lines)


def upd_qh():
    with open("./settings.none", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = lines[:2] + [str(line[2]) + '\n' for line in characters]
    with open("./settings.none", 'w', encoding='utf-8') as f:
        f.writelines(lines)


pg.init()
money = get_bi()
pg.display.init()
screen = pg.display.set_mode([800, 800])
pg.display.set_caption("无限仙界斗牌<单机>")
running = True
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
RED = [255, 0, 0]
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GOLDEN = (205, 127, 50)
BROWN = [128, 64, 0]
scene = 1
onm = None
characters = [["玉皇大帝", 35, 0, YELLOW], ["如来佛祖", 39, 0, YELLOW], ["鸿钧道祖", 51, 0, RED],
              ["接引道人", 42, 0, YELLOW],
              ["准提道人", 42, 0, YELLOW],
              ["通天教主", 44, 0, YELLOW], ["元始天尊", 45, 0, YELLOW], ["太上老君", 46, 0, YELLOW],
              ["女娲", 48, 0, RED], ["盘古", 55, 0, RED],
              ["罗睺", 52, 0, RED], ["土行孙", 8, 0, WHITE], ["东皇太一", 29, 0, PURPLE], ["帝俊", 30, 0, PURPLE],
              ["太乙真人", 30, 0, PURPLE],
              ["阎罗王", 22, 0, BLUE], ["二郎神", 24, 0, BLUE], ["李靖", 19, 0, BLUE],
              ["姜子牙", 25, 0, PURPLE], ["陆压道君", 27, 0, PURPLE], ["祝融", 25, 0, PURPLE], ["共工", 24, 0, BLUE]]
# 白 蓝 紫 黄 红
qh = get_qh()
for i in range(len(characters)):
    characters[i][2] = qh[i]
# scene=1
cg = pg.Rect(300, 590, 200, 100)  # 闯关
gs = get_g()  # 关数
py = pg.Rect(0, 600, 200, 100)  # 培养
qian = pg.Rect(600, 0, 200, 50)
q = pg.Rect(0, 750, 800, 50)
chupaibtn = pg.Rect(0, 330, 30, 65)  # 出牌
onchoose = None
bliting = False
blittime = 54188
qhbtn = pg.Rect(300, 600, 200, 100)
shabi = None
choices = [None, None]
winner = None
clock = pg.time.Clock()
while running:
    screen.fill(WHITE)
    clock.tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            upd_g()
            upd_bi()
            upd_qh()
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if cg.collidepoint(pos) and scene == 1:
                scene = 2
                cards = []
                onchoose = None
                for i in range(20):
                    cards.append(rd.choice(characters))
                    cards[-1] = [cards[-1][0],
                                 rd.randint(cards[-1][1] + cards[-1][2] - 3, cards[-1][1] + cards[-1][2] + 3),
                                 cards[-1][3], 0]  # 3:is onchoose
                shabi = ShabbyAI(cards[:10], cards[10:])
                shabi.human_cards = quick_sort(shabi.human_cards)
                shabi.ai_cards = quick_sort(shabi.ai_cards)
                winner = None
            elif py.collidepoint(pos) and scene == 1:
                scene = 3
            if scene == 3:
                if q.collidepoint(pos):
                    scene = 1
                for i in range(len(characters)):
                    if pg.rect.Rect(i % 8 * 100, int(i / 8) * 150, 98, 145).collidepoint(pos):
                        scene = 4
                        onm = i
            elif scene == 4:
                if q.collidepoint(pos):
                    scene = 3
                if qhbtn.collidepoint(pos):
                    if money >= characters[onm][2] + 1:
                        characters[onm][2] += 1
                        money -= characters[onm][2]
            elif scene == 2:
                for i in range(len(shabi.human_cards)):
                    if pg.Rect(i*80, 650, 100, 150).collidepoint(pos):
                        if onchoose is None or onchoose != i:
                            onchoose = i
                        else:
                            onchoose = None
                if onchoose is not None and chupaibtn.collidepoint(pos) and blittime >= 30:
                    bliting = True
                    blittime = 0
                    choices = [shabi.optimal_ai_move(shabi.human_cards[onchoose]), shabi.human_cards[onchoose]]
                    shabi.human_cards.remove(choices[1])
                    onchoose = None
            elif scene == 5:
                if cg.collidepoint(pos):
                    scene = 1
                    winner = None
    if scene == 1:
        screen.blit(pg.image.load("./images/bj1.png"), [0, 0])
        pg.draw.rect(screen, BLACK, cg, 1)
        pg.draw.rect(screen, GREEN, [cg[0] + 1, cg[1] + 1, cg[2] - 2, cg[3] - 2])
        screen.blit(pg.font.SysFont("华文楷体", 65).render("闯   关", True, BLUE), [301, 591])
        screen.blit(pg.font.SysFont("华文楷体", 70).render("第%s关" % gs, True, BLACK), [100 - 10, 100])
        pg.draw.rect(screen, GREEN, py)
        pg.draw.rect(screen, PURPLE, qian)
        screen.blit(pg.font.SysFont("华文楷体", 65).render("培   养", True, BLACK), [py[0] + 1, py[1] + 1])
        screen.blit(pg.font.SysFont("华文楷体", 30).render(str(money), True, WHITE), [qian[0] + 1, qian[1] + 1])
    elif scene == 2:
        pg.draw.rect(screen, BROWN, [50, 260, 700, 280])
        pg.draw.rect(screen, BLACK, chupaibtn, 1)
        if chupaibtn.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(screen, RED, [chupaibtn[0]+1, chupaibtn[1]+1, chupaibtn[2]-2, chupaibtn[3]-2])
        screen.blit(pg.font.SysFont("华文楷体", 24).render("出", True, BLACK), [0, 331])
        screen.blit(pg.font.SysFont("华文楷体", 24).render("牌", True, BLACK), [0, 360])
        if shabi is None:
            scene = 1
        pt = 650
        screen.blit(pg.font.SysFont("华文楷体", 20).render("人机出的牌：", True, WHITE), [51, 261])
        screen.blit(pg.font.SysFont("华文楷体", 20).render("你出的牌：", True, WHITE), [471, 261])
        if bliting:
            blittime += 1
            if blittime > 30:
                bliting = False
                if choices[0][1] > choices[1][1]:
                    shabi.ai_cards.append(choices[1])
                    shabi.ai_cards = quick_sort(shabi.ai_cards)
                elif choices[1][1] > choices[0][1]:
                    shabi.human_cards.append(choices[0])
                    shabi.human_cards = quick_sort(shabi.human_cards)
            pg.draw.rect(screen, BLACK, [75, 325, 100, 150])
            pg.draw.rect(screen, BLACK, [575, 325, 100, 150])
            pg.draw.rect(screen, choices[0][2], [76, 326, 98, 148])
            screen.blit(pg.font.SysFont("华文楷体", 20).render(choices[0][0], True,
                                                               WHITE if choices[0][2] != WHITE and
                                                                        choices[0][2] != YELLOW else BLACK),
                        [76, 326])
            screen.blit(pg.font.SysFont("华文楷体", 18).render(str(choices[0][1]), True,
                                                               WHITE if choices[0][2] != WHITE and
                                                                        choices[0][2] != YELLOW else BLACK),
                        [76, 326+53])
            pg.draw.rect(screen, choices[1][2], [576, 326, 98, 148])
            screen.blit(pg.font.SysFont("华文楷体", 20).render(choices[1][0], True,
                                                               WHITE if choices[1][2] != WHITE and
                                                                        choices[1][2] != YELLOW else BLACK),
                        [576, 326])
            screen.blit(pg.font.SysFont("华文楷体", 18).render(str(choices[1][1]), True,
                                                               WHITE if choices[1][2] != WHITE and
                                                                        choices[1][2] != YELLOW else BLACK),
                        [576, 326+53])
        chk = shabi.check_game_over()
        if chk[0]:
            scene = 5
            winner = chk[1]
            if winner == 1:
                gs += 1
        for i in range(len(shabi.human_cards)):
            if onchoose == i:
                pt = 610
            else:
                pt = 650
            pg.draw.rect(screen, shabi.human_cards[i][2], [i * 80 + 1, pt+1, 78, 148])
            pg.draw.rect(screen, BLACK, [i * 80, pt, 80, 150], 2)
            screen.blit(pg.font.SysFont("华文楷体", 20).render(shabi.human_cards[i][0], True,
                                                               WHITE if shabi.human_cards[i][2] != WHITE and
                                                                        shabi.human_cards[i][2] != YELLOW else BLACK),
                        [i * 80 + 1, pt+1])
            screen.blit(pg.font.SysFont("华文楷体", 18).render(str(shabi.human_cards[i][1]), True, WHITE if shabi.human_cards[i][2] != WHITE and
                                                                        shabi.human_cards[i][2] != YELLOW else BLACK),
                        [i * 80 + 1, pt+53])
        for i in range(len(shabi.ai_cards)):
            pg.draw.rect(screen, shabi.ai_cards[i][2], [i * 80 + 1, 1, 78, 148])
            pg.draw.rect(screen, BLACK, [i * 80, 0, 80, 150], 2)
            screen.blit(pg.font.SysFont("华文楷体", 20).render(shabi.ai_cards[i][0], True,
                                                               WHITE if shabi.ai_cards[i][2] != WHITE and
                                                                        shabi.ai_cards[i][2] != YELLOW else BLACK),
                        [i * 80 + 1, 1])
            screen.blit(pg.font.SysFont("华文楷体", 18).render(str(shabi.ai_cards[i][1]), True, WHITE if shabi.ai_cards[i][2] != WHITE and
                                                                        shabi.ai_cards[i][2] != YELLOW else BLACK),
                        [i * 80 + 1, 53])
    elif scene == 3:
        pg.draw.rect(screen, BLUE, q)
        screen.blit(pg.font.SysFont("华文楷体", 25).render("退出", True, WHITE), [q[0] + 1, q[1] + 1])
        for i in range(len(characters)):
            pg.draw.rect(screen, characters[i][3], [i % 8 * 100, int(i / 8) * 150, 98, 145])
            screen.blit(pg.font.SysFont("华文楷体", 20).render(characters[i][0], True,
                                                               WHITE if characters[i][3] != WHITE and characters[i][
                                                                   3] != YELLOW else BLACK),
                        [i % 8 * 100 + 1, int(i / 8) * 150 + 1])
            screen.blit(pg.font.SysFont("华文楷体", 30).render(str(characters[i][1] + characters[i][2]), True,
                                                               WHITE if characters[i][3] != WHITE and characters[i][
                                                                   3] != YELLOW else BLACK),
                        [i % 8 * 100 + 1, int(i / 8) * 150 + 52])
    elif scene == 4:
        if onm is None:
            scene = 3
        pg.draw.rect(screen, BLUE, q)
        screen.blit(pg.font.SysFont("华文楷体", 25).render("退出", True, WHITE), [q[0] + 1, q[1] + 1])
        screen.blit(pg.image.load("./images/" + characters[onm][0] + ".jpg"), [0, 0])
        screen.blit(
            pg.font.SysFont("华文楷体", 40).render("点数：" + str(characters[onm][1]) + "+" + str(characters[onm][2]),
                                                   True, BLACK), [200, 460])
        pg.draw.rect(screen, RED, qhbtn)
        screen.blit(pg.font.SysFont("华文楷体", 45).render("强 化 + 1", True, BLACK), [qhbtn[0] + 1, qhbtn[1] + 1])
        pg.draw.rect(screen, PURPLE, qian)
        screen.blit(pg.font.SysFont("华文楷体", 30).render(str(money), True, WHITE), [qian[0] + 1, qian[1] + 1])
    elif scene == 5:
        screen.blit(pg.image.load("./images/bg.jpg"), [0, 0])
        pg.draw.rect(screen, GREEN, cg)
        screen.blit(pg.font.SysFont("华文楷体", 65).render("首   页", True, BLACK), [301, 591])
        screen.blit(pg.font.SysFont("华文楷体", 70).render("你%s了" % ('赢' if winner == 1 else '输'), True, RED), [200, 200])
    pg.display.flip()
pg.quit()

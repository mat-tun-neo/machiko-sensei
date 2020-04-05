from pygame_functions import *
from random import randint

setAutoUpdate(False)
screen = screenSize(1, 1, 1, 1)

# 画像の指定
IMAGE_SET="machiko"
PLAYER_IMAGE = "images/" + IMAGE_SET + "_player.png"
CHILD_IMAGE = "images/" + IMAGE_SET + "_child.png"
ITEM_IMAGE = "images/" + IMAGE_SET + "_item.png"
GAMEOVER_IMAGE = "images/" + IMAGE_SET + "_gameover.png"
SCORE_IMAGE =  "images/score.png"
BACK_IMAGE = "images/back.png"

SCREEN_X = 12                # 画面 横サイズ （×キャラ横ピクセル）
SCREEN_Y = 9                 # 画面 縦サイズ （×キャラ縦ピクセル）
PLAYER_ALLIMAGE = 16         # プレイヤー アニメーション全コマ数
PLAYER_SPEED = 5             # プレイヤー 移動スピード
CHILD_INTERVAL = 18          # 子キャラ 連鎖の間隔
player_xlist = []            # プレイヤー 移動履歴X
player_ylist = []            # プレイヤー 移動履歴Y
CHILD_TOUCH_JUDGE = 40       # プレイヤーと子キャラ 当たり判定　（ピクセル）
ITEM_TOUCH_JUDGE = 40        # プレイヤーとアイテム 当たり判定　（ピクセル）
SCORE_DIGIT = 3              # スコア　桁数

# プレイヤークラス
class Player():
    # コンストラクタ
    def __init__(self, img, n):
        self.speed = PLAYER_SPEED
        self.sprite = makeSprite(img, PLAYER_ALLIMAGE)
        self.width = self.sprite.image.get_rect().width
        self.height = self.sprite.image.get_rect().height
        self.xpos = self.width * 3
        self.ypos = self.width * 3 - self.height
        self.x_direction = 0
        self.y_direction = 0
        self.timeOfNextFrame = clock()
        self.frame = 0
        self.child = None
        self.num = n
        if self.num == 0:
            self.next_xpos = self.width * (SCREEN_X - 1)
            self.next_ypos = self.ypos
    # 移動
    def move(self):
        if self.num > 0:
            self.next_xpos = player_xlist[self.num * CHILD_INTERVAL]
            self.next_ypos = player_ylist[self.num * CHILD_INTERVAL]
        if clock() > self.timeOfNextFrame:
            self.frame = (self.frame + 1) % 4
            self.timeOfNextFrame += 160
        if self.next_xpos != self.xpos:
            self.x_direction = (self.next_xpos - self.xpos) // abs(self.next_xpos - self.xpos)
            self.y_direction = 0
            self.xpos += self.speed * self.x_direction
            changeSpriteImage(self.sprite, (1 - self.x_direction) * PLAYER_ALLIMAGE//4 + self.frame)
        elif self.next_ypos != self.ypos:
            self.x_direction = 0
            self.y_direction = (self.next_ypos - self.ypos) // abs(self.next_ypos - self.ypos)
            self.ypos += self.speed * self.y_direction
            changeSpriteImage(self.sprite, (2 - self.y_direction) * PLAYER_ALLIMAGE//4 + self.frame)
        showSprite(self.sprite)
        moveSprite(self.sprite, self.xpos, self.ypos)
        if self.child != None:
            self.child.move()
    # 当たり判定
    def touching(self, x, y):
        if self.child != None and \
            abs(x - self.child.xpos) < ITEM_TOUCH_JUDGE and \
            abs(y - self.child.ypos) < ITEM_TOUCH_JUDGE:
                return True
        if self.child != None and self.child.touching(x, y):
            return True
        else:
            return False

# アイテムクラス
class Item():
    # コンストラクタ
    def __init__(self, img):
        self.sprite = makeSprite(img)
        self.width = self.sprite.image.get_rect().width
        self.height = self.sprite.image.get_rect().height
        self.move()
    # 移動
    def move(self):
        self.xpos = randint(0, SCREEN_X - 1) * self.width
        self.ypos = randint(0, SCREEN_Y - 1) * self.width
        showSprite(self.sprite)
        moveSprite(self.sprite, self.xpos, self.ypos)
        
# スコアクラス
class Score():
    # コンストラクタ
    def __init__(self, x, y, d = SCORE_DIGIT):
        self.sprite = makeSprite(SCORE_IMAGE, 10)
        self.xpos = x
        self.ypos = y
        self.digit = SCORE_DIGIT - d
        self.width = self.sprite.image.get_rect().width
        showSprite(self.sprite)
        moveSprite(self.sprite, self.xpos, self.ypos)
        changeSpriteImage(self.sprite, 0)
        if d > 1:
            self.child = Score(x + self.width, y, d - 1)
    # スコア更新
    def update(self, n):
        sc = str(n).zfill(SCORE_DIGIT)
        changeSpriteImage(self.sprite, int(sc[self.digit]))
        if hasattr(self, 'child'):
            self.child.update(n)

# スプライト配置／スクリーンサイズ／背景
p = Player(PLAYER_IMAGE, 0)
score = Score(0, 15)
item = Item(ITEM_IMAGE)
last = p
screenSize(p.width * SCREEN_X, p.width * SCREEN_Y, 350, 60)
setBackgroundImage(BACK_IMAGE)

# メインループ
n=0
score.update(0)
while True:
    # プレイヤーの移動履歴
    player_xlist.insert(0, p.xpos)
    player_ylist.insert(0, p.ypos)
    p.move()
    # キー判定
    if p.x_direction != -1 and keyPressed("left"):
        p.next_xpos = 0
        p.next_ypos = p.ypos
    if p.x_direction != 1 and keyPressed("right"):
        p.next_ypos = p.ypos
        p.next_xpos = p.width * (SCREEN_X - 1)
    if p.y_direction != -1 and keyPressed("up"):
        p.next_xpos = p.xpos
        p.next_ypos = 0
    if p.y_direction != 1 and keyPressed("down"):
        p.next_xpos = p.xpos
        p.next_ypos = p.width * SCREEN_Y - p.height
    # アイテム当たり判定
    if abs(p.xpos - item.xpos) < ITEM_TOUCH_JUDGE and abs(p.ypos - item.ypos) < ITEM_TOUCH_JUDGE:
        last.child = Player(CHILD_IMAGE, last.num + 1)
        last = last.child
        last.xpos = player_xlist[last.num * CHILD_INTERVAL]
        last.ypos = player_ylist[last.num * CHILD_INTERVAL]
        item.move()
        n += 1
        score.update(n)
    # 子キャラ当たり判定
    if p.touching(p.xpos, p.ypos):
        break;
    
    updateDisplay()
    tick(60)

# ゲームオーバー
gameover = makeImage(GAMEOVER_IMAGE)
screen.blit(gameover, (p.width * SCREEN_X/3, p.height * SCREEN_Y/5))
endWait()


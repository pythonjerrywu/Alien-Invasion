import pygame

from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类。"""

    def __init__(self, ai_game):
        """初始化飞船并设置其起始位置。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其矩形。
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 将每艘新飞船放在屏幕底部中央。
        self.rect.midbottom = self.screen_rect.midbottom

        # 为飞船的水平位置存储一个小数值。
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志更新飞船的位置。"""
        # 更新飞船的x值，而不是矩形。
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 从self.x更新矩形对象。
        self.rect.x = self.x

    def blitme(self):
        """在当前位置绘制飞船。"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船居中于屏幕。"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

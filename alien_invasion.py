# 这是一个用python编写的项目， 目的是做一款叫《外星人入侵》的2D射击游戏, 版本1.1
# This is a project written in Python with the aim of creating a 2D shooting game
# called "Alien Invasion"
# version 1.1
# Programmer:pythonjerrywu
# 于2024年1月24日开始编写, 1月25日1.1
# Started writing on January 24, 2024, January 25, 1.1
# 描述：在游戏《外星人入侵》中，玩家控制一艘最初出现在屏幕底部中央的宇宙飞船。
# 玩家可以使用方向键左右移动飞船，也可以使用空格键进行射击。
# 游戏一开始，天空中出现了一群外星人，并向屏幕下方移动。
# 玩家的任务就是射杀这些外星人。玩家消灭完所有外星人后，会出现一批新的外星人，且移动速度更快。
# 只要有外星人与玩家的飞船相撞或者到达屏幕底部，玩家就会失去一艘飞船。
# 失去三艘宇宙飞船后，游戏结束。
# Describe:in the game Alien Invasion, players control a spaceship that initially appears in the center at the bottom of
# the screen. Players can use the arrow keys to move the spaceship left and right, and also use the space bar to shoot.
# At the beginning of the game, a group of aliens appeared in the sky and moved towards the bottom of the screen.
# The player's task is to shoot and kill these aliens. After the player has eliminated all the aliens,
# a new group of aliens will appear with faster movement speed.
# As long as an alien collides with the player's spaceship or reaches the bottom of the screen,
# the player loses one spaceship. After losing three spaceships, the game ends.
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的总类。
    Overall class to manage game assets and behavior."""

    def __init__(self):
        """初始化游戏并创建游戏资源。
        Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # 创建存储游戏统计数据的实例，并创建记分牌。
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建开始按钮。
        self.play_button = Button(self, "Play")

    def run_game(self):
        """启动游戏的主循环。
            Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件。
            Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """玩家点击Play按钮时开始新游戏。
            Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏设置。
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # 重置游戏统计数据。
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 清空剩余的外星人和子弹。
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # 创建新的外星人群并将飞船居中。
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标。
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按键。
            Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开按键。
            Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗新子弹并将其加入到子弹编组中。
            Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹。
           Update position of bullets and get rid of old bullets."""
        # 更新子弹的位置。
        # Update bullet positions.
        self.bullets.update()

        # 删除已消失的子弹。
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞。
           Respond to bullet-alien collisions."""
        # 删除发生碰撞的子弹和外星人。
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            # 检查是否有新的最高得分。
            # Check if there is a new highest score.
            self.sb.check_high_score()

        if not self.aliens:
            # 清空现有的子弹并创建一群新的外星人
            # Destroy existing bullets and create new fleet.。
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级。
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        检查是否有外星人位于屏幕边缘，
          更新外星人群中所有外星人的位置。

        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞。
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达屏幕底端。
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端。
           Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 将其视为飞船被撞击。
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """响应飞船被外星人撞击。
           Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # 减少剩余的飞船数量，并更新记分牌。
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空剩余的外星人和子弹。
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # 创建新的外星人群并将飞船居中。
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # 暂停。
            # Pause.
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """创建外星人群。
            Create the fleet of aliens."""
        # 创建一个外星人并找出一行可容纳的外星人数量。
        # 每个外星人间距为一个外星人的宽度。
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可以容纳多少行外星人。
        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建完整的外星人群。
        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其放在当前行。
            Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """如果有外星人到达边缘时采取相应的措施。
            Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """下移整个外星人群并改变它们的方向。
            Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕。
            Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分信息。
        # Draw the score information.
        self.sb.show_score()

        # 如果游戏处于非活动状态，则绘制Play按钮。
        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例，并运行游戏。
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()


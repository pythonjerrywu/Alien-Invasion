class GameStats:
    def __init__(self, ai_game):
        """初始化统计信息。"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 游戏处于非活动状态。
        self.game_active = False

        # 最高分数不应重置。
        self.high_score = 0

        # 尝试从文件中读取最高分
        self.load_high_score()

    # 将最高分写入文件
    def write_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

    # 从文件中加载最高分
    def load_high_score(self):
        try:
            with open('high_score.txt') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            # 如果文件不存在，则默认最高分为0
            self.high_score = 0

    # 检查是否有新的最高分
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
    def reset_stats(self):
        """初始化游戏中可能会变化的统计信息。"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

# 在GameStats类定义结束括号之后，添加以下代码
def check_high_score(self):
    if self.stats.score > self.stats.high_score:
        self.stats.high_score = self.stats.score
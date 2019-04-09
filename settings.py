class Settings():
    #存储外星人所有设置的类

    def __init__(self):
        #初始游戏化设置

        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #飞船设置
        self.ship_speed_factor = 1.5

        #子弹设置
        self.bullet_speed_factor = 1
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 5

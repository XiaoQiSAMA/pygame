class Settings():
    #存储外星人所有设置的类

    def __init__(self):
        #初始游戏化设置

        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 1000
        self.bg_color = (230, 230, 230)

        #飞船设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        #子弹设置
        self.bullet_speed_factor = 4
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 5

        #外星人设置
        self.alien_speed_factor = 1    
        self.fleet_drop_speed = 15
        #fleet_diretion为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

        
import sys

import pygame
from bullet import Bullet
from alien import Alien
from random import randint
from time import sleep

def update_screen(ai_settings, screen, ship, aliens, bullets):
    #更新屏幕上的图像，并切换到新屏幕

    #每次循环都重绘图像
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #让最近绘制的屏幕可见
    pygame.display.flip()

def check_events(ai_settings, screen, ship, bullets):
    #响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    #响应按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        #创建一个子弹，加入到编组bullets中
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ship):
    #响应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    #对子弹的处理
    ##刷新子弹位置
    bullets.update( )

    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets):
    #响应子弹和外星人的碰撞
    ##检查是否有子弹击中外星人
    ##如果是，将删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if len(aliens) == 0:
        #删除现有的子弹并创建一群新的外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    #创建外星人群
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
       

def get_number_aliens_x(ai_settings, alien_width):
    #计算每行可容纳多少外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_heigth, alien_height):
    #计算屏幕可容纳多少行外星人
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_heigth)
    number_rows = int(available_space_y / (3 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #创建外星人
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width 
    alien.x = randint(0, 700)
    alien.rect.y = randint(0, alien.rect.height + 2 * alien.rect.height * row_number)
    alien.rect.x = alien.x
    aliens.add(alien)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    #检查外星人是否位于屏幕边缘，并更新整理外星人位置 
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检测飞船和外星人之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    #外星人到达边缘时采取的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
  
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    #响应被外星人撞到的飞船
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放在屏幕底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)

    else:
        stats.game_active = False

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    #检查是否有外星人到达了屏幕底端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

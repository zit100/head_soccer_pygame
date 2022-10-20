import pygame, os


WIN_WIDTH = 1200
WIN_HEIGHT = 600

PLAYER1_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "player1.png")), (65, 80))
PLAYER2_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "player2.png")), (65, 80))
SHOE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "shoe.png")), (70, 40))
GOALPOSTS_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "goal_posts.png")), (130, 250))
GOALPOST_WIDTH = GOALPOSTS_IMG.get_width()
BALL_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "ball.png")), (40, 40))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BG_IMG = pygame.transform.scale(BG_IMG, (WIN_WIDTH, WIN_HEIGHT))


# Game rectangles
class player_cls:
    IMG = PLAYER1_IMG
    SPEED = 8
    VERTICAL = 10
    MAX_VERTICAL = 45
    GFORCE = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_ground = y
        self.tick_count = 0
        self.x_speed = 0
        self.y_speed = 0
        self.vertical = self.VERTICAL
        self.gforce = self.GFORCE
        self.move_right_clicked = False
        self.move_left_clicked = False
        self.dash_clicked = False
        self.img = self.IMG

    def move_right(self):
        self.move_right_clicked = True

        if self.x_speed != self.SPEED:
            self.x_speed += self.SPEED

        if self.dash_clicked:
            self.x += self.x_speed*2
        else:
            self.x += self.x_speed

    def move_left(self):
        self.move_left_clicked = True

        if self.x_speed != -self.SPEED:
            self.x_speed -= self.SPEED

        if self.dash_clicked:
            self.x += self.x_speed*2
        else:
            self.x += self.x_speed

    def dash(self):
        self.dash_clicked = True

    def jump(self):
        if self.move_right_clicked:
            self.x += self.x_speed * 2
            self.move_right_clicked = False
        if self.move_left_clicked:
            self.x += self.x_speed * 2
            self.move_left_clicked = False

        self.y -= self.vertical
        self.y_speed += self.vertical

    def gravity(self):
        if self.y < self.y_ground:
            self.tick_count += 1

            self.y_speed = self.y_speed - self.gforce * self.tick_count

            d = self.vertical * self.tick_count - self.gforce * self.tick_count ** 2
            if self.y - d <= self.y_ground:
                self.y -= d
            else:
                self.y = self.y_ground
                self.tick_count = 0
                self.y_speed = 0

    def draw(self, window, player_num="1"):
        if player_num == "1":
            self.img = pygame.transform.flip(PLAYER1_IMG, True, False)
        else:
            self.img = PLAYER2_IMG

        window.blit(self.img, (self.x, self.y))

    def get_mask(self):
        surf = self.img.convert_alpha()
        rect = surf.get_rect(topleft=(self.x, self.y))
        mask = pygame.mask.from_surface(surf)

        return mask, rect

class shoe_cls(player_cls):
    IMG = SHOE_IMG
    MAX_ROT = 45
    ROT_VEL = 5

    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.tilt = 0
        self.kick_max = False
        self.speed = 0
        self.shot_power = 1
        self.kick_key_pressed = False
        self.img = self.IMG

    def kick(self):
        if not self.kick_max:
            self.kick_key_pressed = True
            self.shot_power = 5

    def rotate_leg(self, player1):
        if self.kick_max:
            self.shot_power = 1
            if player1:
                self.tilt -= self.ROT_VEL
            else:
                self.tilt += self.ROT_VEL
            if self.tilt == 0:
                self.kick_max = False
        else:
            if self.kick_key_pressed:
                if player1:
                    self.tilt += self.ROT_VEL
                else:
                    self.tilt -= self.ROT_VEL
                if self.tilt == self.MAX_ROT or self.tilt == -self.MAX_ROT:
                    self.kick_max = True
                    self.kick_key_pressed = False

    def draw(self, window, player_num):
        if player_num == "1":
            self.img = SHOE_IMG
        else:
            self.img = pygame.transform.flip(SHOE_IMG, True, False)

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            bottomleft=self.img.get_rect(midtop=(self.x, self.y + SHOE_IMG.get_height() / 2)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        surf = self.img.convert_alpha()
        rotated_surf = pygame.transform.rotate(surf, self.tilt)
        rect = rotated_surf.get_rect(
            bottomleft=self.img.get_rect(midtop=(self.x, self.y + SHOE_IMG.get_height() / 2)).center)
        mask = pygame.mask.from_surface(rotated_surf)

        return mask, rect

class ball_cls:
    IMG = BALL_IMG

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.x_speed = 0
        self.y_speed = 0
        self.y_ground = WIN_HEIGHT - BALL_IMG.get_height()
        self.post_ground = WIN_HEIGHT - GOALPOSTS_IMG.get_height() - BALL_IMG.get_height()
        self.gforce = 0.1
        self.tick_count = 0
        self.tilt = 0
        self.starting_point = (WIN_WIDTH / 2, WIN_HEIGHT / 2)
        self.object_surf = self.IMG.convert_alpha()
        self.img = self.IMG

    def move(self):
        if self.y < WIN_HEIGHT:
            self.tick_count += 1

            self.y_speed = self.y_speed - self.gforce * self.tick_count

            d = self.y_speed * self.tick_count - self.gforce * self.tick_count ** 2

            if self.y - d <= WIN_HEIGHT - GOALPOSTS_IMG.get_height() and (
                    self.x + BALL_IMG.get_width() < GOALPOST_WIDTH + 10
                    or self.x + BALL_IMG.get_width() > WIN_WIDTH - GOALPOST_WIDTH + 10):
                self.tick_count = 0
                self.y = self.post_ground - 2
                self.y_speed *= -1
                self.x_speed += 1

            if self.y - d <= self.y_ground:
                self.y -= d
            else:
                self.tick_count = 0
                self.y = self.y_ground
                self.y_speed *= -1

        self.x += self.x_speed

        if self.x_speed > 0:
            self.x_speed -= 0.1
            self.tilt -= 10
            if self.x_speed < 0:
                self.x_speed = 0
        elif self.x_speed < 0:
            self.x_speed += 0.1
            self.tilt += 10
            if self.x_speed > 0:
                self.x_speed = 0

    def out_of_bounds(self):
        # IF touch ceiling
        if self.y <= 0:
            self.y_speed /= 2

        # IF completly out of bounds
        if self.x + self.img.get_width() < 0:
            self.x = WIN_WIDTH/2
        if self.x > WIN_WIDTH:
            self.x = WIN_WIDTH/2

        # IF touch out of bounds
        if self.x <= 0:
            self.x_speed *= -1
        elif self.x + self.img.get_width() >= WIN_WIDTH:
            self.x_speed *= -1

    def draw(self, window):
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        surf = self.img.convert_alpha()
        mask = pygame.mask.from_surface(surf)

        return mask

class goal_posts_cls:
    IMG = GOALPOSTS_IMG

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = self.IMG

    def draw(self, window, side):
        if side == "left":
            self.img = GOALPOSTS_IMG
        else:
            self.img = pygame.transform.flip(GOALPOSTS_IMG, True, False)
            self.x = WIN_WIDTH - self.img.get_width()

        window.blit(self.img, (self.x, self.y))

    def get_mask(self):
        surf = self.img.convert_alpha()
        rect = surf.get_rect(topleft=(self.x, self.y))
        mask = pygame.mask.from_surface(surf)

        return mask, rect

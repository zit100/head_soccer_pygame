import pygame, os, time, math
from game_rectangles import player_cls, shoe_cls, ball_cls, goal_posts_cls

pygame.font.init()

STAT_FONT = pygame.font.SysFont("comicsans", 30)

GOAL_DECLARATION_FONT = pygame.font.SysFont("david", 200)
GOAL_DECLARATION = GOAL_DECLARATION_FONT.render("GOAAAAL!!!", 1, (0, 0, 255))

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

global h_score, a_scored
h_score = 0
a_score = 0

# Game functions
def get_offset(ball, object_rect):
    offset_x = ball.x - object_rect.left
    offset_y = ball.y - object_rect.top

    return (offset_x, offset_y)

def draw_window(window, player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post, time_left):
    global h_score, a_score
    window.blit(BG_IMG, (0, 0))

    player_num = "1"
    shoe_cls.draw(shoe1, window, player_num)
    player1.draw(window, player_num)
    player_num = "2"
    shoe_cls.draw(shoe2, window, player_num)
    player2.draw(window, player_num)

    ball.draw(window)

    l_goal_post.draw(window, "left")
    r_goal_post.draw(window, "right")

    time_text = STAT_FONT.render("Time: " + str(time_left), 1, (255, 255, 255))
    window.blit(time_text, (WIN_WIDTH / 2 - time_text.get_width() / 2, 10))
    home_score = STAT_FONT.render("Home: " + str(h_score), 1, (255, 255, 255))
    window.blit(home_score, (GOALPOST_WIDTH, 25))
    away_score = STAT_FONT.render("Away: " + str(a_score), 1, (255, 255, 255))
    window.blit(away_score, (WIN_WIDTH - GOALPOST_WIDTH - away_score.get_width(), 25))

    pygame.display.update()

def create_environment():
    player1 = player_cls(WIN_WIDTH / 2 - 200 - SHOE_IMG.get_width(),
                         WIN_HEIGHT - SHOE_IMG.get_height() / 2 - PLAYER1_IMG.get_height())
    player2 = player_cls(WIN_WIDTH / 2 + 200,
                         WIN_HEIGHT - SHOE_IMG.get_height() / 2 - PLAYER2_IMG.get_height())
    shoe1 = shoe_cls(WIN_WIDTH / 2 - 200 + PLAYER1_IMG.get_width() / 3 - SHOE_IMG.get_width(),
                 WIN_HEIGHT - SHOE_IMG.get_height())
    shoe2 = shoe_cls(WIN_WIDTH / 2 + 200 - PLAYER2_IMG.get_width() / 3,
                 WIN_HEIGHT - SHOE_IMG.get_height())
    ball = ball_cls(WIN_WIDTH / 2 - BALL_IMG.get_width() / 2,
                    WIN_HEIGHT / 2 - BALL_IMG.get_height())
    l_goal_post = goal_posts_cls(0,
                                 WIN_HEIGHT - GOALPOSTS_IMG.get_height())
    r_goal_post = goal_posts_cls(WIN_WIDTH - GOALPOST_WIDTH,
                                 WIN_HEIGHT - GOALPOSTS_IMG.get_height())

    return player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post

def check_goal(window, player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post):
    global h_score, a_score

    l_goal_post_mask, l_goal_post_rect = l_goal_post.get_mask()
    r_goal_post_mask, r_goal_post_rect = r_goal_post.get_mask()
    ball_mask = ball.get_mask()

    l_goal_post_offset = get_offset(ball, l_goal_post_rect)
    r_goal_post_offset = get_offset(ball, r_goal_post_rect)

    if l_goal_post_mask.overlap(ball_mask, l_goal_post_offset) \
            or r_goal_post_mask.overlap(ball_mask, r_goal_post_offset):
        if not ball.y <= WIN_HEIGHT - GOALPOSTS_IMG.get_height() + 50:
            if ball.x + BALL_IMG.get_width() < GOALPOST_WIDTH:
                a_score += 1
                window.blit(GOAL_DECLARATION, (WIN_WIDTH / 2 - GOAL_DECLARATION.get_width()/2, WIN_HEIGHT / 4))
                pygame.display.update()
                pygame.time.wait(1000)

                goal('away', player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post)
            elif ball.x > WIN_WIDTH - GOALPOST_WIDTH:
                h_score += 1
                window.blit(GOAL_DECLARATION, (WIN_WIDTH / 2 - GOAL_DECLARATION.get_width()/2, WIN_HEIGHT / 4))
                pygame.display.update()
                pygame.time.wait(1000)

                goal('home', player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post)

def goal(side, player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post):
    player1.__init__(WIN_WIDTH / 2 - 200 - SHOE_IMG.get_width(),
                     WIN_HEIGHT - SHOE_IMG.get_height() / 2 - PLAYER1_IMG.get_height())
    player2.__init__(WIN_WIDTH / 2 + 200,
                     WIN_HEIGHT - SHOE_IMG.get_height() / 2 - PLAYER2_IMG.get_height())
    shoe1.__init__(WIN_WIDTH / 2 - 200 + PLAYER1_IMG.get_width() / 3 - SHOE_IMG.get_width(),
                   WIN_HEIGHT - SHOE_IMG.get_height())
    shoe2.__init__(WIN_WIDTH / 2 + 200 - PLAYER2_IMG.get_width() / 3,
                   WIN_HEIGHT - SHOE_IMG.get_height())
    ball.__init__(WIN_WIDTH / 2 - BALL_IMG.get_width() / 2,
                  WIN_HEIGHT / 2 - BALL_IMG.get_height())

def ball_collision(ball_mask, object_mask, object_offset, ball, object, is_shoe=False):
    # Find ball center point
    ball_center = (round(ball.x + BALL_IMG.get_width() / 2), round(ball.y + BALL_IMG.get_height() / 2))

    # Find the collosion point
    touch_point = object_mask.overlap(ball_mask, object_offset)
    touch_point = (round(object.x + touch_point[0]), round(object.y + touch_point[1]))

    # Compute the angle the collosion make
    ball_triangle_x = touch_point[0] - ball_center[0]
    ball_triangle_y = touch_point[1] - ball_center[1]

    # Can divide by zero??
    if ball_triangle_x != 0:
        ball_triangle_angle = math.atan(ball_triangle_y / ball_triangle_x)

        # v0 + v1 = u0 + u1, u1 = 0
        if is_shoe:
            ball.x_speed = ball.x_speed + object.x_speed*object.shot_power * math.cos(ball_triangle_angle)
            ball.y_speed = ball.y_speed - object.y_speed*object.shot_power - object.x_speed*object.shot_power * math.sin(ball_triangle_angle)
        else:
            ball.x_speed = ball.x_speed + object.x_speed * math.cos(ball_triangle_angle)
            ball.y_speed = ball.y_speed - object.y_speed - object.x_speed * math.sin(ball_triangle_angle)
        ball.tilt += 20

def end_game(window):
    global h_score, a_score

    if h_score > a_score:
        winner = STAT_FONT.render("Winner is " + "Player1", 1, (255, 255, 255))
        window.blit(winner, (WIN_WIDTH/2 - winner.get_width(), WIN_HEIGHT/2))
    elif a_score > h_score:
        winner = STAT_FONT.render("Winner is " + "Player2", 1, (255, 255, 255))
        window.blit(winner, (WIN_WIDTH / 2 , WIN_HEIGHT / 2))

    pygame.display.update()
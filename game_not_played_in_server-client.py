import pygame, socket, select, threading
from game_functions import get_offset, draw_window, create_environment, check_goal, ball_collision, end_game


def receive(player1, player2, shoe1, shoe2):
    while True:
        rlist, wlist, xlist = select.select([my_socket], [], [])
        if my_socket in rlist:
            messages = my_socket.recv(MAX_MSG_LENGTH).decode()[:-1].split(',')
            for message in messages:
                if "player1" in message:
                    if message == "player1_right":
                        player1.move_right()
                        shoe1.move_right()
                    elif message == "player1_left":
                        player1.move_left()
                        shoe1.move_left()
                    elif message == "player1_jump":
                        player1.jump()
                        shoe1.jump()
                    elif message == "player1_kick":
                        shoe1.kick()

                if "player2" in message:
                    if message == "player2_right":
                        player2.move_right()
                        shoe2.move_right()
                    elif message == "player2_left":
                        player2.move_left()
                        shoe2.move_left()
                    elif message == "player2_jump":
                        player2.jump()
                        shoe2.jump()
                    elif message == "player2_kick":
                        shoe2.kick()


MAX_MSG_LENGTH = 1024
def network_setup():
    # Network setup
    my_socket = socket.socket()
    my_socket.connect(('#ip address of the host', 5555))
    # Which side is the player playing
    return my_socket, str(my_socket.recv(MAX_MSG_LENGTH).decode())


my_socket, player_number = network_setup()

WIN_WIDTH = 1200
WIN_HEIGHT = 600

# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(player_number + " " + 'Window')


def main(player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post):
    global h_score, a_score

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    time_left = 0

    collide = False

    former_keys = []
    run = True
    while run:
        time_left = pygame.time.get_ticks() // 1000
        if time_left >= 150:
            end_game(window)
            break

        check_goal(window, player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post)

        draw_window(window, player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post, time_left)

        player1_mask, player1_rect = player1.get_mask()
        player2_mask, player2_rect = player2.get_mask()
        shoe1_mask, shoe1_rect = shoe1.get_mask()
        shoe2_mask, shoe2_rect = shoe2.get_mask()
        ball_mask = ball.get_mask()

        player1_offset = get_offset(ball, player1_rect)
        shoe1_offset = get_offset(ball, shoe1_rect)
        player2_offset = get_offset(ball, player2_rect)
        shoe2_offset = get_offset(ball, shoe2_rect)

        if player1_mask.overlap(ball_mask, player1_offset) and not collide:
            collide = True
            ball_collision(ball_mask, player1_mask, player1_offset, ball, player1)
            collide = False

        if player2_mask.overlap(ball_mask, player2_offset) and not collide:
            collide = True
            ball_collision(ball_mask, player2_mask, player2_offset, ball, player2)
            collide = False

        if shoe1_mask.overlap(ball_mask, shoe1_offset) and not collide:
            collide = True
            ball_collision(ball_mask, shoe1_mask, shoe1_offset, ball, shoe1, True)
            collide = False

        if shoe2_mask.overlap(ball_mask, shoe2_offset) and not collide:
            collide = True
            ball_collision(ball_mask, shoe2_mask, shoe2_offset, ball, shoe2, True)
            collide = False

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if keys[pygame.K_d]:
                msg = player_number + "_right,"
                my_socket.send(msg.encode())

            if keys[pygame.K_a]:
                msg = player_number + "_left,"
                my_socket.send(msg.encode())

            if keys[pygame.K_w]:
                msg = player_number + "_jump,"
                my_socket.send(msg.encode())

            if keys[pygame.K_SPACE]:
                msg = player_number + "_kick,"
                my_socket.send(msg.encode())

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                my_socket.send("exit".encode())
                my_socket.close()
                quit()

        ball.move()
        ball.out_of_bounds()

        player1.gravity()
        shoe1.gravity()
        shoe1.rotate_leg(True)

        player2.gravity()
        shoe2.gravity()
        shoe2.rotate_leg(False)

        pygame.display.update()
        clock.tick(60)

    exit = input()


if __name__ == '__main__':
    player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post = create_environment()

    receive_thread = threading.Thread(target=receive, args=(player1, player2, shoe1, shoe2))
    receive_thread.start()

    main(player1, player2, shoe1, shoe2, ball, l_goal_post, r_goal_post)

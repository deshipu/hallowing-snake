import board
import displayio
import time
import touchio
import random


DX = 0, 1, 0, -1
DY = -1, 0, 1, 0


group = displayio.Group(scale=8)
board.DISPLAY.show(group)
screen = displayio.Bitmap(16, 16, 4)
palette = displayio.Palette(4)
palette[0] = 0x111111
palette[1] = 0xaa0099
palette[2] = 0x22aa00
palette[3] = 0xee00bb
group.append(displayio.TileGrid(screen, pixel_shader=palette))
left = touchio.TouchIn(board.A5)
right = touchio.TouchIn(board.A2)


head = 7, 7
facing = 0
size = 3
apple = 8, 4

body = [head]
screen[apple] = 2
tick = time.monotonic()
while True:
    turn_left = False
    turn_right = False
    tick += 0.5
    while True:
        time.sleep(0.05)
        turn_left = turn_left or left.value
        turn_right = turn_right or right.value
        if tick <= time.monotonic():
            break
    if turn_left:
        facing = (facing - 1) % 4
    if turn_right:
        facing = (facing + 1) % 4
    screen[head] = 1
    head = (head[0] + DX[facing]) % 16, (head[1] + DY[facing]) % 16
    if head in body:
        break
    body.append(head)
    screen[head] = 3
    if head == apple:
        size += 1
        apple = random.randint(0, 15), random.randint(0, 15)
        screen[apple] = 2
    if len(body) > size:
        tail = body.pop(0)
        screen[tail] = 0
    board.DISPLAY.refresh_soon()

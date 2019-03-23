import board
import displayio
import time
import touchio
import random


DX = 0, 1, 0, -1
DY = -1, 0, 1, 0


screen = displayio.Group()
board.DISPLAY.show(screen)
image = displayio.Bitmap(8, 32, 4)
for y in range(8):
    for x in range(8):
        image[x, y] = 0
        image[x, y + 8] = 1
        image[x, y + 16] = 2
        image[x, y + 24] = 3
palette = displayio.Palette(4)
palette[0] = 0x111111
palette[1] = 0xaa0099
palette[2] = 0x22aa00
palette[3] = 0xee00bb
grid = displayio.TileGrid(image, pixel_shader=palette, width=16, height=16,
    tile_width=8, tile_height=8, x=0, y=0)
screen.append(grid)
left = touchio.TouchIn(board.A5)
right = touchio.TouchIn(board.A2)


head = 7, 7
facing = 0
size = 3
apple = 8, 4


body = [head]
grid[apple] = 2
tick = time.monotonic()
while True:
    if left.value:
        facing = (facing - 1) % 4
    if right.value:
        facing = (facing + 1) % 4
    grid[head] = 1
    head = (head[0] + DX[facing]) % 16, (head[1] + DY[facing]) % 16
    if head in body:
        break
    body.append(head)
    grid[head] = 3
    if head == apple:
        size += 1
        apple = random.randint(0, 15), random.randint(0, 15)
        grid[apple] = 2
    if len(body) > size:
        tail = body.pop(0)
        grid[tail] = 0
    board.DISPLAY.refresh_soon()
    now = time.monotonic()
    tick += 0.5
    if tick < now:
        tick = now
    else:
        time.sleep(tick - now)

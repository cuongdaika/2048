import pygame
import random
import math
import asyncio # Bắt buộc cho pygbag
import sys
import platform
import datetime
import time

# --- CẤU HÌNH ---
FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 4, 4
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS
OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 193, 180)
FONT_COLOR = (119, 110, 101)


pygame.display.init()
pygame.font.init()
pygame.mixer.quit()


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Web")

# --- LOAD ASSETS ---
# Dictionary ánh xạ giá trị tile với tên file ảnh
ASSETS = {}
VALUES = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]

def load_assets():
    # Load ảnh nền cho ô trống
    try:
        bg_img = pygame.image.load("assets/Tile Background.png")
        ASSETS[0] = pygame.transform.scale(bg_img, (RECT_WIDTH, RECT_HEIGHT))
    except:
        ASSETS[0] = None # Fallback nếu thiếu ảnh
        
    for val in VALUES:
        try:
            # Giả định tên file là "2 Tile.png", "4 Tile.png"...
            img = pygame.image.load(f"assets/{val} Tile.png")
            ASSETS[val] = pygame.transform.scale(img, (RECT_WIDTH, RECT_HEIGHT))
        except:
            print(f"Warning: Missing image for {val}")
            ASSETS[val] = None # Sẽ vẽ màu thay thế

load_assets()

# Font fallback nếu không load được ảnh
pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20

class Tile:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def draw(self, window):
        # Vẽ ảnh nếu có
        if self.value in ASSETS and ASSETS[self.value]:
            window.blit(ASSETS[self.value], (self.x, self.y))
        else:
            # Fallback vẽ hình chữ nhật màu
            pygame.draw.rect(window, (238, 228, 218), (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))
            text = FONT.render(str(self.value), 1, FONT_COLOR)
            window.blit(
                text,
                (
                    self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                    self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
                ),
            )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

def draw_grid(window):
    # Vẽ lưới
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)
    
    # Vẽ các ô trống nền trước
    if ASSETS[0]:
        for r in range(ROWS):
            for c in range(COLS):
                window.blit(ASSETS[0], (c * RECT_WIDTH, r * RECT_HEIGHT))

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)
    pygame.display.update()

def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)
        if f"{row}{col}" not in tiles:
            break
    return row, col

def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)

def end_move(tiles):
    if len(tiles) == 16:
        return "lost"
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile
    draw(window, tiles)

def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)
    return tiles

# --- GIAO TIẾP VỚI JAVASCRIPT ---
def send_score_to_web(score, start_time, end_time):
    # Chỉ chạy khi ở môi trường Web (Emscripten)
    if sys.platform == "emscripten":
        from platform import window
        
        # Định dạng thời gian ISO
        s_time_iso = datetime.datetime.fromtimestamp(start_time).isoformat()
        e_time_iso = datetime.datetime.fromtimestamp(end_time).isoformat()
        duration = end_time - start_time
        
        # Gọi hàm JS được định nghĩa ở parent window (vì game chạy trong iframe)
        # window.parent truy cập vào frame cha chứa iframe này
        try:
            window.parent.handleGameover(score, s_time_iso, e_time_iso, duration)
        except Exception as e:
            print(f"Error calling JS: {e}")
    else:
        print(f"Game Over! Score: {score}")

async def main():
    clock = pygame.time.Clock()
    run = True
    tiles = generate_tiles()
    
    # Lưu thời gian bắt đầu
    start_timestamp = time.time()
    current_score = 0

    while run:
        clock.tick(FPS)
        
        # Cập nhật điểm (max tile value)
        if tiles:
            current_score = sum(t.value for t in tiles.values())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                status = "continue"
                if event.key == pygame.K_LEFT:
                    status = move_tiles(WINDOW, tiles, clock, "left")
                elif event.key == pygame.K_RIGHT:
                    status = move_tiles(WINDOW, tiles, clock, "right")
                elif event.key == pygame.K_UP:
                    status = move_tiles(WINDOW, tiles, clock, "up")
                elif event.key == pygame.K_DOWN:
                    status = move_tiles(WINDOW, tiles, clock, "down")
                
                if status == "lost":
                    print("Game Over")
                    end_timestamp = time.time()
                    send_score_to_web(current_score, start_timestamp, end_timestamp)
                    # Reset game sau khi thua
                    await asyncio.sleep(2) # Đợi 2 giây
                    tiles = generate_tiles()
                    start_timestamp = time.time()

        draw(WINDOW, tiles)
        # QUAN TRỌNG: Yield control cho browser
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
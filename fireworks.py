import curses
import random
import time
import threading

lock = threading.Lock()  # Khóa để đồng bộ luồng

def draw_firework(stdscr, x, y):
    colors = [curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_YELLOW, curses.COLOR_BLUE, curses.COLOR_MAGENTA]
    symbols = ['*', '+', 'o', 'x', '•']
    for i in range(8):  # Tăng kích thước pháo hoa
        for color in colors:
            curses.init_pair(1, color, curses.COLOR_BLACK)
            with lock:  # Đảm bảo chỉ một luồng ghi lên màn hình tại một thời điểm
                for dx in range(-i, i + 1):
                    for dy in range(-i, i + 1):
                        if dx * dx + dy * dy <= i * i:  # Vẽ hình tròn
                            if 0 <= x + dx < curses.COLS - 1 and 0 <= y + dy < curses.LINES - 1:
                                stdscr.addstr(y + dy, x + dx, random.choice(symbols), curses.color_pair(1))
                stdscr.refresh()
            time.sleep(0.02)

def fade_firework(stdscr, x, y):
    for step in range(3):
        with lock:
            for dx in range(-8, 9):
                for dy in range(-8, 9):
                    if 0 <= x + dx < curses.COLS - 1 and 0 <= y + dy < curses.LINES - 1:
                        stdscr.addstr(y + dy, x + dx, ' ')
            stdscr.refresh()
        time.sleep(0.03)

def launch_firework(stdscr, x, y):
    for i in range(y, max(y - 6, 1), -1):
        with lock:
            stdscr.addstr(i, x, '|')
            stdscr.refresh()
        time.sleep(0.02)
        with lock:
            stdscr.addstr(i, x, ' ')

def firework_thread(stdscr, height, width):
    try:
        x = random.randint(2, max(3, width - 3))
        y = random.randint(height // 3, max(height // 3 + 2, height - 3))
        launch_firework(stdscr, x, y)
        draw_firework(stdscr, x, y - 6)
        fade_firework(stdscr, x, y - 6)
    except curses.error:
        pass

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    stdscr.nodelay(1)

    height, width = stdscr.getmaxyx()

    while True:
        try:
            num_fireworks = random.randint(1, 4)  # Số pháo hoa ngẫu nhiên từ 1 đến 4
            threads = []
            for _ in range(num_fireworks):
                t = threading.Thread(target=firework_thread, args=(stdscr, height, width), daemon=True)
                t.start()
                threads.append(t)
            
            time.sleep(random.uniform(0.5, 1.5))  # Thời gian ngẫu nhiên giữa các đợt bắn
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    curses.wrapper(main)
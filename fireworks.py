import curses
import random
import time
import threading
import math

lock = threading.Lock()

def draw_pixel(stdscr, x, y, symbol, color_pair):
    height, width = stdscr.getmaxyx()
    if 0 <= x < width and 0 <= y < height:
        try:
            stdscr.addstr(y, x, symbol, color_pair)
        except curses.error:
            pass

def draw_firework(stdscr, x, y):
    colors = [curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_YELLOW, 
              curses.COLOR_BLUE, curses.COLOR_MAGENTA, curses.COLOR_CYAN]
    symbols = ['*', '+', 'o', 'x', '•']
    max_radius = random.randint(6, 12)  
    shape = random.choice(['circle', 'star'])  

    for i in range(max_radius):
        curses.init_pair(1, random.choice(colors), curses.COLOR_BLACK)
        with lock:
            for dx in range(-i, i+1):
                for dy in range(-i, i+1):
                    if shape == 'circle' and dx*dx + dy*dy <= i*i:
                        draw_pixel(stdscr, x+dx, y+dy, random.choice(symbols), curses.color_pair(1))
                    elif shape == 'star' and abs(dx) + abs(dy) <= i:
                        draw_pixel(stdscr, x+dx, y+dy, random.choice(symbols), curses.color_pair(1))
            stdscr.refresh()
        time.sleep(0.04)  

    time.sleep(0.5)

def fade_firework(stdscr, x, y):
    fade_steps = random.randint(6, 10)
    for step in range(fade_steps):
        with lock:
            for dx in range(-12, 13):
                for dy in range(-12, 13):
                    if random.random() < 0.5:
                        draw_pixel(stdscr, x+dx, y+dy, ' ', curses.color_pair(0))
            stdscr.refresh()
        time.sleep(0.05)

def launch_firework(stdscr, start_x, start_y, target_y):
    curve = random.choice(['straight', 'left', 'right', 'sin'])
    x = start_x
    for y in range(start_y, target_y, -1):
        with lock:
            draw_pixel(stdscr, x, y, '|', curses.color_pair(0))
            stdscr.refresh()
        time.sleep(0.02)
        with lock:
            draw_pixel(stdscr, x, y, ' ', curses.color_pair(0))
        
        if curve == 'left' and x > 1:
            x -= 1
        elif curve == 'right' and x < curses.COLS - 2:
            x += 1
        elif curve == 'sin':
            x += int(math.sin(y/2) * 1.5)

def firework_thread(stdscr):
    try:
        height, width = stdscr.getmaxyx()
        start_x = random.randint(1, width-2)
        start_y = height - 1
        target_y = random.randint(height//4, 3*height//4)
        explosion_x = start_x + random.randint(-3, 3)
        explosion_y = target_y + random.randint(-2, 2)
        
        launch_firework(stdscr, start_x, start_y, target_y)
        draw_firework(stdscr, explosion_x, explosion_y)
        fade_firework(stdscr, explosion_x, explosion_y)
    except:
        pass

def main(stdscr):
    curses.curs_set(0)
    if curses.has_colors():
        curses.start_color()
    else:
        stdscr.addstr(0, 0, "Terminal không hỗ trợ màu sắc!")
        stdscr.refresh()
        stdscr.getch()
        return
    
    height, width = stdscr.getmaxyx()
    if width < 40 or height < 20:
        stdscr.addstr(0, 0, "Terminal quá nhỏ! Vui lòng mở rộng terminal.")
        stdscr.refresh()
        stdscr.getch()
        return
    
    stdscr.nodelay(1)
    stdscr.timeout(50)  
    active_threads = []

    while True:
        max_threads = 10  
        active_threads = [t for t in active_threads if t.is_alive()]
        
        if len(active_threads) < max_threads:
            num = random.randint(1, 3)  
            for _ in range(num):
                t = threading.Thread(target=firework_thread, args=(stdscr,), daemon=True)
                t.start()
                active_threads.append(t)
        
        sleep_time = random.uniform(0.8, 1.5)  
        time.sleep(sleep_time)
        
        if stdscr.getch() == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)
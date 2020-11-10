from pynput import keyboard
from pynput.mouse import Button, Controller
import time
import threading

def test():
    # 创建控制器
    mouse = Controller()

    # 读取指针位置
    print('当前指针位置 {0}'.format(mouse.position))

    # 设置指针位置
    mouse.position = (10, 20)
    print('现在已经移到 {0}'.format(mouse.position))

    # 相对移动
    mouse.move(5, -5)

    # 按下和释放
    mouse.press(Button.left)
    mouse.release(Button.left)

    # 双击
    mouse.click(Button.left, 2)

    # 往下滚动2步
    mouse.scroll(0, 2)


START = False


def run():
    mouse = Controller()
    while START:
        mouse.press(Button.left)
        mouse.release(Button.left)
        # mouse.click(Button.left, 2)
        time.sleep(0.2)


def on_release(key):
    global START
    try:
        if key.char == 'g':
            START = True
            t = threading.Thread(target=run)
            t.setDaemon(True)
            t.start()
    except Exception:
        pass
    if key == keyboard.Key.esc:
        START = False
        return False


listener = keyboard.Listener(on_release=on_release)
listener.start()
listener.join()
print('Done')

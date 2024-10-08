import ctypes
import psutil
import time

# 定义电源设置的常量
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001


def is_script_running(script_name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'python.exe' and script_name in ' '.join(proc.info['cmdline']):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def prevent_sleep():
    """防止系统进入休眠状态"""
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)


def allow_sleep():
    """允许系统进入休眠状态"""
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)


if __name__ == '__main__':
    # 防止系统休眠
    prevent_sleep()

    # 你的代码逻辑
    # ...

    script_name = 'train_loop.py'
    while is_script_running(script_name):
        print(f"{script_name} is running.")
        time.sleep(10)

    print(f"{script_name} is not running.")

    # 允许系统休眠（可选）
    allow_sleep()

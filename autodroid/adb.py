from subprocess import check_output, run
import os
import shutil
from typing import Union
import re
from functional import seq

from autodroid.device import Device
from autodroid.size import Size

adb_command = None

_physical_size_leading = "Physical size: "
_override_size_leading = "Override size: "
_physical_density_leading = "Physical density: "
_override_density_leading = "Physical density: "


KEYCODE_HOME = 3
KEYCODE_BACK = 4
KEYCODE_POWER = 26


def init_adb():
    global adb_command
    if shutil.which("adb") is not None:
        adb_command = "adb"
    else:
        android_home = os.environ.get("ANDROID_HOME")
        if android_home is not None:
            adb_command = os.path.join(android_home, "platform-tools", "adb")

    if adb_command is None:
        raise Exception("No adb command found!")


def list_devices() -> list[Device]:
    raw_output = check_output(make_command(["devices"]))
    raw_output = str(raw_output, encoding='utf-8')
    lines = raw_output.splitlines()
    return seq(lines)\
        .map(lambda line: line.split("\t"))\
        .filter(lambda it: len(it) == 2)\
        .map(lambda it: it[0])\
        .map(lambda id: Device(id))\
        .to_list()


def make_command(real_cmd: list[str], device: Device = None) -> str:
    if device == None:
        return [adb_command] + real_cmd
    else:
        return [adb_command] + ["-s", device.id] + real_cmd


def run_command(real_cmd: str, device: Device = None):
    run(make_command(real_cmd, device))


def cap_screen_pic(device: Device = None, use_png=True, timeout=None):
    png_flag = ["-p"] if(use_png) else []
    return check_output(make_command(["exec-out", "screencap"] + png_flag, device), timeout=timeout)


def click_point(x: Union[int, float], y: Union[int, float], device: Device = None):
    x = int(x)
    y = int(y)
    run_command(["shell", "input", "tap", str(x), str(y)], device)


def swipe(x1, y1, x2, y2, duration=None, device=None):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    duration = [] if(duration == None) else [str(int(duration*1000))]
    run_command(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2)] + duration, device)


def start_activity(activity: str, device: Device = None):
    """
    activity: package name + activity name, like: com.tencent.mm/com.tencent.mm.ui.LauncherUI
    """
    run_command(["shell", "am", "start", "-n", activity], device)


def launch_app(package_name: str, device: Device = None):
    """
    This command simulates the app icon click,
    so the intent implicit intent LAUNCHER is delivered to the specific receiver declared in app manifest
    """
    run_command(["shell", "monky", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"], device)


def get_screen_size(in_dp=False, device: Device = None) -> Size:
    raw_output = check_output(make_command(["shell", "wm", "size"], device))
    raw_output = str(raw_output, encoding='utf-8')
    output_lines = raw_output.splitlines()
    output_lines = sorted(output_lines)
    sizes = output_lines[0].split(":")[1].strip().split("x")
    sizes = Size(int(sizes[0]), int(sizes[1]))
    if not in_dp:
        return sizes
    else:
        density = get_density()
        width_dp = 480 / density * 360
        height_dp = sizes[1] / sizes[0] * width_dp
        return Size(round(width_dp), round(height_dp))


def get_density(device: Device = None) -> int:
    raw_output = check_output(make_command(["shell", "wm", "density"], device))
    raw_output = str(raw_output, encoding='utf-8')
    output_lines = raw_output.splitlines()
    output_lines = sorted(output_lines)
    density = output_lines[0].split(":")[1].strip()
    return int(density)


def get_dpi(device: Device = None) -> float:
    size_in_px = get_screen_size(in_dp=False, device=device)
    size_in_dp = get_screen_size(in_dp=True, device=device)
    return size_in_px[0] / size_in_dp[0]


def input_key(key_code: int, device: Device = None):
    run_command(["shell", "input", "keyevent", str(key_code)], device)

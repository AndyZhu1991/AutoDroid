from subprocess import check_output
import os
import shutil

adb_command = None

physical_size_leading = "Physical size: "
override_size_leading = "Override size: "
physical_density_leading = "Physical density: "
override_density_leading = "Physical density: "


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


def cap_screen_pic():
    return check_output(f'{adb_command} exec-out screencap -p')


def click_point(x, y):
    x = int(x)
    y = int(y)
    os.system(f'{adb_command} shell input tap {x} {y}')


def start_activity(activity):
    """
    activity: package name + activity name, like: com.tencent.mm/com.tencent.mm.ui.LauncherUI
    """
    os.system(f'{adb_command} shell am start -n {activity}')


def get_screen_size(in_dp=False):
    raw_output = check_output(f'{adb_command} shell wm size')
    raw_output = str(raw_output, encoding='utf-8')
    output_lines = raw_output.splitlines()
    output_lines = sorted(output_lines)
    sizes = output_lines[0].split(":")[1].strip().split("x")
    sizes = (int(sizes[0]), int(sizes[1]))
    if not in_dp:
        return sizes
    else:
        density = get_density()
        width_dp = 480 / density * 360
        height_dp = sizes[1] / sizes[0] * width_dp
        return (round(width_dp), round(height_dp))


def get_density():
    raw_output = check_output(f'{adb_command} shell wm density')
    raw_output = str(raw_output, encoding='utf-8')
    output_lines = raw_output.splitlines()
    output_lines = sorted(output_lines)
    density = output_lines[0].split(":")[1].strip()
    return int(density)


def get_dpi():
    size_in_px = get_screen_size(in_dp=False)
    size_in_dp = get_screen_size(in_dp=True)
    return size_in_px[0] / size_in_dp[0]

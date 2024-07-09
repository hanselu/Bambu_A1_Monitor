import traceback
import ctypes

from typing import Optional

import win32gui
import win32api
import win32con


def find_window_by_title_and_class(title: str, class_name=None):
    """
    根据标题和类名查找窗口句柄
    :param title: 窗口标题
    :param class_name: 窗口类名，留空则忽略匹配标题
    :return:
    """
    handle = win32gui.FindWindow(class_name, title)
    return handle


def enum_child_windows(parent_handle: int, title=None, class_name=None):
    """
    枚举所有子窗口句柄
    :param parent_handle: 父窗口句柄
    :param title: 子窗口标题，留空则忽略匹配标题
    :param class_name: 子窗口类名，留空则忽略匹配标题
    :return:
    """
    child_handles = []

    def enum_child_window_callback(child_hwnd, lParam):
        child_title = win32gui.GetWindowText(child_hwnd)
        child_class_name = win32gui.GetClassName(child_hwnd)
        if (title is None or child_title == title) and (
            class_name is None or child_class_name == class_name
        ):
            child_handles.append(child_hwnd)
        return True

    win32gui.EnumChildWindows(parent_handle, enum_child_window_callback, None)

    return child_handles


def enum_son_windows(hwnd):
    sons = []

    def callback(child_hwnd, _):
        parent_hwnd = win32gui.GetParent(child_hwnd)
        if parent_hwnd == hwnd:
            sons.append(child_hwnd)

    win32gui.EnumChildWindows(hwnd, callback, None)
    return sons


def find_top_level_windows(class_name):
    windows = []

    def callback(hwnd, _):
        if win32gui.GetClassName(hwnd) == class_name and win32gui.GetParent(hwnd) == 0:
            windows.append(hwnd)
        return True

    win32gui.EnumWindows(callback, None)
    return windows


def get_window_text(hwnd: int) -> str:
    """
    获取窗口文本
    :param hwnd: 窗口句柄
    :return:
    """
    return win32gui.GetWindowText(hwnd)


def get_window_class_name(hwnd: int) -> str:
    """
    获取窗口类名
    :param hwnd: 窗口句柄
    :return:
    """
    return win32gui.GetClassName(hwnd)


def get_window_rect(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top
    return (left, top, width, height)


def get_mainwindow_hwnd() -> int:
    try:
        mainwindow_hwnd_list = find_top_level_windows("wxWindowNR")
        if mainwindow_hwnd_list:
            return mainwindow_hwnd_list[0]
        else:
            print("没找到Bambu Studio")
            return 0
    except Exception as e:
        print("查找Bambu Studio出错")
        print(e)
        traceback.print_exc()
        return 0


def show_window_info(_hwnd: int):
    window_text = get_window_text(_hwnd)
    window_class_name = get_window_class_name(_hwnd)
    parent_hwnd = win32gui.GetParent(_hwnd)
    left, top, width, height = get_window_rect(_hwnd)

    print("-" * 50)
    print("句柄:", _hwnd)
    print("标题:", window_text)
    print("类名:", window_class_name)
    print("父句柄:", parent_hwnd)
    print(f"尺寸: {width} x {height}")
    print(f"左上角: ({left}, {top})")


def get_hwnd_info():
    try:
        main_hwnd = get_mainwindow_hwnd()
        if main_hwnd == 0:
            return None

        # 定位 “打印选项” 按钮
        print_option_btn_hwnd_list = enum_child_windows(
            main_hwnd, "打印选项", "wxWindowNR"
        )
        if len(print_option_btn_hwnd_list) != 1:
            print("无法定位打印选项按钮")
            return None
        print_option_btn_hwnd = print_option_btn_hwnd_list[0]

        # 定位右侧容器
        right_container_hwnd = win32gui.GetParent(
            win32gui.GetParent(print_option_btn_hwnd)
        )
        son_hwnd_list = enum_son_windows(right_container_hwnd)
        # 子窗口按位置由上至下排序 定位控制面板
        son_hwnd_list.sort(key=lambda h: win32gui.GetWindowRect(h)[1])
        control_panel_hwnd = son_hwnd_list[1]

        # 定位3个温度面板
        temperature_panel_list = []
        for son_hwnd in enum_son_windows(control_panel_hwnd):
            grandchild_list = enum_son_windows(son_hwnd)
            if len(grandchild_list) == 1:
                if get_window_class_name(grandchild_list[0]) == "Edit":
                    temperature_panel_list.append(son_hwnd)

        # 子窗口按位置由上至下排序
        temperature_panel_list.sort(key=lambda h: win32gui.GetWindowRect(h)[1])
        hwnd_info = {
            "hotend": temperature_panel_list[0],
            "hotbed": temperature_panel_list[1],
            "box": temperature_panel_list[2],
        }

        # 定位底部容器句柄
        brother_hwnd_list = []
        for son_hwnd in enum_son_windows(win32gui.GetParent(right_container_hwnd)):
            grandchild_list = enum_son_windows(son_hwnd)
            if len(grandchild_list) > 10 and son_hwnd != right_container_hwnd:
                brother_hwnd_list.append(son_hwnd)
        brother_hwnd_list.sort(key=lambda h: win32gui.GetWindowRect(h)[3], reverse=True)
        bottom_container_hwnd = brother_hwnd_list[0]

        # 定位任务名、需求容器
        son_container_list = []
        for son_hwnd in enum_son_windows(bottom_container_hwnd):
            grandchild_list = enum_son_windows(son_hwnd)
            if (
                get_window_class_name(son_hwnd) == "wxWindowNR"
                and len(grandchild_list) == 5
            ):
                static_lable_count = 0
                for grandchild_hwnd in grandchild_list:
                    if get_window_class_name(grandchild_hwnd) == "Static":
                        static_lable_count += 1

                if static_lable_count == 5:
                    son_container_list.append(son_hwnd)

        task_container_hwnd = son_container_list[0]

        # 定位任务名、需求标签
        static_lable_hwnd_list = enum_son_windows(task_container_hwnd)
        static_lable_hwnd_list.sort(key=lambda h: win32gui.GetWindowRect(h)[0])
        hwnd_info["task"] = static_lable_hwnd_list[0]
        hwnd_info["total_time"] = static_lable_hwnd_list[2]
        hwnd_info["mass"] = static_lable_hwnd_list[4]

        # 定位进度容器
        progress_container_hwnd = 0
        for son_hwnd in enum_son_windows(bottom_container_hwnd):
            grandchild_list = enum_son_windows(son_hwnd)
            if len(grandchild_list) == 2:
                grandchild_class_name_0 = get_window_class_name(grandchild_list[0])
                grandchild_class_name_1 = get_window_class_name(grandchild_list[1])
                if (
                    grandchild_class_name_0 == "wxWindowNR"
                    and grandchild_class_name_1 == "wxWindowNR"
                ):
                    progress_container_hwnd = son_hwnd
                    break

        if progress_container_hwnd == 0:
            print("无法定位进度容器")
            return None

        get_progress_info_flag = False
        for son_hwnd in enum_son_windows(progress_container_hwnd):
            grandchild_list = enum_son_windows(son_hwnd)
            if len(grandchild_list) == 4:
                get_progress_info_flag = True
                grandchild_list.sort(key=lambda h: win32gui.GetWindowRect(h)[0])
                # 定位进度信息
                hwnd_info["percent"] = grandchild_list[0]
                hwnd_info["layer"] = grandchild_list[2]
                hwnd_info["remaining_time"] = grandchild_list[3]
                break

        if not get_progress_info_flag:
            print("无法定位进度信息")
            return None

        return hwnd_info

    except Exception as e:
        print("获取句柄信息失败")
        traceback.print_exc()
        print(e)
        return None


def get_machine_info() -> dict:
    try:
        # task_hwnd = 74922
        # mass_hwnd = 74930
        # total_time_hwnd = 74926
        # remaining_time_hwnd = 74952
        # layer_hwnd = 74956
        # percent_hwnd = 74948
        # hotend_hwnd = 75006
        # hotbed_hwnd = 75012
        # box_hwnd = 75018

        hwnd_info = get_hwnd_info()
        if hwnd_info is None:
            return None

        task_hwnd = hwnd_info.get("task", 0)
        mass_hwnd = hwnd_info.get("mass", 0)
        total_time_hwnd = hwnd_info.get("total_time", 0)
        remaining_time_hwnd = hwnd_info.get("remaining_time", 0)
        layer_hwnd = hwnd_info.get("layer", 0)
        percent_hwnd = hwnd_info.get("percent", 0)
        hotend_hwnd = hwnd_info.get("hotend", 0)
        hotbed_hwnd = hwnd_info.get("hotbed", 0)
        box_hwnd = hwnd_info.get("box", 0)

        task = get_window_text(task_hwnd)
        mass = get_window_text(mass_hwnd)
        total_time = get_window_text(total_time_hwnd)
        layer = get_window_text(layer_hwnd).replace("层： ", "")
        percent = get_window_text(percent_hwnd)
        remaining_time = get_window_text(remaining_time_hwnd)
        if remaining_time[0] == "-":
            remaining_time = remaining_time[1:]

        hotend_temperature = get_window_text(hotend_hwnd)
        hotbed_temperature = get_window_text(hotbed_hwnd)
        box_temperature = get_window_text(box_hwnd)
        if box_temperature == "_":
            box_temperature = None

        machine_info = {
            "task": task,
            "mass": mass,
            "layer": layer,
            "total_time": total_time,
            "remaining_time": remaining_time,
            "percent": percent,
            "hotend": hotend_temperature,
            "hotbed": hotbed_temperature,
            "box": box_temperature,
        }

        return machine_info
    except Exception as e:
        print("读取机器信息失败")
        traceback.print_exc()
        print(e)
        return None


def show_project_info():
    hotend_hwnd = 75006
    hotbed_hwnd = 75012

    hotend_temperature = get_window_text(hotend_hwnd)
    hotbed_temperature = get_window_text(hotbed_hwnd)

    print(f"喷头温度: {hotend_temperature}")
    print(f"热床温度: {hotbed_temperature}")


if __name__ == "__main__":
    # a = get_hwnd_info()
    # print(a)
    # print(get_machine_info())

    show_window_info(791754)

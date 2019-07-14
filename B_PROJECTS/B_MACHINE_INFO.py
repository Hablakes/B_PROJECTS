import os
import platform
import socket
import sys

import psutil
import requests


cpu_core_count = os.cpu_count()
external_ip = requests.get('https://api.ipify.org').text
filesystem_encoding = sys.getfilesystemencoding()
local_ip = socket.gethostbyname(socket.gethostname())
node_name = platform.node()
os_release = platform.release()
ram = psutil.virtual_memory()
sys_arc = platform.machine()
system_platform = platform.system()

div = ("-" * 100)


def display_stats():
    print()
    print(div)
    print("OS RELEASE:", os_release)
    print(div)
    print("SYSTEM PLATFORM:", system_platform)
    print(div)
    print("SYSTEM ARCHITECTURE:", sys_arc)
    print(div)
    print("NODE NAME:", node_name)
    print(div)
    print("CPU COUNT:", cpu_core_count)
    print(div)
    print("FILE SYSTEM ENCODING:", filesystem_encoding)
    print(div)
    print("RAM TOTAL:", int(ram.total / 1048576), "MB")
    print(div)
    print("LOCAL IP ADDRESS:", local_ip)
    print(div)
    print("EXTERNAL IP ADDRESS:", external_ip)
    print(div)
    print()


while True:
    display_stats()
    break

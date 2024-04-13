#
# Copyright (c) 2021, 2022 Astroncia
# Copyright (c) 2023, 2024 Ame-chan-angel <amechanangel@proton.me>
#
# This file is part of yuki-iptv.
#
# yuki-iptv is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# yuki-iptv is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with yuki-iptv. If not, see <https://www.gnu.org/licenses/>.
#
# The Font Awesome pictograms are licensed under the CC BY 4.0 License.
# Font Awesome Free 5.15.4 by @fontawesome - https://fontawesome.com
# License - https://creativecommons.org/licenses/by/4.0/
#
import time


def get_current_time():
    return time.strftime("%d.%m.%y %H:%M", time.localtime())


def format_bytes(bytes1, hbnames):
    idx = 0
    while bytes1 >= 1024 and idx + 1 < len(hbnames):
        bytes1 = bytes1 / 1024
        idx += 1
    return f"{bytes1:.1f} {hbnames[idx]}"


def format_seconds(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


def convert_size(size_bytes):
    return format_bytes(
        size_bytes, ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    )

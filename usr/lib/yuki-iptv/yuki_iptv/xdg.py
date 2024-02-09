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
import os
import os.path
from pathlib import Path


def get_cache_dir():
    if "XDG_CACHE_HOME" in os.environ:
        cache_dir = os.environ["XDG_CACHE_HOME"]
    else:
        cache_dir = str(Path(os.environ["HOME"], ".cache"))
    if not os.path.isdir(cache_dir):
        try:
            Path(cache_dir).mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
    return cache_dir


def get_config_dir():
    if "XDG_CONFIG_HOME" in os.environ:
        config_dir = os.environ["XDG_CONFIG_HOME"]
    else:
        config_dir = str(Path(os.environ["HOME"], ".config"))
    if not os.path.isdir(config_dir):
        try:
            Path(config_dir).mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
    return config_dir


LOCAL_DIR = str(Path(get_config_dir(), "yuki-iptv"))
SAVE_FOLDER_DEFAULT = str(Path(LOCAL_DIR, "saves"))

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
def convert_xtream_to_m3u(_, data, skip_init=False, append_group=""):
    output = "#EXTM3U\n" if not skip_init else ""
    for channel in data:
        name = channel.name
        # Add EPG channel ID in case channel name and epg_id are different.
        try:
            epg_channel_id = channel.epg_channel_id if channel.epg_channel_id else ""
        except Exception:
            epg_channel_id = ""
        try:
            group = channel.group_title if channel.group_title else ""
        except Exception:
            group = _("All channels")
        if append_group:
            group = append_group + " " + group
        logo = channel.logo if channel.logo else ""
        url = channel.url
        line = "#EXTINF:0"
        if epg_channel_id:
            line += f' tvg-id="{epg_channel_id}"'
        if logo:
            line += f' tvg-logo="{logo}"'
        if group:
            line += f' group-title="{group}"'
        line += f",{name}"
        output += line + "\n" + url + "\n"
    return output

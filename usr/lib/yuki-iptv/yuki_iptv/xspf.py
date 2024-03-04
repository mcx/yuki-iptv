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
import logging
import gettext
import traceback
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)
_ = gettext.gettext
all_channels = _("All channels")


def process_nodes(node, playlists, parent_title):
    # We don't support nested groups, so we call it "Parent title / Title"
    if "title" in node.attrib:
        if node.attrib["title"]:
            # vlc:node
            child_nodes = node.findall("{*}vlc:node")
            if not child_nodes:
                child_nodes = node.findall("{*}node")
            if child_nodes:
                for child_node in child_nodes:
                    process_nodes(
                        child_node,
                        playlists,
                        f"{parent_title}{node.attrib['title']} / ",
                    )
            # vlc:item
            items = node.findall("{*}vlc:item")
            if not items:
                items = node.findall("{*}item")
            if items:
                for item in items:
                    if "tid" in item.attrib:
                        if item.attrib["tid"]:
                            playlists[
                                item.attrib["tid"].strip()
                            ] = f"{parent_title}{node.attrib['title'].strip()}"


def parse_xspf(xspf):
    logger.info("Trying parsing as XSPF...")
    array = []
    tree = ET.ElementTree(ET.fromstring(xspf.lstrip())).getroot()
    playlists = {}

    # Extensions
    try:
        extension = tree.find("{*}extension")
        if extension is not None:
            if "application" in extension.attrib:
                if (
                    extension.attrib["application"]
                    == "http://www.videolan.org/vlc/playlist/0"
                ):
                    nodes = extension.findall("{*}vlc:node")
                    if not nodes:
                        nodes = extension.findall("{*}node")
                    if nodes:
                        for node in nodes:
                            process_nodes(node, playlists, "")
    except Exception:
        pass

    # Default logo
    default_logo = ""
    try:
        tree_default_logo = tree.find("{*}image")
        if tree_default_logo is not None:
            default_logo = tree_default_logo.text.strip()
    except Exception:
        pass

    for track in tree.findall("{*}trackList/{*}track"):
        # XSPF spec requires us to not stop processing
        # if we cannot process one track
        # ( see https://www.xspf.org/spec#61-graceful-failure )
        try:
            # Location
            try:
                location = track.find("{*}location").text.strip()
            except Exception:
                # Ignore channels with no URL
                continue

            # Title
            try:
                title = track.find("{*}title").text.strip()
            except Exception:
                # If title is not specified, use URL
                title = location

            useragent = ""
            referer = ""

            # Group
            group = ""
            group_changed_by_album = False
            try:
                group = track.find("{*}album").text.strip()
                if " - " in group:
                    group = group.split(" - ")[0]
                group_changed_by_album = True
            except Exception:
                pass

            # Logo
            logo = ""
            try:
                logo = track.find("{*}image").text.strip()
            except Exception:
                pass

            # Extensions
            try:
                extension = track.find("{*}extension")
                if extension is not None:
                    if "application" in extension.attrib:
                        if (
                            extension.attrib["application"]
                            == "http://www.videolan.org/vlc/playlist/0"
                        ):
                            # VLC options (User-Agent and HTTP referrer)
                            try:
                                vlc_option = extension.find("{*}vlc:option")
                                if vlc_option is None:
                                    vlc_option = extension.find("{*}option")
                                if vlc_option is not None:
                                    vlc_option = vlc_option.text.strip()
                                    if vlc_option.startswith("http-user-agent="):
                                        useragent = vlc_option.replace(
                                            "http-user-agent=", "", 1
                                        )
                                    if vlc_option.startswith("http-referrer="):
                                        referer = vlc_option.replace(
                                            "http-referrer=", "", 1
                                        )
                            except Exception:
                                pass
                            # Playlists
                            try:
                                vlc_id = extension.find("{*}vlc:id")
                                if vlc_id is None:
                                    vlc_id = extension.find("{*}id")
                                if vlc_id is not None:
                                    if vlc_id.text.strip() in playlists:
                                        if group_changed_by_album:
                                            title = f"{title} ({group})"
                                        group = playlists[vlc_id.text.strip()]
                            except Exception:
                                pass
            except Exception:
                pass

            if not group:
                group = all_channels

            array.append(
                {
                    "title": title,
                    "tvg-name": "",
                    "tvg-ID": "",
                    "tvg-logo": logo if logo else default_logo,
                    "tvg-group": group,
                    "tvg-url": "",
                    "catchup": "default",
                    "catchup-source": "",
                    "catchup-days": "7",
                    "useragent": useragent,
                    "referer": referer,
                    "url": location,
                }
            )
        except Exception:
            logger.warning("Failed to parse channel!")
            logger.warning(traceback.format_exc())

    if not array:
        raise Exception("No channels found or XSPF parsing failed!")

    # Memory optimize
    playlists = None
    tree = None

    return [array, []]

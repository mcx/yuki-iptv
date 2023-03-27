'''Convert XTream to M3U playlist'''
# pylint: disable=missing-class-docstring, missing-function-docstring
# SPDX-License-Identifier: GPL-3.0-only
def convert_xtream_to_m3u(_, data, skip_init=False, append_group=""):
    output = '#EXTM3U\n' if not skip_init else ''
    for channel in data:
        name = channel.name
        try:
            group = channel.group_title if channel.group_title else ''
        except: # pylint: disable=bare-except
            group = _('allchannels')
        if append_group:
            group = append_group + " " + group
        logo = channel.logo if channel.logo else ''
        url = channel.url
        line = '#EXTINF:0'
        if logo:
            line += " tvg-logo=\"{}\"".format(logo)
        if group:
            line += " group-title=\"{}\"".format(group)
        line += ",{}".format(name)
        output += line + '\n' + url + '\n'
    return output
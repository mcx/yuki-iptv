import gzip
import datetime
import xml.etree.ElementTree as ET
from data.modules.astroncia.time import print_with_time

def parse_as_xmltv(epg, settings):
    '''Load EPG file'''
    print_with_time("Trying parsing as XMLTV...")
    try:
        tree = ET.ElementTree(ET.fromstring(epg))
    except ET.ParseError:
        tree = ET.ElementTree(ET.fromstring(gzip.decompress(epg)))
    ids = {}
    programmes_epg = {}
    for channel_epg in tree.findall('./channel'):
        for display_name in channel_epg.findall('./display-name'):
            if not channel_epg.attrib['id'] in ids:
                ids[channel_epg.attrib['id']] = []
            ids[channel_epg.attrib['id']].append(display_name.text)
    for programme in tree.findall('./programme'):
        start = datetime.datetime.strptime(
            programme.attrib['start'].split(" ")[0], '%Y%m%d%H%M%S'
        ).timestamp() + (3600 * settings["offset"])
        stop = datetime.datetime.strptime(
            programme.attrib['stop'].split(" ")[0], '%Y%m%d%H%M%S'
        ).timestamp() + (3600 * settings["offset"])
        chans = ids[programme.attrib['channel']]
        for channel_epg_1 in chans:
            day_start = (
                datetime.datetime.now() - datetime.timedelta(days=1)
            ).replace(hour=0, minute=0, second=0).timestamp() + (3600 * settings["offset"])
            day_end = (
                datetime.datetime.now() + datetime.timedelta(days=1)
            ).replace(hour=23, minute=59, second=59).timestamp() + (3600 * settings["offset"])
            if not channel_epg_1 in programmes_epg:
                programmes_epg[channel_epg_1] = []
            if start > day_start and stop < day_end:
                try:
                    prog_title = programme.find('./title').text
                except: # pylint: disable=bare-except
                    prog_title = ""
                try:
                    prog_desc = programme.find('./desc').text
                except: # pylint: disable=bare-except
                    prog_desc = ""
                programmes_epg[channel_epg_1].append({
                    "start": start,
                    "stop": stop,
                    "title": prog_title,
                    "desc": prog_desc
                })
    return programmes_epg
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
import time
import gettext
from pathlib import Path
from yuki_iptv.qt import get_qt_library


class YukiGUIClass:
    m3u = ""
    epg = ""

    def __init__(self, _, icons_folder, use_dark_icon_theme, mpv_options_link):
        (
            qt_library,
            QtWidgets,
            QtCore,
            QtGui,
            QShortcut,
            QtOpenGLWidgets,
        ) = get_qt_library()

        self._ = _
        self.QtCore = QtCore
        self.QtWidgets = QtWidgets
        self.QtGui = QtGui

        self.main_icon = QtGui.QIcon(
            str(Path("yuki_iptv", icons_folder, "tv-blue.png"))
        )

        self.tv_icon = QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "tv.png")))
        self.tv_icon_small = QtGui.QIcon(self.tv_icon.pixmap(16, 16))
        self.loading_icon_small = QtGui.QIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "loading.gif"))).pixmap(
                16, 16
            )
        )
        self.movie_icon = QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "movie.png")))

        class ScrollableLabel(QtWidgets.QScrollArea):
            def __init__(self, *args, **kwargs):
                QtWidgets.QScrollArea.__init__(self, *args, **kwargs)
                self.setWidgetResizable(True)
                label_qwidget = QtWidgets.QWidget(self)
                bcolor_scrollabel = "white"
                if use_dark_icon_theme:
                    bcolor_scrollabel = "black"
                label_qwidget.setStyleSheet("background-color: " + bcolor_scrollabel)
                self.setWidget(label_qwidget)
                label_layout = QtWidgets.QVBoxLayout(label_qwidget)
                self.label = QtWidgets.QLabel(label_qwidget)
                self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label.setWordWrap(True)
                self.label.setStyleSheet("background-color: " + bcolor_scrollabel)
                label_layout.addWidget(self.label)

            def setText(self, text):
                self.label.setText(text)

        class SettingsScrollableWindow(QtWidgets.QMainWindow):
            def __init__(self):
                super().__init__()
                self.scroll = QtWidgets.QScrollArea()
                self.scroll.setVerticalScrollBarPolicy(
                    QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                )
                self.scroll.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                )
                self.scroll.setWidgetResizable(True)
                self.setCentralWidget(self.scroll)

        self.ScrollableLabel = ScrollableLabel
        self.SettingsScrollableWindow = SettingsScrollableWindow

        # Fonts
        self.font_bold = QtGui.QFont()
        self.font_bold.setBold(True)

        self.font_11_bold = QtGui.QFont()
        self.font_11_bold.setPointSize(11)
        self.font_11_bold.setBold(True)

        self.font_12 = QtGui.QFont()
        self.font_12.setPointSize(12)

        self.font_12_bold = QtGui.QFont()
        self.font_12_bold.setPointSize(12)
        self.font_12_bold.setBold(True)

        class PlaylistWidget(QtWidgets.QWidget):
            def __init__(self, YukiGUI, hidechannellogos):
                super().__init__()

                self.name_label = QtWidgets.QLabel()
                self.name_label.setFont(YukiGUI.font_bold)
                self.description_label = QtWidgets.QLabel()

                self.icon_label = QtWidgets.QLabel()
                self.progress_label = QtWidgets.QLabel()
                self.progress_bar = QtWidgets.QProgressBar()
                self.progress_bar.setFixedHeight(15)
                self.end_label = QtWidgets.QLabel()
                self.opacity = QtWidgets.QGraphicsOpacityEffect()
                self.opacity.setOpacity(100)

                self.layout = QtWidgets.QVBoxLayout()
                self.layout.addWidget(self.name_label)
                self.layout.addWidget(self.description_label)
                self.layout.setSpacing(5)

                self.layout1 = QtWidgets.QGridLayout()
                self.layout1.addWidget(self.progress_label, 0, 0)
                self.layout1.addWidget(self.progress_bar, 0, 1)
                self.layout1.addWidget(self.end_label, 0, 2)

                self.layout2 = QtWidgets.QGridLayout()
                self.layout2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                if not hidechannellogos:
                    self.layout2.addWidget(self.icon_label, 0, 0)
                self.layout2.addLayout(self.layout, 0, 1)
                self.layout2.setSpacing(10)

                self.layout3 = QtWidgets.QVBoxLayout()
                self.layout3.addLayout(self.layout2)
                self.layout3.addLayout(self.layout1)

                self.setLayout(self.layout3)

                self.progress_bar.setStyleSheet(
                    """
                  background-color: #C0C6CA;
                  border: 0px;
                  padding: 0px;
                  height: 5px;
                """
                )
                self.setStyleSheet(
                    """
                  QProgressBar::chunk {
                    background: #7D94B0;
                    width:5px
                  }
                """
                )

            def setDescription(self, text, tooltip):
                self.setToolTip(tooltip)
                self.description_label.setText(text)

            def setIcon(self, image):
                self.icon_label.setPixmap(image.pixmap(QtCore.QSize(32, 32)))

            def setProgress(self, progress_val):
                self.opacity.setOpacity(100)
                self.progress_bar.setGraphicsEffect(self.opacity)
                self.progress_bar.setFormat("")
                self.progress_bar.setValue(progress_val)

            def hideProgress(self):
                self.opacity.setOpacity(0)
                self.progress_bar.setGraphicsEffect(self.opacity)

            def showDescription(self):
                self.description_label.show()
                self.progress_label.show()
                self.progress_bar.show()
                self.end_label.show()

            def hideDescription(self):
                self.description_label.hide()
                self.progress_label.hide()
                self.progress_bar.hide()
                self.end_label.hide()

        self.PlaylistWidget = PlaylistWidget

        self.btn_playpause = QtWidgets.QPushButton()
        self.btn_playpause.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "pause.png")))
        )
        self.btn_playpause.setToolTip(_("Pause"))

        self.btn_stop = QtWidgets.QPushButton()
        self.btn_stop.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "stop.png")))
        )
        self.btn_stop.setToolTip(_("Stop"))

        self.btn_fullscreen = QtWidgets.QPushButton()
        self.btn_fullscreen.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "fullscreen.png")))
        )
        self.btn_fullscreen.setToolTip(_("Fullscreen"))

        self.btn_open_recordings_folder = QtWidgets.QPushButton()
        self.btn_open_recordings_folder.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "folder.png")))
        )
        self.btn_open_recordings_folder.setToolTip(_("Open recordings folder"))

        self.record_icon = QtGui.QIcon(
            str(Path("yuki_iptv", icons_folder, "record.png"))
        )
        self.record_stop_icon = QtGui.QIcon(
            str(Path("yuki_iptv", icons_folder, "stoprecord.png"))
        )

        self.btn_record = QtWidgets.QPushButton()
        self.btn_record.setIcon(self.record_icon)
        self.btn_record.setToolTip(_("Record"))

        self.btn_show_scheduler = QtWidgets.QPushButton()
        self.btn_show_scheduler.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "calendar.png")))
        )
        self.btn_show_scheduler.setToolTip(_("Recording scheduler"))

        self.btn_volume = QtWidgets.QPushButton()
        self.btn_volume.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "volume.png")))
        )
        self.btn_volume.setToolTip(_("Volume"))

        VOLUME_SLIDER_SET_WIDTH = 150
        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(200)
        self.volume_slider.setFixedWidth(VOLUME_SLIDER_SET_WIDTH)

        self.btn_screenshot = QtWidgets.QPushButton()
        self.btn_screenshot.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "screenshot.png")))
        )
        self.btn_screenshot.setToolTip(_("Screenshot").capitalize())

        self.btn_show_archive = QtWidgets.QPushButton()
        self.btn_show_archive.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "timeshift.png")))
        )
        self.btn_show_archive.setToolTip(_("Archive"))

        self.btn_show_settings = QtWidgets.QPushButton()
        self.btn_show_settings.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "settings.png")))
        )
        self.btn_show_settings.setToolTip(_("Settings"))

        self.btn_show_playlists = QtWidgets.QPushButton()
        self.btn_show_playlists.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "tv-blue.png")))
        )
        self.btn_show_playlists.setToolTip(_("Playlists"))

        self.btn_tv_guide = QtWidgets.QPushButton()
        self.btn_tv_guide.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "tvguide.png")))
        )
        self.btn_tv_guide.setToolTip(_("TV guide"))

        self.btn_prev_channel = QtWidgets.QPushButton()
        self.btn_prev_channel.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "prev.png")))
        )
        self.btn_prev_channel.setToolTip(_("Previous channel"))

        self.btn_next_channel = QtWidgets.QPushButton()
        self.btn_next_channel.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "next.png")))
        )
        self.btn_next_channel.setToolTip(_("Next channel"))

        self.label_video_data = QtWidgets.QLabel("")
        self.label_volume = QtWidgets.QLabel("")
        self.label_volume.setMinimumWidth(50)
        self.label_video_data.setFont(self.font_12)
        self.label_volume.setFont(self.font_12)

        self.label_avsync = QtWidgets.QLabel("")
        self.label_avsync.setFont(self.font_12)

        self.label_avsync.setText("A-V -0.00")
        self.label_avsync.setMinimumSize(self.label_avsync.sizeHint())
        self.label_avsync.setText("")

        self.hdd_gif_label = QtWidgets.QLabel()
        self.hdd_gif_label.setPixmap(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "hdd.png"))).pixmap(
                QtCore.QSize(32, 32)
            )
        )
        self.hdd_gif_label.setToolTip("{}...".format(_("Writing EPG cache")))
        self.hdd_gif_label.setVisible(False)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setValue(0)
        self.start_label = QtWidgets.QLabel()
        self.stop_label = QtWidgets.QLabel()

        self.vlayout3 = QtWidgets.QVBoxLayout()
        self.hlayout1 = QtWidgets.QHBoxLayout()
        self.controlpanel_layout = QtWidgets.QHBoxLayout()

        self.hlayout1.addWidget(self.start_label)
        self.hlayout1.addWidget(self.progress)
        self.hlayout1.addWidget(self.stop_label)

        self.controlpanel_btns = [
            self.btn_playpause,
            self.btn_stop,
            self.btn_fullscreen,
            self.btn_record,
            self.btn_show_scheduler,
            self.btn_open_recordings_folder,
            self.btn_volume,
            self.volume_slider,
            self.label_volume,
            self.btn_screenshot,
            self.btn_show_archive,
            self.btn_tv_guide,
            self.btn_prev_channel,
            self.btn_next_channel,
        ]

        self.show_lbls_fullscreen = [
            self.btn_playpause,
            self.btn_stop,
            self.btn_fullscreen,
            self.btn_record,
            self.btn_volume,
            self.volume_slider,
            self.label_volume,
            self.btn_screenshot,
            self.btn_show_archive,
            self.btn_tv_guide,
            self.btn_prev_channel,
            self.btn_next_channel,
        ]

        self.fs_widget = QtWidgets.QWidget()
        self.fs_widget_l = QtWidgets.QHBoxLayout()
        self.btn_show_settings.setMaximumWidth(32)
        self.fs_widget_l.addWidget(self.btn_show_settings)
        self.fs_widget.setLayout(self.fs_widget_l)

        for controlpanel_btn in self.controlpanel_btns:
            self.controlpanel_layout.addWidget(controlpanel_btn)
        self.controlpanel_layout.addStretch(1000000)  # TODO: find better solution
        self.controlpanel_layout.addWidget(self.label_video_data)
        self.controlpanel_layout.addWidget(self.label_avsync)
        self.controlpanel_layout.addWidget(self.hdd_gif_label)

        self.vlayout3.addLayout(self.controlpanel_layout)
        self.controlpanel_layout.addStretch(1)
        self.vlayout3.addLayout(self.hlayout1)

        self.controlpanel_dock_widget = QtWidgets.QWidget()
        self.controlpanel_dock_widget.setLayout(self.vlayout3)

        self.playlist_widget = QtWidgets.QMainWindow()
        self.playlist_widget_orig = QtWidgets.QWidget(self.playlist_widget)
        self.playlist_widget.setCentralWidget(self.playlist_widget_orig)
        self.pl_layout = QtWidgets.QGridLayout()
        self.pl_layout.setVerticalSpacing(0)
        self.pl_layout.setContentsMargins(0, 0, 0, 0)
        self.pl_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.pl_layout.setSpacing(0)
        self.playlist_widget_orig.setLayout(self.pl_layout)
        self.playlist_widget.hide()

        self.controlpanel_widget = QtWidgets.QWidget()
        self.cp_layout = QtWidgets.QVBoxLayout()
        self.controlpanel_widget.setLayout(self.cp_layout)
        self.controlpanel_widget.hide()

        self.btn_update = QtWidgets.QPushButton()
        self.btn_update.hide()

        self.license_btn = QtWidgets.QPushButton()
        self.license_btn.setText(_("License"))

        self.aboutqt_btn = QtWidgets.QPushButton()
        self.aboutqt_btn.setText(_("About Qt"))

        self.close_btn = QtWidgets.QPushButton()
        self.close_btn.setText(_("Close"))

        self.textbox = QtWidgets.QTextBrowser()
        self.textbox.setOpenExternalLinks(True)
        self.textbox.setReadOnly(True)

        self.helpwin_widget_btns = QtWidgets.QWidget()
        self.helpwin_widget_btns_layout = QtWidgets.QHBoxLayout()
        self.helpwin_widget_btns_layout.addWidget(self.license_btn)
        self.helpwin_widget_btns_layout.addWidget(self.aboutqt_btn)
        self.helpwin_widget_btns_layout.addWidget(self.close_btn)
        self.helpwin_widget_btns.setLayout(self.helpwin_widget_btns_layout)

        self.helpwin_widget = QtWidgets.QWidget()
        self.helpwin_layout = QtWidgets.QVBoxLayout()
        self.helpwin_layout.addWidget(self.textbox)
        self.helpwin_layout.addWidget(self.helpwin_widget_btns)
        self.helpwin_widget.setLayout(self.helpwin_layout)

        self.license_str = (
            "This program is free software: you can redistribute it and/or modify\n"
            "it under the terms of the GNU General Public License as published by\n"
            "the Free Software Foundation, either version 3 of the License, or\n"
            "(at your option) any later version.\n"
            "\n"
            "This program is distributed in the hope that it will be useful,\n"
            "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
            "GNU General Public License for more details.\n"
            "\n"
            "You should have received a copy of the GNU General Public License\n"
            "along with this program.  If not, see <https://www.gnu.org/licenses/>.\n"
            "\n"
            "yuki-iptv is based on Astroncia IPTV code.\n"
            "\n"
            "Original Astroncia IPTV code is licensed under GPL-3.0-only.\n"
            "I have permission from original code author (Astroncia)\n"
            "to relicense code to GPL-3.0-or-later.\n"
            "\n"
            "The Font Awesome pictograms are licensed under the CC BY 4.0 License.\n"
            "Font Awesome Free 5.15.4 by @fontawesome - https://fontawesome.com\n"
            "License - https://creativecommons.org/licenses/by/4.0/\n"
        )

        if os.path.isfile("/usr/share/common-licenses/GPL"):
            with open(
                "/usr/share/common-licenses/GPL", encoding="utf8"
            ) as license_gpl_file:
                self.license_str += "\n" + license_gpl_file.read()

        self.licensebox = QtWidgets.QPlainTextEdit()
        self.licensebox.setReadOnly(True)
        self.licensebox.setPlainText(self.license_str)

        self.licensebox_close_btn = QtWidgets.QPushButton()
        self.licensebox_close_btn.setText(_("Close"))

        self.licensewin_widget = QtWidgets.QWidget()
        self.licensewin_layout = QtWidgets.QVBoxLayout()
        self.licensewin_layout.addWidget(self.licensebox)
        self.licensewin_layout.addWidget(self.licensebox_close_btn)
        self.licensewin_widget.setLayout(self.licensewin_layout)

        self.wid5 = QtWidgets.QWidget()
        self.stream_information_win_layout = QtWidgets.QVBoxLayout()
        self.stream_information_layout = QtWidgets.QGridLayout()
        self.stream_information_layout_widget = QtWidgets.QWidget()
        self.stream_information_layout_widget.setLayout(self.stream_information_layout)

        self.url_data_widget = QtWidgets.QWidget()
        self.url_data_layout = QtWidgets.QVBoxLayout()
        self.url_data_widget.setLayout(self.url_data_layout)

        self.url_label = QtWidgets.QLabel(_("URL") + "\n")
        self.url_label.setStyleSheet("color:green")
        self.url_label.setFont(self.font_bold)

        self.url_data_layout.addWidget(self.url_label)

        self.url_text = QtWidgets.QLineEdit()
        self.url_text.setReadOnly(True)

        self.url_data_layout.addWidget(self.url_text)

        self.stream_information_win_layout.addWidget(self.url_data_widget)
        self.stream_information_win_layout.addWidget(
            self.stream_information_layout_widget
        )
        self.wid5.setLayout(self.stream_information_win_layout)

        self.wid4 = QtWidgets.QWidget()

        self.save_btn_xtream_2 = QtWidgets.QPushButton(_("Save"))
        self.save_btn_xtream_2.setStyleSheet("font-weight: bold; color: green;")

        self.xtr_username_input_2 = QtWidgets.QLineEdit()
        self.xtr_password_input_2 = QtWidgets.QLineEdit()
        self.xtr_url_input_2 = QtWidgets.QLineEdit()

        self.layout35 = QtWidgets.QGridLayout()
        self.layout35.addWidget(QtWidgets.QLabel("{}:".format(_("Username"))), 0, 0)
        self.layout35.addWidget(self.xtr_username_input_2, 0, 1)
        self.layout35.addWidget(QtWidgets.QLabel("{}:".format(_("Password"))), 1, 0)
        self.layout35.addWidget(self.xtr_password_input_2, 1, 1)
        self.layout35.addWidget(QtWidgets.QLabel("{}:".format(_("URL"))), 2, 0)
        self.layout35.addWidget(self.xtr_url_input_2, 2, 1)
        self.layout35.addWidget(self.save_btn_xtream_2, 3, 1)
        self.wid4.setLayout(self.layout35)

        self.grid2 = QtWidgets.QGridLayout()
        self.grid2.setSpacing(0)

        self.ssave = QtWidgets.QPushButton(_("Save settings"))
        self.ssave.setStyleSheet("font-weight: bold; color: green;")

        self.sclose = QtWidgets.QPushButton(_("Close"))
        self.sclose.setStyleSheet("color: red;")

        self.sreset = QtWidgets.QPushButton(_("Reset channel settings"))

        self.clear_logo_cache = QtWidgets.QPushButton(_("Clear logo cache"))

        self.sort_widget = QtWidgets.QComboBox()
        self.sort_widget.addItem(_("as in playlist"))
        self.sort_widget.addItem(_("alphabetical order"))
        self.sort_widget.addItem(_("reverse alphabetical order"))
        self.sort_widget.addItem(_("custom"))

        self.ssaveclose = QtWidgets.QWidget()
        self.ssaveclose_layout = QtWidgets.QHBoxLayout()
        self.ssaveclose_layout.addWidget(self.ssave)
        self.ssaveclose_layout.addWidget(self.sclose)
        self.ssaveclose.setLayout(self.ssaveclose_layout)

        self.sbtns = QtWidgets.QWidget()
        self.sbtns_layout = QtWidgets.QHBoxLayout()
        self.sbtns_layout.addWidget(self.sreset)
        self.sbtns_layout.addWidget(self.clear_logo_cache)
        self.sbtns.setLayout(self.sbtns_layout)

        self.grid2.addWidget(self.ssaveclose, 2, 1)
        self.grid2.addWidget(self.sbtns, 3, 1)

        self.donot_label = QtWidgets.QLabel(
            "{}:".format(_("Do not update\nEPG at boot"))
        )
        self.donot_flag = QtWidgets.QCheckBox()

        self.openprevchannel_label = QtWidgets.QLabel(
            "{}:".format(_("Open previous channel\nat startup"))
        )
        self.hidempv_label = QtWidgets.QLabel("{}:".format(_("Hide mpv panel")))
        self.hideepgpercentage_label = QtWidgets.QLabel(
            "{}:".format(_("Hide EPG percentage"))
        )
        self.hideepgfromplaylist_label = QtWidgets.QLabel(
            "{}:".format(_("Hide EPG from playlist"))
        )
        self.multicastoptimization_label = QtWidgets.QLabel(
            "{}:".format(_("Multicast optimization"))
        )
        self.hidebitrateinfo_label = QtWidgets.QLabel(
            "{}:".format(_("Hide bitrate / video info"))
        )
        self.styleredefoff_label = QtWidgets.QLabel(
            "{}:".format(_("Enable styles redefinition"))
        )
        self.volumechangestep_label = QtWidgets.QLabel(
            "{}:".format(_("Volume change step"))
        )
        self.volumechangestep_percent = QtWidgets.QLabel("%")

        self.openprevchannel_flag = QtWidgets.QCheckBox()

        self.hidempv_flag = QtWidgets.QCheckBox()

        self.mpv_label = QtWidgets.QLabel(
            "{} ({}):".format(
                _("mpv options"),
                '<a href="' + mpv_options_link + '">{}</a>'.format(_("list")),
            )
        )
        self.mpv_label.setOpenExternalLinks(True)
        self.mpv_label.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        self.mpv_options = QtWidgets.QLineEdit()

        self.videoaspect_def_choose = QtWidgets.QComboBox()

        self.hideepgpercentage_flag = QtWidgets.QCheckBox()

        self.hideepgfromplaylist_flag = QtWidgets.QCheckBox()

        self.multicastoptimization_flag = QtWidgets.QCheckBox()

        # Mark option as experimental
        self.multicastoptimization_flag.setToolTip(
            _("WARNING: experimental function, working with problems")
        )
        self.multicastoptimization_label.setToolTip(
            _("WARNING: experimental function, working with problems")
        )
        self.multicastoptimization_label.setStyleSheet("color: #cf9e17")

        self.hidebitrateinfo_flag = QtWidgets.QCheckBox()

        self.styleredefoff_flag = QtWidgets.QCheckBox()

        self.volumechangestep_choose = QtWidgets.QSpinBox()
        self.volumechangestep_choose.setMinimum(1)
        self.volumechangestep_choose.setMaximum(50)

        self.flpopacity_label = QtWidgets.QLabel(
            "{}:".format(_("Floating panels opacity"))
        )
        self.flpopacity_input = QtWidgets.QDoubleSpinBox()
        self.flpopacity_input.setMinimum(0.01)
        self.flpopacity_input.setMaximum(1)
        self.flpopacity_input.setSingleStep(0.1)
        self.flpopacity_input.setDecimals(2)

        self.panelposition_label = QtWidgets.QLabel(
            "{}:".format(_("Floating panel\nposition"))
        )
        self.panelposition_choose = QtWidgets.QComboBox()
        self.panelposition_choose.addItem(_("Right"))
        self.panelposition_choose.addItem(_("Left"))
        self.panelposition_choose.addItem(_("Separate window"))

        self.mouseswitchchannels_label = QtWidgets.QLabel(
            "{}:".format(_("Switch channels with\nthe mouse wheel"))
        )
        self.autoreconnection_label = QtWidgets.QLabel(
            "{}:".format(_("Automatic\nreconnection"))
        )
        self.defaultchangevol_label = QtWidgets.QLabel(
            "({})".format(_("by default:\nchange volume"))
        )
        self.defaultchangevol_label.setStyleSheet("color:blue")

        self.mouseswitchchannels_flag = QtWidgets.QCheckBox()

        self.autoreconnection_flag = QtWidgets.QCheckBox()

        # Mark option as experimental
        self.autoreconnection_flag.setToolTip(
            _("WARNING: experimental function, working with problems")
        )
        self.autoreconnection_label.setToolTip(
            _("WARNING: experimental function, working with problems")
        )
        self.autoreconnection_label.setStyleSheet("color: #cf9e17")

        self.showplaylistmouse_label = QtWidgets.QLabel(
            "{}:".format(_("Show playlist\non mouse move"))
        )
        self.showplaylistmouse_flag = QtWidgets.QCheckBox()

        self.showcontrolsmouse_label = QtWidgets.QLabel(
            "{}:".format(_("Show controls\non mouse move"))
        )
        self.showcontrolsmouse_flag = QtWidgets.QCheckBox()

        self.channellogos_label = QtWidgets.QLabel("{}:".format(_("Channel logos")))
        self.channellogos_select = QtWidgets.QComboBox()
        self.channellogos_select.addItem(_("Prefer M3U"))
        self.channellogos_select.addItem(_("Prefer EPG"))
        self.channellogos_select.addItem(_("Do not load from EPG"))
        self.channellogos_select.addItem(_("Do not load any logos"))

        self.nocacheepg_label = QtWidgets.QLabel("{}:".format(_("Do not cache EPG")))
        self.nocacheepg_flag = QtWidgets.QCheckBox()

        self.scrrecnosubfolders_label = QtWidgets.QLabel(
            "{}:".format(_("Do not create screenshots\nand recordings subfolders"))
        )
        self.scrrecnosubfolders_flag = QtWidgets.QCheckBox()

        self.hidetvprogram_label = QtWidgets.QLabel(
            "{}:".format(_("Hide the current television program"))
        )
        self.hidetvprogram_flag = QtWidgets.QCheckBox()

        self.videoaspectdef_label = QtWidgets.QLabel("{}:".format(_("Aspect ratio")))
        self.zoomdef_label = QtWidgets.QLabel("{}:".format(_("Scale / Zoom")))
        self.panscan_def_label = QtWidgets.QLabel("{}:".format(_("Pan and scan")))

        self.panscan_def_choose = QtWidgets.QDoubleSpinBox()
        self.panscan_def_choose.setMinimum(0)
        self.panscan_def_choose.setMaximum(1)
        self.panscan_def_choose.setSingleStep(0.1)
        self.panscan_def_choose.setDecimals(1)

        self.zoom_def_choose = QtWidgets.QComboBox()

        self.catchupenable_label = QtWidgets.QLabel("{}:".format(_("Enable catchup")))
        self.catchupenable_flag = QtWidgets.QCheckBox()

        self.rewindenable_label = QtWidgets.QLabel("{}:".format(_("Enable rewind")))
        self.rewindenable_flag = QtWidgets.QCheckBox()

        self.hidechannellogos_label = QtWidgets.QLabel(
            "{}:".format(_("Hide channel logos"))
        )
        self.hidechannellogos_flag = QtWidgets.QCheckBox()

        self.hideplaylistbyleftmouseclick_label = QtWidgets.QLabel(
            "{}:".format(_("Show/hide playlist by left mouse click"))
        )
        self.hideplaylistbyleftmouseclick_flag = QtWidgets.QCheckBox()

        self.useragent_choose_2 = QtWidgets.QLineEdit()

        self.useragent_lbl_2 = QtWidgets.QLabel("{}:".format(_("User agent")))
        self.referer_lbl = QtWidgets.QLabel(_("HTTP Referer:"))
        self.referer_choose = QtWidgets.QLineEdit()

        self.epgdays_p = QtWidgets.QLabel(
            (gettext.ngettext("%d day", "%d days", 0) % 0).replace("0 ", "")
        )

        self.epgdays_label = QtWidgets.QLabel("{}:".format(_("Load EPG for")))

        self.epgdays = QtWidgets.QSpinBox()
        self.epgdays.setMinimum(1)
        self.epgdays.setMaximum(7)

        self.scache1 = QtWidgets.QSpinBox()
        self.scache1.setMinimum(0)
        self.scache1.setMaximum(120)

        self.soffset = QtWidgets.QDoubleSpinBox()
        self.soffset.setMinimum(-240)
        self.soffset.setMaximum(240)
        self.soffset.setSingleStep(1)
        self.soffset.setDecimals(1)

        self.sfolder = QtWidgets.QPushButton()
        self.sfolder.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", icons_folder, "file.png")))
        )

        self.scache = QtWidgets.QLabel(
            (gettext.ngettext("%d second", "%d seconds", 0) % 0).replace("0 ", "")
        )
        self.sselect = QtWidgets.QLabel("{}:".format(_("Or select provider")))
        self.sselect.setStyleSheet("color: #00008B;")

        self.sfld = QtWidgets.QLineEdit()

        self.shwaccel = QtWidgets.QCheckBox()

        self.sdei = QtWidgets.QCheckBox()

        self.sudp = QtWidgets.QLineEdit()

        self.m3u_label = QtWidgets.QLabel("{}:".format(_("M3U / XSPF playlist")))
        self.update_label = QtWidgets.QLabel(
            "{}:".format(_("Update playlist\nat launch"))
        )
        self.epg_label = QtWidgets.QLabel("{}:".format(_("TV guide\naddress")))
        self.dei_label = QtWidgets.QLabel("{}:".format(_("Deinterlace")))
        self.hwaccel_label = QtWidgets.QLabel("{}:".format(_("Hardware\nacceleration")))
        self.sort_label = QtWidgets.QLabel("{}:".format(_("Channel\nsort")))
        self.cache_label = QtWidgets.QLabel("{}:".format(_("Cache")))
        self.udp_label = QtWidgets.QLabel("{}:".format(_("UDP proxy")))
        self.fld_label = QtWidgets.QLabel(
            "{}:".format(_("Folder for recordings\nand screenshots"))
        )

        self.tabs = QtWidgets.QTabWidget()

        self.tab_main = QtWidgets.QWidget()
        self.tab_video = QtWidgets.QWidget()
        self.tab_network = QtWidgets.QWidget()
        self.tab_other = QtWidgets.QWidget()
        self.tab_gui = QtWidgets.QWidget()
        self.tab_actions = QtWidgets.QWidget()
        self.tab_catchup = QtWidgets.QWidget()
        self.tab_debug = QtWidgets.QWidget()
        self.tab_epg = QtWidgets.QWidget()

        self.tabs.addTab(self.tab_main, _("Main"))
        self.tabs.addTab(self.tab_video, _("Video"))
        self.tabs.addTab(self.tab_network, _("Network"))
        self.tabs.addTab(self.tab_gui, _("GUI"))
        self.tabs.addTab(self.tab_actions, _("Actions"))
        self.tabs.addTab(self.tab_catchup, _("Catchup"))
        self.tabs.addTab(self.tab_epg, _("EPG"))
        self.tabs.addTab(self.tab_other, _("Other"))
        self.tabs.addTab(self.tab_debug, _("Debug"))

        self.tab_main.layout = QtWidgets.QGridLayout()
        self.tab_main.layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.tab_main.layout.addWidget(self.fld_label, 0, 0)
        self.tab_main.layout.addWidget(self.sfld, 0, 1)
        self.tab_main.layout.addWidget(self.sfolder, 0, 2)
        self.tab_main.layout.addWidget(self.scrrecnosubfolders_label, 1, 0)
        self.tab_main.layout.addWidget(self.scrrecnosubfolders_flag, 1, 1)
        self.tab_main.layout.addWidget(self.sort_label, 2, 0)
        self.tab_main.layout.addWidget(self.sort_widget, 2, 1)
        self.tab_main.layout.addWidget(self.openprevchannel_label, 3, 0)
        self.tab_main.layout.addWidget(self.openprevchannel_flag, 3, 1)
        self.tab_main.setLayout(self.tab_main.layout)

        self.tab_video.layout = QtWidgets.QGridLayout()
        self.tab_video.layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.tab_video.layout.addWidget(self.dei_label, 0, 0)
        self.tab_video.layout.addWidget(self.sdei, 0, 1)
        self.tab_video.layout.addWidget(self.hwaccel_label, 1, 0)
        self.tab_video.layout.addWidget(self.shwaccel, 1, 1)
        self.tab_video.layout.addWidget(self.videoaspectdef_label, 2, 0)
        self.tab_video.layout.addWidget(self.videoaspect_def_choose, 2, 1)
        self.tab_video.layout.addWidget(self.zoomdef_label, 3, 0)
        self.tab_video.layout.addWidget(self.zoom_def_choose, 3, 1)
        self.tab_video.layout.addWidget(self.panscan_def_label, 4, 0)
        self.tab_video.layout.addWidget(self.panscan_def_choose, 4, 1)
        self.tab_video.setLayout(self.tab_video.layout)

        self.tab_network.layout = QtWidgets.QGridLayout()
        self.tab_network.layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.tab_network.layout.addWidget(self.udp_label, 0, 0)
        self.tab_network.layout.addWidget(self.sudp, 0, 1)
        self.tab_network.layout.addWidget(self.cache_label, 1, 0)
        self.tab_network.layout.addWidget(self.scache1, 1, 1)
        self.tab_network.layout.addWidget(self.scache, 1, 2)
        self.tab_network.layout.addWidget(self.useragent_lbl_2, 2, 0)
        self.tab_network.layout.addWidget(self.useragent_choose_2, 2, 1)
        self.tab_network.layout.addWidget(self.referer_lbl, 3, 0)
        self.tab_network.layout.addWidget(self.referer_choose, 3, 1)
        self.tab_network.setLayout(self.tab_network.layout)

        self.tab_gui.layout = QtWidgets.QGridLayout()
        self.tab_gui.layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.tab_gui.layout.addWidget(self.panelposition_label, 0, 0)
        self.tab_gui.layout.addWidget(self.panelposition_choose, 0, 1)
        self.tab_gui.layout.addWidget(self.hideplaylistbyleftmouseclick_label, 1, 0)
        self.tab_gui.layout.addWidget(self.hideplaylistbyleftmouseclick_flag, 1, 1)
        self.tab_gui.layout.addWidget(self.hideepgfromplaylist_label, 2, 0)
        self.tab_gui.layout.addWidget(self.hideepgfromplaylist_flag, 2, 1)
        self.tab_gui.layout.addWidget(self.hideepgpercentage_label, 3, 0)
        self.tab_gui.layout.addWidget(self.hideepgpercentage_flag, 3, 1)
        self.tab_gui.layout.addWidget(self.hidebitrateinfo_label, 4, 0)
        self.tab_gui.layout.addWidget(self.hidebitrateinfo_flag, 4, 1)
        self.tab_gui.layout.addWidget(self.hidetvprogram_label, 5, 0)
        self.tab_gui.layout.addWidget(self.hidetvprogram_flag, 5, 1)
        self.tab_gui.layout.addWidget(self.hidechannellogos_label, 6, 0)
        self.tab_gui.layout.addWidget(self.hidechannellogos_flag, 6, 1)
        self.tab_gui.setLayout(self.tab_gui.layout)

        self.tab_actions.layout = QtWidgets.QGridLayout()
        self.tab_actions.layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.tab_actions.layout.addWidget(self.mouseswitchchannels_label, 0, 0)
        self.tab_actions.layout.addWidget(self.mouseswitchchannels_flag, 0, 1)
        self.tab_actions.layout.addWidget(self.defaultchangevol_label, 1, 0)
        self.tab_actions.layout.addWidget(self.showplaylistmouse_label, 3, 0)
        self.tab_actions.layout.addWidget(self.showplaylistmouse_flag, 3, 1)
        self.tab_actions.layout.addWidget(self.showcontrolsmouse_label, 4, 0)
        self.tab_actions.layout.addWidget(self.showcontrolsmouse_flag, 4, 1)
        self.tab_actions.setLayout(self.tab_actions.layout)

        self.tab_catchup.layout = QtWidgets.QGridLayout()
        self.tab_catchup.layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.tab_catchup.layout.addWidget(self.catchupenable_label, 0, 0)
        self.tab_catchup.layout.addWidget(self.catchupenable_flag, 0, 1)
        self.tab_catchup.layout.addWidget(self.rewindenable_label, 1, 0)
        self.tab_catchup.layout.addWidget(self.rewindenable_flag, 1, 1)
        self.tab_catchup.setLayout(self.tab_catchup.layout)

        self.tab_epg.layout = QtWidgets.QGridLayout()
        self.tab_epg.layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        # self.tab_epg.layout.addWidget(self.epgdays_label, 0, 0)
        # self.tab_epg.layout.addWidget(self.epgdays, 0, 1)
        # self.tab_epg.layout.addWidget(self.epgdays_p, 0, 2)
        self.tab_epg.layout.addWidget(self.donot_label, 0, 0)
        self.tab_epg.layout.addWidget(self.donot_flag, 0, 1)
        self.tab_epg.layout.addWidget(self.nocacheepg_label, 1, 0)
        self.tab_epg.layout.addWidget(self.nocacheepg_flag, 1, 1)
        self.tab_epg.setLayout(self.tab_epg.layout)

        self.tab_other.layout = QtWidgets.QGridLayout()
        self.tab_other.layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.tab_other.layout.addWidget(self.mpv_label, 0, 0)
        self.tab_other.layout.addWidget(self.mpv_options, 0, 1)
        self.tab_other.layout.addWidget(self.hidempv_label, 1, 0)
        self.tab_other.layout.addWidget(self.hidempv_flag, 1, 1)
        self.tab_other.layout.addWidget(self.channellogos_label, 2, 0)
        self.tab_other.layout.addWidget(self.channellogos_select, 2, 1)
        self.tab_other.layout.addWidget(self.volumechangestep_label, 3, 0)
        self.tab_other.layout.addWidget(self.volumechangestep_choose, 3, 1)
        self.tab_other.layout.addWidget(self.volumechangestep_percent, 3, 2)
        self.tab_other.setLayout(self.tab_other.layout)

        self.tab_debug_warning = QtWidgets.QLabel(
            _("WARNING: experimental function, working with problems")
        )
        self.tab_debug_warning.setStyleSheet("color: #cf9e17")

        self.tab_debug_widget = QtWidgets.QWidget()
        self.tab_debug.layout = QtWidgets.QGridLayout()
        self.tab_debug.layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.tab_debug.layout.addWidget(self.styleredefoff_label, 0, 0)
        self.tab_debug.layout.addWidget(self.styleredefoff_flag, 0, 1)
        self.tab_debug.layout.addWidget(self.autoreconnection_label, 1, 0)
        self.tab_debug.layout.addWidget(self.autoreconnection_flag, 1, 1)
        self.tab_debug.layout.addWidget(self.multicastoptimization_label, 2, 0)
        self.tab_debug.layout.addWidget(self.multicastoptimization_flag, 2, 1)
        self.tab_debug_widget.setLayout(self.tab_debug.layout)
        self.tab_debug.layout1 = QtWidgets.QVBoxLayout()
        self.tab_debug.layout1.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.tab_debug.layout1.addWidget(self.tab_debug_warning)
        self.tab_debug.layout1.addWidget(self.tab_debug_widget)
        self.tab_debug.setLayout(self.tab_debug.layout1)

        self.grid = QtWidgets.QVBoxLayout()
        self.grid.addWidget(self.tabs)

        self.layout2 = QtWidgets.QVBoxLayout()
        self.layout2.addLayout(self.grid)
        self.layout2.addLayout(self.grid2)

        self.wid2 = QtWidgets.QWidget()
        self.wid2.setLayout(self.layout2)

        self.wid = QtWidgets.QWidget()

        self.title = QtWidgets.QLabel()
        self.title.setFont(self.font_bold)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.deinterlace_lbl = QtWidgets.QLabel("{}:".format(_("Deinterlace")))
        self.useragent_lbl = QtWidgets.QLabel("{}:".format(_("User agent")))
        self.group_lbl = QtWidgets.QLabel("{}:".format(_("Group")))
        self.group_text = QtWidgets.QLineEdit()
        self.hidden_lbl = QtWidgets.QLabel("{}:".format(_("Hide")))
        self.deinterlace_chk = QtWidgets.QCheckBox()
        self.hidden_chk = QtWidgets.QCheckBox()
        self.useragent_choose = QtWidgets.QLineEdit()

        self.epgname_lbl = QtWidgets.QLabel()

        self.contrast_choose = QtWidgets.QSpinBox()
        self.contrast_choose.setMinimum(-100)
        self.contrast_choose.setMaximum(100)
        self.brightness_choose = QtWidgets.QSpinBox()
        self.brightness_choose.setMinimum(-100)
        self.brightness_choose.setMaximum(100)
        self.hue_choose = QtWidgets.QSpinBox()
        self.hue_choose.setMinimum(-100)
        self.hue_choose.setMaximum(100)
        self.saturation_choose = QtWidgets.QSpinBox()
        self.saturation_choose.setMinimum(-100)
        self.saturation_choose.setMaximum(100)
        self.gamma_choose = QtWidgets.QSpinBox()
        self.gamma_choose.setMinimum(-100)
        self.gamma_choose.setMaximum(100)
        self.videoaspect_vars = {
            _("Default"): -1,
            "16:9": "16:9",
            "16:10": "16:10",
            "1.85:1": "1.85:1",
            "2.21:1": "2.21:1",
            "2.35:1": "2.35:1",
            "2.39:1": "2.39:1",
            "4:3": "4:3",
            "5:4": "5:4",
            "5:3": "5:3",
            "1:1": "1:1",
        }
        self.videoaspect_choose = QtWidgets.QComboBox()
        for videoaspect_var in self.videoaspect_vars:
            self.videoaspect_choose.addItem(videoaspect_var)

        self.zoom_choose = QtWidgets.QComboBox()
        self.zoom_vars = {
            _("Default"): 0,
            "1.05": "1.05",
            "1.1": "1.1",
            "1.2": "1.2",
            "1.3": "1.3",
            "1.4": "1.4",
            "1.5": "1.5",
            "1.6": "1.6",
            "1.7": "1.7",
            "1.8": "1.8",
            "1.9": "1.9",
            "2": "2",
        }
        for zoom_var in self.zoom_vars:
            self.zoom_choose.addItem(zoom_var)

        self.panscan_choose = QtWidgets.QDoubleSpinBox()
        self.panscan_choose.setMinimum(0)
        self.panscan_choose.setMaximum(1)
        self.panscan_choose.setSingleStep(0.1)
        self.panscan_choose.setDecimals(1)

        self.contrast_lbl = QtWidgets.QLabel("{}:".format(_("Contrast")))
        self.brightness_lbl = QtWidgets.QLabel("{}:".format(_("Brightness")))
        self.hue_lbl = QtWidgets.QLabel("{}:".format(_("Hue")))
        self.saturation_lbl = QtWidgets.QLabel("{}:".format(_("Saturation")))
        self.gamma_lbl = QtWidgets.QLabel("{}:".format(_("Gamma")))
        self.videoaspect_lbl = QtWidgets.QLabel("{}:".format(_("Aspect ratio")))
        self.zoom_lbl = QtWidgets.QLabel("{}:".format(_("Scale / Zoom")))
        self.panscan_lbl = QtWidgets.QLabel("{}:".format(_("Pan and scan")))
        self.epgname_btn = QtWidgets.QPushButton(_("EPG name"))

        self.referer_lbl_custom = QtWidgets.QLabel(_("HTTP Referer:"))
        self.referer_choose_custom = QtWidgets.QLineEdit()

        self.save_btn = QtWidgets.QPushButton(_("Save settings"))

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addWidget(self.title)

        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2.addWidget(self.deinterlace_lbl)
        self.horizontalLayout2.addWidget(self.deinterlace_chk)
        self.horizontalLayout2.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_1.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_1.addWidget(self.useragent_lbl)
        self.horizontalLayout2_1.addWidget(self.useragent_choose)
        self.horizontalLayout2_1.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_13.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_13.addWidget(self.referer_lbl_custom)
        self.horizontalLayout2_13.addWidget(self.referer_choose_custom)
        self.horizontalLayout2_13.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_13.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_2.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_2.addWidget(self.group_lbl)
        self.horizontalLayout2_2.addWidget(self.group_text)
        self.horizontalLayout2_2.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_3.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_3.addWidget(self.hidden_lbl)
        self.horizontalLayout2_3.addWidget(self.hidden_chk)
        self.horizontalLayout2_3.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_4.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_4.addWidget(self.contrast_lbl)
        self.horizontalLayout2_4.addWidget(self.contrast_choose)
        self.horizontalLayout2_4.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_5.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_5.addWidget(self.brightness_lbl)
        self.horizontalLayout2_5.addWidget(self.brightness_choose)
        self.horizontalLayout2_5.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_6.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_6.addWidget(self.hue_lbl)
        self.horizontalLayout2_6.addWidget(self.hue_choose)
        self.horizontalLayout2_6.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_7.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_7.addWidget(self.saturation_lbl)
        self.horizontalLayout2_7.addWidget(self.saturation_choose)
        self.horizontalLayout2_7.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_8.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_8.addWidget(self.gamma_lbl)
        self.horizontalLayout2_8.addWidget(self.gamma_choose)
        self.horizontalLayout2_8.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_9.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_9.addWidget(self.videoaspect_lbl)
        self.horizontalLayout2_9.addWidget(self.videoaspect_choose)
        self.horizontalLayout2_9.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_10.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_10.addWidget(self.zoom_lbl)
        self.horizontalLayout2_10.addWidget(self.zoom_choose)
        self.horizontalLayout2_10.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_11.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_11.addWidget(self.panscan_lbl)
        self.horizontalLayout2_11.addWidget(self.panscan_choose)
        self.horizontalLayout2_11.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_11.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2_12.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_12.addWidget(self.epgname_btn)
        self.horizontalLayout2_12.addWidget(self.epgname_lbl)
        self.horizontalLayout2_12.addWidget(QtWidgets.QLabel("\n"))
        self.horizontalLayout2_12.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout3.addWidget(self.save_btn)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.wid)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout2)
        self.verticalLayout.addLayout(self.horizontalLayout2_1)
        self.verticalLayout.addLayout(self.horizontalLayout2_13)
        self.verticalLayout.addLayout(self.horizontalLayout2_2)
        self.verticalLayout.addLayout(self.horizontalLayout2_3)
        self.verticalLayout.addLayout(self.horizontalLayout2_4)
        self.verticalLayout.addLayout(self.horizontalLayout2_5)
        self.verticalLayout.addLayout(self.horizontalLayout2_6)
        self.verticalLayout.addLayout(self.horizontalLayout2_7)
        self.verticalLayout.addLayout(self.horizontalLayout2_8)
        self.verticalLayout.addLayout(self.horizontalLayout2_9)
        self.verticalLayout.addLayout(self.horizontalLayout2_10)
        self.verticalLayout.addLayout(self.horizontalLayout2_11)
        self.verticalLayout.addLayout(self.horizontalLayout2_12)
        self.verticalLayout.addLayout(self.horizontalLayout3)
        self.verticalLayout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )

        self.wid.setLayout(self.verticalLayout)

    def create_windows(self):
        _ = self._
        QtCore = self.QtCore
        QtWidgets = self.QtWidgets

        self.settings_win = self.SettingsScrollableWindow()
        self.settings_win.resize(800, 600)
        self.settings_win.setWindowTitle(_("Settings"))
        self.settings_win.setWindowIcon(self.main_icon)

        self.shortcuts_win = QtWidgets.QMainWindow()
        self.shortcuts_win.resize(720, 500)
        self.shortcuts_win.setWindowTitle(_("Shortcuts"))
        self.shortcuts_win.setWindowIcon(self.main_icon)

        self.shortcuts_central_widget = QtWidgets.QWidget(self.shortcuts_win)
        self.shortcuts_win.setCentralWidget(self.shortcuts_central_widget)

        self.shortcuts_grid_layout = QtWidgets.QVBoxLayout()
        self.shortcuts_central_widget.setLayout(self.shortcuts_grid_layout)

        self.shortcuts_table = QtWidgets.QTableWidget(self.shortcuts_win)
        # self.shortcuts_table.setColumnCount(3)
        self.shortcuts_table.setColumnCount(2)

        # self.shortcuts_table.setHorizontalHeaderLabels(
        #     [_('Description'), _('Shortcut'), "Header 3"]
        # )
        self.shortcuts_table.setHorizontalHeaderLabels(
            [_("Description"), _("Shortcut")]
        )

        self.shortcuts_table.horizontalHeaderItem(0).setTextAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.shortcuts_table.horizontalHeaderItem(1).setTextAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        # self.shortcuts_table.horizontalHeaderItem(2).setTextAlignment(
        #     QtCore.Qt.AlignmentFlag.AlignHCenter
        # )

        self.resettodefaults_btn = QtWidgets.QPushButton()
        self.resettodefaults_btn.setText(_("Reset to defaults"))

        self.shortcuts_grid_layout.addWidget(self.shortcuts_table)
        self.shortcuts_grid_layout.addWidget(self.resettodefaults_btn)

        self.shortcuts_win_2 = QtWidgets.QMainWindow()
        self.shortcuts_win_2.resize(300, 100)
        self.shortcuts_win_2.setWindowTitle(_("Modify shortcut"))
        self.shortcuts_win_2.setWindowIcon(self.main_icon)

        self.help_win = QtWidgets.QMainWindow()
        self.help_win.resize(500, 600)
        self.help_win.setWindowTitle(_("&About yuki-iptv").replace("&", ""))
        self.help_win.setWindowIcon(self.main_icon)

        self.license_win = QtWidgets.QMainWindow()
        self.license_win.resize(600, 600)
        self.license_win.setWindowTitle(_("License"))
        self.license_win.setWindowIcon(self.main_icon)

        self.sort_win = QtWidgets.QMainWindow()
        self.sort_win.resize(400, 500)
        self.sort_win.setWindowTitle(_("Channel sort"))
        self.sort_win.setWindowIcon(self.main_icon)

        self.channels_win = QtWidgets.QMainWindow()
        self.channels_win.resize(400, 250)
        self.channels_win.setWindowTitle(_("Video settings"))
        self.channels_win.setWindowIcon(self.main_icon)

        self.ext_win = QtWidgets.QMainWindow()
        self.ext_win.resize(300, 60)
        self.ext_win.setWindowTitle(_("Open in external player"))
        self.ext_win.setWindowIcon(self.main_icon)

        self.epg_win = QtWidgets.QMainWindow()
        self.epg_win.resize(1000, 600)
        self.epg_win.setWindowTitle(_("TV guide"))
        self.epg_win.setWindowIcon(self.main_icon)

        self.xtream_win = QtWidgets.QMainWindow()
        self.xtream_win.resize(400, 140)
        self.xtream_win.setWindowTitle("XTream")
        self.xtream_win.setWindowIcon(self.main_icon)

        self.scheduler_win = QtWidgets.QMainWindow()
        self.scheduler_win.resize(1200, 650)
        self.scheduler_win.setWindowTitle(_("Recording scheduler"))
        self.scheduler_win.setWindowIcon(self.main_icon)

        self.playlists_win = QtWidgets.QMainWindow()
        self.playlists_win.resize(500, 600)
        self.playlists_win.setWindowTitle(_("Playlists"))
        self.playlists_win.setWindowIcon(self.main_icon)

        self.playlists_win_edit = QtWidgets.QMainWindow()
        self.playlists_win_edit.resize(500, 180)
        self.playlists_win_edit.setWindowTitle(_("Playlists"))
        self.playlists_win_edit.setWindowIcon(self.main_icon)

        self.epg_select_win = QtWidgets.QMainWindow()
        self.epg_select_win.resize(400, 500)
        self.epg_select_win.setWindowTitle(_("TV guide"))
        self.epg_select_win.setWindowIcon(self.main_icon)

        self.tvguide_many_win = QtWidgets.QMainWindow()
        self.tvguide_many_win.setWindowTitle(_("TV guide"))
        self.tvguide_many_win.setWindowIcon(self.main_icon)
        self.tvguide_many_win.resize(1000, 700)

    def get_settings(self, old_uuid, SAVE_FOLDER_DEFAULT):
        udp_proxy_text = self.sudp.text()
        udp_proxy_starts = udp_proxy_text.startswith(
            "http://"
        ) or udp_proxy_text.startswith("https://")
        if udp_proxy_text and not udp_proxy_starts:
            udp_proxy_text = "http://" + udp_proxy_text

        sfld_text = self.sfld.text().strip()
        HOME_SYMBOL = "~"
        try:
            if "HOME" in os.environ:
                HOME_SYMBOL = os.environ["HOME"]
        except Exception:
            pass
        try:
            if sfld_text:
                if sfld_text[0] == "~":
                    sfld_text = sfld_text.replace("~", HOME_SYMBOL, 1)
        except Exception:
            pass

        hideplleftmousechk = self.hideplaylistbyleftmouseclick_flag.isChecked()

        settings_arr = {
            "m3u": self.m3u.strip(),
            "epg": self.epg.strip(),
            "deinterlace": self.sdei.isChecked(),
            "udp_proxy": udp_proxy_text,
            "save_folder": sfld_text if sfld_text else SAVE_FOLDER_DEFAULT,
            "epgoffset": self.soffset.value(),
            "hwaccel": self.shwaccel.isChecked(),
            "sort": self.sort_widget.currentIndex(),
            "cache_secs": self.scache1.value(),
            "epgdays": self.epgdays.value(),
            "ua": self.useragent_choose_2.text(),
            "mpv_options": self.mpv_options.text(),
            "donotupdateepg": self.donot_flag.isChecked(),
            "openprevchannel": self.openprevchannel_flag.isChecked(),
            "hidempv": self.hidempv_flag.isChecked(),
            "hideepgpercentage": self.hideepgpercentage_flag.isChecked(),
            "hideepgfromplaylist": self.hideepgfromplaylist_flag.isChecked(),
            "multicastoptimization": self.multicastoptimization_flag.isChecked(),
            "hidebitrateinfo": self.hidebitrateinfo_flag.isChecked(),
            "styleredefoff": self.styleredefoff_flag.isChecked(),
            "volumechangestep": self.volumechangestep_choose.value(),
            "mouseswitchchannels": self.mouseswitchchannels_flag.isChecked(),
            "autoreconnection": self.autoreconnection_flag.isChecked(),
            "showplaylistmouse": self.showplaylistmouse_flag.isChecked(),
            "channellogos": self.channellogos_select.currentIndex(),
            "nocacheepg": self.nocacheepg_flag.isChecked(),
            "scrrecnosubfolders": self.scrrecnosubfolders_flag.isChecked(),
            "hidetvprogram": self.hidetvprogram_flag.isChecked(),
            "showcontrolsmouse": self.showcontrolsmouse_flag.isChecked(),
            "catchupenable": self.catchupenable_flag.isChecked(),
            "hidechannellogos": self.hidechannellogos_flag.isChecked(),
            "hideplaylistbyleftmouseclick": hideplleftmousechk,
            "rewindenable": self.rewindenable_flag.isChecked(),
            "flpopacity": self.flpopacity_input.value(),
            "panelposition": self.panelposition_choose.currentIndex(),
            "videoaspect": self.videoaspect_def_choose.currentIndex(),
            "zoom": self.zoom_def_choose.currentIndex(),
            "panscan": self.panscan_def_choose.value(),
            "referer": self.referer_choose.text(),
            "uuid": old_uuid,
        }

        return settings_arr

    def create_rewind(self, win, Slider, BCOLOR):
        _ = self._
        QtCore = self.QtCore
        QtWidgets = self.QtWidgets

        self.rewind = QtWidgets.QWidget(win)
        self.rewind.setStyleSheet("background-color: " + BCOLOR)
        self.rewind.setFont(self.font_12_bold)
        self.rewind.move(50, 50)
        self.rewind.resize(self.rewind.width(), self.rewind.height() + 5)

        self.rewind_layout = QtWidgets.QVBoxLayout()
        self.rewind_layout.setContentsMargins(100, 0, 50, 0)
        self.rewind_layout.setSpacing(0)
        self.rewind_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.rewind_label = QtWidgets.QLabel(_("Rewind"))
        self.rewind_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rewind_label.setFont(self.font_bold)
        self.rewind_label.setStyleSheet("color: pink")

        self.rewind_slider = Slider(QtCore.Qt.Orientation.Horizontal)
        self.rewind_slider.setTickInterval(1)

        self.rewind_layout.addWidget(self.rewind_label)
        self.rewind_layout.addWidget(self.rewind_slider)

        self.rewind.setLayout(self.rewind_layout)
        self.rewind.hide()

    def create2(
        self,
        win,
        page_count,
        channelfilter_clicked,
        channelfilter_do,
        get_of_txt,
        page_change,
        tvguide_many_clicked,
        MyLineEdit,
        ICONS_FOLDER,
        playmode_selector,
        combobox,
        movies_combobox,
        loading,
    ):
        _ = self._
        QtCore = self.QtCore
        QtWidgets = self.QtWidgets

        self.tvguide_many_widget = QtWidgets.QWidget()
        self.tvguide_many_layout = QtWidgets.QGridLayout()
        self.tvguide_many_widget.setLayout(self.tvguide_many_layout)
        self.tvguide_many_win.setCentralWidget(self.tvguide_many_widget)

        self.tvguide_many_table = QtWidgets.QTableWidget()
        self.tvguide_many_layout.addWidget(self.tvguide_many_table, 0, 0)

        self.tvguide_many = QtWidgets.QPushButton()
        self.tvguide_many.setText(_("TV guide"))
        self.tvguide_many.clicked.connect(tvguide_many_clicked)

        self.tvguide_widget = QtWidgets.QWidget()
        self.tvguide_layout = QtWidgets.QHBoxLayout()
        self.tvguide_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.tvguide_layout.addWidget(self.tvguide_many)
        self.tvguide_widget.setLayout(self.tvguide_layout)

        self.channelfilter = MyLineEdit()
        self.channelfilter.click_event.connect(channelfilter_clicked)
        self.channelfilter.setPlaceholderText(_("Search channel"))
        self.channelfiltersearch = QtWidgets.QPushButton()
        self.channelfiltersearch.setText(_("Search"))
        self.channelfiltersearch.clicked.connect(channelfilter_do)
        self.channelfilter.returnPressed.connect(channelfilter_do)
        self.widget3 = QtWidgets.QWidget()
        self.layout3 = QtWidgets.QHBoxLayout()
        self.layout3.addWidget(self.channelfilter)
        self.layout3.addWidget(self.channelfiltersearch)
        self.widget3.setLayout(self.layout3)
        self.widget4 = QtWidgets.QWidget()
        self.layout4 = QtWidgets.QHBoxLayout()
        self.layout4.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.page_lbl = QtWidgets.QLabel("{}:".format(_("Page")))
        self.of_lbl = QtWidgets.QLabel()
        self.page_box = QtWidgets.QSpinBox()
        self.page_box.setSuffix("        ")
        self.page_box.setMinimum(1)
        self.page_box.setMaximum(page_count)
        self.page_box.setStyleSheet(
            """
            QSpinBox::down-button  {
              subcontrol-origin: margin;
              subcontrol-position: center left;
              left: 1px;
              image: url("""
            + str(Path("yuki_iptv", ICONS_FOLDER, "leftarrow.png"))
            + """);
              height: 24px;
              width: 24px;
            }

            QSpinBox::up-button  {
              subcontrol-origin: margin;
              subcontrol-position: center right;
              right: 1px;
              image: url("""
            + str(Path("yuki_iptv", ICONS_FOLDER, "rightarrow.png"))
            + """);
              height: 24px;
              width: 24px;
            }
        """
        )
        self.page_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.page_box.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.of_lbl.setText(get_of_txt(page_count))

        self.page_box.valueChanged.connect(page_change)
        self.layout4.addWidget(self.page_lbl)
        self.layout4.addWidget(self.page_box)
        self.layout4.addWidget(self.of_lbl)
        self.widget4.setLayout(self.layout4)
        self.layout = QtWidgets.QGridLayout()
        self.layout.setVerticalSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)
        self.widget.layout().addWidget(QtWidgets.QLabel())
        self.widget.layout().addWidget(playmode_selector)
        self.widget.layout().addWidget(combobox)
        # == Movies start ==
        movies_combobox.hide()
        self.widget.layout().addWidget(movies_combobox)
        # == Movies end ==
        self.widget.layout().addWidget(self.widget3)
        self.widget.layout().addWidget(win.listWidget)
        # Movies start
        win.moviesWidget.hide()
        self.widget.layout().addWidget(win.moviesWidget)
        # Movies end
        # Series start
        win.seriesWidget.hide()
        self.widget.layout().addWidget(win.seriesWidget)
        # Series end
        self.widget.layout().addWidget(self.widget4)
        self.widget.layout().addWidget(self.channel)
        self.widget.layout().addWidget(loading)

    def create3(self, win, centerwidget, ICONS_FOLDER):
        _ = self._
        QtCore = self.QtCore
        QtWidgets = self.QtWidgets
        QtGui = self.QtGui

        self.channel = QtWidgets.QLabel(_("No channel selected"))
        self.channel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.channel.setStyleSheet("color: green")
        self.channel.setFont(self.font_11_bold)
        self.channel.resize(200, 30)

        self.loading1 = QtWidgets.QLabel(win)
        self.loading_movie = QtGui.QMovie(
            str(Path("yuki_iptv", ICONS_FOLDER, "loading.gif"))
        )
        self.loading1.setMovie(self.loading_movie)
        self.loading1.setStyleSheet("background-color: white;")
        self.loading1.resize(32, 32)
        self.loading1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        centerwidget(self.loading1)
        self.loading1.hide()

        self.loading2 = QtWidgets.QLabel(win)
        self.loading_movie2 = QtGui.QMovie(
            str(Path("yuki_iptv", ICONS_FOLDER, "recordwait.gif"))
        )
        self.loading2.setMovie(self.loading_movie2)
        self.loading2.setToolTip(_("Processing record..."))
        self.loading2.resize(32, 32)
        self.loading2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        centerwidget(self.loading2, 50)
        self.loading2.hide()
        self.loading_movie2.stop()

        self.lbl2_offset = 15
        self.tvguide_lbl_offset = 30 + self.lbl2_offset

        self.lbl2 = QtWidgets.QLabel(win)
        self.lbl2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl2.setStyleSheet("color: #e0071a")
        self.lbl2.setWordWrap(True)
        self.lbl2.resize(230, 30)
        self.lbl2.move(0, self.lbl2_offset)
        self.lbl2.hide()

    def create_scheduler_widgets(self, current_time):
        _ = self._
        QtCore = self.QtCore
        QtWidgets = self.QtWidgets

        self.scheduler_widget = QtWidgets.QWidget()
        self.scheduler_layout = QtWidgets.QGridLayout()
        self.scheduler_clock = QtWidgets.QLabel(current_time)
        self.scheduler_clock.setFont(self.font_11_bold)
        self.scheduler_clock.setStyleSheet("color: green")
        self.plannedrec_lbl = QtWidgets.QLabel("{}:".format(_("Planned recordings")))
        self.activerec_lbl = QtWidgets.QLabel("{}:".format(_("Active recordings")))
        self.statusrec_lbl = QtWidgets.QLabel()
        self.statusrec_lbl.setFont(self.font_bold)
        self.choosechannel_lbl = QtWidgets.QLabel("{}:".format(_("Choose channel")))
        self.choosechannel_ch = QtWidgets.QComboBox()
        self.tvguide_sch = QtWidgets.QListWidget()
        self.addrecord_btn = QtWidgets.QPushButton(_("Add"))
        self.delrecord_btn = QtWidgets.QPushButton(_("Remove"))

        self.schedulerchannelfilter = QtWidgets.QLineEdit()
        self.schedulerchannelfilter.setPlaceholderText(_("Search channel"))
        self.schedulerchannelfiltersearch = QtWidgets.QPushButton()
        self.schedulerchannelfiltersearch.setText(_("Search"))

        self.schedulerchannelwidget = QtWidgets.QWidget()
        self.schedulerchannellayout = QtWidgets.QHBoxLayout()
        self.schedulerchannellayout.addWidget(self.schedulerchannelfilter)
        self.schedulerchannellayout.addWidget(self.schedulerchannelfiltersearch)
        self.schedulerchannelwidget.setLayout(self.schedulerchannellayout)

        self.scheduler_layout.addWidget(self.scheduler_clock, 0, 0)
        self.scheduler_layout.addWidget(self.choosechannel_lbl, 1, 0)
        self.scheduler_layout.addWidget(self.schedulerchannelwidget, 2, 0)
        self.scheduler_layout.addWidget(self.choosechannel_ch, 3, 0)
        self.scheduler_layout.addWidget(self.tvguide_sch, 4, 0)

        self.starttime_lbl = QtWidgets.QLabel("{}:".format(_("Start record time")))
        self.endtime_lbl = QtWidgets.QLabel("{}:".format(_("End record time")))
        self.starttime_w = QtWidgets.QDateTimeEdit()
        self.starttime_w.setDateTime(
            QtCore.QDateTime.fromString(
                time.strftime("%d.%m.%Y %H:%M", time.localtime()), "d.M.yyyy hh:mm"
            )
        )
        self.endtime_w = QtWidgets.QDateTimeEdit()
        self.endtime_w.setDateTime(
            QtCore.QDateTime.fromString(
                time.strftime("%d.%m.%Y %H:%M", time.localtime(time.time() + 60)),
                "d.M.yyyy hh:mm",
            )
        )

        self.praction_lbl = QtWidgets.QLabel("{}:".format(_("Post-recording\naction")))
        self.praction_choose = QtWidgets.QComboBox()
        self.praction_choose.addItem(_("Nothing to do"))
        self.praction_choose.addItem(_("Press Stop"))

        self.schedulers = QtWidgets.QListWidget()
        self.activerec_list = QtWidgets.QListWidget()

        self.scheduler_layout_2 = QtWidgets.QGridLayout()
        self.scheduler_layout_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.scheduler_layout_2.addWidget(self.starttime_lbl, 0, 0)
        self.scheduler_layout_2.addWidget(self.starttime_w, 1, 0)
        self.scheduler_layout_2.addWidget(self.endtime_lbl, 2, 0)
        self.scheduler_layout_2.addWidget(self.endtime_w, 3, 0)
        self.scheduler_layout_2.addWidget(self.addrecord_btn, 4, 0)
        self.scheduler_layout_2.addWidget(self.delrecord_btn, 5, 0)
        self.scheduler_layout_2.addWidget(QtWidgets.QLabel(), 6, 0)
        self.scheduler_layout_2.addWidget(self.praction_lbl, 7, 0)
        self.scheduler_layout_2.addWidget(self.praction_choose, 8, 0)

        self.scheduler_layout_3 = QtWidgets.QGridLayout()
        self.scheduler_layout_3.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.scheduler_layout_3.addWidget(self.statusrec_lbl, 0, 0)
        self.scheduler_layout_3.addWidget(self.plannedrec_lbl, 1, 0)
        self.scheduler_layout_3.addWidget(self.schedulers, 2, 0)

        self.scheduler_layout_4 = QtWidgets.QGridLayout()
        self.scheduler_layout_4.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.scheduler_layout_4.addWidget(self.activerec_lbl, 0, 0)
        self.scheduler_layout_4.addWidget(self.activerec_list, 1, 0)

        self.scheduler_layout_main_w = QtWidgets.QWidget()
        self.scheduler_layout_main_w.setLayout(self.scheduler_layout)

        self.scheduler_layout_main_w2 = QtWidgets.QWidget()
        self.scheduler_layout_main_w2.setLayout(self.scheduler_layout_2)

        self.scheduler_layout_main_w3 = QtWidgets.QWidget()
        self.scheduler_layout_main_w3.setLayout(self.scheduler_layout_3)

        self.scheduler_layout_main_w4 = QtWidgets.QWidget()
        self.scheduler_layout_main_w4.setLayout(self.scheduler_layout_4)

        self.scheduler_layout_main1 = QtWidgets.QHBoxLayout()
        self.scheduler_layout_main1.addWidget(self.scheduler_layout_main_w)
        self.scheduler_layout_main1.addWidget(self.scheduler_layout_main_w2)
        self.scheduler_layout_main1.addWidget(self.scheduler_layout_main_w3)
        self.scheduler_layout_main1.addWidget(self.scheduler_layout_main_w4)
        self.scheduler_widget.setLayout(self.scheduler_layout_main1)

        self.warning_lbl = QtWidgets.QLabel(
            _("Recording of two channels simultaneously is not available!")
        )
        self.warning_lbl.setFont(self.font_11_bold)
        self.warning_lbl.setStyleSheet("color: red")
        self.warning_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.scheduler_layout_main = QtWidgets.QVBoxLayout()
        self.scheduler_layout_main.addWidget(self.scheduler_widget)
        self.scheduler_widget_main = QtWidgets.QWidget()
        self.scheduler_widget_main.setLayout(self.scheduler_layout_main)

        self.scheduler_win.setCentralWidget(self.scheduler_widget_main)

    def create4(self, keyseq, StreaminfoWin, ICONS_FOLDER):
        _ = self._
        QtCore = self.QtCore
        QtWidgets = self.QtWidgets
        QtGui = self.QtGui

        self.la_sl = QtWidgets.QLabel()
        self.la_sl.setFont(self.font_bold)
        self.la_sl.setText(_("Press the key combination\nyou want to assign"))

        self.keyseq_cancel = QtWidgets.QPushButton(_("Cancel"))
        self.keyseq_ok = QtWidgets.QPushButton(_("OK"))

        self.shortcuts_win_2_widget_2 = QtWidgets.QWidget()
        self.shortcuts_win_2_layout_2 = QtWidgets.QHBoxLayout()
        self.shortcuts_win_2_layout_2.addWidget(self.keyseq_cancel)
        self.shortcuts_win_2_layout_2.addWidget(self.keyseq_ok)
        self.shortcuts_win_2_widget_2.setLayout(self.shortcuts_win_2_layout_2)

        self.shortcuts_win_2_widget = QtWidgets.QWidget()
        self.shortcuts_win_2_layout = QtWidgets.QVBoxLayout()
        self.shortcuts_win_2_layout.addWidget(self.la_sl)
        self.shortcuts_win_2_layout.addWidget(keyseq)
        self.shortcuts_win_2_layout.addWidget(self.shortcuts_win_2_widget_2)
        self.shortcuts_win_2_widget.setLayout(self.shortcuts_win_2_layout)

        self.shortcuts_win_2.setCentralWidget(self.shortcuts_win_2_widget)

        self.streaminfo_win = StreaminfoWin()
        self.streaminfo_win.setWindowIcon(self.main_icon)

        self.tvguidechannelfilter = QtWidgets.QLineEdit()
        self.tvguidechannelfilter.setPlaceholderText(_("Search channel"))
        self.tvguidechannelfiltersearch = QtWidgets.QPushButton()
        self.tvguidechannelfiltersearch.setText(_("Search"))

        self.tvguidechannelwidget = QtWidgets.QWidget()
        self.tvguidechannellayout = QtWidgets.QHBoxLayout()
        self.tvguidechannellayout.addWidget(self.tvguidechannelfilter)
        self.tvguidechannellayout.addWidget(self.tvguidechannelfiltersearch)
        self.tvguidechannelwidget.setLayout(self.tvguidechannellayout)

        self.showonlychplaylist_lbl = QtWidgets.QLabel()
        self.showonlychplaylist_lbl.setText(
            "{}:".format(_("Show only channels in playlist"))
        )
        self.showonlychplaylist_chk = QtWidgets.QCheckBox()
        self.showonlychplaylist_chk.setChecked(True)
        self.epg_win_checkbox = QtWidgets.QComboBox()

        self.epg_win_count = QtWidgets.QLabel()
        self.epg_win_count.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.epg_select_date = QtWidgets.QCalendarWidget()
        self.epg_select_date.setDateRange(
            QtCore.QDate().currentDate().addDays(-31),
            QtCore.QDate().currentDate().addDays(31),
        )
        self.epg_select_date.setMaximumWidth(300)

        self.epg_win_1_widget = QtWidgets.QWidget()
        self.epg_win_1_layout = QtWidgets.QHBoxLayout()
        self.epg_win_1_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.epg_win_1_layout.addWidget(self.showonlychplaylist_lbl)
        self.epg_win_1_layout.addWidget(self.showonlychplaylist_chk)
        self.epg_win_1_widget.setLayout(self.epg_win_1_layout)

        self.tvguide_lbl_2 = self.ScrollableLabel()

        self.epg_win_widget2 = QtWidgets.QWidget()
        self.epg_win_layout2 = QtWidgets.QHBoxLayout()
        self.epg_win_layout2.addWidget(self.epg_select_date)
        self.epg_win_layout2.addWidget(self.tvguide_lbl_2)
        self.epg_win_widget2.setLayout(self.epg_win_layout2)

        self.epg_win_widget = QtWidgets.QWidget()
        self.epg_win_layout = QtWidgets.QVBoxLayout()
        self.epg_win_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.epg_win_layout.addWidget(self.epg_win_1_widget)
        self.epg_win_layout.addWidget(self.tvguidechannelwidget)
        self.epg_win_layout.addWidget(self.epg_win_checkbox)
        self.epg_win_layout.addWidget(self.epg_win_count)
        self.epg_win_layout.addWidget(self.epg_win_widget2)
        self.epg_win_widget.setLayout(self.epg_win_layout)
        self.epg_win.setCentralWidget(self.epg_win_widget)

        self.name_label_1 = QtWidgets.QLabel("{}:".format(_("Name")))
        self.m3u_label_1 = QtWidgets.QLabel("{}:".format(_("M3U / XSPF playlist")))
        self.epg_label_1 = QtWidgets.QLabel("{}:".format(_("TV guide\naddress")))
        self.name_edit_1 = QtWidgets.QLineEdit()
        self.m3u_edit_1 = QtWidgets.QLineEdit()
        self.m3u_edit_1.setPlaceholderText(_("Path to file or URL"))
        self.epg_edit_1 = QtWidgets.QLineEdit()
        self.epg_edit_1.setPlaceholderText(_("Path to file or URL"))
        self.m3u_file_1 = QtWidgets.QPushButton()
        self.m3u_file_1.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", ICONS_FOLDER, "file.png")))
        )
        self.epg_file_1 = QtWidgets.QPushButton()
        self.epg_file_1.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", ICONS_FOLDER, "file.png")))
        )
        self.save_btn_1 = QtWidgets.QPushButton(_("Save"))
        self.save_btn_1.setStyleSheet("font-weight: bold; color: green;")
        self.soffset_1 = QtWidgets.QDoubleSpinBox()
        self.soffset_1.setMinimum(-240)
        self.soffset_1.setMaximum(240)
        self.soffset_1.setSingleStep(1)
        self.soffset_1.setDecimals(1)
        self.offset_label_1 = QtWidgets.QLabel("{}:".format(_("TV guide offset")))
        self.offset_label_hours = QtWidgets.QLabel(
            (gettext.ngettext("%d hour", "%d hours", 0) % 0).replace("0 ", "")
        )

        self.xtream_btn_1 = QtWidgets.QPushButton("XTream")

        self.playlists_win_edit_widget = QtWidgets.QWidget()
        self.playlists_win_edit_layout = QtWidgets.QGridLayout()
        self.playlists_win_edit_layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.playlists_win_edit_layout.addWidget(self.name_label_1, 0, 0)
        self.playlists_win_edit_layout.addWidget(self.name_edit_1, 0, 1)
        self.playlists_win_edit_layout.addWidget(self.m3u_label_1, 1, 0)
        self.playlists_win_edit_layout.addWidget(self.m3u_edit_1, 1, 1)
        self.playlists_win_edit_layout.addWidget(self.m3u_file_1, 1, 2)
        self.playlists_win_edit_layout.addWidget(self.xtream_btn_1, 2, 0)
        self.playlists_win_edit_layout.addWidget(self.epg_label_1, 3, 0)
        self.playlists_win_edit_layout.addWidget(self.epg_edit_1, 3, 1)
        self.playlists_win_edit_layout.addWidget(self.epg_file_1, 3, 2)
        self.playlists_win_edit_layout.addWidget(self.offset_label_1, 4, 0)
        self.playlists_win_edit_layout.addWidget(self.soffset_1, 4, 1)
        self.playlists_win_edit_layout.addWidget(self.offset_label_hours, 4, 2)
        self.playlists_win_edit_layout.addWidget(self.save_btn_1, 5, 1)
        self.playlists_win_edit_widget.setLayout(self.playlists_win_edit_layout)
        self.playlists_win_edit.setCentralWidget(self.playlists_win_edit_widget)

        self.yuki_iptv_icon = QtWidgets.QLabel()
        self.yuki_iptv_icon.setPixmap(self.tv_icon.pixmap(QtCore.QSize(32, 32)))
        self.yuki_iptv_label = QtWidgets.QLabel()
        self.yuki_iptv_label.setFont(self.font_11_bold)
        self.yuki_iptv_label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.yuki_iptv_label.setText(
            '<br>&nbsp;<span style="color: #b35900;">yuki-iptv</span><br>'
        )

        self.yuki_iptv_widget = QtWidgets.QWidget()
        self.yuki_iptv_layout = QtWidgets.QHBoxLayout()
        self.yuki_iptv_layout.addWidget(self.yuki_iptv_icon)
        self.yuki_iptv_layout.addWidget(self.yuki_iptv_label)
        self.yuki_iptv_widget.setLayout(self.yuki_iptv_layout)

        self.yuki_iptv_layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )

        self.esw_input = QtWidgets.QLineEdit()
        self.esw_input.setPlaceholderText(_("Search"))
        self.esw_button = QtWidgets.QPushButton()
        self.esw_button.setText(_("Search"))
        self.esw_select = QtWidgets.QListWidget()

        self.esw_widget = QtWidgets.QWidget()
        self.esw_widget_layout = QtWidgets.QHBoxLayout()
        self.esw_widget_layout.addWidget(self.esw_input)
        self.esw_widget_layout.addWidget(self.esw_button)
        self.esw_widget.setLayout(self.esw_widget_layout)

        self.epg_select_win_widget = QtWidgets.QWidget()
        self.epg_select_win_layout = QtWidgets.QVBoxLayout()
        self.epg_select_win_layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.epg_select_win_layout.addWidget(self.esw_widget, 0)
        self.epg_select_win_layout.addWidget(self.esw_select, 1)
        self.epg_select_win_widget.setLayout(self.epg_select_win_layout)
        self.epg_select_win.setCentralWidget(self.epg_select_win_widget)

        self.ext_player_txt = QtWidgets.QLineEdit()
        self.ext_open_btn = QtWidgets.QPushButton()
        self.ext_open_btn.setText(_("Open"))
        self.ext_widget = QtWidgets.QWidget()
        self.ext_layout = QtWidgets.QGridLayout()
        self.ext_layout.addWidget(self.ext_player_txt, 0, 0)
        self.ext_layout.addWidget(self.ext_open_btn, 0, 1)
        self.ext_layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.ext_widget.setLayout(self.ext_layout)
        self.ext_win.setCentralWidget(self.ext_widget)

        self.playlists_list = QtWidgets.QListWidget()
        self.playlists_select = QtWidgets.QPushButton(_("Select"))
        self.playlists_select.setStyleSheet("font-weight: bold; color: green;")
        self.playlists_add = QtWidgets.QPushButton(_("Add"))
        self.playlists_edit = QtWidgets.QPushButton(_("Edit"))
        self.playlists_delete = QtWidgets.QPushButton(_("Delete"))
        self.playlists_favourites = QtWidgets.QPushButton(_("Favourites+"))
        self.playlists_settings = QtWidgets.QPushButton(_("Settings"))
        self.playlists_settings.setStyleSheet("color: blue;")

        self.playlists_win_widget = QtWidgets.QWidget()
        self.playlists_win_layout = QtWidgets.QGridLayout()
        self.playlists_win_layout.addWidget(self.playlists_add, 0, 0)
        self.playlists_win_layout.addWidget(self.playlists_edit, 0, 1)
        self.playlists_win_layout.addWidget(self.playlists_delete, 0, 2)
        self.playlists_win_layout.addWidget(self.playlists_favourites, 0, 3)
        self.playlists_win_widget.setLayout(self.playlists_win_layout)

        self.playlists_win_widget_main = QtWidgets.QWidget()
        self.playlists_win_widget_main_layout = QtWidgets.QVBoxLayout()
        self.playlists_win_widget_main_layout.addWidget(self.yuki_iptv_widget)
        self.playlists_win_widget_main_layout.addWidget(self.playlists_list)
        self.playlists_win_widget_main_layout.addWidget(self.playlists_select)
        self.playlists_win_widget_main_layout.addWidget(self.playlists_win_widget)
        self.playlists_win_widget_main_layout.addWidget(self.playlists_settings)
        self.playlists_win_widget_main.setLayout(self.playlists_win_widget_main_layout)

        self.playlists_win.setCentralWidget(self.playlists_win_widget_main)

    def create_sort_widgets(self):
        _ = self._
        QtCore = self.QtCore
        QtWidgets = self.QtWidgets

        self.close_sort_btn = QtWidgets.QPushButton(_("Close"))
        self.close_sort_btn.clicked.connect(self.sort_win.hide)
        self.close_sort_btn.setStyleSheet("color: red;")

        self.save_sort_btn = QtWidgets.QPushButton(_("Save"))
        self.save_sort_btn.setStyleSheet("font-weight: bold; color: green;")

        self.sort_label = QtWidgets.QLabel(
            _("Do not forget\nto set custom sort order in settings!")
        )
        self.sort_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.sort_widget3 = QtWidgets.QWidget()

        self.sort_widget4 = QtWidgets.QWidget()
        self.sort_widget4_layout = QtWidgets.QHBoxLayout()
        self.sort_widget4_layout.addWidget(self.save_sort_btn)
        self.sort_widget4_layout.addWidget(self.close_sort_btn)
        self.sort_widget4.setLayout(self.sort_widget4_layout)

        self.sort_widget_main = QtWidgets.QWidget()
        self.sort_layout = QtWidgets.QVBoxLayout()
        self.sort_layout.addWidget(self.sort_label)
        self.sort_layout.addWidget(self.sort_widget3)
        self.sort_layout.addWidget(self.sort_widget4)
        self.sort_layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.sort_widget_main.setLayout(self.sort_layout)
        self.sort_win.setCentralWidget(self.sort_widget_main)

    def create_sort_widgets2(self, ICONS_FOLDER):
        _ = self._
        QtCore = self.QtCore
        QtWidgets = self.QtWidgets
        QtGui = self.QtGui

        self.sort_upbtn = QtWidgets.QPushButton()
        self.sort_upbtn.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", ICONS_FOLDER, "arrow-up.png")))
        )
        self.sort_downbtn = QtWidgets.QPushButton()
        self.sort_downbtn.setIcon(
            QtGui.QIcon(str(Path("yuki_iptv", ICONS_FOLDER, "arrow-down.png")))
        )

        self.sort_widget2 = QtWidgets.QWidget()
        self.sort_layout2 = QtWidgets.QVBoxLayout()
        self.sort_layout2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sort_layout2.addWidget(self.sort_upbtn)
        self.sort_layout2.addWidget(self.sort_downbtn)
        self.sort_widget2.setLayout(self.sort_layout2)

        self.sort_list = QtWidgets.QListWidget()
        self.sort_layout3 = QtWidgets.QHBoxLayout()
        self.sort_layout3.addWidget(self.sort_list)
        self.sort_layout3.addWidget(self.sort_widget2)
        self.sort_widget3.setLayout(self.sort_layout3)

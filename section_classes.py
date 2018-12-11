# Gloomhaven tracker app: Element Definitions
# Created by: Joshua Meade
# Created on: 9/25/18

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QComboBox, QProgressBar, QListWidget, QTableWidget, \
    QTableWidgetItem


# <editor-fold desc="Title & Nav Bar Classes">
class TitleBar(QLabel):
    def __init__(self, *args):
        super(QLabel, self).__init__(*args)

        self.resize(self.parent().geometry().width(), self.parent().geometry().height() * 0.05)
        self.setText("Gloomhaven Tracker Application.      Please Load or Create a Campaign.")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.lightGray)
        self.setPalette(palette)


class SysNavBar(QWidget):
    def __init__(self, *args):
        super(QWidget, self).__init__(*args)

        self.resize(self.parent().geometry().width(), self.parent().geometry().height() * 0.0625)
        self.move(0, self.parent().geometry().height() * 0.9375)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtCore.Qt.darkRed)
        self.setPalette(palette)

        self.app_btn = self.SysNavButton("Application", 0, 0, parent=self)
        self.city_btn = self.SysNavButton("Gloomhaven", 1, 1, parent=self)
        self.party_btn = self.SysNavButton("Party", 2, 2, parent=self)
        self.char_btn = self.SysNavButton("Characters", 3, 3, parent=self)
        self.scene_btn = self.SysNavButton("Scenario", 4, 4, parent=self)
        self.save_exit_btn = self.SysNavButton("Save && Exit", 5, 5, parent=self)

    class SysNavButton(QPushButton):
        def __init__(self, text, position, connect, **kwargs):
            super(QPushButton, self).__init__(**kwargs)
            nav_bar = self.parent()
            mane = nav_bar.parent()

            self.spacer = QWidget(self.parent())
            self.spacer.resize(self.parent().geometry().width() * (1/6), self.parent().geometry().height())

            self.tall = self.spacer.geometry().height() * .75
            self.wide = self.spacer.geometry().width() * .75
            self.resize(self.wide, self.tall)
            self.move((self.spacer.geometry().width() * .125) + (position * self.spacer.geometry().width()),
                      self.spacer.geometry().height() * .145)
            self.setText(text)
            self.clicked.connect(lambda state, main=mane, button=connect: mane.btn.sys_nav(main, button))
            self.setDisabled(True)
            self.spacer.setParent(None)
# </editor-fold>


# <editor-fold desc="ContentPane Parent Class">
class ContentPane(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.mane = self.parent()

        self.resize(self.mane.geometry().width(), self.mane.geometry().height() * 0.8875)
        self.move(0, self.mane.geometry().height() * 0.05)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtCore.Qt.darkCyan)
        self.setPalette(palette)
        self.side = self.SidePane(self)
        self.view_area = (self.geometry().width() * (5/6), self.geometry().height())
        self.content_groups = []

    class SidePane(QWidget):
        def __init__(self, parent):
            super(QWidget, self).__init__(parent)
            self.mane = self.parent().mane

            self.resize(self.parent().geometry().width() * (1/6), self.parent().geometry().height())
            self.move(self.parent().geometry().width() * (5/6), 0)

            self.setAutoFillBackground(True)
            palette = self.palette()
            palette.setColor(QtGui.QPalette.Window, QtCore.Qt.darkGreen)
            self.setPalette(palette)

    def update_groups(self):
        for i in self.content_groups:
            i.update_values()

    def disappear(self):
        self.setVisible(False)
# </editor-fold>


class ModuleApp(ContentPane):
    def __init__(self, *args):
        super(ModuleApp, self).__init__(*args)
        cg = ContentGroup
        cgi = ContentGroup.ContentItemDescriptor
        cgv = ContentGroup.ContentItemValue

        self.label_1 = SidePaneLabel("Campaign", 0, parent=self.side)
        self.new = SidePaneButton("New", 1, "camp_new", parent=self.side)
        self.load = SidePaneButton("Load", 2, "camp_load", parent=self.side)
        self.save = SidePaneButton("Save", 3, "camp_save", parent=self.side)
        self.help = SidePaneButton("Help", 12, "app_help", parent=self.side)
        self.about = SidePaneButton("About", 13, "app_about", parent=self.side)

        self.app_data = cg(self, (30, 10), (1, 1), "Gloomhaven Tracker Application")
        self.app_author = cgi(self.app_data, ("Created by: The TLB"), (1.5, 3))
        self.app_data_version = cgi(self.app_data, ("Version: [ver #]"), (2.25, 3))
        self.app_data_update = cgi(self.app_data, ("Last Updated: [date]"), (3, 3))


class ModuleChar(ContentPane):
    def __init__(self, *args):
        super().__init__(*args)

        self.setVisible(False)
        self.side.setParent(None)
        self.view_area = (self.geometry().width(), self.geometry().height())

        self.char_tiles = CharTiles(self)


class ModuleCity(ContentPane):
    def __init__(self, *args):
        super(ModuleCity, self).__init__(*args)
        cg = ContentGroup
        cgi = ContentGroup.ContentItemDescriptor
        cgv = ContentGroup.ContentItemValue
        cgp = ContentGroup.ContentProgressBar
        cgb = ContentGroup.ContentActionButton
        cgtb = ContentGroup.ContentTitleButton
        cgl = ContentGroup.ContentList

        self.party_label = SidePaneLabel("Party Actions", 0, parent=self.side)
        self.party_return = SidePaneButton("To Town", 1, "city_return", parent=self.side)
        self.party_explore = SidePaneButton("Explore", 2, "city_explore", parent=self.side)

        self.active_char_label = SidePaneLabel("Active Char", 4, parent=self.side)
        self.active_char_toggle = SidePaneButtonSelector(self.side, "None", 5, "char_toggle")
        self.active_char_shop = SidePaneButton("Shop", 6, "set_up_shop", parent=self.side)
        self.active_char_donate = SidePaneButton("Donate", 7, "city_donate", parent=self.side)
        self.active_char_manage = SidePaneButton("Manage", 8, "char_manage", parent=self.side)
        self.active_char_solo = SidePaneButton("Solo", 9, "char_solo", parent=self.side)

        self.setVisible(False)

        self.prosperity = cg(self, (20, 13), (2, 1), "Prosperity")
        self.prosperity_level_desc = cgi(self.prosperity, "Level: ", (1, 5))
        self.prosperity_level_val = cgv(self.prosperity, ("camp", "prosperity_level"), (1, 5))
        self.prosperity_points_desc = cgi(self.prosperity, "Points: ", (2, 5))
        self.prosperity_points_val = cgv(self.prosperity, ("camp", "prosperity_points"), (2, 5))
        self.prosperity_prog_label = cgi(self.prosperity, "Progress to next level:", (3, 5))
        self.prosperity_prog_bar = cgp(self.prosperity, ("camp", "prosperity_minimum", "prosperity_needed",
                                                         "prosperity_points"), (4, 5))
        self.prosperity_loss_btn = cgb(self.prosperity, "-", "prosp_loss_misc", (5, 5), (1, 2))
        self.prosperity_gain_btn = cgb(self.prosperity, "+", "prosp_gain_misc", (5, 5), (2, 2))

        self.donations = cg(self, (20, 13), (2, 17), "Donations")
        self.donation_total_desc = cgi(self.donations, "Donations: ", (1, 5))
        self.donation_total_val = cgv(self.donations, ("camp", "donation_total"), (1, 5))
        self.donation_prog_label = cgi(self.donations, "Progress to Goal:", (2, 5))
        self.donation_prog_bar = cgp(self.donations, ("camp", "donation_start", "donation_needed",
                                                      "donation_total"), (3, 5))

        self.library = cg(self, (20, 13), (2, 33), "Great Library")

        self.locations = cg(self, (40, 48), (25, 1), "Available Locations")
        self.location_add = cgtb(self.locations, "Add", "location_unlock_misc")
        self.location_list = cgl(self.locations, ("camp", "build_loc_list"))

        self.achievements = cg(self, (30, 48), (68, 1), "Global Achievements")
        self.achieve_add = cgtb(self.achievements, "Add", "achieve_global_misc")
        self.achieve_list = cgl(self.achievements, ("camp", "achievement_list"))


class ModuleParty(ContentPane):
    def __init__(self, *args):
        super(ModuleParty, self).__init__(*args)
        cg = ContentGroup
        cgi = ContentGroup.ContentItemDescriptor
        cgv = ContentGroup.ContentItemValue
        cgp = ContentGroup.ContentProgressBar
        cgb = ContentGroup.ContentActionButton
        cgtb = ContentGroup.ContentTitleButton
        cgl = ContentGroup.ContentList

        self.setVisible(False)

        self.party_manage_label = SidePaneLabel("Parties", 0, parent=self.side)
        self.party_new = SidePaneButton("New", 2, "party_new", parent=self.side)
        self.party_change = SidePaneButton("Change", 1, "app_help", parent=self.side)
        self.party_retire = SidePaneButton("Retire", 3, "app_help", parent=self.side)

        self.player_manage_label = SidePaneLabel("Players", 5.5, parent=self.side)
        self.player_new = SidePaneButton("New", 6.5, "player_new", parent=self.side)
        self.player_retire = SidePaneButton("Retire", 7.5, "app_help", parent=self.side)

        self.char_manage_label = SidePaneLabel("Characters", 10, parent=self.side)
        self.char_new = SidePaneButton("Recruit", 11, "char_new", parent=self.side)
        self.char_retire = SidePaneButton("Retire", 12, "app_help", parent=self.side)

        self.reputation = cg(self, (20, 13), (2, 1), "Reputation")
        self.reputation_desc = cgi(self.reputation, "Reputation: ", (1, 5))
        self.reputation_val = cgv(self.reputation, ("party_active", "reputation_display"), (1, 5))
        self.reputation_desc = cgi(self.reputation, "Shop Modifier: ", (2, 5))
        self.reputation_val = cgv(self.reputation, ("party_active", "set_shop_modifier"), (2, 5))
        self.reputation_prog_label = cgi(self.reputation, "Proximity to change:", (3, 5))
        self.reputation_prog_bar = cgp(self.reputation, ("party_active", "reputation_decrease", "reputation_increase",
                                                         "reputation"), (4, 5))
        self.reputation_loss_btn = cgb(self.reputation, "-", "reputation_loss_misc", (5, 5), (1, 2))
        self.reputation_gain_btn = cgb(self.reputation, "+", "reputation_gain_misc", (5, 5), (2, 2))

        self.roster = cg(self, (20, 32), (2, 17), "Roster")
        self.roster_list = cg.PartyRoster(self.roster)

        self.adventures = cg(self, (40, 48), (25, 1), "Adventure History")

        self.achievements = cg(self, (30, 48), (68, 1), "Party Achievements")
        self.achieve_add = cgtb(self.achievements, "Add", "achieve_party_misc")
        self.achieve_list = cgl(self.achievements, ("party_active", "achievements"))


class ModuleScene(ContentPane):
    def __init__(self, *args):
        super(ModuleScene, self).__init__(*args)

        self.setVisible(False)

        self.display_test = DisplayPaneLabel("Scene Page Test", (1, 1), parent=self)


class ModuleShop(ContentPane):
    def __init__(self, *args):
        super(ModuleShop, self).__init__(*args)
        self.setVisible(False)

        self.label_1 = SidePaneLabel("Active:", 0, parent=self.side)
        self.active_char_toggle = SidePaneButtonSelector(self.side, "None", 1, "char_toggle")
        self.active_char_purchase = SidePaneButton("Buy", 2, "char_shop_buy", parent=self.side)

        self.item_table = ItemTable(self)


class ModuleCharDetail(ContentPane):
    def __init__(self, *args):
        super().__init__(*args)
        self.setVisible(False)

        self.active_char = SidePaneLabel("Dudeman", 0, parent=self.side)

        self.overview_button = SidePaneButton("Overview", 2, "char_show_overview", parent=self.side)
        self.gear_button = SidePaneButton("Gear", 3, "char_show_gear", parent=self.side)
        self.kills_button = SidePaneButton("Kills", 4, "char_show_kills", parent=self.side)
        self.perks_button = SidePaneButton("Perks", 5, "char_show_perks", parent=self.side)
        self.retirement_button = SidePaneButton("Retirement", 6, "char_show_retprog", parent=self.side)
        self.notes_button = SidePaneButton("Notes", 7, "char_show_notes", parent=self.side)

    def update_info(self, char):
        self.active_char.setText(char.name)


# <editor-fold desc="SidePane Items">
class SidePaneButton(QPushButton):
    def __init__(self, text, position, connect, **kwargs):
        super(QPushButton, self).__init__(**kwargs)
        pane = self.parent()
        disp = pane.parent()
        mane = disp.parent()

        pane_size = (pane.geometry().width(), pane.geometry().height())

        self.resize(pane_size[0] * .76, pane_size[1] * .055)
        self.move(pane_size[0] * .12, (pane_size[1] * .07) * position + (pane_size[1] * .025))
        self.setText(text)
        action = getattr(mane.btn, connect)
        self.clicked.connect(lambda state, main=mane: action(main))


class SidePaneButtonSelector(QPushButton):
    def __init__(self, parent, text, position, connect):
        super(QPushButton, self).__init__(parent)
        pane = self.parent()
        disp = pane.parent()
        mane = disp.parent()

        pane_size = (pane.geometry().width(), pane.geometry().height())

        self.resize(pane_size[0] * .76, pane_size[1] * .055)
        self.move(pane_size[0] * .12, (pane_size[1] * .07) * position + (pane_size[1] * .025))
        self.setText(text)

        action = getattr(mane.btn, connect)
        self.clicked.connect(lambda state, main=mane: action(self, main))

    def update_value(self):
        return


class SidePaneLabel(QLabel):
    def __init__(self, text, position, **kwargs):
        super(QLabel, self).__init__(**kwargs)
        pane_size = (self.parent().geometry().width(), self.parent().geometry().height())

        self.resize(pane_size[0] * .76, pane_size[1] * .055)
        self.move(pane_size[0] * .12, (pane_size[1] * .07) * position + (pane_size[1] * .03))
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.DemiBold))
# </editor-fold>


class DisplayPaneLabel(QLabel):
    def __init__(self, text, coord, **kwargs):
        super(QLabel, self).__init__(**kwargs)
        pane_size = (self.parent().view_area[0], self.parent().view_area[1])
        offset = (pane_size[0] * (coord[0] * .01), pane_size[1] * (coord[1] * .02))

        self.resize(pane_size[0] * .2, pane_size[1] * .05)
        self.move(offset[0], offset[1])
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignVCenter)
        self.setFont(QtGui.QFont("Times", 10, weight=QtGui.QFont.Medium))


class ContentGroup(QWidget):
    def __init__(self, parent, size, coord, title):
        super(QWidget, self).__init__(parent)
        pane_size = (self.parent().view_area[0], self.parent().view_area[1])
        group_size = (pane_size[0] * (size[0] * .01), pane_size[1] * (size[1] * .02))
        offset = (pane_size[0] * (coord[0] * .01), pane_size[1] * (coord[1] * .02))

        self.resize(group_size[0], group_size[1])
        self.move(offset[0], offset[1])

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtCore.Qt.lightGray)
        self.setPalette(palette)

        if title:
            self.title = QLabel(self)
            self.title.setFont(QtGui.QFont("Times", 10, weight=QtGui.QFont.Medium))
            self.title.setText(title)
            height = self.title.geometry().height()
            self.title.resize(self.geometry().width(), height)
            self.title.setAlignment(QtCore.Qt.AlignHCenter)

        self.parent().content_groups.append(self)
        self.value_items = []

    def update_values(self):
        for i in self.value_items:
            i.update_content()

    class ContentActionButton(QPushButton):
        def __init__(self, parent, text, connect, item_num, btn_num):
            super(QPushButton, self).__init__(parent)
            index = item_num[0]
            head = parent.title.geometry().height() + parent.geometry().height() * .05
            body = parent.geometry().height() - head
            slot_size = body / item_num[1]
            offset = (head + ((index - 1) * slot_size))

            cg = self.parent()
            mod = cg.parent()
            mane = mod.parent()

            high = slot_size * .9
            slot_wide = (self.parent().geometry().width() / btn_num[1])
            wide = slot_wide * .75
            inset = (slot_wide * .125) + ((btn_num[0]-1) * slot_wide)

            self.resize(wide, high)
            self.move(inset, offset + slot_size * .04)
            self.setText(text)
            connection = getattr(mane.btn, connect)
            self.pressed.connect(lambda main=mane: connection(main))

    class ContentItemDescriptor(QLabel):
        def __init__(self, parent, text, item_num, **kwargs):
            super(QLabel, self).__init__(parent, **kwargs)
            index = item_num[0]
            head = parent.title.geometry().height() + parent.geometry().height() * .05
            body = parent.geometry().height() - head
            slot_size = body / item_num[1]
            offset = (head + ((index-1) * slot_size))

            self.setFont(QtGui.QFont("Times", 9, weight=QtGui.QFont.Normal))
            self.setText(text)
            self.move(0, offset)
            self.setAlignment(QtCore.Qt.AlignVCenter)

    class ContentItemValue(QLabel):
        def __init__(self, parent, value, item_num, **kwargs):
            super(QLabel, self).__init__(parent, **kwargs)
            index = item_num[0]
            head = parent.title.geometry().height() + parent.geometry().height() * .05
            body = parent.geometry().height() - head
            slot_size = body / item_num[1]
            offset = (head + ((index - 1) * slot_size))

            self.data_type = value[0]
            self.data_item = value[1]

            self.setFont(QtGui.QFont("Times", 10, weight=QtGui.QFont.Normal))
            self.setText("")
            self.move(0, offset)
            height = slot_size
            self.resize(self.parent().geometry().width(), height)
            self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

            self.parent().value_items.append(self)

        def update_content(self):
            cg = self.parent()
            mod = cg.parent()
            mane = mod.parent()

            camp_data = getattr(mane, "camp")
            if self.data_type == "camp":
                sec = camp_data
            else:
                sec = getattr(camp_data, self.data_type)

            try:
                value = getattr(sec, self.data_item)
                try:
                    value = value()
                except TypeError:
                    pass
            except AttributeError:
                value = ""
            self.setText(str(value))

    class ContentList(QListWidget):
        def __init__(self, parent, item_list):
            super(QListWidget, self).__init__(parent)
            space = self.parent().geometry().height() - self.parent().title.geometry().height()

            self.resize(self.parent().geometry().width(), space)
            self.move(0, self.parent().title.geometry().height())
            self.setSelectionMode(0)
            self.data_type = item_list[0]
            self.data_list = item_list[1]

            self.parent().value_items.append(self)

        def update_content(self):
            cg = self.parent()
            mod = cg.parent()
            mane = mod.parent()

            camp_data = getattr(mane, "camp")
            if self.data_type == "camp":
                sec = camp_data
            else:
                sec = getattr(camp_data, self.data_type)

            if sec:
                i_list = getattr(sec, self.data_list)
                try:
                    i_list = i_list()
                except TypeError:
                    pass
            else:
                i_list = []
            self.clear()
            self.addItems(i_list)
            self.sortItems()

    class ContentProgressBar(QProgressBar):
        def __init__(self, parent, values, item_num, **kwargs):
            super(QProgressBar, self).__init__(parent, **kwargs)
            index = item_num[0]
            head = parent.title.geometry().height() + parent.geometry().height() * .05
            body = parent.geometry().height() - head
            slot_size = body / item_num[1]
            offset = (head + ((index - 1) * slot_size))

            orient = QtCore.Qt.Horizontal
            min_val = 0
            max_val = 0
            curr_val = 0

            self.move(self.parent().geometry().width() * .05, offset)
            self.resize(self.parent().geometry().width() * .9, slot_size * .85)
            self.setOrientation(orient)
            self.setRange(min_val, max_val)
            self.setValue(curr_val)
            self.setTextVisible(False)

            self.data_type = values[0]
            self.data_min = values[1]
            self.data_max = values[2]
            self.data_value = values[3]

            self.parent().value_items.append(self)

        def update_content(self):
            cg = self.parent()
            mod = cg.parent()
            mane = mod.parent()

            camp_data = getattr(mane, "camp")
            if self.data_type == "camp":
                sec = camp_data
            else:
                sec = getattr(camp_data, self.data_type)

            try:
                value = getattr(sec, self.data_value)
                val_min = getattr(sec, self.data_min)
                val_max = getattr(sec, self.data_max)
            except AttributeError:
                value = 0
                val_min = 0
                val_max = 0

            self.setRange(val_min, val_max)
            self.setValue(value)

    class ContentTitleButton(QPushButton):
        def __init__(self, parent, text, connect):
            super(QPushButton, self).__init__(parent)

            cg = self.parent()
            mod = cg.parent()
            mane = mod.parent()

            wide = parent.title.geometry().width() * .15
            high = parent.title.geometry().height() * .9
            self.resize(wide, high)

            inset = parent.title.geometry().width() - ((parent.title.geometry().width() * .02) + wide)
            offset = parent.title.geometry().height() * .05
            self.move(inset, offset)

            self.setText(text)
            connection = getattr(mane.btn, connect)
            self.pressed.connect(lambda main=mane: connection(main))

    class PartyRoster(QWidget):
        def __init__(self, parent):
            super(QWidget, self).__init__(parent)
            cg = self.parent()
            mod = cg.parent()

            head = cg.title.geometry().height() + cg.geometry().height() * .01
            self.body = cg.geometry().height() - head
            self.resize(cg.geometry().width(), self.body)
            self.move(0, head)
            self.max_players = 8
            self.slot_size = (self.body / self.max_players) / 2
            self.name_slots = []
            self.char_slots = []
            self.listed_names = []

            for i in range(self.max_players * 2):
                if not i % 2:
                    slot = QLabel(self)
                    slot.setText("")
                    slot.resize(cg.geometry().width(), self.slot_size)
                    slot.move(0, i * self.slot_size)
                    slot.setFont(QtGui.QFont("Times", 8.5, weight=QtGui.QFont.Normal))
                    self.name_slots.append(slot)
                else:
                    slot = QLabel(self)
                    slot.move(0, i * self.slot_size)
                    slot.resize(cg.geometry().width(), self.slot_size)
                    slot.setText("")
                    slot.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
                    self.char_slots.append(slot)

            cg.value_items.append(self)

        def update_content(self):
            cg = self.parent()
            mod = cg.parent()
            mane = mod.parent()

            if mane.active:
                if mane.camp.party_active:
                    party = mane.camp.party_active
                    for s in self.name_slots:
                        s.setText("")
                    for i, p in enumerate(party.players_active_list):
                        self.name_slots[i].setText(p.name.title())
                        if p.char_active:
                            self.char_slots[i].setText(p.char_active.name.title() + "  ")
                        else:
                            self.char_slots[i].setText("No active character  ")
                else:
                    pass
            else:
                pass


class CharTiles(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.resize(parent.geometry().width(), parent.geometry().height())

        self.parent().content_groups.append(self)
        self.value_items = []

        for n in range(8):
            tile = self.CharTile(self, n)
            self.value_items.append(tile)

    def update_values(self):
        for i in self.value_items:
            i.update_content()

    class CharTile(QWidget):
        def __init__(self, parent, slot):
            super(QWidget, self).__init__(parent)
            wide = self.parent().geometry().width() * .2
            tall = self.parent().geometry().height() * .425
            set_in = self.parent().geometry().width() * .04
            set_down = self.parent().geometry().height() * .05

            col = slot + 1
            if slot > 3:
                col -= 4
            row = 1
            if slot > 3:
                row += 1
            x = (col * set_in) + ((col - 1) * wide)
            y = (row * set_down) + ((row - 1) * tall)

            self.resize(wide, tall)
            self.move(x, y)
            self.slot = slot

            self.cg = self.parent()
            self.mod = self.cg.parent()
            self.mane = self.mod.parent()

            self.setAutoFillBackground(True)
            palette = self.palette()
            palette.setColor(QtGui.QPalette.Window, QtCore.Qt.gray)
            self.setPalette(palette)

            self.name = QLabel(self)
            self.name.setFont(QtGui.QFont("Times", 10, weight=QtGui.QFont.DemiBold))
            self.name.setText("Test")
            height = self.name.geometry().height()
            self.name.resize(self.geometry().width(), height)
            self.name.setAlignment(QtCore.Qt.AlignHCenter)
            self.name.setVisible(False)

            self.level = QLabel(self)
            self.level.setFont(QtGui.QFont("Times", 9, weight=QtGui.QFont.Medium))
            self.level.setText("Level: 2")
            self.level.resize(self.geometry().width() * .3, self.geometry().height() * .1)
            self.level.move(self.geometry().width() * .56, self.geometry().height() * .135)
            self.level.setAlignment(QtCore.Qt.AlignRight)
            self.level.setVisible(False)

            self.race_class = QLabel(self)
            self.race_class.setFont(QtGui.QFont("Times", 9, weight=QtGui.QFont.Normal))
            self.race_class.setText("Orchid \nSpellweaver")
            self.race_class.move(self.geometry().width() * .035, self.geometry().height() * .16)
            self.race_class.setVisible(False)

            self.kills = QLabel(self)
            self.kills.setFont(QtGui.QFont("Times", 9, weight=QtGui.QFont.Medium))
            self.kills.setText("Kills: 42")
            self.kills.resize(self.geometry().width() * .3, self.geometry().height() * .1)
            self.kills.move(self.geometry().width() * .56, self.geometry().height() * .295)
            self.kills.setAlignment(QtCore.Qt.AlignRight)
            self.kills.setVisible(False)

            self.level_progress_label = QLabel(self)
            self.level_progress_label.setFont(QtGui.QFont("Times", 9, weight=QtGui.QFont.Medium))
            self.level_progress_label.setText("XP")
            self.level_progress_label.move(self.geometry().width() * .9, self.geometry().height() * .78)
            self.level_progress_label.setVisible(False)
            self.level_progress = QProgressBar(self)
            self.level_progress.setOrientation(QtCore.Qt.Vertical)
            self.level_progress.resize(self.geometry().width() * .06, self.geometry().height() * .645)
            self.level_progress.move(self.geometry().width() * .91, self.geometry().height() * .135)
            self.level_progress.setVisible(False)

            self.gp = QLabel(self)
            self.gp.setFont(QtGui.QFont("Times", 9, weight=QtGui.QFont.Medium))
            self.gp.setText("Gold: 20")
            self.gp.resize(self.geometry().width() * .3, self.geometry().height() * .1)
            self.gp.setAlignment(QtCore.Qt.AlignRight)
            self.gp.move(self.geometry().width() * .56, self.geometry().height() * .215)
            self.gp.setVisible(False)

            self.retire_label = QLabel(self)
            self.retire_label.setFont(QtGui.QFont("Times", 9, weight=QtGui.QFont.Medium))
            self.retire_label.setText("Retirement:")
            self.retire_label.move(0, self.geometry().height() * .9)
            self.retire_label.setVisible(False)
            self.retire_progress = QProgressBar(self)
            self.retire_progress.resize(self.geometry().width() * .585, self.geometry().height() * .07)
            self.retire_progress.move(self.geometry().width() * .385, self.geometry().height() * .91)
            self.retire_progress.setVisible(False)

            self.button_details = QPushButton(self)
            self.button_details.setText("Details")
            self.button_details.resize(self.geometry().width() * .35, self.geometry().height() * .1)
            self.button_details.move(self.geometry().width() * .05, self.geometry().height() * .45)
            self.button_details.setVisible(False)

            self.button_GP_adjust = QPushButton(self)
            self.button_GP_adjust.setText("Adj GP")
            self.button_GP_adjust.resize(self.geometry().width() * .35, self.geometry().height() * .1)
            self.button_GP_adjust.move(self.geometry().width() * .05, self.geometry().height() * .71)
            self.button_GP_adjust.setVisible(False)

            self.button_XP_adjust = QPushButton(self)
            self.button_XP_adjust.setText("Adj XP")
            self.button_XP_adjust.resize(self.geometry().width() * .35, self.geometry().height() * .1)
            self.button_XP_adjust.move(self.geometry().width() * .05, self.geometry().height() * .58)
            self.button_XP_adjust.setVisible(False)

            self.button_level_up = QPushButton(self)
            self.button_level_up.setText("Level Up")
            self.button_level_up.resize(self.geometry().width() * .35, self.geometry().height() * .1)
            self.button_level_up.move(self.geometry().width() * .5, self.geometry().height() * .45)
            self.button_level_up.setVisible(False)

            self.button_retire = QPushButton(self)
            self.button_retire.setText("Retire")
            self.button_retire.resize(self.geometry().width() * .35, self.geometry().height() * .1)
            self.button_retire.move(self.geometry().width() * .5, self.geometry().height() * .58)
            self.button_retire.setVisible(False)

            self.button_death = QPushButton(self)
            self.button_death.setText("Death")
            self.button_death.resize(self.geometry().width() * .35, self.geometry().height() * .1)
            self.button_death.move(self.geometry().width() * .5, self.geometry().height() * .71)
            self.button_death.setVisible(False)

            self.things = [
                self.name, self.level, self.gp, self.race_class, self.kills, self.level_progress_label,
                self.level_progress, self.retire_label, self.retire_progress, self.button_level_up,
                self.button_XP_adjust, self.button_GP_adjust, self.button_details, self.button_retire, self.button_death
                           ]

        def update_content(self):
            cg = self.parent()
            mod = cg.parent()
            mane = mod.parent()

            # Confirm there is an active campaign
            if mane.active:
                # Confirm there is an active party
                if mane.camp.party_active:
                    # Confirm there are active players
                    party = mane.camp.party_active
                    if party.players_active_list:
                        # Actually start updating the GD tiles.
                        try:
                            player = party.players_active_list[self.slot]
                            char = player.char_active
                            if char:
                                for i in self.things:
                                    i.setVisible(True)
                                self.name.setText(str(char.name))
                                self.level.setText("Level: " + str(char.level_current))
                                self.gp.setText("Gold: " + str(char.gold))
                                self.race_class.setText(str(char.char_class_race) + "\n" + str(char.char_class_name))
                                self.kills.setText("Kills: " + str(char.kill_count))
                                self.level_progress.setRange(char.level_start_xp, char.level_up_xp)
                                self.level_progress.setValue(char.experience)
                                self.retire_progress.setRange(0, 3)
                                self.retire_progress.setValue(1)

                                # Confirm buttons are set to appropriate functions.
                                self.connect_function(self.button_level_up.clicked, lambda: char.gain_level(self.mane))
                                self.connect_function(self.button_XP_adjust.clicked, lambda: char.adjust_xp(self.mane))
                                self.connect_function(self.button_GP_adjust.clicked, lambda: char.adjust_gp(self.mane))
                                self.connect_function(self.button_details.clicked, lambda: char.view_details(self.mane))
                                self.connect_function(self.button_retire.clicked, lambda: char.retire(self.mane))
                                self.connect_function(self.button_death.clicked, lambda: char.kill(self.mane))
                            else:
                                for t in self.things:
                                    t.setVisible(False)
                        except IndexError:
                            for t in self.things:
                                t.setVisible(False)
                    else:
                        pass
                else:
                    pass
            else:
                pass

        def connect_function(self, button, newhandler):
            while True:
                try:
                    button.disconnect()
                except TypeError:
                    break
            button.connect(newhandler)


class ItemTable(QTableWidget):
    def __init__(self, parent):
        super(QTableWidget, self).__init__(parent)
        mod = self.parent()
        mane = mod.parent()

        self.resize(self.parent().view_area[0] * .94, self.parent().view_area[1] * .94)
        self.move(self.parent().view_area[0] * .03, self.parent().view_area[1] * .03)
        self.parent().content_groups.append(self)

    def update_values(self):
        mod = self.parent()
        mane = mod.parent()
        if not mane.camp:
            pass
        else:
            item_ref = mane.ref.items
            inventory_prosp = mane.camp.items_from_prosperity
            inventory_unlock = mane.camp.items_unlocked
            inventory_avail = []
            for c_u in inventory_unlock:
                if c_u[0] >= inventory_prosp:
                    inventory_avail.append(c_u[0])
            for c_i in range(inventory_prosp):
                inventory_avail.append(c_i + 1)
            rows = len(inventory_avail)

            self.setRowCount(rows)
            print(rows)
            self.setColumnCount(5)
            self.verticalHeader().hide()
            self.setHorizontalHeaderLabels(["#", "Item", "Cost", "Slot", "Description", "Stock"])
            self.setColumnWidth(0, 20)
            self.setColumnWidth(2, 55)
            self.setColumnWidth(3, 110)
            self.setColumnWidth(5, 55)

            for c_a in inventory_avail:
                index = inventory_avail.index(c_a)
                card_info = item_ref[c_a]
                if c_a > 99:
                    c_a_num = str(c_a)
                elif c_a > 9:
                    c_a_num = " " + str(c_a)
                else:
                    c_a_num = "  " + str(c_a)

                number = QTableWidgetItem(c_a_num)
                number.setTextAlignment(QtCore.Qt.AlignCenter)
                # number.setFont(other_font)
                name = QTableWidgetItem(card_info[0])
                name.setTextAlignment(QtCore.Qt.AlignVCenter)
                # name.setFont(head_font)
                cost = QTableWidgetItem(str(card_info[3]))
                cost.setTextAlignment(QtCore.Qt.AlignCenter)
                # cost.setFont(other_font)
                slot = QTableWidgetItem(card_info[4])
                slot.setTextAlignment(QtCore.Qt.AlignCenter)
                # slot.setFont(other_font)
                desc = QTableWidgetItem(card_info[1])
                desc.setTextAlignment(QtCore.Qt.AlignVCenter)
                # desc.setFont(other_font)
                stock = QTableWidgetItem(str(card_info[2]))
                stock.setTextAlignment(QtCore.Qt.AlignCenter)
                # stock.setFont(other_font)

                self.setItem(index, 0, number)
                self.setItem(index, 1, name)
                self.setItem(index, 2, cost)
                self.setItem(index, 3, slot)
                self.setItem(index, 4, desc)
                self.setItem(index, 5, stock)
                self.setItem(index, 6, QTableWidgetItem(str(c_a)))

            self.setColumnHidden(6, True)
            self.resizeColumnToContents(1)
            header = self.horizontalHeader()
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
            self.resizeRowsToContents()
            self.sortItems(0)
            self.setSortingEnabled(True)
            header.sectionClicked.connect(self.resizeRowsToContents)




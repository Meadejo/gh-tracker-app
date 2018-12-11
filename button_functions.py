# Gloomhaven tracker app: Button Functions
# Created by: Joshua Meade
# Created on: 10/15/18

import pickle
import os
from PyQt5 import QtWidgets
from camp_classes import Campaign
from datetime import date


class ButtonFunctions:
    def __init__(self):
        pass

    def achieve_global(self, main, item):
        def thing():
            m_achieve_data = main.ref.global_achievements
            m_achieve_list = []
            m_achieve_type = []
            for i in m_achieve_data:
                m_achieve_list.append(i[0])
                m_achieve_type.append(i[1])

            c_achieve_data = main.camp.achievement_data
            c_achieve_list = []
            for i in c_achieve_data:
                c_achieve_list.append(i[0])
            c_achieve_type = []
            for i in c_achieve_list:
                c_achieve_type.append(m_achieve_type[m_achieve_list.index(i)])
            item_type = m_achieve_type[m_achieve_list.index(item)]
            level = 1

            if item_type == "Tech" or item_type == "Corrupt":
                if item_type in c_achieve_type:
                    index = c_achieve_type.index(item_type)
                    level = c_achieve_data[index][1] + 1
                    del c_achieve_data[index]
            elif item_type != "Unique":
                if item_type in c_achieve_type:
                    index = c_achieve_type.index(item_type)
                    del c_achieve_data[index]

            main.camp.achievement_data.append((item, level))

            main.camp.achievement_list = []
            for i in main.camp.achievement_data:
                if i[1] > 1:
                    name = i[0] + " Lv " + str(i[1])
                else:
                    name = i[0]
                main.camp.achievement_list.append(name)

            main.update_display()
            main.confirmation()
        return thing()

    def achieve_global_misc(self, main):
        def thing():
            achieve_data = main.ref.global_achievements
            curr_achieve_data = main.camp.achievement_data
            curr_achieve_list = []
            for i in curr_achieve_data:
                curr_achieve_list.append(i[0])
            master_achieve_list = []
            achieve_avail = []
            for i in achieve_data:
                master_achieve_list.append(i[0])
            for i in master_achieve_list:
                if i not in curr_achieve_list or i == "Ancient Technology" or i == "End of Corruption":
                    achieve_avail.append(i)

            input_loop = True
            while input_loop:
                item, ok_pressed = QtWidgets.QInputDialog.getItem(main, "Global Achievement",
                                                                  "Select an achievement:               "
                                                                  "                               ",
                                                                  achieve_avail, 0, False)
                if ok_pressed and item:
                    input_loop = False
                if not ok_pressed:
                    return

            self.achieve_global(main, item)
        return thing()

    def achieve_party(self, main, item):
        def thing():
            main.camp.party_active.achievements.append(item)
            main.update_display()
            main.confirmation()
        return thing()

    def achieve_party_misc(self, main):
        def thing():
            achieve_data = main.ref.party_achievements
            try:
                curr_achieve_list = main.camp.party_active.achievements
                achieve_avail = []
                for i in achieve_data:
                    if i not in curr_achieve_list:
                        achieve_avail.append(i)

                input_loop = True
                while input_loop:
                    item, ok_pressed = QtWidgets.QInputDialog.getItem(main, "Party Achievement",
                                                                      "Select an achievement:               "
                                                                      "                               ",
                                                                      achieve_avail, 0, False)
                    if ok_pressed and item:
                        input_loop = False
                    if not ok_pressed:
                        return

                self.achieve_party(main, item)
            except AttributeError:
                QtWidgets.QMessageBox.information(main, "Nope!", "No active party. \n"
                                                                 "Please create or set an active party.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
        return thing()

    def activate(self, main):
        main.sys_nav.app_btn.setDisabled(False)
        main.sys_nav.city_btn.setDisabled(False)
        main.sys_nav.party_btn.setDisabled(False)
        main.sys_nav.char_btn.setDisabled(False)
        main.sys_nav.scene_btn.setDisabled(False)
        main.sys_nav.save_exit_btn.setDisabled(False)

        main.active = True
        main.update_display()

    def app_about(self, main):
        def thing():
            print("About Button. No Function.")
        return thing()

    def app_help(self, main):
        def thing():
            print("Help Button. No Function.")
        return thing()

    def camp_load(self, main):
        def thing():
            mb = QtWidgets.QMessageBox
            fd = QtWidgets.QFileDialog
            if main.active and main.last_save != main.camp:
                reply = mb.question(main, 'DID YOU SAVE?!?', "Any unsaved data will be overwritten."
                                                             "\nAre you sure?",
                                    mb.Yes | mb.No, mb.No)
                if reply != mb.Yes:
                    return

            app_path = os.path.dirname(__file__)
            file_path = app_path + "\\saves\\"
            file, ext = fd.getOpenFileName(main, "Load Campaign", file_path, filter="GH Campaign (*.ghv)")
            if file != '':
                with open(str(file), 'rb') as f:
                    main.camp = pickle.load(f)
                    main.update_display()
                    if not main.active:
                        self.activate(main)
            else:
                return
        return thing()

    def camp_new(self, main):
        def thing():
            if main.active:
                reply = QtWidgets.QMessageBox.question(main, 'New Campaign', "Are you sure? \nAll current unsaved "
                                                                             "campaign info will be lost.",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

                if reply == QtWidgets.QMessageBox.Yes:
                    pass
                else:
                    return

            input_loop = True
            while input_loop:
                name, ok_pressed = QtWidgets.QInputDialog.getText(main, "New Campaign",
                                                                  "Campaign Name:                  "
                                                                  "                               ",
                                                                  QtWidgets.QLineEdit.Normal, "Gloomhaven")
                if ok_pressed and name != '':
                    input_loop = False
                if not ok_pressed:
                    return

            main.camp = Campaign(name)
            self.activate(main)
        return thing()

    def camp_save(self, main):
        def thing():
            mb = QtWidgets.QMessageBox
            if main.camp:
                app_path = os.path.dirname(__file__)
                file_path = app_path + "\\saves\\"
                os.makedirs(file_path, exist_ok=True)
                file = main.camp.name + ".ghv"
                with open(str(file_path + file), 'wb') as f:
                    pickle.dump(main.camp, f)
                main.last_save = main.camp
                mb.information(main, "Done!", "Campaign Successfully Saved!",
                               mb.Ok, mb.Ok)
            else:
                print("camp_save; No function assigned.")
                pass
        return thing()

    def char_new(self, main):
        def thing():
            party = main.camp.party_active
            # Check there is an active party.
            if not party:
                QtWidgets.QMessageBox.information(main, "Do what?!?", "There is no active party. \n"
                                                                      "Please create or set an active party.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return

            # Check there are active players in the party.
            elif not party.players_active_list:
                QtWidgets.QMessageBox.information(main, "Do what?!?", "The active party has no players. \n"
                                                                      "Please add a new player to the active party.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            # Active Party w/ Players. Continue w/ function.
            else:
                avail_players = []
                for i in party.players_active_list:
                    if not i.char_active:
                        avail_players.append(i)
                # Check that one or more active players don't have active characters.
                if len(avail_players) < 1:
                    QtWidgets.QMessageBox.information(main, "Do what?!?", "All players have active characters. \n"
                                                                          "Please create a new player or retire a character.",
                                                      QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                    return
                # If multiple players need characters, choose a player.
                elif len(avail_players) > 1:
                    player_names = []
                    for i in avail_players:
                        player_names.append(i.name)
                    input_loop = True
                    while input_loop:
                        player, ok_pressed = QtWidgets.QInputDialog.getItem(main, "New Character",
                                                                            "Select a player:               "
                                                                            "                               ",
                                                                            player_names, 0, False)
                        if ok_pressed and player:
                            index = player_names.index(player)
                            player = avail_players[index]
                            input_loop = False
                        if not ok_pressed:
                            return
                else:
                    player = avail_players[0]

            # Create list of available Classes and present for selection.
            avail_classes = main.camp.classes_unlocked
            for i in party.classes_in_use:
                if i in avail_classes:
                    avail_classes.remove(i)
            avail_class_names = []
            for i in avail_classes:
                lib = main.ref.classes[i]
                race = lib[1]
                common_name = lib[0]
                avail_class_names.append(race + " " + common_name)
            input_loop = True
            while input_loop:
                char_class, ok_pressed = QtWidgets.QInputDialog.getItem(main, "New Character",
                                                                        "Select a character:               "
                                                                        "                               ",
                                                                        avail_class_names, 0, False)
                if ok_pressed and char_class:
                    index = avail_class_names.index(char_class)
                    char_class = avail_classes[index]
                    input_loop = False
                if not ok_pressed:
                    return

            # Select a starting level (if Prosperity Level greater than 1)
            prosp_level = main.camp.prosperity_level
            if prosp_level > 1:
                level_options = []
                for i in range(prosp_level):
                    level_options.append(str(i+1))
                input_loop = True
                while input_loop:
                    char_level, ok_pressed = QtWidgets.QInputDialog.getItem(main, "New Character",
                                                                            "Select a starting level:       "
                                                                            "                               ",
                                                                            level_options, 0, False)
                    if ok_pressed and char_level:
                        input_loop = False
                    if not ok_pressed:
                        return
            else:
                char_level = 1
            start_xp = main.ref.xp_to_level[char_level-1]

            # Choose retire Quest

            # Name your character
            input_loop = True
            while input_loop:
                name, ok_pressed = QtWidgets.QInputDialog.getText(main, "New Character",
                                                                  "Name your new character:               "
                                                                  "                               ",
                                                                  QtWidgets.QLineEdit.Normal, "")
                if ok_pressed and name != '':
                    input_loop = False
                if not ok_pressed:
                    return
            char = Campaign.Party.Character(name, player, char_class, start_xp, retire_quest="")
            player.char_active = char
            party.chars_active_list.append(char)
            party.classes_in_use.append(char_class)
            main.update_display()
        return thing()

    def char_level_up(self, main):
        def thing():
            print("This will level up your dude!")
        return thing()

    def char_manage(self, main):
        def thing():
            print("Button: Manage Character")
        return thing()

    def char_shop_buy(self, main):
        def thing():
            print("Gonna buy me a thing.")
        return thing()

    def char_toggle(self, button, main):
        def thing():
            try:
                chars = main.camp.party_active.chars_active_list
                char_names = []
                for c in range(len(chars)):
                    dude = chars[c]
                    char_names.append(dude.name)
                input_loop = True
                while input_loop:
                    char_name, ok_pressed = QtWidgets.QInputDialog.getItem(main, "Active Character",
                                                                           "Select a character to do a thing:          "
                                                                           "                               ",
                                                                           char_names, 0, False)
                    if ok_pressed and char_name:
                        input_loop = False
                    if not ok_pressed:
                        return
                index = char_names.index(char_name)
                main.camp.party_active.char_town_active = chars[index]
                button.setText(main.camp.party_active.char_town_active.name)
            except AttributeError:
                QtWidgets.QMessageBox.information(main, "Nope!", "No active characters. \n"
                                                                 "Please create some dudes.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
        return thing()

    def char_show_overview(self, main):
        def thing():
            pass
        return thing()

    def char_show_gear(self, main):
        def thing():
            pass
        return thing()

    def char_show_kills(self, main):
        def thing():
            pass
        return thing()

    def char_show_perks(self, main):
        def thing():
            pass
        return thing()

    def char_show_retprog(self, main):
        def thing():
            pass
        return thing()

    def char_show_notes(self, main):
        def thing():
            pass
        return thing()

    def char_solo(self, main):
        def thing():
            print("Button: Solo Adventure")
        return thing()

    def city_explore(self, main):
        def thing():
            party = main.camp.party_active
            try:
                party.location_current
            except AttributeError:
                QtWidgets.QMessageBox.information(main, "Do what?!?", "There is no active party. \n"
                                                                      "Please create or set an active party.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            if party.location_current != 0:
                QtWidgets.QMessageBox.information(main, "Exploring the city", "You're not in town! \n"
                                                  "You should fix that.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            elif party.city_explored:
                QtWidgets.QMessageBox.information(main, "Exploring the city", "You've already explored! \n"
                                                                              "There's no more trouble to root up.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            else:
                input_loop = True
                while input_loop:
                    result, ok_pressed = QtWidgets.QInputDialog.getText(main, "Exploring the city",
                                                                        "What happened in your City Event?:           "
                                                                        "                            ",
                                                                        QtWidgets.QLineEdit.Normal, "")
                    if ok_pressed and result != "":
                        input_loop = False
                    if not ok_pressed:
                        return
                party.city_explored = True
                party.city_event_log.append((date.today(), result))
            main.update_display()
            main.confirmation()
        return thing()

    def city_return(self, main):
        def thing():
            party = main.camp.party_active
            try:
                party.location_current
            except AttributeError:
                QtWidgets.QMessageBox.information(main, "Do what?!?", "There is no active party. \n"
                                                                      "Please create or set an active party.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            if party.location_current != 0:
                party.location_current = 0
                party.city_explored = False
                if len(party.chars_active_list) > 1:
                    for c in party.chars_active_list:
                        c.has_donated = False
                else:
                    party.chars_active_list[0].has_donated = False
            else:
                QtWidgets.QMessageBox.information(main, "Do what?!?", "You're already in town!.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            main.update_display()
        return thing()

    def city_donate(self, main):
        def thing():
            party = main.camp.party_active
            try:
                party.location_current
            except AttributeError:
                QtWidgets.QMessageBox.information(main, "Do what?!?", "There is no active party. \n"
                                                                      "Please create or set an active party.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            if party.location_current != 0:
                QtWidgets.QMessageBox.information(main, "Donate to the Sanctuary", "You're not in town! \n"
                                                  "You should fix that.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            elif not party.char_town_active:
                QtWidgets.QMessageBox.information(main, "Donate to the Sanctuary", "There is no active character! \n"
                                                                                   "You should fix that.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            elif party.char_town_active.has_donated:
                QtWidgets.QMessageBox.information(main, "Donate to the Sanctuary", str(party.char_town_active.name) +
                                                  " has already donated! \nPerhaps someone else has coin?",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            elif party.char_town_active.gold < 10:
                QtWidgets.QMessageBox.information(main, "Donate to the Sanctuary", str(party.char_town_active.name) +
                                                  " does not have enough gold! \nPerhaps someone else has coin?",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            else:
                camp = main.camp
                char = party.char_town_active

                char.gold -= 10
                char.has_donated = True
                camp.donation_total += 10
                camp.donation_tracking.append((date.today(), char.name))
                if camp.donation_total >= camp.donation_needed:
                    camp.donation_influence += 0
                    self.prosp_gain(main, "Sanctuary Donations", conf=False)
                    new_marks = main.ref.donation_landmarks[camp.donation_influence]
                    camp.donation_start = new_marks[0]
                    camp.donation_needed = new_marks[1]
            main.update_display()
        return thing()

    def location_unlock(self, main, scene, reason):
        def thing():
            if scene in main.camp.locations_unlocked:
                QtWidgets.QMessageBox.information(main, "Nope!", "This scenario has already been unlocked.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            else:
                main.camp.locations_unlocked.append(scene)
                main.camp.locations_unlocked_count += 1
                main.camp.locations_incomplete.append(int(scene))
                main.camp.locations_unlock_log.append((scene, date.today(), reason))
                main.update_display()
                main.confirmation()
        return thing()

    def location_unlock_misc(self, main):
        def thing():
            input_loop = True
            while input_loop:
                scene, ok_pressed = QtWidgets.QInputDialog.getText(main, "Unlock Location",
                                                                   "What is the number of the location you unlocked?:",
                                                                   QtWidgets.QLineEdit.Normal, "")
                if ok_pressed and int(scene) < 96:
                    input_loop = False
                if not ok_pressed:
                    return
            scene = int(scene)

            input_loop = True
            while input_loop:
                reason, ok_pressed = QtWidgets.QInputDialog.getText(main, "Unlock Location",
                                                                    "What did you do to unlock this scene?:",
                                                                    QtWidgets.QLineEdit.Normal, "")
                if ok_pressed and reason != "":
                    input_loop = False
                if not ok_pressed:
                    return

            self.location_unlock(main, scene, reason)
        return thing()

    def party_new(self, main):
        def thing():
            campaign = main.camp
            input_loop = True
            while input_loop:
                name, ok_pressed = QtWidgets.QInputDialog.getText(main, "New Party",
                                                                  "Party Name:                        "
                                                                  "                                  ",
                                                                  QtWidgets.QLineEdit.Normal, "Riders of Brohan")
                if ok_pressed and name != '':
                    input_loop = False
                if not ok_pressed:
                    return
            party_id_num = len(campaign.parties_created)
            party_uid = str("party" + str(party_id_num))
            party = Campaign.Party(name)
            party.uid = party_uid
            setattr(campaign, party_uid, party)
            campaign.parties_created.append(party)
            campaign.party_active = party
            main.update_display()
        return thing()

    def player_new(self, main):
        def thing():
            if main.camp.party_active:
                party = main.camp.party_active
                input_loop = True
                while input_loop:
                    name, ok_pressed = QtWidgets.QInputDialog.getText(main, "New Player",
                                                                      "What your name be?:            "
                                                                      "                               ",
                                                                      QtWidgets.QLineEdit.Normal, "")
                    if ok_pressed and name != '':
                        input_loop = False
                    if not ok_pressed:
                        return

                player = Campaign.Party.Player(name, party)
                party.players_active_list.append(player)
                main.update_display()
            else:
                QtWidgets.QMessageBox.information(main, "Nope!", "No active party. \n"
                                                                 "Please create or set an active party.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        return thing()

    def prosp_gain(self, main, reason, conf=True):
        def thing():
            main.camp.prosperity_points += 1
            main.camp.prosperity_log.append((date.today(), "+1", reason))
            if main.camp.prosperity_points >= main.camp.prosperity_needed:
                main.camp.prosperity_level += 1
                if main.camp.prosperity_level < 9:
                    new_marks = main.ref.prosperity_landmarks[main.camp.prosperity_level - 1]
                    main.camp.prosperity_needed = new_marks[1]
                    main.camp.prosperity_minimum = new_marks[0]
            main.update_display()
            if conf:
                main.confirmation()
        return thing()

    def prosp_gain_misc(self, main):
        def thing():
            input_loop = True
            while input_loop:
                reason, ok_pressed = QtWidgets.QInputDialog.getText(main, "Prosperity Gain",
                                                                    "What caused you to gain prosperity:               "
                                                                    "                               ",
                                                                    QtWidgets.QLineEdit.Normal, "")
                if ok_pressed and reason != '':
                    input_loop = False
                if not ok_pressed:
                    return

            self.prosp_gain(main, reason)
        return thing()

    def prosp_loss(self, main, reason):
        def thing():
            minim = main.camp.prosperity_minimum
            curr = main.camp.prosperity_points
            if curr-1 < minim:
                main.camp.prosperity_log.append((date.today(), "0* (-1)", reason))
                QtWidgets.QMessageBox.information(main, "Saved! (Sorta)", "Prosperity cannot be lowered. \n"
                                                                          "The event has still been logged.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            else:
                main.camp.prosperity_points -= 1
                main.camp.prosperity_log.append((date.today(), "-1", reason))
                main.update_display()
                main.confirmation()
        return thing()

    def prosp_loss_misc(self, main):
        def thing():
            input_loop = True
            while input_loop:
                reason, ok_pressed = QtWidgets.QInputDialog.getText(main, "Prosperity Loss",
                                                                    "What caused you to lose prosperity:               "
                                                                    "                               ",
                                                                    QtWidgets.QLineEdit.Normal, "")
                if ok_pressed and reason != '':
                    input_loop = False
                if not ok_pressed:
                    return

            self.prosp_loss(main, reason)
        return thing()

    def reputation_gain(self, main, reason):
        def thing():
            party = main.camp.party_active
            curr = party.reputation
            if curr+1 > 40:
                party.reputation_log.append((date.today(), "0* (+1)", reason))
                QtWidgets.QMessageBox.information(main, "Saved! (Sorta)", "Reputation cannot be increased. \n"
                                                                          "The event has still been logged.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

            else:
                party.reputation += 1
                party.reputation_display += 1
                party.reputation_log.append((date.today(), "+1", reason))
                if party.reputation >= party.reputation_increase:
                    party.reputation_modifier += 1
                    marks = main.ref.reputation_thresholds[party.reputation_modifier]
                    party.reputation_decrease = marks[0]
                    party.reputation_increase = marks[1]

                main.update_display()
                main.confirmation()
        return thing()

    def reputation_gain_misc(self, main):
        def thing():
            party = main.camp.party_active
            if not party:
                QtWidgets.QMessageBox.information(main, "Do what?!?", "There is no active party. \n"
                                                                      "Please create or set an active party.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            else:
                input_loop = True
                while input_loop:
                    reason, ok_pressed = QtWidgets.QInputDialog.getText(main, "Reputation Gain",
                                                                        "What caused you to gain reputation:           "
                                                                        "                               ",
                                                                        QtWidgets.QLineEdit.Normal, "")
                    if ok_pressed and reason != '':
                        input_loop = False
                    if not ok_pressed:
                        return
                self.reputation_loss(main, reason)
        return thing()

    def reputation_loss(self, main, reason):
        def thing():
            party = main.camp.party_active
            curr = party.reputation
            if curr-1 < 0:
                party.reputation_log.append((date.today(), "0* (-1)", reason))
                QtWidgets.QMessageBox.information(main, "Saved! (Sorta)", "Reputation cannot be lowered. \n"
                                                                          "The event has still been logged.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

            else:
                party.reputation -= 1
                party.reputation_display -= 1
                party.reputation_log.append((date.today(), "-1", reason))
                if party.reputation <= party.reputation_decrease:
                    party.reputation_modifier -= 1
                    marks = main.ref.reputation_thresholds[party.reputation_modifier]
                    party.reputation_decrease = marks[0]
                    party.reputation_increase = marks[1]

                main.update_display()
                main.confirmation()
        return thing()

    def reputation_loss_misc(self, main):
        def thing():
            party = main.camp.party_active
            if not party:
                QtWidgets.QMessageBox.information(main, "Do what?!?", "There is no active party. \n"
                                                                      "Please create or set an active party.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            else:
                input_loop = True
                while input_loop:
                    reason, ok_pressed = QtWidgets.QInputDialog.getText(main, "Reputation Loss",
                                                                        "What caused you to lose reputation:           "
                                                                        "                               ",
                                                                        QtWidgets.QLineEdit.Normal, "")
                    if ok_pressed and reason != '':
                        input_loop = False
                    if not ok_pressed:
                        return
                self.reputation_loss(main, reason)
        return thing()

    def set_up_shop(self, main):
        def thing():
            main.display_current.disappear()
            main.display_current = main.module_shop
            main.module_shop.setVisible(True)
            main.update_display()
        return thing()

    def sys_nav(self, main, button):
        def thing():
            if button < 5:
                main.display_current.setVisible(False)
                main.module_pages[button].setVisible(True)
                main.display_current = main.module_pages[button]
                main.update_display()
            elif button == 5:
                self.camp_save(main)
                main.close()
            else:
                print("This is button " + str(button))
        return thing()

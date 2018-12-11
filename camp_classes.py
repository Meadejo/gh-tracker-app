# Gloomhaven tracker app: Campaign Data & Definitions
# Created by: Joshua Meade
# Created on: 10/16/18

import math
from datetime import date
from reference import Reference


class Campaign:
    ref = Reference()

    def __init__(self, name):
        self.name = name

        self.classes_unlocked = ["Trispike", "Gear", "Star", "Daggers", "Shatter", "Brain"]
        self.classes_unlocked_count = 6
        self.classes_start = 6
        self.classes_max = 17

        self.prosperity_points = 0
        self.prosperity_minimum = 0
        self.prosperity_needed = 4
        self.prosperity_level = 1
        self.prosperity_log = []  # (date, value, "reason")

        self.locations_unlocked = [0, 1]
        self.locations_unlocked_count = 2
        self.locations_start = 2
        self.locations_max = 95
        self.locations_unlock_log = [(1, date.today(), "Starts Unlocked")]
        self.locations_completed = []
        self.locations_incomplete = [1]
        self.locations_unlooted = []

        self.achievement_data = [("City Rule: Militaristic", 1)]  # (Achievement, Level)
        self.achievement_list = ["City Rule: Militaristic"]

        self.donation_total = 0
        self.donation_start = 0
        self.donation_needed = 100
        self.donation_influence = 0
        self.donation_tracking = []

        self.parties_created = []
        self.parties_retired = []
        self.party_active = None

        self.items_from_prosperity = 14
        self.items_unlocked = []  # (Item#, Qty)

        self.unlocks_misc_start = 0
        self.unlocks_misc_max = 6
        self.unlocks_misc_current = 0

    def build_loc_list(self):
        ref = self.ref.locations
        names = []
        for l in self.locations_incomplete:
            name = ref[l][0]
            names.append(name)
        return names

    class Party:
        ref = Reference()

        def __init__(self, name):
            self.name = name

            self.is_hardcore = False

            self.players_max_active = 8
            self.players_active_list = []
            self.players_retired_list = []
            self.players_slot_available = True

            self.chars_active_list = []
            self.classes_in_use = []
            self.char_town_active = []

            self.achievements = []

            self.reputation = 20
            self.reputation_increase = 23
            self.reputation_decrease = 17
            self.reputation_display = 0
            self.reputation_modifier = 5
            self.reputation_log = []

            self.location_current = 0

            self.city_explored = False
            self.city_event_log = []

            self.items_in_inventories = []

            # Adventure Logs
            self.adventure_log = {
                # outing_number: (date, scene, diff, result, (chars), "road_notes", "scene_notes", "misc_notes")

            }

        def set_shop_modifier(self):
            mod = (self.reputation_modifier - 5) * -1
            return mod

        class Player:
            def __init__(self, name, party):
                self.name = name
                self.party = party
                self.party_join_date = date.today()

                self.is_hardcore = party.is_hardcore

                # Character references
                self.char_active = None
                self.char_retired_list = []
                self.char_killed_list = []
                self.char_abandoned_list = []

        class Character:
            ref = Reference()

            def __init__(self, name, player, char_class, start_xp, retire_quest):
                self.name = name
                self.player = player
                self.active = True

                # Basic Info
                self.char_class_info = self.ref.classes[char_class]
                self.char_class_name = self.char_class_info[0]
                self.char_class_race = self.char_class_info[1]
                self.char_class_perks = self.char_class_info[2]
                self.char_class_retire_events = self.char_class_info[4]

                # Startup Stats
                self.start_level = self.ref.xp_to_level.index(start_xp) + 1
                self.start_gold = (self.start_level * 15) + 15

                # General Stats
                self.level_current = 1
                self.level_start_xp = 0
                self.level_up_xp = 45
                self.experience = start_xp
                self.gold = self.start_gold

                # Kill Stats
                self.kill_count = 0
                self.boss_kills = []
                self.mob_kills = {
                    "Bandit Archer: Normal": 3,
                    "Demon, Earth: Elite": 1
                }

                # Perks & Checks
                self.checks_battle_goals_history = []
                self.checks_battle_goals_total = 0
                self.checks_misc_gain = []
                self.checks_misc_lost = []
                self.checks_total = 0

                self.perk_gain_player = len(player.char_retired_list)
                self.perk_gain_checks = math.floor(self.checks_total / 3)
                self.perk_gain_level = self.level_current
                self.perk_total = self.perk_gain_checks + self.perk_gain_level + self.perk_gain_player
                self.perk_active_list = []

                # Attack Deck
                self.attack_deck = self.ref.starting_attack_deck

                # In-City Activities
                self.has_donated = False
                self.can_level_up = False
                self.can_retire = False
                self.can_solo_adventure = False

                # Adventures
                self.adventure_experience = 0
                self.adventure_gold = 0

                # Shopping
                self.purchase_history = []
                self.purchase_gold_spent = 0
                self.purchase_gold_made = 0

                # Gear Slots
                self.items_in_inventory = []
                self.item_on_head = None
                self.item_on_body = None
                self.item_on_legs = None
                self.item_in_left = None
                self.item_in_right = None
                self.items_small_list = []
                self.items_small_count = 0
                self.item_small_max = math.ceil(self.level_current / 2)

            def adjust_gp(self, main):
                self.gold += 5
                main.update_display()

            def adjust_xp(self, main):
                self.experience += 5
                main.update_display()

            def gain_level(self, main):
                self.level_current += 1
                main.update_display()

            def retire(self, main):
                print("Retire character " + str(self.name))
                main.update_display()

            def kill(self, main):
                print("Kill character " + str(self.name))
                main.update_display()

            def view_details(self, main):
                main.display_current.disappear()
                main.display_current = main.module_char_detail
                main.module_char_detail.setVisible(True)
                main.module_char_detail.update_info(self)
                main.update_display()


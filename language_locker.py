import random


class LanguageLocker:
    def __init__(self, en="", fr="", it="", es=""):
        self.en = en
        self.fr = fr
        self.it = it
        self.es = es
        self.current_language_selected = ""

    def pull_language_set(self, args):
        # Basically return a list so that a random choice can be made upon loading the card
        if 0 not in args:
            return [self.fr, self.it, self.es]

        language_package_back = []

        if args[0] == 1:
            # French
            print("French Chosen")
            language_package_back.append({"french": self.fr})

        if args[1] == 1:
            print("second")
            language_package_back.append({"italian": self.it})

        if args[2] == 1:
            print("third")
            language_package_back.append({"spanish": self.es})

        return language_package_back

    def select_random_from_locker(self, args):
        # index_of_chosen_language = random.choice(range(len(self.pull_language_set(args))))
        # print(index_of_chosen_language)
        # if index_of_chosen_language == 0:
        #     self.current_language_selected = "french"
        # elif index_of_chosen_language == 1:
        #     self.current_language_selected = "italian"
        # elif index_of_chosen_language == 2:
        #     self.current_language_selected = "spanish"
        # holder_list = [self.en, self.pull_language_set(args)[index_of_chosen_language]]
        # holder_list =
        return [self.en, random.choice(self.pull_language_set(args))]

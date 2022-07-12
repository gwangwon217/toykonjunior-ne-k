from mycroft import MycroftSkill, intent_file_handler


class ToykonjuniorNeK(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('k.ne.toykonjunior.intent')
    def handle_k_ne_toykonjunior(self, message):
        self.speak_dialog('k.ne.toykonjunior')


def create_skill():
    return ToykonjuniorNeK()


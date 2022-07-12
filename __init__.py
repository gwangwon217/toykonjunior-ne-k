from mycroft import MycroftSkill, intent_file_handler
import os

class ToykonjuniorNeK(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        
    @intent_file_handler('k.ne.toykonjunior.intent')
    def handle_k_ne_toykonjunior(self, message):
        self.speak_dialog('k.ne.toykonjunior')

    @intent_file_handler('update.intent')
    def handle_update(self, message):
        os.system("git reset --hard origin/master") 
        os.system("git pull") 
        self.speak_dialog('updated success !')

def create_skill():
    return ToykonjuniorNeK()


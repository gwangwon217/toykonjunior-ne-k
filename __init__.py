import imp
from mycroft import MycroftSkill, intent_file_handler
import json
import sys
import os
class ToykonjuniorNeK(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
        
        
        with open(ROOT_DIR+'/data.json') as json_file:
            self.json_data = json.load(json_file)
            print(self.json_data)


    @intent_file_handler('k.ne.toykonjunior.intent')
    def handle_k_ne_toykonjunior(self, message):
        self.speak_dialog('k.ne.toykonjunior')

    #@intent_file_handler('update.intent')
    #def handle_update(self, message):
    #    self.speak_dialog('updated success !12312')


    # 유닛 종료되었을때
    def endUnit(self):
        self.speak_dialog('end.dialog')


    # 완전히 스킬이 종료되었을때?
    def stop(self):
        self.speak_dialog('end.dialog')
        return super().stop()   
    def converse(self, message=None):
        return super().converse(message)
def create_skill():
    return ToykonjuniorNeK()

 
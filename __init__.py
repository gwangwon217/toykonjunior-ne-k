
from mycroft import MycroftSkill, intent_file_handler,intent_handler
from adapt.intent import IntentBuilder
from mycroft.skills.context import adds_context, removes_context
import json
import sys
import os
from mycroft.util.parse import fuzzy_match
from mycroft.audio import wait_while_speaking
import time
class ToykonjuniorNeK(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.json_data = None    
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
    
        
       
    #Go to Nature and Earth, Step K. 
    @intent_handler(IntentBuilder('enterIntent').require('goto').require('bookname').require('step').require('steplist').build())
    def handle_command(self,message):


        self.bookname = message.data.get('bookname')
        self.step = message.data.get('steplist')
        self.unit = 1
        
        bookFileName = '{}_{}.json'.format(self.bookname.replace(" ","") , self.step)
        with open(self.ROOT_DIR+'/'+bookFileName) as json_file:
            self.json_data = json.load(json_file)
            print(self.json_data)

        if(self.json_data == None):
            #책이름을 못찾은 경우 
            self.speak("not found book file ")
        else:
            #책이름을 찾은 경우 
            self.speak('welcome bookname - {}   step  {}'.format(self.bookname, self.step))

            self.set_context("bookContext", self.bookname)
            self.set_context('stepContext',self.step)
        #self.set_context('unitContext', self.unit)
        # # 메뉴로 진입 (dialogue, word , song, minibook )
            self.unitList = self.json_data.get("unitlist")
            # 유닛 리스트를 가져온다 
            print(self.unitList)
            self.get_response()
            




    #go to unit 1 dialogue
    @intent_handler(
    IntentBuilder('dialogue').require('goto').require('unit'
    ).optionally('number')
    .require('dialogue')
    #.require('bookContext')
    .build())
    @adds_context('dialogueContext')
    def handle_dialogue(self, message):
        if( message.data.get('number') != None):
            self.unit = message.data.get('number')
        
        if(self.json_data == None):
            #test mode  .require('bookContext') 주석 해제해야 함 
            
            bookFileName = 'natureandearth_k.json' 
            with open(self.ROOT_DIR+'/'+bookFileName) as json_file:
                self.json_data = json.load(json_file)
                print(self.json_data)
        self.unitList = self.json_data.get("unitlist")
        self.unitIdx = int(self.unit) - 1   # 1이 배열 0
        if ( self.unitIdx < len(self.unitList) ) :
            
            self.contents = self.unitList[self.unitIdx]
            
           
            self.dialogueContents = self.contents.get('dialogue')
            title = self.dialogueContents.get('title')
            self.speak('unit {} {}'.format(self.unit, title)) # dialogue 주제?공지? 를 말해준다. 

            self.listenList = self.dialogueContents.get('listen')
            self.sayList = self.dialogueContents.get('say')
            #for idx in range(0, len(self.listenList)) :
            idx = 0 
            for rang in self.listenList:
                self.speak(self.sayList[idx], wait = True, expect_response = False)
                wait_while_speaking()
                idx = idx + 1
                time.sleep(3)
            
            #time.sleep(2)
            
            self.dialogLen = idx
            self.dialogReadIdx = 0 
            self.speak('Listen and say. ',  expect_response = True)
            self.handle_dialogue_say(message)
            #  읽을 대화문의 갯수 
            #idx = 0 
            #for rang in self.sayList:
            #    if idx % 2 == 0 :# 먼저 질문 
            #        self.speak(self.sayList[idx], wait = True, expect_response = False)
            #    else:# 사용자 응답 
            #        time.sleep(3)
                    #self.response = self.get_response(num_retries= 0)
            #        self.speak( wait = True, expect_response = False)
                    
            #    idx = idx + 1
            #    time.sleep(3)

            # for rang  in self.listenList :    
            #     print('list')    
            #     self.listen = self.listenList[idx]
            #     self.say = self.sayList[idx]
            #     self.lestenAndSay(self.listen,self.say)               
            #     idx = idx + 1

            #self.speak('end dialogue')# 신호음으로 대체해야함 

        #self.speak_dialog('start dialogue  unit {}'.format(self.unitList[0]))
        else:# 인덱스가 배열갯수 초과 시  종료? 다음 유닛?
            self.speak('next unit!?? now {}'.foramt(self.unitIdx) )
    @intent_handler(IntentBuilder('dailogueintent').require('dialogueContext').build())
    def handle_dialogue_say(self, message):
        #self.speak(' in dialogue   {}   / {}'.format(self.dialogReadIdx , self.dialogLen))
        #if self.dialogReadIdx % 2 == 0 :
        if self.dialogReadIdx < self.dialogLen :
            self.speak(self.sayList[self.dialogReadIdx], expect_response = True)
            
            self.dialogReadIdx = self.dialogReadIdx + 1 
        else:
            removes_context('dialogueContext')
            self.speak('end Dialogue')
            return
        
        self.dialogReadIdx = self.dialogReadIdx + 1     
     
    
    #go to unit 1 word
    @intent_handler(
    IntentBuilder('wordIntent').require('goto').require('unit'
    ).optionally('number')
    .require('word')
    #.require('bookContext')
    .build())
    def handle_word(self, message):
        if( message.data.get('number') != None):
            self.unit = message.data.get('number')
        
        if(self.json_data == None):
            #test mode  .require('bookContext') 주석 해제해야 함 
           
            bookFileName = 'natureandearth_k.json' 
            with open(self.ROOT_DIR+'/'+bookFileName) as json_file:
                self.json_data = json.load(json_file)
                print(self.json_data)
        self.unitList = self.json_data.get("unitlist")
        self.unitIdx = int(self.unit) - 1   # 1이 배열 0
        if ( self.unitIdx < len(self.unitList) ) :
            
            self.contents = self.unitList[self.unitIdx]
        
            self.wordContents = self.contents.get('word')
            self.wordList = self.wordContents.get('listen')
            title = self.wordContents.get('title')
            self.speak('unit {} {}'.format(self.unit, title)) # dialogue 주제?공지? 를 말해준다. 

            #for idx in range(0, len(self.listenList)) :
            idx = 0 
            for rang  in self.wordList :    
                #print('list')    
                self.word = self.wordList[idx]
                self.lestenAndSay(self.word,self.word)
                idx = idx + 1

            self.speak('end word')# 신호음으로 대체해야함 

        #self.speak_dialog('start dialogue  unit {}'.format(self.unitList[0]))
        else:# 인덱스가 배열갯수 초과 시  종료? 다음 유닛?
            self.speak('next unit!?? now {}'.foramt(self.unitIdx) )
    

      #go to unit 1 minibook
    @intent_handler(
    IntentBuilder('minibookIntent').require('goto').require('unit'
    ).optionally('number')
    .require('minibook')
    #.require('bookContext')
    .build())
    def handle_minibook(self, message):
        if( message.data.get('number') != None):
            self.unit = message.data.get('number')
        
        if(self.json_data == None):
            #test mode  .require('bookContext') 주석 해제해야 함 
            ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
            bookFileName = 'natureandearth_k.json' 
            with open(ROOT_DIR+'/'+bookFileName) as json_file:
                self.json_data = json.load(json_file)
                print(self.json_data)
        self.unitList = self.json_data.get("unitlist")
        self.unitIdx = int(self.unit) - 1   # 1이 배열 0
        if ( self.unitIdx < len(self.unitList) ) :
            
            self.contents = self.unitList[self.unitIdx]
        
            self.minibook = self.contents.get('minibook')
            self.listenList = self.minibook.get('listen')
            title = self.minibook.get('title')
            self.speak('unit {} {}'.format(self.unit, title)) # dialogue 주제?공지? 를 말해준다. 

            self.minibookFuzzy(self.listenList)
            self.speak('end word')# 신호음으로 대체해야함 

        #self.speak_dialog('start dialogue  unit {}'.format(self.unitList[0]))
        else:# 인덱스가 배열갯수 초과 시  종료? 다음 유닛?
            self.speak('next unit!?? now {}'.foramt(self.unitIdx) )
      

    # 제시어, 정답 을 주고 듣고 말한 값을 비교 
    def lestenAndSay(self, listen, answer):
        self.response =  self.get_response(listen, num_retries= 0)
        wait_while_speaking()
        msg = ''
        if( self.response != None):
            fuzzy = fuzzy_match(self.response.lower(), answer.lower()) # 실제 정답과 비교 
            msg = self.checkedFuzzy(fuzzy)
            #self.speak ('fuzzy {0} /. msg = {1}'.format(fuzzy, msg))
            self.speak ('{0}'.format(msg))
            time.sleep(2)
    #미니북 평가 듣고 말하고 실행 후 누적 점수를 알려준다. 
    def minibookFuzzy(self, list):
        sumFuzzy  = 0 
        size = len(list)
        
        idx = 0
        for rang  in list :    
            listen = list[idx]
            self.speak(listen)
            time.sleep(10)
            self.response =  self.get_response(num_retries= 0)
            #반복 횟수를 주거나. 시간을 늘리거나.. (늘리는 방법은?)            
            if self.response == None:
                fuzzy = 0
            else:
                fuzzy = fuzzy_match(self.response, listen.lower() )
            
            sumFuzzy = sumFuzzy + fuzzy
            idx = idx + 1 

        resultFuzzy = sumFuzzy / size 
        msg = self.checkedFuzzy(resultFuzzy)
        self.speak ('{0}'.format(msg))
        time.sleep(2)
    #말하기 점수매칭에 따른 결과메세지 반환 
    def checkedFuzzy (self, fuzzy):
        msg = ''
        if fuzzy > 0.2 :
            msg = 'Great.'
        else:
            if fuzzy > 0.9:
                msg = "you're Perfect."
            else:
                msg = 'Great.'
        return msg

    @intent_handler(IntentBuilder('playSong').require('playsong').require('bookContext').require('unitContext').build())
    def handle_playthesong(self,message):
        self.speak('play the song')

    # @intent_handler(IntentBuilder('word').build())
    # def handle_word(self,message):
    #     self.speak_dialog('start word')

    # 유닛 종료되었을때
    def endUnit(self):
        # TODO  유닛을 증가시켜 다음으로 이동?
        self.speak('end unit')

    # # 완전히 스킬이 종료되었을때?
    @removes_context('bookContext')
    def stop(self):
        
        #self.speak_dialog('end.dialog')
        return super().stop()   
    # def converse(self, message=None):
    #     return super().converse(message)
def create_skill():
    return ToykonjuniorNeK()

 
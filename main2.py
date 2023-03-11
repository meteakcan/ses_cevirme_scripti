

import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import make_chunks
import time
import speech_recognition as sr

class Translation:

    def __init__(self,path):
        self.path=fr"{path}"
        self.parts=0
        self.current_part=0
        self.execute_time=0
        self.current_path=os.getcwd()

        temp=""
        for i in self.path[::-1]:
            if(i=="."):break
            temp+=i

        self.format=temp[::-1]
        self.sound = AudioSegment.from_file(self.path,self.format)

        temp=""
        for i in path[::-1]:
            if(i=="\\"):
                break
            temp+=i

        filename=""
        status=False

        for i in temp:

            if(status==True):
                filename+=i
            if(i=="."):status=True

        filename=filename[::-1] 
        self.filename=filename

    def cut_sound_by_range(self,duration=45,r_s=5,process=False):

        if(duration-r_s<=0):return None
        sound_duration=int(str(len(self.sound))[:-3])

        cut_ranges=[]
        for i in range(10000):
            if(i>=1):
                cut_ranges.append((i*(duration-r_s),duration+(i*(duration-r_s))))
                if(duration+(i*(duration-r_s)))>=sound_duration:break
                continue
            cut_ranges.append((0,(i+1)*duration))

        try:
            os.mkdir(f"{self.filename}_files")
        except FileExistsError:
            pass
        os.chdir(f"{self.filename}_files")
        counter=0
        for x,y in cut_ranges:
            new_file=self.sound[(x*1000):(y*1000)]
            new_file.export(f"{self.filename}_part{counter+1}.wav",format="wav")
            counter+=1

        if(process):
            self.parts=counter
            print(counter)

    def convert(self,external_path=None,process=False,save=False):

        start=time.time()

        r = sr.Recognizer()
        if(process==False):
            external_path=self.path

        file = sr.AudioFile(external_path)
        print("işlem sürüyor")
        result=""
        try:
            with file as source:
                audio = r.record(source)
                result = r.recognize_google(audio,language="tr")
        except FileNotFoundError:
            print("dosya yok")
        except:
            if(process):result+=f"{self.filename}"+f"_part{self.current_part}.wav "+"bir hatadan dolayı okunamadı."
            else:result+=f"{self.filename}, bir hatadan dolayı okunamadı."


        if(process):result+=f"...\nEnding Part {self.current_part}\n------------------------------\n"
        else: result+=f"...\nENDING {self.filename}\n-----------------------\n"
        print(f"Part {self.current_part}/{self.parts}",)

        if(save):
            with open(self.current_path,"a+",encoding="utf-8") as file:
                file.write(result)

        stop=time.time()
        total_time=float(f"{(stop-start):.2f}")

        print(f"It took {total_time} seconds")
        if(process):
            kalan_sure=(self.parts-self.current_part)*total_time
            kalan_sure_dk=int(kalan_sure//60)
            kalan_sure_sn=int(kalan_sure%60)
            print(f"Tahmini kalan süre : {kalan_sure_dk}dk {kalan_sure_sn}sn")
    
        return result
            
    def process_all(self):

        self.cut_sound_by_range(duration=100,r_s=5,process=True)
        print(self.parts)
        for i in range(1,self.parts+1):
            self.current_part=i
            self.convert(self.filename+f"_part{i}.wav",True,save=True)

mypath=r"C:\Users\Akcan\Desktop\file_will_convert.mp4"

x=Translation(mypath)
x.process_all()
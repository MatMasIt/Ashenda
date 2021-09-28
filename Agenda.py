import sys
import npyscreen
import datetime
import subprocess
import glob
import os
ps.system("git pull")
def shell(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        output = str(e.output)
    return output

class TestMenuForm(npyscreen.ActionForm):
    def create(self):
        self.lastC = False
        self.lastH = 0
        self.date = self.add(npyscreen.TitleDateCombo, name = "Data")
        self.heavy = self.add(npyscreen.TitleSlider, out_of=10, name = "Carico del giorno")
        self.content =  self.add(npyscreen.MultiLineEdit,
               value = "",
               max_height=20, rely=9)    
    def while_editing(self):
        try:
            partsDate = self.date.value.strftime("%Y-%m-%d").split("-")
        except:
            return False
        if self.heavy.value!=self.lastH:
            if len(partsDate)==3:
                open(glob.glob(partsDate[0]+'/'+str(int(partsDate[1]))+'_*/'+partsDate[2]+'_*/main.md')[0].replace("main.md","howhard"),"w+").write(str(self.heavy.value))     
        if self.content.value!=self.lastC and self.lastC!=False:
            open(glob.glob(partsDate[0]+'/'+str(int(partsDate[1]))+'_*/'+partsDate[2]+'_*/main.md')[0],"w").write(self.content.value)
            self.lastH = self.heavy.value
        self.lastC = self.content.value
        if len(partsDate)==3:
             val = shell('cat '+partsDate[0]+'/'+str(int(partsDate[1]))+'_*/'+partsDate[2]+'_*/main.md')
             if len(glob.glob(partsDate[0]+'/'+str(int(partsDate[1]))+'_*/'+partsDate[2]+'_*/howhard')):
                 howhard=shell('cat '+partsDate[0]+'/'+str(int(partsDate[1]))+'_*/'+partsDate[2]+'_*/howhard')
                 try:
                     howhard = float(howhard)
                 except:
                     howhard = 0.0
             else:
                 howhard = 0.0
             try:
                 val=val.decode("utf-8")
             except:
                 None
             self.content.value = val
             self.heavy.value = howhard
        return False
class TestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        testMenuForm = TestMenuForm(name="Diario")
        self.registerForm('MAIN', testMenuForm)


def main(args):
    App = TestApp()
    try:
        App.run()
    except KeyboardInterrupt as e:
        os.system("git add *")
        os.system("git commit")
        os.system("git push origin main")
if __name__ == '__main__':
    main(sys.argv)

from pandac.PandaModules import loadPrcFile

import sys
import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.actor import Actor

from direct.showbase.DirectObject import DirectObject
import random

size = 5
base.disableMouse()
#text from manual
text = TextNode('node name')
text.setText('Jubriba Tetris')
textNodePath = aspect2d.attachNewNode(text)
textNodePath.setScale(0.07)
textNodePath.setPos(-1,0,.8)
#cmr12 = loader.loadFont('cmr12')
text.setWordwrap(10.0)
#text.setFont(cmr12)
text.setSmallCaps(1)
text.setSmallCapsScale(0.7)
text.setTextColor(1, 1, 0.5, 1)
text.setShadow(0.05, 0.05)
text.setShadowColor(0, 0, 0, 1)
text.setFrameColor(0.5, 0.8, 0.5, 1)
text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
text.setCardColor(0.5, 0.8, 0.5, 0.3)
text.setCardAsMargin(0.2, 0.2, 0.1, 0.1)
modelspath = "data/models/"

class Shape:
    def __init__(self, type, pos = (0,0,0), parent=render):
        self.type = type
        self.chBoxs = []
        for i in range(4):
            brickActor = Actor.Actor()
            brickActor.loadModel(modelspath+"brick")
            brickActor.loadAnims({'anim':modelspath+"anim"})
            brickActor.loadAnims({'anim1':modelspath+"anim1"})
##            brickActor.loop('anim',fromFrame = 0, toFrame = 30)
            self.chBoxs.append(brickActor)
##            self.chBoxs.append(loader.loadModelCopy(modelspath+"brick"))
        for i in range(1,4):
            self.chBoxs[i].reparentTo(self.chBoxs[0])
        
        if   type == 1:
            self.pieces = [0,0],[1,0],[1,1],[2,1]
            for i in range(4):
                self.chBoxs[i].setColor(1,1,0,1)
        elif type == 2:
            self.pieces = [0,0],[1,0],[0,1],[-1,1]
            for i in range(4):
                self.chBoxs[i].setColor(0,1,0,1)
        elif type == 3:
            self.pieces = [0,0],[1,0],[-1,0],[0,1]
            for i in range(4):
                self.chBoxs[i].setColor(0,1,1,1)
        elif type == 4:
            self.pieces = [0,0],[1,0],[0,1],[1,1]
            for i in range(4):
                self.chBoxs[i].setColor(0,0,1,1)
        elif type == 5:
            self.pieces = [0,0],[-1,0],[1,0],[2,0]
            for i in range(4):
                self.chBoxs[i].setColor(1,0,0,1)
        elif type == 6:
            self.pieces = [0,0],[0,1],[-1,1],[0,-1]
            for i in range(4):
                self.chBoxs[i].setColor(1,0,1,1)
        elif type == 7:
            self.pieces = [0,0],[0,1],[1,1],[0,-1]
            for i in range(4):
                self.chBoxs[i].setColor(0.9,0.6,0.3,1)
            
        
            
        
        
        self.chBoxs[0].setPos(pos[0],pos[1],pos[2])    
        self.rePos()
        self.chBoxs[0].reparentTo(parent)
        
    def rePos(self):
        for i in range(1,4):
            self.chBoxs[i].setPos(self.pieces[i][0]*size,0,self.pieces[i][1]*size)
        
    def hide(self):
        for chb in self.chBoxs:
            chb.hide() 
    def detachNode(self):
        for chb in self.chBoxs:
            chb.detachNode()    
    
    def moveDown(self):
        self.chBoxs[0].setZ(self.chBoxs[0].getZ()-size)
    
    def moveUp(self):
        self.chBoxs[0].setZ(self.chBoxs[0].getZ()+size)
        
            
    def rotRight(self):
        for i in range(1,4):
            tmp = self.pieces[i][0]
            self.pieces[i][0] = self.pieces[i][1]
            self.pieces[i][1] = -1*tmp
            self.rePos()
            #self.chBoxs[i].setZ(-1*self.chBoxs[i].getX())
            #self.chBoxs[i].setX(self.chBoxs[i].getZ())
    
    def rotLeft(self):
        for i in range(1,4):
            tmp = self.pieces[i][0]
            self.pieces[i][0] = -1*self.pieces[i][1]
            self.pieces[i][1] = tmp
            self.rePos()
            #self.chBoxs[i].setZ(self.chBoxs[i].getX())
            #self.chBoxs[i].setX(-1*self.chBoxs[i].getZ())
    
    def moveLeft(self):
        self.chBoxs[0].setX(self.chBoxs[0].getX()-size)
    
    def moveRight(self):
        self.chBoxs[0].setX(self.chBoxs[0].getX()+size)
        
class WorldGame(DirectObject):
    def __init__(self):
      self.go = True
      base.setBackgroundColor(0.5, 0.5, 0.5)
      self.title = "Jubriba Tetris"
      self.linesRem = 0
      self.score = 0
      self.actScore = 20
      #messenger.toggleVerbose()
      self.tetBoard = render.attachNewNode('Tetris Board')
      #self.tetBoard.setAntialias(7)
      self.tetBoard.setPos(0,0,-50)
      self.tetGame = self.tetBoard.attachNewNode('Tetris game')
      self.tetGame.setTransparency(1)
      self.boxsToRem = self.tetGame.attachNewNode('ToRemove')
##      self.messageText = OnscreenText(text = 'my text string', pos = (0, 0), scale = .1)
      self.createGUI()
      self.ppMusic = loader.loadMusic("data/music/pp1.mp3")
      self.ppMusic.setVolume(0.5)
      self.embedSound = loader.loadSfx("data/sounds/embed.wav")
      toremSound1 = loader.loadSfx("data/sounds/torem1.wav")
      toremSound2 = loader.loadSfx("data/sounds/torem2.wav")
      toremSound3 = loader.loadSfx("data/sounds/torem3.wav")
      toremSound4 = loader.loadSfx("data/sounds/torem4.wav")
      self.goSound = loader.loadSfx("data/sounds/go.wav")
      self.toremSounds = [toremSound1,toremSound2,toremSound3,toremSound4]
      self.speed1 = 0.5
      self.speed10 = 0.06
      self.speed = self.speed1
      self.p = 0
      self.cass = []
      self.cass.append([])
      for i in range(11):
        self.cass[0].append(1)        
      for i in range(1,22):
        self.cass.append([])
        self.cass[i].append(1)
        for j in range(9):
          self.cass[i].append(0)
        self.cass[i].append(1)
          
##        self.dcass = []
##        self.dcass.append([])
##        dts = "......"
##        for i in range(11):
##            for j in range(0,22):
##                dt = TextNode(str(i)+","+str(j))
##                dt.setText(str(self.cass[j][i]))
##                dtnp = self.tetGame.attachNewNode(dt)
##                dtnp.setPos((i-5)*size,-5,j*size-2)
##                dtnp.setScale(2)
##                self.dcass.append([])
##                self.dcass[i].append(dt)
          
      self.shapeTest = Shape(1,pos=(50,0,0),parent=render)
      self.shapeTest.hide()

      self.rows = []
      for i in range(22):
        self.rows.append([])
          
      
      self.frame = loader.loadModel(modelspath+"frame")
      self.frame.setColor(0.3,0.3,0.5,1)
      self.frame.reparentTo(self.tetBoard)
      
      self.accept('escape', self.areYouSure)
      self.accept('k',self.rotR)
      self.accept('arrow_up',self.rotR)
      self.accept('i',self.rotL)
      self.accept('j',self.movL)
      self.accept('arrow_left',self.movL)
      self.accept('l',self.movR)
      self.accept('arrow_right',self.movR)
      self.accept('s',self.start)
      self.accept('p',self.pause)
      self.accept('space', self.toTheEnd)
      self.accept('arrow_down',self.toTheEnd)
      self.accept('a',self.speedUp)
      self.accept('a-up',self.speedDown)
      self.accept('z',self.levelUp)
      
    def aysRes(self,value):
      print value
      if value: sys.exit()
      else: 
        self.disableButtons(DGG.NORMAL)
        self.aysDiag.hide() 
        self.pause()
      
    def disableButtons(self, state):
      self.buttonStart['state'] = state
      self.buttonExit['state'] = state
      
      
    def areYouSure(self):
      self.disableButtons(DGG.DISABLED)
      self.pause()
      self.aysDiag.show()
                                
      
      
    def createGUI(self):
      aysbg = loader.loadModel('data/models/aysBg')
      self.aysDiag = YesNoDialog(text = '', dialogName = 'dialog name',
                                 buttonTextList = ('si','no'),
                                 geom = aysbg.find('**/areYouSureBg'),
                                 geom_scale = (0.7, 0, 0.7/2),
                                 #relief = FLAT,
##                                 text_bg = (1,1,3,0.5),
                                 pad = (0,0), topPad = 0, midPad = 0, sidePad = 0,
                                 frameSize = (0,0.1,0,0.1),
                                 fadeScreen = 0 ,
                                 frameColor = (1,1,0,0),
				 suppressKeys = 1,
                                 command = self.aysRes,
                                 buttonValueList = (True,False))
      self.aysDiag.hide()
      self.buttons = DirectFrame(pos=(1,0,.8))
      maps = loader.loadModel('data/models/button_start_maps')
      self.buttonStart = DirectButton(relief = None, command = self.start,
                                     rolloverSound = None, clickSound = None,
                                     geom = (maps.find('**/button_ready'),
                                     maps.find('**/button_click'),
                                     maps.find('**/button_rollover'),
                                     maps.find('**/button_disabled')))
      self.buttonStart.setSx(0.4)
      self.buttonStart.setSz(0.4/4)
      self.buttonStart.reparentTo(self.buttons)
      maps = loader.loadModel('data/models/button_exit_maps')
      self.buttonExit = DirectButton(pos = (0,0,-0.1), relief = None, command = self.areYouSure,
                                     rolloverSound = None, clickSound = None,
                                     geom = (maps.find('**/button_ready_exit'),
                                     maps.find('**/button_click_exit'),
                                     maps.find('**/button_rollover_exit'),
                                     maps.find('**/button_disabled_exit')))
      self.buttonExit.setSx(0.4)
      self.buttonExit.setSz(0.4/4)
      self.buttonExit.reparentTo(self.buttons)
    
    def debugInfo(self):
      for i in range(11):
        for j in range(0,22):
          self.dcass[i][j].setText(str(self.cass[j][i]))
    
    def restartBoard(self):
      self.cass = []
      self.cass.append([])
      for i in range(11):
        self.cass[0].append(1)        
      for i in range(1,22):
        self.cass.append([])
        self.cass[i].append(1)
        for j in range(9):
            self.cass[i].append(0)
        self.cass[i].append(1)
      self.shapeTest.detachNode()
      for row in self.rows:
        for np in row:
          np.detachNode()
      self.rows = []
      for i in range(22):
        self.rows.append([])
        
    def updateText(self):
        stext = self.title+"\nlines: "+str(self.linesRem)
        stext = stext + "\nscore: "+str(self.score)
        stext = stext + "\nspeed: "+str(self.speed)
        stext = stext + "\nlevel: "+str(int((1-(self.speed-self.speed10)/(self.speed1-self.speed10))*10+1))
        text.setText(stext)

    def ticTac(self,task):
        if ((task.time - self.mTime) or self.go) < self.speed:
            pass
        else:
            self.mov()
            self.mTime = task.time
        return Task.cont
    def salir(self):
      self.areYouSure()
    def start(self):
        self.spd = False
        self.go = False
        self.title = "Jubriba Tetris"
        self.speed = self.speed1
        self.linesRem = 0
        self.actScore = 20
        self.score=0
         
        self.updateText()
        self.restartBoard()
        self.makeNewShape()
        self.p = False
        
        #self.sec.finish()
        #self.sec = Sequence(self.intTic,Wait(self.speed))
        #self.sec.loop()
        self.mTime = 0
        taskMgr.add(self.ticTac, 'TicTac')
        self.ppMusic.setLoop(True)
        self.ppMusic.play()

    def pause(self):
        self.go = not self.go
        if self.go:
            self.title = "Pause"
        else:
            self.title = "Jubriba Tetris"
        self.updateText()
    
    def stop(self):
        taskMgr.remove('TicTac')

    def levelUp(self):
        self.speed = self.speed - (self.speed1-self.speed10)/10
        if self.speed < self.speed10: self.speed = self.speed1
        self.updateText()
        
    def speedUp(self):
        if not self.spd:
            self.oldSpeed = self.speed
            self.spd = not self.spd
            self.speed = 0
            
    def speedDown(self):
        self.spd = False
        self.speed = self.oldSpeed
        
    def makeNewShape(self):
      ty = random.randint(1,7)
      self.shapeTest = Shape(ty,pos = (0,0,95), parent = self.tetGame)
      if not self.isValidPos():
        self.stop()
        self.go = True
        self.title = "Game Over"
        self.ppMusic.stop()
        self.goSound.play()
        self.updateText()
    
    def isValid(self,x,z):
        if self.cass[z][x]!=0:
          return False
        return True
    
    def embedShape(self):
      self.embedSound.play()
      self.score = self.score + self.actScore
      torem = []
      for i in range(4):
        if(i==0):
          x = int(self.shapeTest.chBoxs[0].getX())/5+5
          y = int(self.shapeTest.chBoxs[0].getY())/5
          z = int(self.shapeTest.chBoxs[0].getZ())/5+1
        else:
          x = int(self.shapeTest.chBoxs[0].getX()+self.shapeTest.chBoxs[i].getX())/5+5
          y = int(self.shapeTest.chBoxs[0].getY()+self.shapeTest.chBoxs[i].getY())/5
          z = int(self.shapeTest.chBoxs[0].getZ()+self.shapeTest.chBoxs[i].getZ())/5+1
        self.cass[z][x] = self.shapeTest.type
        self.shapeTest.chBoxs[i].wrtReparentTo(self.tetGame)
        self.shapeTest.chBoxs[i].setColorScale(.6,.6,.6,1)
        self.shapeTest.chBoxs[i].play('anim', fromFrame = 0, toFrame = 6)
        self.rows[z].append(self.shapeTest.chBoxs[i])
        if len(self.rows[z]) == 9:
          self.linesRem = self.linesRem + 1
          if self.linesRem % 10 == 0:
            self.levelUp()
          torem.append(z)
      torem.sort()
      for i in range(len(torem)):
        self.score = self.score + (i+1)*10
      
      for i in torem:
        for j in self.rows[i]:
          j.wrtReparentTo(self.boxsToRem)
          j.loop('anim1', fromFrame = 0, toFrame = 30)
          
      if (len(torem)!=0):
        self.go = True
        lsi = LerpPosInterval(self.boxsToRem,0.5,Point3(0,3000,0),blendType = "easeIn")
        lsi1 = LerpPosInterval(self.boxsToRem,0.2,Point3(0,-20,0),blendType = "easeInOut")
        lsi2 = LerpPosInterval(self.boxsToRem,0.2,Point3(0,20,0),blendType = "easeInOut")
        lci = LerpColorScaleInterval(self.boxsToRem,0.2,Point4(1.4,1.4,1.4,1),blendType = "easeIn")
        fi = Func(self.clank,torem)  
        seq = Sequence(lci,lsi1,lsi,fi)
        self.toremSounds[len(torem)-1].play()
        seq.start()
      self.actScore = 20
      self.updateText()
      
    def clank(self, torem):
      self.boxsToRem.setPos(0,0,0)
      for i in torem:
        for j in self.rows[i]:
          j.detachNode()
      c = 0
      for i in torem:
        for k in range(i-c,21):
          for j in range(1,10):
            self.cass[k][j] = self.cass[k+1][j]
          for j in self.rows[k]:
            j.setZ(j.getZ()-size)
          self.rows[k] = self.rows[k+1]
          self.rows[21] = [] 
        c = c+1
        self.go = False
    
    def checkRow(self,z):
      for i in range(1,11):
        pass
    
    def isValidPos(self):
        x = int(self.shapeTest.chBoxs[0].getX())/5+5
        y = int(self.shapeTest.chBoxs[0].getY())/5
        z = int(self.shapeTest.chBoxs[0].getZ())/5+1
        if not self.isValid(x, z):
                return False
        for i in range(1,4):
            x = int(self.shapeTest.chBoxs[0].getX()+self.shapeTest.chBoxs[i].getX())/5+5
            y = int(self.shapeTest.chBoxs[0].getY()+self.shapeTest.chBoxs[i].getY())/5
            z = int(self.shapeTest.chBoxs[0].getZ()+self.shapeTest.chBoxs[i].getZ())/5+1
            if not self.isValid(x, z):
                return False
        return True
    
    def mov(self):
        if self.go: return False
        self.shapeTest.moveDown()
        if not self.isValidPos():
            self.shapeTest.moveUp()
            self.embedShape()
            self.makeNewShape()
            return False
        self.actScore = self.actScore - 1
        return True

    def toTheEnd(self):
        while self.mov():
            self.actScore = self.actScore + 1
    
    def rotR(self):
        self.shapeTest.rotRight()
        if not self.isValidPos():
            self.shapeTest.rotLeft()
        else:
            self.actScore = self.actScore - 1
    
    def rotL(self):
        self.shapeTest.rotLeft()
        if not self.isValidPos():
            self.shapeTest.rotRight()
        else:
            self.actScore = self.actScore - 1
        
    def movR(self):
        self.shapeTest.moveRight()
        if not self.isValidPos():
            self.shapeTest.moveLeft()
        else:
            self.actScore = self.actScore - 1
            
    def movL(self):
        self.shapeTest.moveLeft()
        if not self.isValidPos():
            self.shapeTest.moveRight()
        else:
            self.actScore = self.actScore - 1
  
  
class Menu(DirectObject):
  def __init__(self):
    base.setBackgroundColor(0, 0, 0)
      
camera.setPos(0, -210, -5)

# Now create some lights to apply to everything in the scene.

# Create Ambient Light
ambientLight = AmbientLight( 'ambientLight' )
ambientLight.setColor( Vec4( 0.4, 0.4, 0.4, 1 ) )
ambientLightNP = render.attachNewNode( ambientLight)
render.setLight(ambientLightNP)

# Directional light 01
directionalLight = DirectionalLight( "directionalLight" )
directionalLight.setColor( Vec4( 0.8, 0.8, 0.8, 1 ) )
directionalLightNP = render.attachNewNode( directionalLight)
# This light is facing backwards, towards the camera.
directionalLightNP.setHpr(180, -20, 0)
render.setLight(directionalLightNP)

# Directional light 02
directionalLight = DirectionalLight( "directionalLight" )
directionalLight.setColor( Vec4( 0.8, 0.8, 0.8, 1 ) )
directionalLightNP = render.attachNewNode( directionalLight)
# This light is facing forwards, away from the camera.
directionalLightNP.setHpr(0, -20, 0)
render.setLight(directionalLightNP)





wg = Menu()    
wg = WorldGame()



run()

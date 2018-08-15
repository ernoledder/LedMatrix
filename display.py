import threading
import time
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
import weather
from PIL import Image

ReceivedText = "Send me text"           #Standard text in case there is no available text

class Display(threading.Thread):
    def __init__(self, weather, dimmer):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._dimmer = dimmer

        # Configure LED matrix driver
        self._matrix = RGBMatrix(32, 2, 1)
        self._matrix.pwmBits = 11
        self._matrix.brightness = 25
        
        
        # Load fonts
        self._font_large = graphics.Font()          #Different fonts can be found online or you can make one yourself
        self._font_large.LoadFont("rpi-rgb-led-matrix/fonts/10x20.bdf")
        self._font_small = graphics.Font()
        self._font_small.LoadFont("rpi-rgb-led-matrix/fonts/6x10.bdf")
        self._font_tiny = graphics.Font()
        self._font_tiny.LoadFont("rpi-rgb-led-matrix/fonts/4x6.bdf")
        
        # Define colors
        self._white = graphics.Color(255, 255, 255)             #You can add your own colours by adding the corresponding rgb values
        self._red = graphics.Color(229, 18, 18)
        self._blue = graphics.Color(64, 64, 255)
    
    #This function draws the clock on the ledmatrix
    def _drawClock(self, canvas):
        canvas.Clear()                  #Clears the ledmatrix so something new can be written
        
        graphics.DrawText(canvas, self._font_large, 1, 13, self._white, time.strftime("%-2I:%M"))   
        graphics.DrawText(canvas, self._font_small, 53, 13, self._white, time.strftime("%p"))

        graphics.DrawText(canvas, self._font_small, 2, 22, self._white, time.strftime("%a %b %-d"))
        
        graphics.DrawText(canvas, self._font_tiny, 0, 31, self._white, "send me something")
        
    #Draws the last received text
    def _drawText(self, canvas):
        canvas.Clear()
        file = open("text.txt", "r")
        ReceivedText = file.read()
        
        i = ReceivedText.find('}')          #All received text have a } to know where the text ends
        ReceivedText = ReceivedText[:i]
        
        if(len(ReceivedText) > 16):                 #There can't be more than 16 characters on one line
            i = int(len(ReceivedText)/16)
            for x in range(i):
                q = 16 * x 
                z = 16 * (x+1)
                if(x == (i-1)):                      # On the last line the remaining characters are drawn
                    graphics.DrawText(canvas, self._font_tiny, 1, ((x+1) * 7), self._white, ReceivedText[q:])
                else:    
                    graphics.DrawText(canvas, self._font_tiny, 1, ((x+1) * 7), self._white, ReceivedText[q:z])
            
            
        else:    
            graphics.DrawText(canvas, self._font_large, 1, 8, self._white, ReceivedText)    #If there are less than 16 characters a larger font can be used
        
        
    #Opens and reads the rgb values of each pixel of a png file    
    def _drawPic(self, canvas):
        
        canvas.Clear()
        
        im = Image.open('image.png', 'r')
        width, height = im.size
        pixel_values = list(im.getdata())
        i = 0
        for x in range(width):
            for y in range(height):
                r = int(pixel_values[i][0])
                g = int(pixel_values[i][1])
                b = int(pixel_values[i][2])
                i = i + 1
                canvas.SetPixel(x,y,r,g,b)              #With SetPixel you can light a led with rgb values r,g,b on place x,y
            
    
    def run(self):
        canvas = self._matrix.CreateFrameCanvas()      #Creates the canvas that we will draw on
        ToShow = 1                                     #Is used to alter between text and picture
        while True:
            self._drawClock(canvas)
            time.sleep(0.05)
            canvas = self._matrix.SwapOnVSync(canvas)
            self._matrix.brightness = self._dimmer.brightness
            time.sleep(5)                               #Change between text and picture every 5 seconds
            if(ToShow == 0):
                self._drawText(canvas)
                ToShow = 1
            else:
                self._drawPic(canvas)
                ToShow = 0
            
            canvas = self._matrix.SwapOnVSync(canvas)
            self._matrix.brightness = self._dimmer.brightness       #It is possible to adjust the brightness of the screen (on your own risk)
            time.sleep(5)
            

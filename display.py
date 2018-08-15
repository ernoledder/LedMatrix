import threading
import time
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
import weather
from PIL import Image

ReceivedText = "Send me text"

class Display(threading.Thread):
    def __init__(self, weather, dimmer):
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self._weather = weather
        self._dimmer = dimmer

        # Configure LED matrix driver
        self._matrix = RGBMatrix(32, 2, 1)
        self._matrix.pwmBits = 11
        self._matrix.brightness = 25
        
        
        # Load fonts
        self._font_large = graphics.Font()
        self._font_large.LoadFont("rpi-rgb-led-matrix/fonts/10x20.bdf")
        self._font_small = graphics.Font()
        self._font_small.LoadFont("rpi-rgb-led-matrix/fonts/6x10.bdf")
        self._font_tiny = graphics.Font()
        self._font_tiny.LoadFont("rpi-rgb-led-matrix/fonts/4x6.bdf")
        
        # Define colors
        self._white = graphics.Color(255, 255, 255)
        self._red = graphics.Color(229, 18, 18)
        self._blue = graphics.Color(64, 64, 255)

    def _drawClock(self, canvas):
        canvas.Clear()
        
        graphics.DrawText(canvas, self._font_large, 1, 13, self._white, time.strftime("%-2I:%M"))
        graphics.DrawText(canvas, self._font_small, 53, 13, self._white, time.strftime("%p"))

        graphics.DrawText(canvas, self._font_small, 2, 22, self._white, time.strftime("%a %b %-d"))
        
        graphics.DrawText(canvas, self._font_tiny, 0, 31, self._white, "send me something")
        

    def _drawText(self, canvas):
        canvas.Clear()
        file = open("text.txt", "r")
        ReceivedText = file.read()
        
        i = ReceivedText.find('}')
        ReceivedText = ReceivedText[:i]
        
        if(len(ReceivedText) > 16):
            i = int(len(ReceivedText)/16)
            for x in range(i):
                q = 16 * x 
                z = 16 * (x+1)
                if(x == (i-1)):
                    graphics.DrawText(canvas, self._font_tiny, 1, ((x+1) * 7), self._white, ReceivedText[q:])
                else:    
                    graphics.DrawText(canvas, self._font_tiny, 1, ((x+1) * 7), self._white, ReceivedText[q:z])
            
            
        else:    
            graphics.DrawText(canvas, self._font_large, 1, 8, self._white, ReceivedText)
        
        
        
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
                canvas.SetPixel(x,y,r,g,b)
            
    
    def run(self):
        canvas = self._matrix.CreateFrameCanvas()
        ToShow = 1
        while True:
            self._drawClock(canvas)
            time.sleep(0.05)
            canvas = self._matrix.SwapOnVSync(canvas)
            self._matrix.brightness = self._dimmer.brightness
            time.sleep(5)
            if(ToShow == 0):
                self._drawText(canvas)
                ToShow = 1
            else:
                self._drawPic(canvas)
                ToShow = 0
            
            canvas = self._matrix.SwapOnVSync(canvas)
            self._matrix.brightness = self._dimmer.brightness
            time.sleep(5)
            
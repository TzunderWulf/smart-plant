import adafruit_dht as dht
from time import sleep
import adafruit_character_lcd.character_lcd as character_lcd
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import board, digitalio, busio

delay = 7
dht = dht.DHT11(board.D4, False)

lcd_columns = 16
lcd_rows = 2

lcd_rs = digitalio.DigitalInOut(board.D14)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)

lcd = character_lcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
lcd.clear()

# set up MCP3008
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

# function to print message to lcd
def message(message):
    lcd.clear()
    lcd.message = message
    sleep(delay)

message("Measuring...\nPlease wait")

while True:
    try:
        temp = dht.temperature
        humid = dht.humidity
        moist = round(chan.value / 900.0)
        message("Temperature: " + str(temp) + "C\nHumidity: " + str(humid) + "%")
        message("Moisture soil: \n" + str(moist) + "%")
        if (moist > 40):
            message("Plant is happy\nGood job!")
        else:
            message("Plant sad, do a\nbetter job! :(")
    except RuntimeError as error:
        message("Wait a second,\nrecalibrating.")
        sleep(delay)
        continue
    except KeyboardInterrupt:
        message("Error: program\nstopped.")
        lcd.clear()
    except Exception as error:
        dht.exit()
        message("Error: please\nrestart the pi")

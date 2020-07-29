import usocket as socket
from machine import Pin
import network
import esp
import gc

def connect(essid,pw,ap):
    import network
    if ap==False:
        print('STA mode')
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(essid,pw)
            while not wlan.isconnected():
                pass
        print('network config:', wlan.ifconfig())
    else:
        print('AP mode')
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=essid, password=pw) 
        ap.active(True)
        while ap.active() == False:
          pass
        print('network config:', ap.ifconfig())
    
def html():
  gpio0=Pin(0, Pin.OUT).value()==0  
  gpio2=Pin(2, Pin.OUT).value()==0
  gpio3=Pin(3, Pin.OUT).value()==0
  gpio5=Pin(5, Pin.OUT).value()==0
  gpio12=Pin(12, Pin.OUT).value()==0 
  gpio13=Pin(13, Pin.OUT).value()==0 
  gpio14=Pin(14, Pin.OUT).value()==0 
  gpio15=Pin(15, Pin.OUT).value()==0 
  gpio16=Pin(16, Pin.OUT).value()==0
  states=[gpio0,gpio2,gpio3,gpio5]    
  html = """<html><head>
    <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{font-family: Calibri; display:inline-block; margin: 0px auto;}
    h1{color: #0F3376}
    p{font-size: 1.5rem;}
    button{background-color: #f0644c; border: none; border-radius: 12px; color: white; padding: 15px 30px; font-size: 20px; margin: 0px; cursor: pointer;}
    .False{background-color:  #34ec37;}</style></head>
    <body>
    <h1>ESP 8266 GPIO states</h1>
    <table>
    <tr><th>GPIO 0 is<br><strong>""" + str(states[0]) + """</strong></th>
        <th>GPIO 2 is<br><strong>""" + str(states[1]) + """</strong></th>
        <th>GPIO 3 is<br><strong>""" + str(states[2]) + """</strong></th>
        <th>GPIO 5 is<br><strong>""" + str(states[3]) + """</strong></th>
    </tr>
    <tr><td><p><a href="/?gpio0=""" + str(states[0]==False) + """"><button class=" """ + str(states[0]==False) + """">0</p></a></button></td>
        <td><p><a href="/?gpio2=""" + str(states[1]==False) + """"><button class=" """ + str(states[1]==False) + """">2</p></a></button></td>
        <td><p><a href="/?gpio3=""" + str(states[2]==False) + """"><button class=" """ + str(states[2]==False) + """">3</p></a></button></td>
        <td><p><a href="/?gpio5=""" + str(states[3]==False) + """"><button class=" """ + str(states[3]==False) + """">5</p></a></button></td>
    </tr>
    </table>
    </body></html>"""
  return html

esp.osdebug(None)
gc.collect()
ssid = 'ESP8266'
pw =   '123456789'
connect(ssid, pw, ap=True)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Connection: %s' % str(addr))
  
  request = conn.recv(1024)
  request = str(request)
  print('Request: %s' % request)
  
  if request.find('/?gpio0=True') == 6:
    print('GPIO0 ON')
    Pin(0, Pin.OUT).value(0)
  if request.find('/?gpio0=False')== 6:
    print('GPIO0 OFF')
    Pin(0, Pin.OUT).value(1)
    
  if request.find('/?gpio2=True') == 6:
    print('GPIO2 ON')
    Pin(2, Pin.OUT).value(0)
  if request.find('/?gpio2=False')== 6:
    print('GPIO2 OFF')
    Pin(2, Pin.OUT).value(1)
    
  if request.find('/?gpio3=True') == 6:
    print('GPIO3 ON')
    Pin(3, Pin.OUT).value(0)
  if request.find('/?gpio3=False')== 6:  
    print('GPIO3 OFF')
    Pin(3, Pin.OUT).value(1)

  if request.find('/?gpio5=True') == 6:
    print('GPIO5 ON')
    Pin(5, Pin.OUT).value(0)
  if request.find('/?gpio5=False')== 6:  
    print('GPIO5 OFF')
    Pin(5, Pin.OUT).value(1)
    
  response = html()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
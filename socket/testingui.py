from Tkinter import *
import threading
import logging
logging.basicConfig()
import websocket
import time

''' Very basic Websocket client with Tkinter UI.
    Uses python websocketclient module. 
    
    @author Jon Hough
'''

# Client app
class WebsocketClientApp():
	'''Tkinter websocket UI client '''
	def __init__(self):
		
		self.root = Tk()
		self.root.title("Simple Websocket Client")
		self.topframe = Frame(self.root)
		self.toplabel= Label(self.topframe, fg='blue', text='Websocket client')
		self.toplabel.pack()
		self.hostlabel = Label(self.topframe, fg='blue', text='host name')
		self.hostlabel.pack(side=LEFT)
		self.hostentry = Entry(self.topframe)
		self.hostentry.delete(0, END)
		self.hostentry.insert(0, "ws://echo.websocket.org") #default, for testing
		self.hostentry.pack(side=LEFT)
		self.portlabel = Label(self.topframe, fg='blue', text='Port: ')
		self.portlabel.pack(side=LEFT)

		self.portentry = Entry(self.topframe)
		self.portentry.delete(0, END)
		self.portentry.insert(0, "80")#default, for testing
		self.portentry.pack(side=LEFT)
		self.topframe.pack(side=TOP)

		self.statusframe = Frame(self.root)
		self.statuslabel = Label(self.statusframe, fg='red', text='Status: NO CONNECTION')
		self.statuslabel.pack(side=LEFT)
		self.connectbutton = Button(self.statusframe, fg='red', text='Connect', command=self.ws_connect)
		self.connectbutton.pack(side=LEFT)
		self.connectbutton = Button(self.statusframe, fg='red', text='Disconnect', command=self.disconnect)
		self.connectbutton.pack(side=LEFT)
		self.statusframe.pack(side=TOP)
		
		
		# Frame for scrollbars etc.
	
		self.middleframe = Frame(self.root)
		self.middleframe.pack(side=BOTTOM)
		
		self.lframe = Frame(self.middleframe)
		self.lframe.pack(side=LEFT)
		self.inputlabel = Label(self.lframe, fg='blue', text='Input')
		self.inputlabel.pack(side=TOP)
		self.scrollbar = Scrollbar(self.lframe)
		self.scrollbar.pack( side = LEFT, fill=Y )
		self.text = Text(self.lframe, yscrollcommand = self.scrollbar.set, height=50, width=30 )
		self.text.pack( side = LEFT, fill = Y )
		self.text.bind('<Return>', self.send)
		self.scrollbar.config( command = self.text.yview )
		
		self.rframe = Frame(self.middleframe)
		self.rframe.pack(side=RIGHT)
		self.outputlabel = Label(self.rframe, fg='blue', text='Response')
		self.outputlabel.pack(side=TOP)
		self.scrollbar2 = Scrollbar(self.rframe)
		self.scrollbar2.pack( side = RIGHT, fill=Y )
		self.text2 = Text(self.rframe, yscrollcommand = self.scrollbar2.set, height=50, width=30 )
		self.text2.pack( side = RIGHT, fill = Y )
		self.scrollbar2.config( command = self.text2.yview )
		
		self.root.geometry("500x300")
		#client object
		self.client = None
		
		self.lock = threading.Lock()
		
	def ws_connect(self):
		'''Connect. Opens websocket connection.'''
		if self.client is None and self.hostentry.get() is not None:
			#self.start_connection()
			self.ws_thread = threading.Thread(target=self.start_connection)
			self.ws_thread.start()
			self.status_thread = threading.Thread(target=self.on_status_change)
			self.status_thread.start()
			
	def start_connection(self):	
		'''Opens connection'''
		self.client = websocket.WebsocketController(None, None, None)
		self.client.begin_connection()
		

	def send(self, event):
		self.lock.acquire()
		msg = self.text.get("insert linestart", "end")
		self.lock.release()
		if msg is not None and self.client is not None:
			self.client.send_message(msg)
			
		
		
	def on_status_change(self):
		pass
		''' Listens for client connection status changes and updates UI.'''
		while True:
			time.sleep(0.5)
			try:
				self.lock.acquire()
				if self.client is not None:
					if True:#self.client.status == 1:
						self.statuslabel.config(text='Status: CONNECTED')
				
					else: 
						self.statuslabel.config(text='Status: NO CONNECTION')
					
					if len(self.client.response_buffer) > 0:
						for msg in self.client.response_buffer:
							self.text2.insert(END, msg)
							self.client.response_buffer.remove(msg)
				else:
					self.statuslabel.config(text='Status: NO CONNECTION')
				self.lock.release()
			except Exception as e:
				print e
				break
		
			
		
	def disconnect(self):
		'''Disconnect. Closes the websocket connection if it is open. 
		Does nothing otherwise.'''
		if self.client is not None:
			self.lock.acquire()
			self.client.close()
			self.client = None
			self.lock.release()
			print "change status"
			self.statuslabel.config(text='Status: NO CONNECTION')


app = WebsocketClientApp()		
mainloop()


import sys, os, time

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print("Please set MODIM_HOME environment variable to MODIM folder.")
    sys.exit(1)

import ws_client
from ws_client import *

def medConfirmation():
	print("HOLA")

def intStart():

	while True:
		im.init()
		flagP = False
		detected = False
		t1 = False
		t2 = False

		im.executeModality('TEXT_default','Waiting for a patient')

		#Checking if human stay in front of Pepper more than 2 seconds
		im.robot.startSensorMonitor()
		while not flagP:
			time.sleep(0.1)  # avoid CPU overload
			while not detected:
				p = im.robot.sensorvalue() #p is the array with data of all the sensors
				detected = p[1] > 0.0 and p[1] < 1.0 #p[1] is the Front sonar
				time.sleep(0.1)  # avoid CPU overload
			if detected:
				print('*Person Detected*')
				time.sleep(2)
				p = im.robot.sensorvalue()
				detected = p[1] > 0.0 and p[1] < 1.0
				if detected:
					print('*Person interaction confirmed*')
					flagP = True
				else:
					print('*Person gone*')
		im.robot.stopSensorMonitor()


		#Starting the script when human stays 2+ seconds
		im.execute('greeting')
		subprocess.call(['espeak', 'Hi there! I am AURA, your robotic assistant for elderly care ! You can talk to me, or if you prefer, click the tablet to navigate my actions '])
		im.execute('faceRecognition')
		subprocess.call(['espeak', 'Stand still in front of me so I can recognize your face!'])
		a0 = im.ask('faceRecognition', timeout=999)

		#If it is a patient, load its information	
		if a0 == 'welcomePatient':
			im.execute('welcomePatient') 
			subprocess.call(['espeak', 'Welcome Marcelo! I hope you are having a great day. Let me load your information. Just one second.' ])
			im.execute('patientProfile')
			subprocess.call(['espeak', 'Is time for your medication?' ])
			t0 = im.ask('patientProfile',timeout=999)
			
			#If its time for medication
			if t0 == 'medication':
				im.execute('medConfirmation')
				subprocess.call(['espeak', 'Take your medicine please.' ])
				# Checking if Pepper is touched on the head middle sensor
				im.robot.startSensorMonitor()
				flagT = False
				timeout = 60  # seconds
				start_time = time.time()
				while not flagT and (time.time() - start_time < timeout):
					t = im.robot.sensorvalue()  # [frontlaser, frontsonar, rearsonar, headtouch, lefthandtouch, righthandtouch]]
					if t[3]:  # HeadMiddle touched
						print('*Head middle touched*')
						flagT = True
						t1 = True
					time.sleep(0.1)  # avoid CPU overload
				im.robot.stopSensorMonitor()

				if not flagT:
					print('*No touch detected within timeout*')
					t1 = False
					m0 = False

				#If patient took medication
				if t1 :
					im.execute('success')
					subprocess.call(['espeak', 'Great! You took your medicine.' ])
					im.execute('finishInteraction')
					subprocess.call(['espeak', 'Bye! I hope I was helpful to you!' ])
					time.sleep(3)
				#If patient did not took medication
				else:
					im.execute('chatInterface')
					subprocess.call(['espeak', " Why didn't you take the medication? Let's talk." ])
					time.sleep(3)
					im.execute('medConfirmation')
					subprocess.call(['espeak', "Let's try again! Take your medicine." ])
					# Checking if Pepper is touched on the head middle sensor
					im.robot.startSensorMonitor()
					flagT2 = False
					timeout = 60  # seconds
					start_time = time.time()
					while not flagT2 and (time.time() - start_time < timeout):
						t = im.robot.sensorvalue()  # [frontlaser, frontsonar, rearsonar, headtouch, lefthandtouch, righthandtouch]]
						if t[3]:  # HeadMiddle touched
							print('*Head middle touched*')
							flagT = True
							t2 = True
						time.sleep(0.1)  # avoid CPU overload
					im.robot.stopSensorMonitor()

					if not flagT:
						print('*No touch detected within timeout*')
						t2 = False

					#If patient took medication
					if t2 :
						im.execute('success')
						subprocess.call(['espeak', 'Great! You took your medicine.' ])
						im.execute('finishInteraction')
						subprocess.call(['espeak', 'Bye! I hope I was helpful to you!' ])
						time.sleep(3)
						
						#if patient was convinced to take medication
						if m1 == 'yes':
							im.execute('success')
							subprocess.call(['espeak', 'Great! You took your medicine.' ])
							im.execute('finishInteraction')
							time.sleep(3)
						# if he is still reluctant to medication
						else:
							im.execute('humanIntervention')
							subprocess.call(['espeak', 'I am calling a nurse, please remain calm.' ])
							time.sleep(3)
							im.execute('finishInteraction')

			# if its not time for medication
			else:
				
				im.execute('chatInterface')
				subprocess.call(['espeak', 'No medication for you now. How can I help you?'])
				time.sleep(3)
				im.execute('finishInteraction')
				subprocess.call(['espeak', 'Bye! I hope I was helpful to you!'  ])

		#If it is not a patient, offer help	
		else:
			
			im.execute('chatInterface')	
			subprocess.call(['espeak', 'You are not a patient. How can I help you?'])	
			time.sleep(3)
			im.execute('finishInteraction')
			subprocess.call(['espeak', 'Bye! I hope I was helpful to you!'  ])
		

		
if __name__ == "__main__":
	mws = ModimWSClient()
	mws.setDemoPathAuto(__file__)
	mws.run_interaction(intStart)

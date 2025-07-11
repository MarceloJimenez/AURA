import sys, os, time

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print "Please set MODIM_HOME environment variable to MODIM folder."
    sys.exit(1)

import ws_client
from ws_client import *

def intStart():

	while True:
		im.init()
		flagP = False
		detected = False

		im.executeModality('TEXT_default','Waiting for a patient')

		#Checking if human stay in front of Pepper more than 2 seconds
		im.robot.startSensorMonitor()
		while not flagP:
			while not detected:
				p = im.robot.sensorvalue() #p is the array with data of all the sensors
				detected = p[1] > 0.0 and p[1] < 1.0 #p[1] is the Front sonar
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
		subprocess.call(['espeak', 'Hello! I am AURA, your robotic assistant for elderly care ! You can talk to me, or if you prefer, click the tablet to navigate my actions '])
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
				subprocess.call(['espeak', 'Take your medicine and confirm please.' ])
				m0 = im.ask('medConfirmation')

				#If patient took medication
				if m0 == 'finish':
					im.execute('finishInteraction')
					subprocess.call(['espeak', 'Bye! I hope I was helpful to you!' ])
				#If patient did not took medication
				else:
					im.execute('chatInterface')
					subprocess.call(['espeak', 'Lets talk' ])
					im.execute('medConfirmation')
					subprocess.call(['espeak', 'Take your medicine and confirm please.' ])
					m1 = im.ask('medConfirmation')
					
					#if patient was convinced to take medication
					if m1 == 'yes':
						im.execute('finishInteraction')
				 	# if he is still reluctant to medication
					else:
						im.execute('humanIntervention')
						subprocess.call(['espeak', 'I am calling a nurse, please remain calm.' ])
						im.execute('finishInteraction')

			# if its not time for medication
			else:
				
				im.execute('chatInterface')
				subprocess.call(['espeak', 'No medication for you now. How can I help you?'])
				im.execute('finishInteraction')

		#If it is not a patient, offer help	
		else:
			
			im.execute('chatInterface')	
			subprocess.call(['espeak', 'You are not a patient. How can I help you?'])	
			im.execute('finishInteraction')
		# time.sleep(6)

		
if __name__ == "__main__":
	mws = ModimWSClient()
	mws.setDemoPathAuto(__file__)
	mws.run_interaction(intStart)

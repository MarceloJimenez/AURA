import sys, os, time

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print("Please set MODIM_HOME environment variable to MODIM folder.")
    sys.exit(1)

import ws_client
from ws_client import *

def intStart():

	user_profiles = {
		"pedro-perez": {
			"first_name": "Pedro",
			"last_name": "Perez",
			"age": 79,
			"medication_schedule": [
				{"name": "Antihypertensive", "hour": "08:00"},
				{"name": "Aspirin", "hour": "20:00"}
			],
			"medication_due": True,
			"general_behaviour": "Calm and cooperative. Responds well to clear instructions and prefers brief interactions.",
			"greeting": "Welcome Pedro! I hope you are having a great day. Let me load your information. Just one second.",
			"welcome":"welcomePedro",
			"profile":"profilePedro"

		},
		"ana-silva": {
			"first_name": "Ana",
			"last_name": "Silva",
			"age": 83,
			"medication_schedule": [
				{"name": "Antidepressant", "hour": "09:30"},
				{"name": "Vitamin D", "hour": "12:00"},
				{"name": "Sleep aid", "hour": "22:00"}
			],
			"medication_due": False,
			"general_behaviour": "Often confused and hesitant. Needs clear, slow communication and frequent reassurance during interactions.",
			"greeting": "Hello Ana! Let me check your record. Hold on a moment.",
			"welcome":"welcomeAna",
			"profile":"profileAna"
		}
	}



	while True:
		im.init()
		flagP = False
		detected = False
		t1 = False
		t2 = False
		#WAITING FOR PATIENT SCREEN
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

		#GREETING SCREEN
		#Starting the script when human stays 2+ seconds
		im.execute('greeting')
		subprocess.call(['espeak', 'Hi there! I am AURA, your robotic assistant for elderly care! '])
		#FACE RECGNITION SCREEN
		im.execute('faceRecognition')
		subprocess.call(['espeak', 'Are you a patient? Stand still in front of me so I can recognize your face!'])
		a0 = im.ask('faceRecognition', timeout=60)

		#If it is a patient, load its information	
		if a0  in user_profiles:
			profile = user_profiles[a0]
			#WELCOME PATIENT SCREEN
			im.execute(profile['welcome']) 
			subprocess.call(['espeak', profile['greeting'] ])
			#PATIENT PROFILE SCREEN
			im.execute(profile['profile'])
			time.sleep(3)

			#If its time for medication
			if profile['medication_due']:
				#MED CONFIRMATION 1
				im.execute('medConfirmation')
				subprocess.call(['espeak', ' You have medication scheduled for now! Please take your medication.' ])
				# Checking if Pepper is touched on the head middle sensor
				im.robot.startSensorMonitor()
				flagT = False
				timeout = 30  # seconds
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

				#If patient took medication first time
				if t1 :
					#SUCCESS 1 SCREEN
					im.execute('success')
					subprocess.call(['espeak', 'Great! You took your medicine.' ])
					#FINISH SCREEN
					im.execute('finishInteraction')
					subprocess.call(['espeak', 'Bye! I hope I was helpful to you!' ])
					time.sleep(3)

				#If patient did not took medication first time
				else:
					#CHAT 1 SCREN
					im.execute('chatInterface1')
					subprocess.call(['espeak', " You did not took your medication! Why? Can I help you? Chat with me" ])
					chat1 = im.ask('chatInterface1', timeout=30) 
					if chat1 == 'done' or 'timeout':
						#MED CONFIRMATION 2 SCREN
						im.execute('medConfirmation')
						subprocess.call(['espeak', "Let's try again! Take your medicine." ])
						# Checking if Pepper is touched on the head middle sensor
						im.robot.startSensorMonitor()
						flagT2 = False
						timeout = 30  # seconds
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
							#HUMAN INTERVENTION SCREEN
							im.execute('humanIntervention')
							subprocess.call(['espeak', 'Human intervention needed, I am calling a nurse, please remain calm.' ])
							time.sleep(3)
							#FINISH
							im.execute('finishInteraction')
							t2 = False
						#If patient took medication second time
						if t2 :
							#SUCCESS 2 SREEN
							im.execute('success')
							subprocess.call(['espeak', 'Great! You took your medicine.' ])
							#FINISH SCREEN
							im.execute('finishInteraction')
							subprocess.call(['espeak', 'Bye! I hope I was helpful to you!' ])
							time.sleep(3)						
	
	
			# if its not time for medication
			else:				
				im.execute('chatInterface2')
				subprocess.call(['espeak', 'No medication for you now. How can I help you?'])
				chat2 = im.ask('chatInterface2', timeout=30) 
				if chat2 == 'done' or 'timeout':					
					im.execute('finishInteraction')
					subprocess.call(['espeak', 'Bye! I hope I was helpful to you!'  ])

		#If it is not a patient, offer help	
		else:
			im.execute('chatInterface3')	
			subprocess.call(['espeak', 'You are not a patient. How can I help you? Chat with me.'])	
			chat3 = im.ask('chatInterface3', timeout=30) 
			if chat3 == 'done' or 'timeout':
				im.execute('finishInteraction')
				subprocess.call(['espeak', 'Bye! I hope I was helpful to you!'  ])
		

		
if __name__ == "__main__":
	mws = ModimWSClient()
	mws.setDemoPathAuto(__file__)
	mws.run_interaction(intStart)

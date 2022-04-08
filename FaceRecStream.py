from __future__ import print_function
#Importation des bibliothèques
import face_recognition
import os
import cv2
import imutils
import numpy
from numpy import array
import tkinter
from tkinter import simpledialog
#from tkinter import *
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
from singlemotiondetector import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import datetime
import time
#insert at 1, 0 is the script path (or ' ' in REPL)
import sys
sys.path.insert(1, '/home/appartement/Reconnaissance_Faciale_H22/StreamonWeb')

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)

#Fichier des faces connus
FACES_CONNUES_DIR = "Faces_Connues"
#Taux de tolérance de reconnaissance faciale (de 0 à 1)
TOLERANCE = 0.55
 
#Paramètres visuels du cadre
FRAME_THICKNESS = 2
FONT_THINCKNESS = 1
 
#Model de reconnaissance faciale utilisant le CPU (hog) si pas accès au GPU (cnn)
MODEL = "hog"

#Instantiation d'une variable de lecture vidéo avec la caméra a l'indice 0 (WebCam)
#video = cv2.VideoCapture("http://192.168.1.176:8081")
#video = cv2.VideoCapture(0)
# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
#print("[INFO] sampling THREADED frames from webcam...")
#video = WebcamVideoStream(src=0).start()
#fps = FPS().start()

# initialize the video stream and allow the camera sensor to
# warmup
#video = VideoStream(usePiCamera=1).start()
video = VideoStream(src=0).start()
time.sleep(2.0)

 
@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")
	
def detect_motion(frameCount):
	print("In Detect_Motion")
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock
	# initialize the motion detector and the total nuqmber of frames
	# read thus far
	#md = SingleMotionDetector(accumWeight=0.1)
	total = 0
	
	DEFAULT = True
	# loop over frames from the video stream
	while True:
		key = cv2.waitKey(1) & 0xFF
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = video.read()
		frame = imutils.resize(frame, width=400)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7, 7), 0)
		# grab the current timestamp and draw it on the frame
		timestamp = datetime.datetime.now()
		cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		# if the total number of frames has reached a sufficient
		# number to construct a reasonable background model, then
		# continue to process the frame
		#if total > frameCount:
			# detect motion in the image
		#	motion = md.detect(gray)
			# check to see if motion was found in the frame
		#	if motion is not None:
				# unpack the tuple and draw the box surrounding the
				# "motion area" on the output frame
		#		(thresh, (minX, minY, maxX, maxY)) = motion
		#		cv2.rectangle(frame, (minX, minY), (maxX, maxY),
		#			(0, 0, 255), 2)
		
		# update the background model and increment the total number
		# of frames read thus far
		#md.update(gray)
		#total += 1
		
		
		   #Instantiation d'un tableau de coordonnée selon le model 'hog':
		#0 = y du haut de la face
		#1 = x du côté droit de la face
		#2 = y du bas de la face
		#3 = x du côté gauche de la face
		locations = face_recognition.face_locations(frame, model=MODEL)
		#Encodage du présent frame
		encodings = face_recognition.face_encodings(frame,locations)
 
		if DEFAULT:    #Mode reconnaissance faciale activé       
			TitreActuel = "Video"
	  		#Pour chaque encodage et endroit d'une face dans une liste pairée de ceux-ci
			for face_encoding, face_location in zip(encodings, locations):
				#Retour d'une valeur True ou False de la comparaison entre l'encodage
				# d'une image a une position donnée dans la frame et l'encodage des 
				# faces connues dans le tableau 'faces_connus' selon une certaine tolérance
				results = face_recognition.compare_faces(faces_connus, face_encoding, TOLERANCE)
		   		#Instantiation de la variable 'match' avec rien
				match = None
	 
				x = face_location[3]
				y = face_location[0]
				x2 = face_location[1]
				y2 = face_location[2]
		 
				#Si la comparaison retourne un True...
				if True in results:
					#On retourne l'index du résultat True (qui sera le même pour les
				 	# noms connus puisqu'il est le même que pour faces_connus)
				 	#Avec cet index, on retourne le nom de la personne reconnue
				 	match = noms_connus[results.index(True)]
				 	#Affichage du nom de la personne reconnue en dessous du rectangle
				 	cv2.putText(frame, match, (x+10, y2+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), FONT_THINCKNESS)        
				 	color = [0, 255, 0]
			 
				 	#Instantiation des paramêtres du rectangle autour du visage
				 	top_left = (x, y)
				 	bottom_right = (x2, y2)         
				 	cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)
	   
		else: #Mode enregistrement activé
	 
			color = [255, 0, 0]
                       #cv2.imshow(TitreActuel, original)
			#Si il y a au moins une face dans l'écran...     
			if key == ord('k') and len(locations)==1: #and BoucleSupp == False:
				#BoucleSupp = True
				messageConfirmation = "Voulez-vous ajouter cette photo à votre nom? "
				#cv2.destroyWindow(TitrePrecedent)
				#Pour chaque encodage et endroit d'une face dans une liste pairée de ceux-ci

				for face_encoding, face_location in zip(encodings, locations):
					results = face_recognition.compare_faces(faces_connus, face_encoding, TOLERANCE)
					#Instantiation de la variable 'match' avec rien 
					match = None

					#Instantiation de la fenêtre mère pour demander une entrée d'information de l'utilisateur
					root = tkinter.Tk()
					root.withdraw()
					#Apparition de la fenêtre de confirmation pour l'enregistrement
					# des encodages de la frame présente
					MsgBox = tkinter.messagebox.askquestion('New Face', messageConfirmation, icon = 'warning')
	 
					if MsgBox == 'yes':
						#Si la comparaison retourne un True...
						if True in results:
							#On retourne l'indexe du résultat True (qui sera le même 
							#pour les noms connus puisqu'il est le même que pour faces_connus)
							#Avec cet indexe, on retourne le nom de la personne reconnue
							match = noms_connus[results.index(True)]
							path, dir, files = next(os.walk(FACES_CONNUES_DIR + "/" + match))
							fileNumber = len(files) + 1
							if fileNumber > 50:
								fileNumber = 50
							TitreActuel = "UTILISATEUR RECONNU: " + match
							name = match
						else:
							fileNumber = 1
							TitreActuel = "NOUVEL UTILISATEUR"
							messageConfirmation += " Vous allez être enregistré au système seulement si vous acceptez: "                      
							ROOT = tkinter.Tk()
							ROOT.withdraw()
							name = simpledialog.askstring(title = "Allo", prompt = "Veuillez entrer votre nom pour vous enregistrer (utilisez '_' pour les espaces): ")
							if name:
								os.mkdir(FACES_CONNUES_DIR + "/" + name)
	 
						#cv2.imshow(TitreActuel, original)                           
						if name:
							file = open(FACES_CONNUES_DIR + "/" + name + "/Face_#" + str(fileNumber), "w")
							strEncodings = array(encodings).__repr__()
							strEncodings = strEncodings[7:]
							strEncodings = strEncodings[:-2]
							file.write(strEncodings)
							file.close()
	 
							file = open(FACES_CONNUES_DIR + "/" + name + "/Face_#" + str(fileNumber), "r")          
							encodings = ""          
							for line in file:
								encodings+=line
		                  
							faces_connus.append(eval(encodings))
							noms_connus.append(name)
							file.close()
	 
			for face_location in locations:
				top_left = (face_location[3], face_location[0])
				bottom_right = (face_location[1], face_location[2])
				cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)
	 
		#Tant que l'on n'appuit pas sur la touche 'q', la WebCam continuera à traiter chaque frame
		cv2.imshow('Video', frame)
		TitrePrecedent = TitreActuel
	 
		if key == ord('s'):
			if DEFAULT:
				DEFAULT = False
			else:
				DEFAULT = True
		elif key == ord('q'):
			break
	       
	       
	       
		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()
def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')
			
@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
		
#####Programme principal#####

print("loading known faces")
#Instantiation d'un tableau de faces connus
faces_connus = []
#Instantiation d'un tableau de noms connus
noms_connus = []		
#Pour chaque document de personne connue...
for name in os.listdir(FACES_CONNUES_DIR):
   fileNumber = 0
   #Pour chaque document contenant des encodages de personne connue...
   for filename in os.listdir(FACES_CONNUES_DIR + "/" + name):
       fileNumber+=1
       #On ouvre le fichier en mode lecture
       file = open(FACES_CONNUES_DIR + "/" + name + "/Face_#" + str(fileNumber), "r")
      
      #On récolte, ligne par ligne les encodages de chaque document
       encodings = ""
       for line in file:
           encodings+=line

        #Évaluation du string d'encodage en matrice qui est ajouté à la liste des encodages de faces connues
       faces_connus.append(eval(encodings))
       #Dans une autre liste, on ajoute le nom lié à ces encodages au même indice
       noms_connus.append(name)
       #Fermeture du fichier
       file.close()
 
print("processing video feed")
 
TitrePrecedent, TitreActuel = " ", " "


# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())
	# start a thread that will perform motion detection
	print("Starting Thread")
	t = threading.Thread(target=detect_motion, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()
	# start the flask app
	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)
	print("End of Main")
# release the video stream pointer
video.stop()

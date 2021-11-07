import numpy as numpy
import cv2
import time
import imutils
import datetime



def Motion_Detection():
	capture_duration = 10 #set the recording period to 10 seconds
	video_capture = cv2.VideoCapture(0)
	time.sleep(2)
	fourcc = cv2.VideoWriter_fourcc(*'XVID') #encode video using the XVID coding method
	out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))#create an output file with the frame rate and the resolution. 
	
	first_frame = None
	while True:
		frame = video_capture.read()[1]
		text = 'unoccupied'
		
		greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21,21),0)
		blur_frame = cv2.blur(gaussian_frame, (5,5))
		greyscale_image = blur_frame
		
		if first_frame is None:
			first_frame = greyscale_image
		else:
			pass
			
		frame = imutils.resize(frame, width=500)
		frame_delta = cv2.absdiff(first_frame, greyscale_image)
		
		thresh = cv2.threshold(frame_delta, 100, 225, cv2.THRESH_BINARY)[1]
		
		dilate_image = cv2.dilate(thresh, None, iterations=2)
		
		cnt = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
		
		for c in cnt:
			if cv2.contourArea(c) > 800:
				(x, y, w, h) = cv2.boundingRect(c)
				cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
				text = 'occupied'
				start_time = time.time() #create a start time when a motion is detected
				while( int(time.time() - start_time) < capture_duration ): #create a statment where the within 10 seconds of the detection the movement will be detected
					ret, frame = video_capture.read()#start capturing the video 
					out.write(frame)#write down the footage recorded
					cv2.imshow('frame',frame)#create a frame to show the recorded footage

			else:
				pass
				
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame, f'[+] Room Status:{text}', (10,20), font, 0.5, (0,0,255),2)
		
		cv2.putText(frame, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'), (10, frame.shape[0] -10), font, 0.35, (0,0,255), 1)
		
		cv2.imshow('Security Feed', frame)
		cv2.imshow('Threshold', dilate_image)
		cv2.imshow('Frame Delta', frame_delta)
		
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			cv2.destroyAllWindows()
			break
			

if __name__ == '__main__':
	Motion_Detection()

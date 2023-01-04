import cv2,os,time
os.system('cls')
#os.system('ls> L.txt')
#time.sleep(2)
video=cv2.VideoCapture(input("Nombre del video\n"))
while video.isOpened():
    ret,frame = video.read()
    if(ret==True):
        cv2.imshow('frame del video',frame)
        if (cv2.waitKey(30)==ord('s')):
            break
video.release()
cv2.destroyAllWindows   
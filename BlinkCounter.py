import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import text


# loading the video
cap = cv2.VideoCapture("project_test_video.mp4")

# Creating object for face mesh
detector = FaceMeshDetector(maxFaces=1)

# Creating object for live graph
live_plot = LivePlot(640, 360, [20, 50])

# object for text file
tts = text.tts()

# Basic initializations
blink_counter = 0
idlist = [22, 23, 24, 26, 110,  157, 158, 159, 160, 161, 130, 243]  # eye id numbers
ratiolist = []
bit = 0
t = ""
sleeping = False
alert = 0


while True:

    # Break if system alert >= 10
    if alert >= 10:
        tts.text_to_speech("Driver Found Sleeping. moving vehicle to the safest location.")
        break

    # playing video in a cycle
    sleeping = False
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # capturing the frames in the video
    success, img = cap.read()

    img, faces = detector.findFaceMesh(img, draw=False) # face mesh will identify 468 points on the face

    if faces:
        face = faces[0]
        for id in idlist:
            cv2.circle(img, face[id], 2, (255, 0, 255), cv2.FILLED)

        # key points
        leftup = face[159]
        leftdown = face[23]
        leftleft = face[130]
        leftright = face[243]

        # vertical and horizontal distances
        lenght_v,_ = detector.findDistance(leftup, leftdown)
        lenght_h,_ = detector.findDistance(leftleft, leftright)

        # drawing the line
        cv2.line(img, leftleft, leftright, (0, 200, 0), 1)
        cv2.line(img, leftup, leftdown, (0, 200, 0), 1)
        cv2.rectangle(img, face[70], face[340], (0, 200, 0), 3)

        # calculating the ration and average
        ratio = (lenght_v/lenght_h)*100
        ratiolist.append(ratio)
        if len(ratiolist) > 3:
            ratiolist.pop(0)
        ratioavg = sum(ratiolist)/len(ratiolist)

        if ratioavg <= 33:
            blink_counter += 1
            bit += 1
            if bit >= 50:
                t = "DRIVER IN DANGER"
                sleeping = True
        else:
            sleeping = False
            bit = -1
            t = "DRIVER SAFE"

        # cvzone.putTextRect(img, f"Blink count : {blink_counter}", (100, 100))
        cvzone.putTextRect(img, t, (100, 400))

        # plotting image
        imgplot = live_plot.update(ratioavg)

        # resizing the image
        img = cv2.resize(img, (640, 360))

        # stacking images together
        imgstack = cvzone.stackImages([img, imgplot], 2, 1)

        if sleeping:
            tts.text_to_speech("sleeping found")
            # time.sleep(0.2)
            bit //= 2
            alert += 1

    else:

        # if face not found it shows 2 face side by side
        img = cv2.resize(img, (640, 360))
        imgstack = cvzone.stackImages([img, img], 2, 1)


    cv2.imshow("output", imgstack)
    cv2.waitKey(1)

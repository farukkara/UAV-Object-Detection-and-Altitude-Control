import cv2
import numpy as np

# Load the object detection model
model = cv2.CascadeClassifier("path/to/model.xml")

# Start video capture
cap = cv2.VideoCapture(0)

# Initialize the previous frame
prev_frame = None

while True:
    # Read the next frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect objects in the frame
    objects = model.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw a bounding box around each object
    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the frame
    cv2.imshow("Frame", frame)

    # Check if a moving object was detected
    if prev_frame is not None:
        diff = cv2.absdiff(prev_frame, gray)
        diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        cnts, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            if cv2.contourArea(c) > 1000:
                print("Moving object detected!")
                break

    prev_frame = gray

    # Get the altitude of the object
    altitude = get_altitude(objects[0])

    # Set the UAV's altitude
    set_altitude(altitude)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()

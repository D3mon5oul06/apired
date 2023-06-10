from fastapi import FastAPI, UploadFile, File, HTTPException,Form
import cv2
import imutils
import numpy as np
import sys
import dlib
import numpy as np
from skimage.filters import threshold_otsu
from skimage.feature import canny
from skimage.transform import probabilistic_hough_line
from skimage.transform import rotate
from skimage.filters import gaussian

app = FastAPI()

detector = dlib.get_frontal_face_detector()
win = dlib.image_window()

def align_images(image, template, maxFeatures=500, keepPercent=0.2, debug=False):
    image="C:\\Users\\oziel\\Downloads\\ApiRed\\app\\ine.jpg"
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Use ORB to detect keypoints and extract (binary) local invariant features
    orb = cv2.ORB_create(maxFeatures)
    (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
    (kpsB, descsB) = orb.detectAndCompute(templateGray, None)

    # Match the features
    method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv2.DescriptorMatcher_create(method)
    matches = matcher.match(descsA, descsB, None)

    # Sort the matches by their distance (the smaller the distance,
    # the "more similar" the features are)
    matches = sorted(matches, key=lambda x: x.distance)

    # Keep only the top matches
    keep = int(len(matches) * keepPercent)
    matches = matches[:keep]

    # Check if we should visualize the matched keypoints
    if debug:
        matchedVis = cv2.drawMatches(image, kpsA, template, kpsB, matches, None)
        matchedVis = imutils.resize(matchedVis, width=1000)
        cv2.imshow("Matched Keypoints", matchedVis)
        cv2.waitKey(0)

    # Allocate memory for the keypoints (x, y)-coordinates from the
    # top matches -- we'll use these coordinates to compute our
    # homography matrix
    ptsA = np.zeros((len(matches), 2), dtype="float")
    ptsB = np.zeros((len(matches), 2), dtype="float")


    # Loop over the top matches

    
    img = dlib.load_rgb_image(image)
    
    
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    image = cv2.GaussianBlur(image, (3, 3), 0, 0)
    
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(12, 12))
    image = clahe.apply(image)
    
    
    _, image = cv2.threshold(image, thresh=165, maxval=255, type=cv2.THRESH_TRUNC + cv2.THRESH_OTSU)
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            i, d.left(), d.top(), d.right(), d.bottom()))

    win.clear_overlay()
    win.set_image(img)
    win.add_overlay(dets)
    dlib.hit_enter_to_continue()


# Finally, if you really want to, you can ask the detector to tell you the score
# for each detection.  The score is bigger for more confident detections.
# The third argument to run is an optional adjustment to the detection threshold,
# where a negative value will return more detections and a positive value fewer.
# Also, the idx tells you which of the face sub-detectors matched.  This can be
# used to broadly identify faces in different orientations.
    print("openningdss")
    img = dlib.load_rgb_image(image)
    dets, scores, idx = detector.run(img, 1, -1)
    for i, d in enumerate(dets):
        print("Detection {}: score: {}, face_type:{}".format(
            i, scores[i], idx[i]))

    def skew_correction(gray_image):
        orig = gray_image
        
        # threshold to get rid of extraneous noise
        thresh = threshold_otsu(gray_image)
        normalize = gray_image > thresh
        blur = gaussian(normalize, 3)
        edges = canny(blur)
        hough_lines = probabilistic_hough_line(edges)
        
        # Calculate the slopes of the lines
        slopes = [(y2 - y1) / (x2 - x1) if (x2 - x1) else 0 for (x1, y1), (x2, y2) in hough_lines]
        rad_angles = [np.arctan(x) for x in slopes]
        deg_angles = [np.degrees(x) for x in rad_angles]
        
        # Find the most common degree value
        histo = np.histogram(deg_angles, bins=100)
        rotation_number = histo[1][np.argmax(histo[0])]
        
        # Correcting for 'sideways' alignments
        if rotation_number > 45:
            rotation_number = -(90 - rotation_number)
        elif rotation_number < -45:
            rotation_number = 90 - abs(rotation_number)
        
        # Rotate the image to deskew it
        rotated = rotate(orig, rotation_number, resize=True)
        
        return np.array(rotated), rotation_number

    image = cv2.copyMakeBorder(
        src=image,
        top=20,
        bottom=20,
        left=20,
        right=20,
        borderType=cv2.BORDER_CONSTANT,
        value=(255, 255, 255))
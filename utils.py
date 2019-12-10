import cv2

def cap_image(str_i):
    # imageName = 'DontCare.jpg' #Just a random string
    cap = cv2.VideoCapture(2)
    # fgbg = cv2.createBackgroundSubtractorMOG2() 

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #For capture image in monochrome
        rgbImage = frame  # For capture the image in RGB color space

        # fgmask = fgbg.apply(frame)

        # cv2.imshow('fgmask', frame)
        # cv2.imshow('frame', fgmask)

        # Display the resulting frame
        cv2.imshow('Webcam',rgbImage)
        # Wait to press 'q' key for capturing
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Set the image name to the date it was captured
            # imageName = str(time.strftime("%Y_%m_%d_%H_%M")) + '.jpg'
            # Save the image
            cv2.imwrite(str_i+".png", rgbImage)
            break
    # When everything done, release the capture
    cap.release()
    
    cv2.destroyAllWindows()
    # Returns the captured image's name
    return rgbImage


def get_mask2(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    

    ret2,ho = cv2.threshold(gray,246,255,cv2.THRESH_BINARY)
    # cv2.imshow("umbralitos",ho)
    sk = ho
    return cv2.cvtColor(sk,cv2.COLOR_GRAY2BGR)

def get_mask(sinimg,conimg):

    sinimg = cv2.cvtColor(sinimg, cv2.COLOR_BGR2GRAY)
    conimg = cv2.cvtColor(conimg, cv2.COLOR_BGR2GRAY)
    # sinimg = cv2.imread("sinfondo.jpg")
    # conimg = cv2.imread("conimg.jpg")

    cv2.imshow("sin img",sinimg)
    cv2.imshow("con img",conimg)

    new_img = sinimg-conimg
    
    for i in range((new_img.shape[0])):
        for j in range(new_img.shape[1]):
            if new_img[i][j] > 240:
                new_img[i][j] = 255
            if new_img[i][j] < 15:
                new_img[i][j] = 255
                

    cv2.imshow("resta",new_img)


    # gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    
    gray=new_img

    # ret, bw_img = cv2.threshold(gray,108,255,cv2.THRESH_BINARY)

    # gray = cv2.medianBlur(gray,5)
    # ho=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #             cv2.THRESH_BINARY,11,2)

    gray = cv2.GaussianBlur(gray,(7,7),0)
    cv2.imshow("gaussian" , gray)
    ret2,ho = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    sk = ho
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    # sk = cv2.morphologyEx(ho, cv2.MORPH_OPEN, kernel)

    # sk = cv2.GaussianBlur(sk,(5,5),0)
    sk = cv2.dilate(sk, kernel,iterations =6 )
    sk = cv2.erode(sk,kernel,iterations = 15    )
    sk = cv2.dilate(sk, kernel,iterations =10 )

    cv2.imshow("gry",gray)
    cv2.imshow("binary",sk)

    k = cv2.waitKey(0)

    if k==27:
        cv2.destroyAllWindows()

    return cv2.cvtColor(sk,cv2.COLOR_GRAY2BGR)

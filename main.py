# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2
import numpy as np
import tkinter

cam=cv2.VideoCapture('Lane Detection Test Video-01.mp4')

left_top = 0, 0
left_bottom = 0, 0
right_top = 0, 0
right_bottom = 0,0
old_list = [left_top, left_bottom, right_top, right_bottom]

#Get Screen Size
app = tkinter.Tk()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()


while True:

    ret, frame = cam.read()


    if ret is False:
        break

    #Resize Frame

    resized_height=screen_height//3
    resized_width = screen_width // 4


    frame=cv2.resize(frame,(resized_width, resized_height))
    [heigth,width,dim]=frame.shape

    #Gray Scale

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #R, G, B = frame[:, :, 0],frame[:, :, 1],frame[:, :, 2]

    #Y = 0.299*R + 0.587*G + 0.114*B
    #gray_frame[:, :, 0] = Y
    #gray_frame[:, :, 1] = Y
    #gray_frame[:, :, 2] = Y



    #Select only road

    #Corners
    upper_left = (int(width*0.55), int(heigth*0.76))
    lower_left = (0, heigth)
    upper_right = (int(width*0.42), int(heigth*0.76))
    lower_right = (width, heigth)


    trapezoid_bounds = np.array([upper_right, upper_left, lower_right, lower_left], dtype=np.int32)
    #trapezoid_bounds = np.array([upper_left, lower_left, lower_right, upper_right], dtype=np.int32)
    # Draw Trapezoid
    black_frame = np.zeros((heigth, width), dtype=np.uint8)
    trapezoid = cv2.fillConvexPoly(black_frame,trapezoid_bounds,1)
    #Combine gray and trapezoid to select only the road
    only_road=trapezoid*gray_frame


    #5. Stretch Trapezoid

    #Corners of the frame

    upl=(0,0)
    upr=(width,0)
    lowl=(0,heigth)
    lowr=(width,heigth)

    #Creation  of Frame Bounds
    frame_bounds = np.array([upl, upr, lowr, lowl], dtype=np.float32)

    #Convert to float
    trapezoid_bounds = np.float32(trapezoid_bounds)

    magic_matrix=cv2.getPerspectiveTransform(trapezoid_bounds, frame_bounds)
    strecthed_onlyroad_frame=cv2.warpPerspective(only_road, magic_matrix, (width, heigth))

    #6. Blurred Image
    blurred_frame=cv2.blur(strecthed_onlyroad_frame, ksize=(7, 7))

    #7. Edge Detection
    #Sobel-vertical
    sobel_vertical=np.float32([[-1, -2, -1],
                             [ 0,  0,  0],
                             [+1, +2, +1]])
    #Sobel Horizontal
    sobel_horizontal=np.transpose(sobel_vertical)

    sobel_hor=np.float32(blurred_frame)
    sobel_ver=np.float32(blurred_frame)



    #Applying Horizontal/Vertical filter
    sob_ver=cv2.filter2D(sobel_ver, -1, sobel_vertical)
    sob_hor = cv2.filter2D(sobel_hor, -1, sobel_horizontal)

    edge_detection=np.sqrt((sob_ver**2) +(sob_hor**2))
    edgedetection_frame=cv2.convertScaleAbs(edge_detection)


    #8. Binarize the Frame
    _, binarized_frame = cv2.threshold(edgedetection_frame, 80, 255, cv2.THRESH_BINARY, None)

    #9 Street Coordinates
    #Copy Frame
    copy_frame=binarized_frame.copy()
    #Make the first and last 5% columns of the frame black
    first_percentage_index=int(width*0.050)
    last_percentage_index=width-first_percentage_index
    copy_frame[:,0:first_percentage_index]=0
    copy_frame[:,width-first_percentage_index:width]=0
    #copy_frame[0:first_percentage_index,last_percentage_index:width]=0
    #copy_frame[heigth-300:heigth, last_percentage_index:width] = 0

    #Slice in half the frame

    left_frame=copy_frame[:,:(width//2)]
    right_frame=copy_frame[:,(width//2):]

    #10 Find the regression lines

    left=np.argwhere(left_frame>1)
    right=np.argwhere(right_frame>1)
    a=left[:,1]
    b=left[:,0]
    c=right[:,1]+(width//2)
    d=right[:,0]

    left_xs=np.array(a)
    left_ys=np.array(b)

    right_xs=np.array(c)
    right_ys=np.array(d)

    #Regression for the coordinates of left and right
    #Regression line coefficients for left
    bl,al=np.polynomial.polynomial.polyfit(left_xs,left_ys,1)


    #Regression line coefficients for right
    br,ar = np.polynomial.polynomial.polyfit(right_xs, right_ys, 1)
    #Points to draw lines for left and right



    left_top_y=0
    left_top_x=(left_top_y - bl)/al


    left_bottom_y=heigth
    left_bottom_x=(left_bottom_y -bl)/al


    right_top_y=0
    right_top_x=(right_top_y - br)/ar


    right_bottom_y=heigth
    right_bottom_x=(right_bottom_y - br)/ar

    left_top = left_top_x, left_top_y
    left_bottom = left_bottom_x, left_bottom_y
    right_top = right_top_x, right_top_y
    right_bottom = right_bottom_x,right_bottom_y


    list=[left_top,left_bottom,right_top,right_bottom]


    for i in range(len(list)):

        if(list[i][0]>10**8 or list[i][0]<-10**8):
             list[i]=old_list[i]







    left_top = int(list[0][0]),int(list[0][1])
    left_bottom = int(list[1][0]),int(list[1][1])
    right_top = int(list[2][0]),int(list[2][1])
    right_bottom = int(list[3][0]),int(list[3][1])

    #Drawing the line
    old_list = [left_top, left_bottom, right_top, right_bottom]
    line1=cv2.line(copy_frame, left_top, left_bottom, (255, 0, 0), 5)
    line2 = cv2.line(copy_frame, right_top, right_bottom, (100, 0, 0), 12)




    #11
    frame_bounds2 = np.array([upr, upl, lowr, lowl], dtype=np.float32)

    new_frame1 = np.zeros((heigth, width), dtype=np.uint8)
    cv2.line(new_frame1, left_top, left_bottom, (255, 0, 0), 5)
    magic_matrix_left = cv2.getPerspectiveTransform(frame_bounds, trapezoid_bounds)
    ceva1=cv2.warpPerspective(new_frame1, magic_matrix_left, (width, heigth))
    left1 = np.argwhere(ceva1 > 1)

    xl = left1[:, 1]
    yl = left1[:, 0]


    new_frame2 = np.zeros((heigth, width), dtype=np.uint8)
    cv2.line(new_frame2, right_top, right_bottom, (255, 0, 0), 5)
    magic_matrix_right = cv2.getPerspectiveTransform(frame_bounds, trapezoid_bounds)
    ceva2=cv2.warpPerspective(new_frame2, magic_matrix_right, (width, heigth))
    right1 = np.argwhere(ceva2 > 1)

    xr = right1[:, 1]
    yr = right1[:, 0]


    copy_of_original=frame.copy()
    copy_of_original[yl, xl] = (50, 50, 250)
    copy_of_original[yr,xr]=(50, 250, 50)



    #Output
    cv2.imshow('Original', frame)
    cv2.imshow('Gray Scale', gray_frame)
    cv2.imshow("OnlyRoad Black", trapezoid * 255)
    cv2.imshow("OnlyRoad", only_road)
    cv2.imshow("OnlyRoad Stretched", strecthed_onlyroad_frame)
    cv2.imshow("OnlyRoad Stretched Blurred", blurred_frame)
    cv2.imshow("Edge Detection", edgedetection_frame)
    cv2.imshow("Binarized Frame", binarized_frame)
    cv2.imshow("Copy Frame", line1)
    cv2.imshow("End", copy_of_original)
    #cv2.imshow("Right", right_frame)
    # .imshow("Left", left_frame)





    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break


cam.release()
cv2.destroyAllWindows()
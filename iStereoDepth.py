import numpy as np
import cv2
import iCamera as iCAM




#CALIBRATE CAMERA

def CalirbrateCamera(CameraNumber, NumberOfFrames, ChesboardColumns, ChessboardRows, Stereo = None):

    # Camera = iCAM.Camera(CameraNumber)
    Camera = iCAM.Camera(CameraNumber,320*3, 240*3, Format = "MJPEG", FPS = 60)

     # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((ChesboardColumns*ChessboardRows,3), np.float32)
    objp[:,:2] = np.mgrid[0:ChesboardColumns,0:ChessboardRows].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    ObjectPoints = [] # 3d point in real world space
    ImagePoints = [] # 2d points in image plane.


    for i in range(NumberOfFrames):

        print(i)
        Frame = Camera.GetFrame()

        if Stereo == "Left":
            Left, Right = SplitStereoImage(Frame)
            Frame = Left
        if Stereo == "Right":
            Left, Right = SplitStereoImage(Frame)
            Frame = Right

    
        Gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(Gray, (ChesboardColumns,ChessboardRows), None)
        
        # If found, add object points, image points (after refining them)
        if ret == True:
            ObjectPoints.append(objp)
            corners2 = cv2.cornerSubPix(Gray,corners, (11,11), (-1,-1), criteria)
            ImagePoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(Frame, (ChesboardColumns,ChessboardRows), corners2, ret)

        cv2.imshow('img', Frame)
        cv2.waitKey(1)

    Camera.Close()

    ret, CameraMatrix, DistortionCoefficient, rvecs, tvecs = cv2.calibrateCamera(ObjectPoints, ImagePoints, Gray.shape[::-1], None, None)
    print("Done")
    print(CameraMatrix)
    print(DistortionCoefficient)
    return CameraMatrix, DistortionCoefficient


#UNDISTORTION

#first funciton in opencv docs
def UndistortImage1(Image, CameraMatrix, DistortionCoefficient):

    h,  w = Image.shape[:2]
    NewCameraMatrix, ROI=cv2.getOptimalNewCameraMatrix(CameraMatrix,DistortionCoefficient,(w,h),1,(w,h))

    # undistort
    UndistortedImage = cv2.undistort(Image, CameraMatrix, DistortionCoefficient, None, NewCameraMatrix)

    # crop the image
    x,y,w,h = ROI
    UndistortedImage = UndistortedImage[y:y+h, x:x+w]
    return UndistortedImage


#second function in opencv docs
def UndistortImage2(Image, CameraMatrix, DistortionCoefficient):

    h,  w = Image.shape[:2]
    NewCameraMatrix, ROI=cv2.getOptimalNewCameraMatrix(CameraMatrix,DistortionCoefficient,(w,h),1,(w,h))

    # undistort
    mapx,mapy = cv2.initUndistortRectifyMap(CameraMatrix,DistortionCoefficient,None,NewCameraMatrix,(w,h),5)
    UndistortedImage = cv2.remap(Image,mapx,mapy,cv2.INTER_LINEAR)

    # crop the image
    x,y,w,h = ROI
    UndistortedImage = UndistortedImage[y:y+h, x:x+w]
    return UndistortedImage

#RECTIFICATION (stereo rectification, between left and right)

def compute_stereo_rectification_maps(stereo_rig, im_size, size_factor):
    new_size = (int(im_size[1] * size_factor), int(im_size[0] * size_factor))
    rotation1, rotation2, pose1, pose2 = cv2.stereoRectify(cameraMatrix1=stereo_rig.cameras[0].intrinsics.intrinsic_mat,
                                                            distCoeffs1=stereo_rig.cameras[0].intrinsics.distortion_coeffs,
                                                            cameraMatrix2=stereo_rig.cameras[1].intrinsics.intrinsic_mat,
                                                            distCoeffs2=stereo_rig.cameras[1].intrinsics.distortion_coeffs,
                                                            imageSize=(im_size[1], im_size[0]),
                                                            R=stereo_rig.cameras[1].extrinsics.rotation,
                                                            T=stereo_rig.cameras[1].extrinsics.translation,
                                                            flags=cv2.CALIB_ZERO_DISPARITY,
                                                            newImageSize=new_size
                                                            )[0:4]
    map1x, map1y = cv2.initUndistortRectifyMap(stereo_rig.cameras[0].intrinsics.intrinsic_mat,
                                               stereo_rig.cameras[0].intrinsics.distortion_coeffs,
                                               rotation1, pose1, new_size, cv2.CV_32FC1)
    map2x, map2y = cv2.initUndistortRectifyMap(stereo_rig.cameras[1].intrinsics.intrinsic_mat,
                                               stereo_rig.cameras[1].intrinsics.distortion_coeffs,
                                               rotation2, pose2, new_size, cv2.CV_32FC1)
    return map1x, map1y, map2x, map2y 



#DISPARITY POST FILTERING
#https://docs.opencv.org/4.x/d3/d14/tutorial_ximgproc_disparity_filtering.html



#STEREO IMAGES
def SplitStereoImage(Image, Grey = None):  #horizontal stereo iamge
    Image1 = Image[:,0:int(Image.shape[1]/2),:]
    Image2 = Image[:,int(Image.shape[1]/2):,:]

    if Grey:
        Image1 = cv2.cvtColor(Image1, cv2.COLOR_BGR2GRAY)
        Image2 = cv2.cvtColor(Image2, cv2.COLOR_BGR2GRAY)

    return Image1, Image2


#example from opencv
def GetDisparityMap(Image1, Image2):  #StereoBM
    stereo = cv2.StereoBM_create(numDisparities=64, blockSize=29)   #16 ,15
    Image1 = cv2.cvtColor(Image1, cv2.COLOR_BGR2GRAY)
    Image2 = cv2.cvtColor(Image2, cv2.COLOR_BGR2GRAY)
    disparity = stereo.compute(Image1,Image2)

    # Normalize the image for representation
    min = disparity.min()
    max = disparity.max()
    # disparity = np.uint8(6400 * (disparity - min) / (max - min))


    disparity = cv2.normalize(disparity, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

   
    
    disparity = (disparity*255).astype(np.uint8)
    disparity = cv2.applyColorMap(disparity , cv2.COLORMAP_MAGMA)


    return disparity

#example from t265 github
def GetDisparityMap2(Image1, Image2): #StereoSGMB

    # Configure the OpenCV stereo algorithm. See https://docs.opencv.org/3.4/d2/d85/classcv_1_1StereoSGBM.html for a description of the parameters
    window_size = 5
    min_disp = 0
    # must be divisible by 16
    num_disp = 112 - min_disp
    max_disp = min_disp + num_disp
    stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
                                    numDisparities = num_disp,
                                    blockSize = 16,
                                    P1 = 8*3*window_size**2,
                                    P2 = 32*3*window_size**2,
                                    disp12MaxDiff = 1,
                                    uniquenessRatio = 10,
                                    speckleWindowSize = 100,
                                    speckleRange = 32)


    # compute the disparity on the center of the frames and convert it to a pixel disparity (divide by DISP_SCALE=16)
    disparity = stereo.compute(Image1, Image2).astype(np.float32) / 16.0

    # # re-crop just the valid part of the disparity
    # disparity = disparity[:,max_disp:]

    return disparity

def ColorDisparity(Disparity):
    # convert disparity to 0-255 and color it
    # disp_vis = 255*(disparity - min_disp)/ num_disp
    disp_vis = 255*(Disparity)/ 16
    disp_color = cv2.applyColorMap(cv2.convertScaleAbs(disp_vis,1), cv2.COLORMAP_JET)
    return disp_color

def GetDepthFromDisparity(Disparity, B, f): #Disparity = X-X'  B=Baseline  f=focal length

    Depth = (B*f)/Disparity # same unit as B, (f and Disparity shhould have some unit in mm or pixels)
    return Depth


















# # CODR FROM T265

# #!/usr/bin/python
# # https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/t265_stereo.py


# #T265: in this example we show how to set up OpenCV to undistort the images and compute stereo depth from them.


# # Import OpenCV and numpy
# import cv2
# import numpy as np
# from math import tan, pi

# """
# The T265 uses very wide angle lenses, so the distortion is modeled using a four parameter distortion model known as Kanalla-Brandt. OpenCV supports this
# distortion model in their "fisheye" module, more details can be found here: https://docs.opencv.org/3.4/db/d58/group__calib3d__fisheye.html
# """


# #FRAMES LEFT AND RIGHT
# frame_data = {"left"  : None, "right" : None, "timestamp_ms" : None}


# #OpenCV stereo https://docs.opencv.org/3.4/d2/d85/classcv_1_1StereoSGBM.html
# window_size = 5
# min_disp = 0
# # must be divisible by 16
# num_disp = 112 - min_disp
# max_disp = min_disp + num_disp
# stereo = cv2.StereoSGBM_create(minDisparity = min_disp, numDisparities = num_disp, blockSize = 16, P1 = 8*3*window_size**2, P2 = 32*3*window_size**2, disp12MaxDiff = 1, uniquenessRatio = 10, speckleWindowSize = 100, speckleRange = 32)



# # GET ALL THE MATRIXES

# # GET INTRINSICS FROM CAMERA
# intrinsics = {"left"  : streams["left"].get_intrinsics(), "right" : streams["right"].get_intrinsics()}

# #Returns a camera matrix K from librealsense intrinsics
# def camera_matrix(intrinsics):
#     return np.array([[intrinsics.fx,             0, intrinsics.ppx],
#                      [            0, intrinsics.fy, intrinsics.ppy],
#                      [            0,             0,              1]])

# K_left  = camera_matrix(intrinsics["left"])
# K_right = camera_matrix(intrinsics["right"])


# #Returns the fisheye distortion from librealsense intrinsics
# def fisheye_distortion(intrinsics):
#     return np.array(intrinsics.coeffs[:4])

# D_left  = fisheye_distortion(intrinsics["left"])  
# D_right = fisheye_distortion(intrinsics["right"])


# (width, height) = (intrinsics["left"].width, intrinsics["left"].height)



# #Returns R, T transform from src to dst
# def get_extrinsics(src, dst):
#     extrinsics = src.get_extrinsics_to(dst)
#     R = np.reshape(extrinsics.rotation, [3,3]).T
#     T = np.array(extrinsics.translation)
#     return (R, T)

# # Get the relative extrinsics between the left and right camera
# (R, T) = get_extrinsics(streams["left"], streams["right"])





# # MATH TO UNDISTORT THE IMAGES

# # We need to determine what focal length our undistorted images should have in order to set up the camera matrices for initUndistortRectifyMap.  We could use stereoRectify, but here we show how to derive these projection matrices from the calibration and a desired height and field of view
# # We calculate the undistorted focal length:
# #
# #         h
# # -----------------
# #  \      |      /
# #    \    | f  /
# #     \   |   /
# #      \ fov /
# #        \|/
# stereo_fov_rad = 90 * (pi/180)  # 90 degree desired fov
# stereo_height_px = 300          # 300x300 pixel stereo output
# stereo_focal_px = stereo_height_px/2 / tan(stereo_fov_rad/2)

# # We set the left rotation to identity and the right rotation the rotation between the cameras
# R_left = np.eye(3)
# R_right = R

# # The stereo algorithm needs max_disp extra pixels in order to produce valid disparity on the desired output region. This changes the width, but the center of projection should be on the center of the cropped image
# stereo_size = (stereo_height_px + max_disp, stereo_height_px)
# stereo_cx = (stereo_height_px - 1)/2 + max_disp
# stereo_cy = (stereo_height_px - 1)/2

# # Construct the left and right projection matrices, the only difference is that the right projection matrix should have a shift along the x axis of baseline*focal_length
# P_left = np.array([[stereo_focal_px, 0, stereo_cx, 0],
#                     [0, stereo_focal_px, stereo_cy, 0],
#                     [0,               0,         1, 0]])
# P_right = P_left.copy()
# P_right[0][3] = T[0]*stereo_focal_px


# #Undistort And Rectify
# m1type = cv2.CV_32FC1
# (lm1, lm2) = cv2.fisheye.initUndistortRectifyMap(K_left, D_left, R_left, P_left, stereo_size, m1type)
# (rm1, rm2) = cv2.fisheye.initUndistortRectifyMap(K_right, D_right, R_right, P_right, stereo_size, m1type)
# undistort_rectify = {"left"  : (lm1, lm2), "right" : (rm1, rm2)}



# while True:

#     # Undistort and crop the center of the frames
#     center_undistorted = {"left" : cv2.remap(src = frame_data["left"], map1 = undistort_rectify["left"][0], map2 = undistort_rectify["left"][1], interpolation = cv2.INTER_LINEAR),
#                         "right" : cv2.remap(src = frame_data["right"], map1 = undistort_rectify["right"][0], map2 = undistort_rectify["right"][1], interpolation = cv2.INTER_LINEAR)}

#     # compute the disparity on the center of the frames and convert it to a pixel disparity (divide by DISP_SCALE=16)
#     disparity = stereo.compute(center_undistorted["left"], center_undistorted["right"]).astype(np.float32) / 16.0

#     # re-crop just the valid part of the disparity
#     disparity = disparity[:,max_disp:]

#     # convert disparity to 0-255 and color it
#     disp_vis = 255*(disparity - min_disp)/ num_disp
#     disp_color = cv2.applyColorMap(cv2.convertScaleAbs(disp_vis,1), cv2.COLORMAP_JET)
#     color_image = cv2.cvtColor(center_undistorted["left"][:,max_disp:], cv2.COLOR_GRAY2RGB)



#     key = cv2.waitKey(1)

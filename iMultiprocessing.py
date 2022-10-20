import iCamera as iCAM

print("Camera")
print(iCAM.PrintCamerasInfo())


# print(iCAM.GetAllCameraResolutions(5))



for CameraNumber in iCAM.GetCamerasNumbersAndNames()[0]:
        iCAM.LaunchCamera(CameraNumber, 640,480,30, True, True)
        

# iCAM.LaunchCamera(iCAM.GetCameraNumberByName('SPCA2100 PC Camera: PC Camera'), 640*2,480,30, True, True)
# iCAM.LaunchCamera(iCAM.GetCameraNumberByName('HBV HD CAMERA: HBV HD CAMERA'), 640*2,360*2,30, True, True)


print("end")

# print(iCAM.CheckIfCameraIsUsedByAnotherProcess(2))
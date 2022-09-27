
### Running Example As-Is:
`python3 main.py` - Runs without point cloud visualization
`python3 main.py -pcl` - Enables point cloud visualization


This will run subpixel disparity by default.

### Real-Time Depth from DepthAI Stereo Pair

StereoDepth configuration options:
```
lrcheck  = True   # Better handling for occlusions
extended = False  # Closer-in minimum depth, disparity range is doubled 
subpixel = True   # Better accuracy for longer distance, fractional disparity 32-levels
```

If one or more of the additional depth modes (lrcheck, extended, subpixel) are enabled, then:
 - depth output is FP16. TODO enable U16.
 - median filtering is disabled on device. TODO enable.
 - with subpixel, either depth or disparity has valid data.

Otherwise, depth output is U16 (mm) and median is functional. But like on Gen1, either depth or disparity has valid data. TODO enable both.


Select one pipeline to run:
```
   #pipeline, streams = create_rgb_cam_pipeline()
   #pipeline, streams = create_mono_cam_pipeline()
    pipeline, streams = create_stereo_depth_pipeline()
```

# Lane Detection

## Small description of this repo content
Hi!<br>
So, this is a small computer vision project made in python using opencv and numpy that takes in a video file that could be your car camera and
tries to track the edges of the lane you are currently in.</br>
In order to do so it needs to go trough many steps of image processing such as...

### Aquiring the video

![in.png](readme_res%2Fin.png)

### GrayScaling it

![grayscale.png](readme_res%2Fgrayscale.png)

### Applying a Mask

![mask.png](readme_res%2Fmask.png)

### Stretching and blurring the selected portion


![stretch_blur.png](readme_res%2Fstretch_blur.png)

### Filter Applying


![filter.png](readme_res%2Ffilter.png)

### Binarization

![binarization.png](readme_res%2Fbinarization.png)


### Regression line Calculation

![copy.png](readme_res%2Fcopy.png)


### So we can finally compose this:
![out.png](readme_res%2Fout.png)

All of this steps where done for each frame of the input video

## Conclusion
The final result is not 100% perfect as the lines sometimes flicker but it was a fun project overall and a nice training ground.

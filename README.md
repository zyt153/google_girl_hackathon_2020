# google_girl_hackathon_2020 #
**Project:** Design of covid-19 prevention and monitoring platform for universities.

**Team:** NoCodeFarmer

## Environment

Python 3.7.6

Keras 2.3.1

Tensorflow 1.14.0

Flask 1.1.2

chrome 83.0.4103.116

## Crawler

Including **crawler_JWC(XXMH).py**, **crawler_YJSY.py** and **crawler_TSG.py** .

The three are used to crawl the homepage announcements of the Academic Affairs Office (Information Portal), graduate school and library website of BUPT respectively. 

The notification title, date and url link are stored in the database **test.db**.

**Notice:** The crawler only runs at 8 o'clock every day, and **crawler_JWC(XXMH).py** cannot be run directly.

## Mask detection (based on yolov3)

Model file (h5): https://drive.google.com/file/d/1YuIPlB2MSnGUByUKka-IjCQyklfyNnPu/view?usp=sharing

After downloading, please place the model file in the model_data directory.

The test results include have_mask and no_mask.

Single image detection: `python3 yolo_video.py [OPTIONS...] --image`

Single video detection: `python3 yolo_video.py [video_path] [output_path (optional)]`

**Examples of test results:**

<img src="https://github.com/zyt153/google_girl_hackathon_2020/blob/master/static/mask_results/1.jpg" width = 30% height = 30% />
<img src="https://github.com/zyt153/google_girl_hackathon_2020/blob/master/static/mask_results/result_3.jpg" width = 30% height = 30% />

**mask_test.py** can batch detect and save the mask information in the picture.

Place the picture to be detected in the **mask** folder, and the result after detection will be stored in **static\mask_results**.

**density_test.py** is similar.

It will count the number of targets in the picture and record it in the database.

## Front-end

Files related to the front-end include **static**, **templates**, **main.py** and **test.db**.

The flask framework is used to support front-end and back-end interactive.

Run **main.py** to view and test the interface.


## Contributor:
GJ, LL, LX, ZYT

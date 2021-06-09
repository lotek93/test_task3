There is a dataset with vehicles labeling made from both RGB and thermal cameras. All labels are mixed up.
The task is to separate labels for visible vehicles and labels for those vehicles which are basically invisible for RGB camera because of light spots or something.
Download dataset from https://www.kaggle.com/aalborguniversity/aau-rainsnow/download

Visible vehicles are marked by green bounding boxes, and invisible ones are marked by red bounding boxes.

1) Place unpacked data into local directory, say, /tmp/data

2) Download Dockerfile.

3) Build docker image:<br>
    docker build -t test/test . 

4) Run docker container:<br>
    docker run -ti --rm -v /tmp/data:/home/test/data --name test3 test/test

Output images will be in /tmp/data/out/

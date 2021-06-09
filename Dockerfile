FROM ubuntu:20.04

WORKDIR /home/test

RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN apt-get update && apt-get -y upgrade && apt-get -y install git python3
#RUN apt-get install -y tzdata
#RUN apt-get -y install libopencv-dev 
RUN apt-get -y install python3-opencv
RUN apt-get -y install python3-pip
RUN apt-get -y install cython
RUN pip3 install numpy
RUN pip3 install matplotlib
RUN pip3 install pycocotools
RUN pip3 install tqdm
RUN pip3 install Cython
RUN git clone https://github.com/lotek93/test_task3 /home/test

CMD ["python3", "./separate_labels.py"]

# bag_splitter
ROS bag splitter for Udacity Self Driving Car challenge2 datasets

## Split the bag files into smaller bags that contain image topics only
You can use this program to split into smaller bags. Right now, it only writes image topics in the output files. Can be modified to include steering info also. Or a new method can be written to just extract/split steering topics (TODO)

I believe this helps for the following reasons
* Downloading a large bag is very time consuming. Multiple smaller bags can be downloaded in parallel.
* Processing can also be parallelized when we have access to multiple smaller bags
* Smaller bags can be directly used as part of your TensorFlow data_input pipeline or one can create different kinds of records (as per one's conventions) out of these smaller bag files beforehand

## Example Usage
To split the first 4 seconds of dataset.bag, you can run the command as:
python ros_bag_splitter.py dataset.bag 0 4

## Requirements
* I used Python2.7 running on Ubuntu 14.04 (VM running inside MacBook Pro as well as AWS EC2 instance)
* Install numpy (pip install numpy)
* Install ROS indigo. I followed the instructions listed here: http://wiki.ros.org/indigo/Installation/Ubuntu (check if you can run rosbag at terminal after installing it)





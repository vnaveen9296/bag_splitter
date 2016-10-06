# bag_splitter
ROS bag splitter for Udacity Self Driving Car challenge2 datasets

## Split the bag files into smaller bags that contain image topics only
You can use this program to split into smaller bags. Right now, it only writes image topics in the output files. Can be modified to include steering info also. Or a new method can be written to just extract/split steering topics (TODO)

I believe this helps for the following reasons
* Downloading a large bag is very time consuming. Multiple smaller bags can be downloaded in parallel.
* Processing can also be parallelized when we have access to multiple smaller bags
* Smaller bags can be directly used as part of your TensorFlow data_input pipeline or one can create different kinds of records (as per one's conventions) out of these smaller bag files beforehand




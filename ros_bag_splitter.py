import os
import numpy as np
import rosbag
import sys

class RosBagSplitter(object):
    '''Splits the input bag into multiple small bags. Cares about image and steering report messages only at present.'''
    def __init__(self, inbag, outfile_prefix, outdir):
        self.inbag = inbag
        self.outfile_prefix = outfile_prefix
        self.outdir = outdir
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        self.image_topics=['/left_camera/image_color', '/center_camera/image_color', '/right_camera/image_color']
        self.fps = 20
        # total messages from one camera source
        self.total_messages = sum(1 for x in rosbag.Bag(self.inbag).read_messages(topics=['/left_camera/image_color']))

    def split(self, start, end, num_seconds=1):
        '''Splits image topics based on duration (aka num_seconds).
        It's easy to create a shell script that launches multiple instances of this program to take advantage of
        multiple cores'''
        assert start >=0 and start < end and num_seconds > 0, 'Hmmm.. something is not right in the args you passed'
        self.msg_counter = 0
        self.gen = rosbag.Bag(self.inbag).read_messages(topics=self.image_topics)
        for j in range(start,end,num_seconds):
            msg_start = j*self.fps
            msg_end = (j+num_seconds)*self.fps
            #print msg_start, ':', msg_end
            outbag = self.outfile_prefix + 'image_only_' + str(j) + '_' + str(j+num_seconds) + '.bag' 
            outbag = os.path.join(self.outdir, outbag)
            self.extract(msg_start, msg_end, outbag=outbag)

    def extract(self, msg_start, msg_end, outbag=None):
        '''Extracts one chunk of image topics between [msg_start, msg_end)'''
        assert msg_start >=0 and msg_start < msg_end, 'Hmmm.. something is not right in the args you passed'
        if msg_start >= self.total_messages:
            return
        #msg_counter = 0
        if outbag is None:
            outbag = self.outfile_prefix + str(msg_start) + str(msg_end)
            outbag = os.path.join(self.outdir, outbag)
        with rosbag.Bag(outbag, 'w') as f:
            #for topic, msg, t in rosbag.Bag(self.inbag).read_messages(topics=self.image_topics):
            for topic, msg, t in self.gen:
                if self.msg_counter >= len(self.image_topics)*msg_start:
                    f.write(topic, msg, t)
                self.msg_counter += 1
                if self.msg_counter >= len(self.image_topics)*msg_end:
                    break

# entry to main land
if __name__=='__main__':
    if len(sys.argv) < 4:
        print 'Usage: ', sys.argv[0], ' ', 'dataset.bag start_second end_second'
        sys.exit(1)

    inbag = sys.argv[1]
    base = os.path.splitext(os.path.basename(inbag))[0]
    # create a splitter
    splitter = RosBagSplitter(inbag, outfile_prefix=base+'_small_', outdir=base+'_split_bags')
    # split into 1 second bags for image topics only between seconds specified by start_second and end_second
    splitter.split(int(sys.argv[2]), int(sys.argv[3]), 1)


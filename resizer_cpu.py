import cv2
import argparse
import os
import sys
from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool
import time

parser = argparse.ArgumentParser(description='Barch Opencv resizer',)

parser.add_argument('infolder',help='Path to target folder')
parser.add_argument('s', type=int, help='Scale factor (percent)')

args = parser.parse_args()

def resizer(cur_file):
    if 'resized' in cur_file : return None
    print (cur_file)
    image = cv2.imread(cur_file)
    width = int(image.shape[1] * s / 100)
    height = int(image.shape[0] * s / 100)
    #image = cv2.UMat(image)

    dsize = (width, height)
    if s < 100:
        output = cv2.resize(image, dsize, interpolation=cv2.INTER_AREA)
    else :
        output = cv2.resize(image, dsize, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(cur_file[:-4]+'_resized.jpg',output, [cv2.IMWRITE_JPEG_QUALITY, 80])

F = args.infolder
s = args.s

if s <=0 or s == 100 :
    print ("Wrong scaling factor entered. It can't be >=0 or 100")
    sys.exit()

flist = os.listdir(F)
flist.sort()
#print (temp)
flist = [F+"\\"+e for e in flist]
#print (flist)

#pool = ThreadPool(4)
#pool.map(resizer, flist)
start = time.time()
pool = ThreadPool()
pool.map(resizer, flist)
pool.close()
pool.join()
end = time.time()
print ('Executed in: ', end-start)

sys.exit()

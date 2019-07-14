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
    image = cv2.imread(cur_file)
    width = int(image.shape[1] * s / 100)
    height = int(image.shape[0] * s / 100)
    image = cv2.UMat(image)

    dsize = (width, height)
    if s < 100:
        output = cv2.resize(image, dsize, interpolation=cv2.INTER_AREA)
    else :
        output = cv2.resize(image, dsize, interpolation=cv2.INTER_CUBIC)
    wfile = cur_file[:-4]+'_resized.jpg'
    cv2.imwrite(wfile,output, [cv2.IMWRITE_JPEG_QUALITY, 80])
    resizer.counter += 1
    sys.stdout.write ('\rWritten: ' + wfile + '  Processed ' + str(resizer.counter) + ' of ' + str(len(flist)))
    sys.stdout.flush
resizer.counter = 0

def jpgfilter(x):
  if '.jpg'  in x or '.jpeg'  in x or '.JPG' in x or '.JPEG' in x:
    return True
  else:
    return False

F = args.infolder
s = args.s

if s <=0 or s == 100 :
    print ("Wrong scaling factor entered. It can't be >=0 or 100")
    sys.exit()

iflist = os.listdir(F)

flist = [x for x in iflist if '.jpg' in x or '.JPG' in x or '.jpeg' in x or '.JPEG' in x]
flist = [x for x in flist if '_resized.' not in x]
if len(flist) == 0 :
    print ("No JPEG images in directory. Exiting")
    sys.exit()
flist.sort()
flist = [F+"\\"+e for e in flist]
print ('Files to be processed:', len(flist))
start = time.time()
pool = ThreadPool()
pool.map(resizer, flist)
pool.close()
pool.join()
end = time.time()
print ('\nExecuted in: ' + str(round(end-start,3))+'s')
print ('Files processed: ' + str(len(flist)) + ' Average per file: ' + str(round(((end-start)/len(flist)),3)) + 's')
sys.exit()

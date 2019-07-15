import cv2
import argparse
import os
import sys
from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool
import time
import signal

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

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
    wfile = os.path.dirname(cur_file) + "\\Resized\\" + os.path.basename(cur_file)
    cv2.imwrite(wfile,output, [cv2.IMWRITE_JPEG_QUALITY, 80])
    resizer.counter += 1
    sys.stdout.write ('\rProcessed ' + str(resizer.counter) + ' of ' + str(len(flist)))
    #sys.stdout.write ('    Written: ' + wfile)
    sys.stdout.flush()

def jpgfilter(x):
  if '.jpg'  in x or '.jpeg'  in x or '.JPG' in x or '.JPEG' in x:
    return True
  else:
    return False

#Main program
parser = argparse.ArgumentParser(description='Barch Opencv resizer',)

parser.add_argument('infolder',help='Path to target folder')
parser.add_argument('s', type=int, help='Scale factor (percent)')

args = parser.parse_args()

F = args.infolder
s = args.s
resizer.counter = 0

if s <=0 or s == 100 :
    print ("Wrong scaling factor entered. It can't be <=0 or 100")
    sys.exit()

iflist = os.listdir(F)

flist = [x for x in iflist if '.jpg' in x or '.JPG' in x or '.jpeg' in x or '.JPEG' in x]
flist = [x for x in flist if '_resized.' not in x]
if len(flist) == 0 :
    print ("No JPEG images in directory. Exiting")
    sys.exit()
flist.sort()
flist = [F+"\\"+e for e in flist]
#print (os.path.dirname(flist[1]))
#print (os.path.basename(flist[1]))
#sys.exit()
if os.path.isdir(F+"\\Resized") == False:
    os.mkdir(os.path.dirname(F) + "\\Resized\\")
print ('Files to be processed:', len(flist))
print ('Writting resized images to: ', os.path.dirname(F) + "\\Resized\\")
print ('Trying to use',os.cpu_count(),'CPUs. If your system has GPU which OpenCV supports, it may use some GPU power. May be...')
print ('Press ALT+F4 for EMERGENCY BRAKE (will close terminal)')
start = time.time()
#sys.exit()
pool = ThreadPool(os.cpu_count())
try:
    pool.map(resizer,flist)
except KeyboardInterrupt:
    print ("\nCaught KeyboardInterrupt, terminating workers")
    pool.terminate()
    pool.join()

else:
    print ("\nQuitting normally")
    pool.close()
    pool.join()

end = time.time()
print ('\nExecuted in: ' + str(round(end-start,3))+'s')
print ('Files processed: ' + str(len(flist)) + ' Average per file: ' + str(round(((end-start)/len(flist)),3)) + 's')
sys.exit()

# -*- coding: utf-8 -*-
from PIL import Image
import psutil
import argparse
import os
from pathlib import Path, PureWindowsPath
import sys
from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool
import time

parent = psutil.Process()
parent.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)

def resizer(cur_file):
    if 'resized' in cur_file : return None
    image = Image.open(cur_file)
    (width, height) = (int(image.width * s / 100), int(image.height * s / 100))
    if s < 100:
        output = image.resize((width, height), resample=Image.BICUBIC)
    else :
        output = image.resize((width, height), resample=Image.LANCZOS)
    wfile = os.path.dirname(cur_file) + "\\Resized\\" + os.path.basename(cur_file)
    output.save(wfile, "JPEG", quality=85, exif=image.info['exif'])
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
parser = argparse.ArgumentParser(description='Ultra-fast batch JPEG resizer with EXIF preserved',)
parser.add_argument('infolder',help='Path to source folder')
parser.add_argument('s', type=int, help='Scale factor (percent). Only keep aspect ratio')

args = parser.parse_args()

F = args.infolder
s = args.s
resizer.counter = 0
fsize = 0

if s <=0 or s == 100 :
    print ("Wrong scaling factor entered. It can't be <=0 or 100")
    sys.exit()

iflist = os.listdir(F)

flist = [x for x in iflist if '.jpg' in x or '.JPG' in x or '.jpeg' in x or '.JPEG' in x]
if len(flist) == 0 :
    print ("No JPEG images in source folder. Exiting")
    sys.exit()
flist.sort()
flist = [F+"\\"+e for e in flist]
for x in flist:
    fsize += os.stat(x).st_size
#print (os.path.dirname(flist[1]))
#print (os.path.basename(flist[1]))
#sys.exit()

F = PureWindowsPath(F)
if os.path.isdir(F / 'Resized') == False:
    os.mkdir(F / 'Resized')
print ('Files to be processed:', len(flist))
print ('Total files size to be processed:',round(fsize/1024/1024,3), 'MB')
print ('Writting resized images to: ', F / 'Resized')
print ('Trying to use',os.cpu_count(),'threads.')
print ('Press ALT+F4 as EMERGENCY BRAKE (will close terminal)')
start = time.time()
#sys.exit()
pool = ThreadPool(os.cpu_count())
#pool = ThreadPool()
#pool.map_async(resizer,flist)
pool.imap_unordered(resizer,flist)
pool.close()
pool.join()
end = time.time()
print ('\nExecuted in: ' + str(round(end-start,3))+'s')
print ('Files processed: ' + str(len(flist)) + ' Average per file: ' + str(round(((end-start)/len(flist)),3)) + 's')
print ('Average data processing speed (source):',round(fsize/1024/1024/(end-start),3),'MB/sec')
sys.exit()

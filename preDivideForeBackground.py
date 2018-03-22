import numpy as np
import scipy
import skimage
from skimage.io import imread
from skimage import exposure
import random

GMUfore_dir='./GMUfore/'
GMUback_dir='./GMUback/'
count = 0
with open("./localGMU_train.txt") as f:
    while True:
        count += 1
        line = f.readline()
        if line == '':
            break
        if count < 20472:
            continue
        if line.find('.png')>-1:
            foreground = np.zeros((1080,1920,3))
            img = imread(line.strip())
            background = img.copy()
            img_name = line.strip().split('/')[-3]+'_'+line.strip().split('/')[-1]
            for i in range(5):
                t = f.readline()
            #t = int(f.readlines(4)[-1].strip())
            t = int(t)
            print img_name, t
            while t>0:
                t=t-1
                bbox = f.readline().strip().split(' ')
                bbox = bbox[-4:]
                int_bbox = [int(x) for x in bbox]

                ymin = max(0, int_bbox[1]-8)
                ymax = min(1080, int_bbox[3]+8)
                xmin = max(0, int_bbox[0]-8)
                xmax = min(1920, int_bbox[2]+8)

                temp = img.copy()
                nm = random.randint(0, 2)
                if nm > 2:
                    noise_mode = ['gaussian', 'poisson']
                    temp = skimage.util.random_noise(img, mode=noise_mode[nm])

                # # gamma
                # if mode == 1:
                degree = round(random.random()*3+0.2, 2)
                temp = exposure.adjust_gamma(temp, degree)
                # log
                #if mode == 2:
                #    degree = round(random.random()+0.5, 2)
                #    temp = exposure.adjust_log(temp, degree)
                # intensify
                #if mode == 3:
                    #temp = exposure.rescale_intensity(img)

                foreground[ymin:ymax,xmin:xmax] = temp[ymin:ymax,xmin:xmax]
                background[ymin:ymax,xmin:xmax] = 0
            scipy.misc.imsave(GMUfore_dir+img_name[:-4]+'_fore.png', foreground)
            scipy.misc.imsave(GMUback_dir+ img_name[:-4] + '_back.png', background)
import numpy as np
import scipy
import skimage
from skimage.io import imread
from skimage import exposure
import random

GMUfore_dir='./GMUforePatch/'
GMUback_dir='./GMUbackPatch/'
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
            #foreground = np.zeros((1080,1920,3))
            img = imread(line.strip())
            #background = img.copy()
            img_name = line.strip().split('/')[-3]+'_'+line.strip().split('/')[-1]
            for i in range(5):
                t = f.readline()
            #t = int(f.readlines(4)[-1].strip())
            t = int(t)
            print img_name, t
            for i in range(t):
                temp = img.copy()
                bbox = f.readline().strip().split(' ')
                bbox = bbox[-4:]
                int_bbox = [int(x) for x in bbox]

                ymin = max(0, int_bbox[1]-4)
                ymax = min(1080, int_bbox[3]+4)
                xmin = max(0, int_bbox[0]-4)
                xmax = min(1920, int_bbox[2]+4)


                w = xmax - xmin
                h = ymax - ymin

                patch_size = 256
                while w > patch_size or h > patch_size:
                    patch_size += 64

                fore = np.zeros((patch_size, patch_size, 3))
                back = np.zeros((patch_size, patch_size, 3))
                pad_w = patch_size - w
                pad_h = patch_size - h

                pad_left = min(random.randint(0, pad_w),xmin)
                pad_right = pad_w - pad_left
                pad_up = min(random.randint(0, pad_h),ymin)
                pad_bottom = pad_h - pad_up

                pad_xmin = xmin - pad_left
                pad_xmax = xmax + pad_right
                pad_ymin = ymin - pad_up
                pad_ymax = ymax + pad_bottom

                fore[pad_up:pad_up+h,pad_left:pad_left+w] = temp[ymin:ymax,xmin:xmax] # only for bounding box
                back = temp[pad_ymin:pad_ymax,pad_xmin:pad_xmax]
                back[pad_up:patch_size-pad_bottom,pad_left:patch_size-pad_right] = 0

                if w > 256 or h > 256:
                    fore = scipy.misc.imresize(fore,[256,256])
                    back = scipy.misc.imresize(back,[256,256])


                nm = random.randint(0, 2)
                if nm > 2:
                    noise_mode = ['gaussian', 'poisson']
                    fore = skimage.util.random_noise(fore, mode=noise_mode[nm])
                degree = round(random.random()*3+0.2, 2)
                fore = exposure.adjust_gamma(fore, degree)
                scipy.misc.imsave(GMUfore_dir + img_name[:-4] + '_box' + str(i) + '_fore.png', fore)
                scipy.misc.imsave(GMUback_dir + img_name[:-4] + '_box' + str(i) + '_back.png', back)

                # foreground[ymin:ymax,xmin:xmax] = temp[ymin:ymax,xmin:xmax]
                # background[ymin:ymax,xmin:xmax] = 0

            #scipy.misc.imsave(GMUfore_dir+img_name[:-4]+'_fore.png', foreground)
            #scipy.misc.imsave(GMUback_dir+ img_name[:-4] + '_back.png', background)
import json
import re
import matplotlib.image as mpimg


def convert(size, x1, y1, x2, y2):
    """
    input:
        size: width, height
        (x1, y1) upper left point
        (x2, y2) lower right point
    output:
        (x, y) center, normalized
        (w, h) width,height, normalized
    """
    dw = 1.0/size[0]
    dh = 1.0/size[1]

    x = (x1 + x2)*0.5 
    y = (y1 + y2)*0.5
    w = x2-x1
    h = y2-y1

    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def get_image_size(img_path):
    """
    input: image's path
    return: width, height
    """
    img=mpimg.imread(img_path)
    return img.shape[1], img.shape[0]

def write_label_for_one_img(labelpath, line, size, categories2num):
    """
    categories2num: {category -> number}
    size: (width, height)
    """
    write_success = 0
    with open(labelpath,'w') as fo:
        xx = line.split(';')
        for tmp in xx:
            if tmp=='':
                break
            items = tmp.split(',')
            if len(items)<5:
                continue
            x2, y2 = float(items[1]),float(items[2]) # lower right
            x1, y1 = float(items[3]),float(items[4]) # upper left
            x,y,w,h = convert(size, x1, y1, x2, y2)

            category = items[-1]
            if category not in categories2num:
                categories2num[category] = len(categories2num)
            line = [categories2num[category],x,y,w,h]
            line = [str(i) for i in line]
            line = ' '.join(line)
            fo.write(line+'\n')
            write_success = 1
    return categories2num, write_success


def write_files(anno, path, imgout):
    """
    input: 
        anno: path of annotation file
        path: path of image folder
        imgout: name of output image path list file
    output:
        no return;
        write three types of files:
            1) imgout: the file of paths of all images 
            2) a label file for each image
            3) class names
    """
    fo = open(imgout,'w')
    categories2num = {}
    with open(anno) as f:
        count = 0
        for c,i in enumerate(f):
            xx = i.strip().split(':')
            if len(xx)==2 and xx[1]=='':
                continue
            count += 1

            if c%10000 == 0:
                print ("write label file",c)

            imgname = xx[0]
            imgpath = '%s/%s'%(path,imgname)

            labelpath = re.sub('images','labels',imgpath)
            labelpath = re.sub('jpg','txt',labelpath)
            size = get_image_size(imgpath) # size = (w, h)
            
            categories2num,write_success = write_label_for_one_img(labelpath, xx[1], 
                    size, categories2num)
            if write_success:
                fo.write(imgpath+'\n')
	    
    fo.close()
    num2categories = {}

    for key in categories2num:
        value = categories2num[key]
        num2categories[value] = key

    classname = imgout.split('/')
    classname[-1] = 'traffic_sign_names.txt'
    classname = '/'.join(classname)
    with open(classname,'w') as fo:
        for i in sorted(num2categories):
            name = num2categories[i]
            fo.write(name+'\n')

    print("total number of images: %d"%count)

annotation = 'D:/DL_security/data/traffic_sign/sweden/annotations_part0.txt'
path = 'D:/DL_security/data/traffic_sign/sweden/images'
write_files(annotation, path, 'train_traffic_sign.txt')



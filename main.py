import cv2
import os

wrong_labels = []
point_extend = []
def read_image_crop(image_file, crop_image_file):
    # image_file = "/data/VOC/ABBY/JPEGImages/TRAIN/20220811_table/data_3/20220811_1152/53_1660218773099631.jpg"
    label_file = image_file.replace("JPEGImages","labels").replace("jpg","txt")
    print(label_file)
    crop_label_file = crop_image_file.replace("JPEGImages","labels").replace("jpg","txt")
    image = cv2.imread(image_file)

    with open(label_file, 'r') as f:
        file = f.readlines()

        print(file)
        desk_number = 0
        for i in range(len(file)):
            file1 = file[i]
            file1 = file1.split()
            print(file1)
            print(float(file1[1])*image.shape[1])
            if (file1[0] != '7'):
                continue
            desk_number += 1
            if len(file1) != 13:
                continue

            xmin = int(float(file1[1])*image.shape[1])
            ymin = int(float(file1[2])*image.shape[0])
            width = int(float(file1[3])*image.shape[1])
            height = int(float(file1[4])*image.shape[0])
            xmin = max(0, int(xmin - width/2))
            ymin = max(0,int(ymin - height/2))
            # cv2.rectangle(image,(xmin,ymin),(xmin+width,ymin+height),(0,0,0),2)

            point1x = int(float(file1[5]) * image.shape[1])
            point2x = int(float(file1[7]) * image.shape[1])
            point3x = int(float(file1[9]) * image.shape[1])
            point4x = int(float(file1[11]) * image.shape[1])

            point1y = int(float(file1[6])*image.shape[0])
            point2y = int(float(file1[8])*image.shape[0])
            point3y = int(float(file1[10])*image.shape[0])
            point4y = int(float(file1[12])*image.shape[0])

            new_image = image[ymin:ymin+height,xmin:xmin+width,:].copy()

            # cv2.circle(image,(point1x,point1y),0,(0,0,255),2)
            # cv2.circle(image, (point2x, point2y), 0, (0, 0, 255), 2)
            # cv2.circle(image, (point3x, point3y), 0, (0, 0, 255), 2)
            # cv2.circle(image, (point4x, point4y), 0, (0, 0, 255), 2)

            # xmin = float(file1[1]) - float(file1[3])/2
            # ymin = float(file1[2]) - float(file1[4])/2
            # print("image.size: ", image.shape)
            # cv2.circle(new_image,(point1x - xmin, point1y - ymin),0,(0,0,255),2)
            # cv2.circle(new_image, (point2x - xmin, point2y - ymin), 0, (0, 0, 255), 2)
            # cv2.circle(new_image, (point3x - xmin, point3y - ymin), 0, (0, 0, 255), 2)
            # cv2.circle(new_image, (point4x - xmin, point4y - ymin), 0, (0, 0, 255), 2)

            new_point1x, new_point1y = point1x - xmin, point1y - ymin
            new_point2x, new_point2y = point2x - xmin, point2y - ymin
            new_point3x, new_point3y = point3x - xmin, point3y - ymin
            new_point4x, new_point4y = point4x - xmin, point4y - ymin
            key_points = []
            print(new_image.shape)
            key_points.append(float(new_point1x) / new_image.shape[1])
            key_points.append(float(new_point1y) / new_image.shape[0])
            key_points.append(float(new_point2x) / new_image.shape[1])
            key_points.append(float(new_point2y) / new_image.shape[0])
            key_points.append(float(new_point3x) / new_image.shape[1])
            key_points.append(float(new_point3y) / new_image.shape[0])
            key_points.append(float(new_point4x) / new_image.shape[1])
            key_points.append(float(new_point4y) / new_image.shape[0])
            if min(key_points) < 0:
                continue
            if max(key_points) > 1:
                continue
            if i > 0:
                crop_label_file = crop_label_file.split('.')[0] + "_second.txt"
                crop_image_file = crop_image_file.split('.')[0] + "_second.jpg"
            with open(crop_label_file, 'w') as f:
                for value in key_points:
                    f.write(str(value))
                    f.write(' ')
            cv2.imwrite(crop_image_file, new_image)
        if desk_number > 1:
            wrong_labels.append(label_file)
          # cv2.imshow("1", image)
        # cv2.imwrite("1.jpg", image)


def show_desk_key_point(image_file, lable_file):
    image = cv2.imread(image_file)
    with open(lable_file,'r') as f:
        file = f.readlines()
        for line in file:
            points = line.split()
            points = list(map(float,points))
            cv2.circle(image,(int(image.shape[1]*points[0]),int(image.shape[0] * points[1])),0,(0,255,0),2)
            cv2.circle(image,(int(image.shape[1]*points[2]),int(image.shape[0] * points[3])),0,(0,255,0),2)
            cv2.circle(image,(int(image.shape[1]*points[4]),int(image.shape[0] * points[5])),0,(0,255,0),2)
            cv2.circle(image,(int(image.shape[1]*points[6]),int(image.shape[0] * points[7])),0,(0,255,0),2)
        cv2.imwrite("image_crop.jpg", image)
def show_desk_rectangle(image_label):
    image_file = image_label.replace("labels","JPEGImages").replace("txt", "jpg")
    image = cv2.imread(image_file)
    with open(image_label,'r') as f:
        lines = f.readlines()
        print(lines)
        print(image.shape)
        for line in lines:
            xmin = int(float(line.split(' ')[1])*image.shape[1])
            ymin = int(float(line.split(' ')[2])*image.shape[0])
            width = int(float(line.split(' ')[3])*image.shape[1])
            height = int(float(line.split(' ')[4])*image.shape[0])

            xmin = max(0, int(xmin - width/2))
            ymin = max(0,int(ymin - height/2))

            cv2.rectangle(image,(xmin,ymin),(xmin+width,ymin+height),(0,0,0),2)
    cv2.imwrite("/work/ljdong/Pycharm/DeskKeyPoint/test/temp/" + image_label.split('/')[-1] + ".jpg",image)

def image_list_2_crop_dir(image_list, save_dir):

    with open(image_list, 'r') as f:
        file = f.readlines()
        for image_file in file:
            image_file = image_file.replace("\n","")
            print(image_file,"====")
            image_file_dir = image_file.split('/')[:-1]
            save_image_dir = os.path.join(save_dir, os.path.join(*image_file_dir))
            save_labels_dir = save_image_dir.replace("JPEGImages","labels")
            save_image = os.path.join(save_image_dir, image_file.split('/')[-1])
            print("save_image: ", save_image)
            if not os.path.exists(save_image_dir):
                os.makedirs(save_image_dir)
            if not os.path.exists(save_labels_dir):
                os.makedirs(save_labels_dir)

            read_image_crop(image_file, save_image)

if __name__ == '__main__':

    image_list = "/data/VOC/ABBY/darknet/version2.0.16/train.txt"
    save_dir = "/work/ljdong/Pycharm/DeskKeyPoint/test/"

    image_list_2_crop_dir(image_list, save_dir)

    # with open("wrong_labels_val.txt", "w") as f:
    #     for wrong_label in wrong_labels:
    #         f.write(wrong_label)
    #         f.write('\n')
    # print(wrong_labels)

    # with open("wrong_labels_val.txt", "r") as f:
    #     lines = f.readlines()
    #     print(lines)
    #     for line in lines:
    #         line = line.replace("\n","")
    #         show_desk_rectangle(line)



    # show_desk_key_point("/work/ljdong/Pycharm/DeskKeyPoint/crop/JPEGImages/1.jpg", "/work/ljdong/Pycharm/DeskKeyPoint/crop/labels/1.txt")
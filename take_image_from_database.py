import pymysql
import cv2
import os
import re

def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def auto_save_file(path):
    directory, file_name = os.path.split(path)
    while os.path.isfile(path):
        pattern = '(\d+)\)\.'
        if re.search(pattern, file_name) is None:
            file_name = file_name.replace('.', '(0).')
        else:
            current_number = int(re.findall(pattern, file_name)[-1])
            new_number = current_number + 1
            file_name = file_name.replace(f'({current_number}).', f'({new_number}).')
        path = os.path.join(directory + os.sep + file_name)
    return path

def get_frame_from_video(video_name, frame_time, img_dir, img_name):
    """
    get a specific frame of a video by time in milliseconds
    :param video_name: video name
    :param frame_time: time of the desired frame
    :param img_dir: path which use to store output image
    :param img_name: name of output image
    :return: None
    """
    vidcap = cv2.VideoCapture(video_name)
    # Current position of the video file in milliseconds.
    vidcap.set(cv2.CAP_PROP_POS_MSEC, frame_time - 1)
    # read(): Grabs, decodes and returns the next video frame
    success, image = vidcap.read()

    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    if success:
        # save frame as JPEG file
        cv2.imwrite(auto_save_file(img_dir + img_name), image)
        # cv2.imshow("frame%s" % frame_time, image)
        # cv2.waitKey()
    else:
        print('cant read')
    vidcap.release()

result_path = './images/'
if not os.path.exists(result_path):
    os.makedirs(result_path)
else:
    del_file(result_path)

conn = pymysql.connect('localhost', user='root', passwd='dsax')
conn.select_db('fishdata')
cur = conn.cursor()

# insert = cur.execute("insert into fishdata values(1,'tom',18)")
# print('添加语句受影响的行数：',insert)

cur.execute('select * from hengze_20210125')
#取所有数据
resTuple=cur.fetchall()
print('共%d条数据'%len(resTuple))
print(resTuple)
for i in resTuple:
    fish_id = str(i[0])
    length = int(i[2])
    video_path = i[8]
    if fish_id == '7':
        get_frame_from_video(video_path, 45*1000, result_path, str(length)+'.jpg')
    else:
        get_frame_from_video(video_path, 30 * 1000, result_path, str(length) + '.jpg')
    print(f'video {video_path} complete!')

cur.close()
conn.close()
print('sql执行成功')
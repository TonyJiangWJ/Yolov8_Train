##
# 复制指定的一些文件
##

import os
import shutil
import json
from PIL import Image
from dataset_sql import OriginalImage, create_sqlite_connection
from lib.mylogger import LOGGER


def list_all_images(path):
    files = os.listdir(path)
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(path, file)
            # print(f"file path: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                json_info = json.load(f)
                desc = json_info['desc']
                image_id = json_info['imageId']
                image_path = os.path.join(path, image_id+'.jpg')
                if os.path.exists(image_path) is False:
                    shutil.copyfile(os.path.join(path, image_id+'.jpg.data'), image_path)
                width, height = get_image_size(image_path)
                print(f"desc: {desc} image: {image_id} width: {width} height: {height}")
                f.close()
                if height < width:
                    LOGGER.error(f"image invalid: {image_id} desc: {desc}")
                    continue
                OriginalImage('manor', desc, image_id).save(conn)
                shutil.copyfile(image_path,
                                os.path.join(local_dataset_path, image_id + '.jpg'))


def get_image_size(image_path):
    # 打开图像文件
    image = Image.open(image_path)

    # 获取图像分辨率
    width, height = image.size
    return width, height


def do_copy_images():
    for sub_path in os.listdir(img_path):
        LOGGER.verbose(f"check path: {sub_path}")
        list_all_images(os.path.join(img_path, sub_path))


def copy_specific_types_of_image(target_path, target_types, limit=100):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    for target_type in target_types:
        query_sql = f"SELECT image_id FROM original_image t1 where dataset_type='manor' and desc='{target_type}'" \
                    f" and not exists(select 1 from dataset_images t2 where t1.image_id=t2.image_id and t2.dataset_id=8)" \
                    f" limit 0, {limit}"
        cursor = conn.cursor()
        LOGGER.verbose(f"{query_sql}")
        cursor.execute(query_sql)
        results = cursor.fetchall()
        if len(results) <= 0:
            LOGGER.verbose(f'there is no image for this type: {target_type}')
        LOGGER.info(f"count for type: {target_type} is {len(results)}")
        for row in results:
            image_id = row[0]
            LOGGER.verbose(f"copy image: {image_id}")
            shutil.copyfile(os.path.join(local_dataset_path, image_id + '.jpg'),
                            os.path.join(target_path, image_id + '.jpg'))


def do_copy_manor_images():
    target_types = [
        '关闭按钮成功',
        '加速吃饭中',
        # '右侧小鸡带拳头',
        # '吃饭中可能没加速',
        # '好友界面失败',
        # '小鸡主界面失败',
        # '小鸡主界面成功',
        # '小鸡在好友家',
        # '小鸡外出',
        # '小鸡外出了',
        # '小鸡有饭吃',
        # '小鸡没饭吃',
        # '左侧小鸡带拳头',
        # '左侧无小鸡',
        # '左侧有小鸡',
        '执行捡屎',
        # '有屎可以捡',
        # '没有屎可以捡',
        # '睡觉中',
        # '领饲料失败',
        # '领饲料成功'
    ]
    copy_specific_types_of_image(r"H:\Projects\repository\datasets\manor_checking2", target_types, 50)


def do_copy_manor_to_group():
    distinct_sql = "select distinct desc from original_image where dataset_type='manor'"
    cursor = conn.cursor()
    cursor.execute(distinct_sql)
    types = cursor.fetchall()
    target_root_path = r"H:\Projects\repository\datasets\manor_grouped"
    if os.path.exists(target_root_path) is False:
        os.makedirs(target_root_path)
    if types is not None:
        for desc in types:
            desc = desc[0]
            LOGGER.verbose(f"check type: {desc}")
            query_sql = f"SELECT image_id FROM original_image t1 where dataset_type='manor' and desc='{desc}'"
            cursor = conn.cursor()
            cursor.execute(query_sql)
            results = cursor.fetchall()
            if results is not None:
                group_path = os.path.join(target_root_path, desc)
                if os.path.exists(group_path) is False:
                    os.makedirs(group_path)
                for result in results:
                    image_id = result[0]
                    target_image_path = os.path.join(group_path, image_id + '.jpg')
                    if os.path.exists(target_image_path) is True:
                        continue
                    shutil.copyfile(os.path.join(local_dataset_path, image_id + '.jpg'), target_image_path)


if __name__ == '__main__':
    img_path = r'Z:\disk2\脚本同步\小鸡\待标注数据\1124'
    # 从z盘nas复制到本地磁盘
    local_dataset_path = r"H:\Projects\repository\datasets\manor"
    conn = create_sqlite_connection(r'K:\YOLOV8_train_clean\datasets\datasets.db')
    # 复制所有图片到本地
    # do_copy_images()
    # 复制指定类型的图片到目标路径
    # do_copy_manor_images()
    # 将所有图片进行分类，并复制到对应文件夹
    do_copy_manor_to_group()
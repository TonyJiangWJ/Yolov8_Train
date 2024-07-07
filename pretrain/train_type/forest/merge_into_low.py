import shutil

import dataset_sql
from lib.mylogger import LOGGER
import label_config
import os


def delete_data(image_id, dataset_id, conn):
    del_sql = f"delete from image_labels where dataset_id='{dataset_id}' and image_id={image_id}"
    cursor = conn.cursor()
    cursor.execute(del_sql)
    conn.commit()


def merge_target_label(source_dataset_id, target_dataset_id, target_label):
    global source_path
    global target_path
    global conn
    query_sql = f"""select distinct image_id from image_labels where dataset_id='{source_dataset_id}' and label_name='{target_label}' and image_id not in (
        select image_id from image_labels where dataset_id='{target_dataset_id}'
    ) order by random() limit 50"""
    LOGGER.verbose(f"query sql:{query_sql}")
    cur = conn.cursor()
    cur.execute(query_sql)
    results = cur.fetchall()
    if os.path.exists(target_path) is False:
        os.mkdir(target_path)
    if results is not None:
        image_ids = [result[0] for result in results]
        for image_id in image_ids:
            image_id = str(image_id)
            if os.path.exists(os.path.join(source_path, image_id + '.json')) is False:
                LOGGER.error(f"标签数据不存在：{os.path.join(source_path, image_id + '.json')}")
                if os.path.exists(os.path.join(source_path, image_id + '.jpg')) is False:
                    LOGGER.error(f"图片数据不存在：{os.path.join(source_path, image_id + '.jpg')}")
                else:
                    LOGGER.warn(f"但是图片数据存在：{os.path.join(source_path, image_id + '.jpg')}")
                delete_data(image_id, source_dataset_id, conn)
                continue
            LOGGER.verbose(f"复制labels数据：{os.path.join(source_path, image_id + '.json')}")
            shutil.copyfile(os.path.join(source_path, image_id + '.json'),
                            os.path.join(target_path, image_id + '.json'))
            LOGGER.verbose(f"复制图片数据：{os.path.join(source_path, image_id + '.jpg')}")
            shutil.copyfile(os.path.join(source_path, image_id + '.jpg'),
                            os.path.join(target_path, image_id + '.jpg'))


if __name__ == '__main__':
    conn = dataset_sql.create_sqlite_connection(r'../../../datasets\datasets.db')
    source_path = r"../../../data/forest_new_tmp"
    target_path = r"../../../data/forest_low_2_merge"
    merge_target_label(4, 5, 'gift')
    # merge_target_label(4, 5, 'sea_ball')
    merge_target_label(4, 5, 'sea_ocr')
    merge_target_label(4, 5, 'one_key')
    merge_target_label(4, 5, 'patrol_ball')


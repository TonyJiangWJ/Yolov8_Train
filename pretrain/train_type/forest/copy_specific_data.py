import shutil

import dataset_sql
from lib.mylogger import LOGGER
import label_config
import os


## 从旧的数据集中抽取一部分旧的标签数据加入到新的标签训练，避免模型遗忘
def delete_data(image_id, dataset_id, conn):
    del_sql = f"delete from image_labels where dataset_id='{dataset_id}' and image_id={image_id}"
    cursor = conn.cursor()
    cursor.execute(del_sql)
    conn.commit()


def get_image_ids(dataset_id, labels, conn, limit=50):
    result_images = []
    for label in labels:
        query_sql = f"""select distinct image_id from image_labels where dataset_id='{dataset_id}' and image_id in (
            select t.image_id from image_labels t where dataset_id='{dataset_id}' and t.label_name = '{label}'
        ) order by random() limit 0,{limit}"""
        LOGGER.verbose(f"query sql:{query_sql}")
        cur = conn.cursor()
        cur.execute(query_sql)
        results = cur.fetchall()
        if results is not None:
            for result in results:
                result_images.append(result[0])
    return result_images


if __name__ == '__main__':
    conn = dataset_sql.create_sqlite_connection(r'../../../datasets\datasets.db')
    dataset_id = 7
    source_path = r"../../../data/forest_20240625"
    target_path = r"../../../data/forest_20240705/home"
    if os.path.exists(target_path) is False:
        os.mkdir(target_path)
    else:
        shutil.rmtree(target_path)
        os.mkdir(target_path)
    image_ids = get_image_ids(dataset_id, ['magic_species'], conn, 999999)
    for image_id in image_ids:
        image_id = str(image_id)
        if os.path.exists(os.path.join(source_path, image_id + '.json')) is False:
            LOGGER.error(f"标签数据不存在：{os.path.join(source_path, image_id + '.json')}")
            if os.path.exists(os.path.join(source_path, image_id + '.jpg')) is False:
                LOGGER.error(f"图片数据不存在：{os.path.join(source_path, image_id + '.jpg')}")
            else:
                LOGGER.warn(f"但是图片数据存在：{os.path.join(source_path, image_id + '.jpg')}")
            delete_data(image_id, dataset_id, conn)
            continue
        LOGGER.verbose(f"复制labels数据：{os.path.join(source_path, image_id + '.json')}")
        shutil.copyfile(os.path.join(source_path, image_id + '.json'),
                        os.path.join(target_path, image_id + '.json'))
        LOGGER.verbose(f"复制图片数据：{os.path.join(source_path, image_id + '.jpg')}")
        shutil.copyfile(os.path.join(source_path, image_id + '.jpg'),
                        os.path.join(target_path, image_id + '.jpg'))

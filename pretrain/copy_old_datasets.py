import shutil

import dataset_sql
from lib.mylogger import LOGGER
import label_config
import os


# dataset_name 数据集名称
# new_data_path 新的数据集目录，
# old_amount 旧标签数据量，尽量多一些，新标签数量少时可以减少，训练到后面需要逐渐增加旧数据的量 否则准确度会降低很多
def copy_all_random(dataset_name, new_data_path, old_amount=200):
    conn = dataset_sql.create_sqlite_connection(r'../datasets\datasets.db')
    labels = label_config.to_list(label_config.ant_forest)
    dataset = dataset_sql.get_dataset_from_db(conn, dataset_name)
    if not os.path.exists(new_data_path):
        os.mkdir(new_data_path)
    for label in labels:
        query_sql = f"select image_id from image_labels where dataset_id='{dataset.id}' and label_name='{label}' order by random() limit 0,{old_amount}"
        LOGGER.verbose(f"query sql:{query_sql}")
        cur = conn.cursor()
        cur.execute(query_sql)
        results = cur.fetchall()
        if results is not None:
            image_ids = [result[0] for result in results]
            print(f"label:{label} image ids:{image_ids}")
            for image_id in image_ids:
                image_id = str(image_id)
                if os.path.exists(os.path.join('..', dataset.data_dir_path, image_id + '.jpg')) is False:
                    LOGGER.warn(f"图片数据不再存在，需要考虑删除：{image_id} label: {label}")
                    continue
                LOGGER.verbose(f"复制labels数据：{os.path.join('..', dataset.data_dir_path, image_id + '.json')}")
                shutil.copyfile(os.path.join('..', dataset.data_dir_path, image_id + '.json'), os.path.join(new_data_path, image_id+'.json'))
                LOGGER.verbose(f"复制图片数据：{os.path.join('..', dataset.data_dir_path, image_id + '.jpg')}")
                shutil.copyfile(os.path.join('..', dataset.data_dir_path, image_id + '.jpg'), os.path.join(new_data_path, image_id+'.jpg'))




## 从旧的数据集中抽取一部分旧的标签数据加入到新的标签训练，避免模型遗忘
if __name__ == '__main__':
    copy_all_random('forest_new', '../data/forest_20240625', old_amount=100)


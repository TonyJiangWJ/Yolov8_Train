import shutil

import dataset_sql
from lib.mylogger import LOGGER
import label_config
import os

## 删除指定查询结果的数据
if __name__ == '__main__':
    conn = dataset_sql.create_sqlite_connection(r'../../../datasets\datasets.db')

    query_sql = f"""select distinct image_id from image_labels where dataset_id='3' and image_id not in (
    select t.image_id from image_labels t where dataset_id='3' and (t.label_name='item' or t.label_name='backpack')
)"""
    LOGGER.verbose(f"query sql:{query_sql}")
    cur = conn.cursor()
    cur.execute(query_sql)
    results = cur.fetchall()
    source_path=r"../../../data/forest_new_tmp"
    if results is not None:
        image_ids = [result[0] for result in results]
        for image_id in image_ids:
            image_id = str(image_id)
            LOGGER.verbose(f"删除labels数据：{os.path.join(source_path, image_id + '.json')}")
            os.remove(os.path.join(source_path, image_id + '.json'))
            LOGGER.verbose(f"删除图片数据：{os.path.join(source_path, image_id + '.jpg')}")
            os.remove(os.path.join(source_path, image_id + '.jpg'))



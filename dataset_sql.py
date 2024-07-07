import json
import os
import sqlite3
import label_config
from lib.mylogger import LOGGER


# 数据集

###
# create table dataset
# (
#     ID            integer      not null
#         constraint dataset_pk
#             primary key autoincrement,
#     dataset_name  varchar(32)  not null,
#     data_dir_path varchar(512) not null,
#     create_time   varchar(20)  not null,
#     modify_time   varchar(20)  not null
# );
###
class Dataset:
    def __init__(self, dataset_name, data_dir_path, id=None):
        self.dataset_name = dataset_name
        self.data_dir_path = data_dir_path
        self.id = id

    def save(self, cnx):
        cursor = cnx.cursor()
        insert_sql = f"INSERT INTO dataset (dataset_name, data_dir_path, create_time, modify_time)" \
                     f" SELECT '{self.dataset_name}', '{self.data_dir_path}', current_timestamp, current_timestamp" \
                     f" where not exists(select 1 from dataset where dataset_name ='{self.dataset_name}')"
        LOGGER.verbose(f"insert sql:{insert_sql}")
        cursor.execute(insert_sql)
        if cursor.rowcount > 0:
            LOGGER.info(f"insert success")
        select_id = f"select id from dataset where dataset_name='{self.dataset_name}'"
        cursor.execute(select_id)
        result = cursor.fetchone()
        if result is not None:
            self.id = result[0]
        LOGGER.verbose(f"数据集 id:{self.id}")
        cnx.commit()


def get_dataset_from_db(cnx, dataset_name):
    cursor = cnx.cursor()
    sql = f"SELECT dataset_name, data_dir_path, id from dataset where dataset_name='{dataset_name}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is not None:
        return Dataset(result[0], result[1], id=result[2])
    return None


###
# create table dataset_images
# (
#     ID          integer
#         constraint dataset_images_pk
#             primary key autoincrement,
#     dataset_id  integer not null,
#     image_id    varchar(32),
#     file_name   varchar(64),
#     create_time varchar(20),
#     modify_time varchar(20)
# );
#
# create index dataset_images_img_id_index
#     on dataset_images (dataset_id, image_id);
###
class DatasetImages:
    def __init__(self, dataset_id, image_id, file_name):
        self.dataset_id = dataset_id
        self.image_id = image_id
        self.file_name = file_name

    def save(self, cnx):
        cursor = cnx.cursor()
        insert_sql = f"INSERT INTO dataset_images (dataset_id, image_id, file_name, create_time, modify_time)" \
                     f" SELECT '{self.dataset_id}', '{self.image_id}', '{self.file_name}', current_timestamp," \
                     f" current_timestamp" \
                     f" where not exists(" \
                     f"select 1 from dataset_images where dataset_id ='{self.dataset_id}'" \
                     f" and image_id='{self.image_id}')"
        LOGGER.verbose(f"insert sql:{insert_sql}")
        cursor.execute(insert_sql)
        if cursor.rowcount > 0:
            LOGGER.info(f"insert success")
        cnx.commit()


###
# create table dataset_labels
# (
#     ID          integer
#         constraint dataset_labels_pk
#             primary key autoincrement,
#     dataset_id  integer     not null,
#     label_name  varchar(32) not null,
#     class_id    integer,
#     label_chz   varchar(128),
#     total_count integer,
#     create_time varchar(20) not null,
#     modify_time varchar(20)
# );
#
# create index dataset_labels_data_id_index
#     on dataset_labels (dataset_id);
###
class DatasetLabels:
    def __init__(self, dataset_id, label_name, class_id, label_chz, total_count):
        self.dataset_id = dataset_id
        self.label_name = label_name
        self.class_id = class_id
        self.label_chz = label_chz
        self.total_count = total_count

    def save(self, cnx):
        cursor = cnx.cursor()
        select_id = f"select id from dataset_labels where dataset_id='{self.dataset_id}' and label_name='{self.label_name}'"
        cursor.execute(select_id)
        id_result = cursor.fetchone()
        if id_result is None:
            insert_sql = f"INSERT INTO dataset_labels (dataset_id, label_name, class_id, label_chz, total_count, create_time, modify_time)" \
                         f" SELECT '{self.dataset_id}', '{self.label_name}', '{self.class_id}', '{self.label_chz}', '{self.total_count}', current_timestamp," \
                         f" current_timestamp" \
                         f" where not exists(" \
                         f"select 1 from dataset_labels where dataset_id ='{self.dataset_id}'" \
                         f" and label_name='{self.label_name}')"
            LOGGER.verbose(f"insert sql:{insert_sql}")
            cursor.execute(insert_sql)
        else:
            update_sql = f"UPDATE dataset_labels set label_chz='{self.label_chz}', total_count='{self.total_count}' WHERE " \
                         f"label_name='{self.label_name}' and dataset_id='{self.dataset_id}'"
            LOGGER.verbose(f"update sql:{update_sql}")
            cursor.execute(update_sql)
            if cursor.rowcount > 0:
                LOGGER.verbose(f"update success")
        cnx.commit()


###
# create table image_labels
# (
#     ID          integer
#         constraint image_labels_pk
#             primary key autoincrement,
#     image_id    integer      not null,
#     label_name  varchar(32)  not null,
#     shape_type  varchar(32) default 'rectangle',
#     points      varchar(256) not null,
#     create_time varchar(20)  not null,
#     modify_time varchar(20)  not null,
#     dataset_id  integer
# );
#
# create index image_labels_ID_index
#     on image_labels (ID);
#
# create index image_labels_data_label_index
#     on image_labels (dataset_id, label_name);
#
# create index image_labels_img_id_index
#     on image_labels (image_id);
###
class ImageLabels:
    def __init__(self, dataset_id, image_id, label_name, points, shape_type='rectangle'):
        self.dataset_id = dataset_id
        self.image_id = image_id
        self.label_name = label_name
        self.shape_type = shape_type
        self.points = json.dumps(points)
        self.id = None

    def save(self, cnx):
        cursor = cnx.cursor()
        insert_sql = f"INSERT INTO image_labels (dataset_id, image_id, label_name, points, shape_type, create_time, modify_time)" \
                     f" SELECT '{self.dataset_id}', '{self.image_id}', '{self.label_name}', '{self.points}', '{self.shape_type}', current_timestamp," \
                     f" current_timestamp" \
                     f" where not exists(" \
                     f"select 1 from image_labels where dataset_id ='{self.dataset_id}'" \
                     f" and image_id='{self.image_id}' and label_name='{self.label_name}' and points = '{self.points}')"
        LOGGER.verbose(f"insert sql:{insert_sql}")
        cursor.execute(insert_sql)
        cnx.commit()

    def delete_label_by_image_id(self, cnx):
        cursor = cnx.cursor()
        del_sql = f"delete from image_labels where dataset_id='{self.dataset_id}' and image_id='{self.image_id}'"
        LOGGER.verbose(f"delete sql:{del_sql}")
        cursor.execute(del_sql)
        cnx.commit()

###
# create table original_image(
#     id integer primary key autoincrement ,
#     desc varchar(256) not null,
#     image_id varchar(32) not null,
#     dataset_type varchar(32) not null
# );
# create index idx_datatype_desc on original_image(dataset_type,desc);
# create index idx_datatype_img_id on original_image(dataset_type,image_id);
###
class OriginalImage:
    def __init__(self, dataset_type, desc, image_id):
        self.dataset_type = dataset_type
        self.desc = desc
        self.image_id = image_id

    def save(self, cnx):
        cursor = cnx.cursor()
        insert_sql = f"INSERT INTO original_image (dataset_type, desc, image_id)" \
                     f"SELECT '{self.dataset_type}','{self.desc}','{self.image_id}' where not exists(" \
                     f"select 1 from original_image where dataset_type='{self.dataset_type}' and image_id='{self.image_id}')"
        LOGGER.verbose(f"insert sql: {insert_sql}")
        cursor.execute(insert_sql)
        cnx.commit()


def create_sqlite_connection(db_file='datasets/datasets.db'):
    return sqlite3.connect(db_file)


def summary_dataset_labels(dataset, labels, labels_chz, conn, group_counter):
    for label in labels:
        cls_id = labels.index(label)
        summary_sql = f"select count(*) from image_labels where dataset_id='{dataset.id}' AND label_name='{label}'"
        LOGGER.verbose(f"summary sql: {summary_sql}")
        cur = conn.cursor()
        cur.execute(summary_sql)
        result = cur.fetchone()
        if result is None:
            LOGGER.error(f"标签未找到对应的数据：{label}")
            group_counter[label] = 0
            continue
        group_counter[label] = result[0]
        if cls_id < len(labels_chz):
            dataset_labels = DatasetLabels(dataset.id, label, cls_id, labels_chz[cls_id], result[0])
            dataset_labels.save(conn)
        else:
            LOGGER.warn(f'标签对应中文值未配置：{label}')


##
# 读取数据集标签信息，并保存到数据库
##
def remove_all_image_file_not_exists(_dataset, _conn, relative_path):
    cursor = _conn.cursor()
    query_sql = f"select image_id from dataset_images where dataset_id='{_dataset.id}'"
    cursor.execute(query_sql)
    result = cursor.fetchall()
    if result is not None and len(result) > 0:
        for row in result:
            image_id = row[0]
            if os.path.exists(os.path.join(relative_path, _dataset.data_dir_path, image_id, '.jpg')):
                LOGGER.warn(f"image file not exists: {_dataset.data_dir_path}/{image_id}.jpg")
                # del_sql = f"delete from dataset_images where image_id='{image_id}' and dataset_id='{_dataset.id}'"
                # del_sql2 = f"delete from image_labels where image_id='{image_id}' and dataset_id='{_dataset.id}'"
                # cursor.execute(del_sql)
                # cursor.execute(del_sql2)
                # _conn.commit()


def check_json_labels_and_save(_dataset, _conn, relative_path='', overwrite=False, filter_image_ids=None):
    if overwrite:
        LOGGER.warn("delete all image labels")
        del_image_labels = f"delete from image_labels where dataset_id='{_dataset.id}'"
        cursor = _conn.cursor()
        cursor.execute(del_image_labels)
        _conn.commit()
    from convert_to_yolo_txt import load_label_file
    for json_file in os.listdir(os.path.join(relative_path, _dataset.data_dir_path)):
        if json_file.endswith('json'):
            image_id = json_file.replace('.json', '')
            if filter_image_ids is not None and image_id not in filter_image_ids:
                continue
            json_shapes, file_name = load_label_file(os.path.join(relative_path, _dataset.data_dir_path, json_file))
            dataset_image = DatasetImages(_dataset.id, image_id, file_name)
            dataset_image.save(_conn)
            first = True
            for jsonShape in json_shapes:
                image_label = ImageLabels(_dataset.id, image_id, jsonShape.label, jsonShape.points)
                if overwrite is False and first:
                    first = False
                    image_label.delete_label_by_image_id(_conn)
                image_label.save(_conn)
    if overwrite is False:
        remove_all_image_file_not_exists(_dataset, _conn, relative_path)

if __name__ == '__main__':

    conn = sqlite3.connect('datasets/datasets.db')
    root_path = 'data/manor'
    dataset = Dataset('manor', root_path)
    dataset.save(conn)
    labels = label_config.to_list(label_config.manor)
    labels_chz = label_config.to_list(label_config.manor_chz)
    check_json_labels_and_save(dataset, conn)
    summary_dataset_labels(dataset, labels, labels_chz, conn)

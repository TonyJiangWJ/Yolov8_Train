import dataset_sql
from lib.mylogger import LOGGER
import label_config


##
# 保存图片和其对应的标签信息，用于后续处理
##
if __name__ == '__main__':
    conn = dataset_sql.create_sqlite_connection('../datasets/datasets.db')
    # 指定数据集图片原始路径
    root_path = 'data/manor'
    dataset_name = 'manor'
    # 指定当前数据集名称
    dataset = dataset_sql.Dataset(dataset_name, root_path)
    # 保存数据集，已存在则跳过
    dataset.save(conn)
    labels = label_config.to_list(label_config.manor)
    labels_chz = label_config.to_list(label_config.manor_chz)
    # 获取
    dataset_sql.check_json_labels_and_save(dataset, conn, '..')
    dataset_sql.summary_dataset_labels(dataset, labels, labels_chz, conn)
-- 数据集
create table dataset
(
    ID            integer      not null
        constraint dataset_pk
            primary key autoincrement,
    dataset_name  varchar(32)  not null,
    data_dir_path varchar(512) not null,
    create_time   varchar(20)  not null,
    modify_time   varchar(20)  not null
);


create table dataset_images
(
    ID          integer
        constraint dataset_images_pk
            primary key autoincrement,
    dataset_id  integer not null,
    image_id    varchar(32),
    file_name   varchar(64),
    create_time varchar(20),
    modify_time varchar(20)
);

create index dataset_images_img_id_index
    on dataset_images (dataset_id, image_id);


create table dataset_labels
(
    ID          integer
        constraint dataset_labels_pk
            primary key autoincrement,
    dataset_id  integer     not null,
    label_name  varchar(32) not null,
    class_id    integer,
    label_chz   varchar(128),
    total_count integer,
    create_time varchar(20) not null,
    modify_time varchar(20)
);

create index dataset_labels_data_id_index
    on dataset_labels (dataset_id);


create table image_labels
(
    ID          integer
        constraint image_labels_pk
            primary key autoincrement,
    image_id    integer      not null,
    label_name  varchar(32)  not null,
    shape_type  varchar(32) default 'rectangle',
    points      varchar(256) not null,
    create_time varchar(20)  not null,
    modify_time varchar(20)  not null,
    dataset_id  integer
);

create index image_labels_ID_index
    on image_labels (ID);

create index image_labels_data_label_index
    on image_labels (dataset_id, label_name);

create index image_labels_img_id_index
    on image_labels (image_id);


create table original_image(
    id integer primary key autoincrement ,
    desc varchar(256) not null,
    image_id varchar(32) not null,
    dataset_type varchar(32) not null
);
create index idx_datatype_desc on original_image(dataset_type,desc);
create index idx_datatype_img_id on original_image(dataset_type,image_id);


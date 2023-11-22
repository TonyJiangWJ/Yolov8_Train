# 指定任务为目标检测，Yolo模型为yolov8s.pt，指定data配置文件 batch-1交给程序自己判断 epochs指定训练次数
yolo task=detect mode=train model=yolov8s.pt data=xiaoji.yaml batch=-1 epochs=20

yolo task=detect mode=train model=yolov8s.pt data=forest.yaml batch=-1 epochs=20

#更小分辨率，更快的模型
yolo task=detect mode=train model=yolov8n.pt data=forest.yaml imgsz=320 batch=-1 epochs=120F

#更小分辨率，更快的模型
yolo task=detect mode=train model=yolov8n.pt data=ads.yaml imgsz=320 batch=-1 epochs=120

# patience指定200个训练回合内判断最优解，如果越训练越废则直接停止
yolo task=detect mode=train model=yolov8n.pt data=ads.yaml imgsz=640 batch=-1 epochs=1200 patience=200

yolo task=detect mode=train model=yolov8n.pt data=vd_process.yaml imgsz=640 batch=-1 epochs=50

yolo task=detect mode=train model=yolov8n.pt data=config/forest.yaml imgsz=640 batch=-1 epochs=20

yolo task=detect mode=train model=runs\detect\train2\weights\best.pt data=config/forest.yaml imgsz=640 batch=-1 epochs=20

yolo task=detect mode=train model=runs\detect\train3\weights\best.pt data=config/forest2.yaml imgsz=640 batch=-1 epochs=250

yolo task=detect mode=train model=runs\detect\train5\weights\best.pt data=config/forest3.yaml imgsz=320 batch=-1 epochs=250

yolo task=detect mode=train model=runs\detect\forest_v2\weights\best.pt data=config/forest2.yaml imgsz=640 batch=-1 epochs=100
yolo task=detect mode=train model=runs\detect\train2\weights\best.pt data=config/forest2.yaml imgsz=640 batch=-1 epochs=100
yolo task=detect mode=train model=runs\detect\train7\weights\best.pt data=config/forest2.yaml imgsz=640 batch=-1 epochs=300
yolo task=detect mode=train model=runs\detect\forest_v3\weights\best.pt data=config/forest2.yaml imgsz=640 batch=-1 epochs=500 patience=250
yolo task=detect mode=train model=runs\detect\forest_v3\weights\best.pt data=config/forest2.yaml imgsz=640 batch=-1 epochs=100

yolo task=detect mode=train model=runs\detect\forest_v4_alpha\weights\best.pt data=config/forest.yaml imgsz=640 batch=-1 epochs=500
yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/forest.yaml imgsz=320 batch=-1 epochs=500
# 训练320的模型
yolo task=detect mode=train model=runs\detect\forest_v3\weights\best.pt data=config/forest2.yaml imgsz=320 batch=-1 epochs=1500 patience=550
yolo task=detect mode=train model=runs\detect\train2\weights\best.pt data=config/forest.yaml imgsz=320 batch=-1 epochs=150


yolo task=detect mode=train model=runs\detect\forest_v4\weights\best.pt data=config/forest3.yaml imgsz=320 batch=-1 epochs=500 patience=100

# 蚂蚁庄园
yolo task=detect mode=train model=yolov8n data=config/manor.yaml imgsz=480 batch=-1 epochs=20

yolo task=detect mode=train model=runs\detect\manor_v2\weights\best.pt data=config/manor.yaml imgsz=480 batch=-1 epochs=120

yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/manor2.yaml imgsz=480 batch=-1 epochs=120
yolo task=detect mode=train model=runs\detect\train2\weights\best.pt data=config/manor3.yaml imgsz=480 batch=-1 epochs=120


yolo task=detect mode=train model=runs\detect\manor_v3\weights\best.pt data=config/manor_punish.yaml imgsz=480 batch=-1 epochs=120

yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/manor_punish.yaml imgsz=480 batch=-1 epochs=120

yolo task=detect mode=train model=runs\detect\train2\weights\best.pt data=config/manor.yaml imgsz=480 batch=-1 epochs=1200 patience=300

# 龟饲料识别，初始化
yolo task=detect mode=train model=yolov8s.pt data=config/feed.yaml imgsz=640 batch=25 epochs=120
yolo task=detect mode=train model=runs\detect\train4\weights\best.pt data=config/feed.yaml imgsz=640 batch=-1 epochs=240 patience=100

yolo task=detect mode=train model=runs\detect\feed_v1\weights\best.pt data=config/feed.yaml imgsz=640 batch=25 epochs=240 patience=100
yolo task=detect mode=train model=runs\detect\feed_v2\weights\best.pt data=config/feed.yaml imgsz=640 batch=20 epochs=400 patience=100

yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/feed2.yaml imgsz=640 batch=-1 epochs=200 patience=100

yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/feed2.yaml imgsz=640 batch=25 epochs=2400 patience=0
yolo task=detect mode=train model=runs\detect\train3\weights\best.pt data=config/feed3.yaml imgsz=640 batch=-1 epochs=100
yolo task=detect mode=train model=runs\detect\train4\weights\best.pt data=config/feed4.yaml imgsz=640 batch=25 epochs=300 patience=100

# 原神，初始化
yolo task=detect mode=train model=yolov8n.pt data=config/yuanshen.yaml imgsz=640 batch=-1 epochs=100
yolo task=detect mode=train model=runs\detect\train2\weights\best.pt data=config/yuanshen.yaml imgsz=640 batch=-1 epochs=300
yolo task=detect mode=train model=runs\detect\train3\weights\best.pt data=config/yuanshen2.yaml imgsz=640 batch=-1 epochs=300
yolo task=detect mode=train model=runs\detect\train5\weights\best.pt data=config/yuanshen2.yaml imgsz=640 batch=-1 epochs=300
yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/yuanshen.yaml imgsz=640 batch=-1 epochs=500 patience=100
yolo task=detect mode=train model=runs\detect\train5\weights\best.pt data=config/yuanshen.yaml imgsz=640 batch=-1 epochs=4000 patience=1000
yolo task=detect mode=train model=runs\detect\train3\weights\best.pt data=config/yuanshen.yaml imgsz=640 batch=-1 epochs=4000 patience=500

# 补充训练 石头和丘丘人
yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/yuanshen_stone.yaml imgsz=640 batch=-1 epochs=300
yolo task=detect mode=train model=runs\detect\train2\weights\best.pt data=config/yuanshen_stone.yaml imgsz=640 batch=-1 epochs=300

# 抖音 初始化
yolo task=detect mode=train model=yolov8s.pt data=config/tiktok.yaml imgsz=1000 batch=-1 epochs=100
yolo task=detect mode=train model=runs\detect\train3\weights\best.pt data=config/tiktok.yaml imgsz=1024 batch=-1 epochs=200
yolo task=detect mode=train model=runs\detect\train4\weights\best.pt data=config/tiktok.yaml imgsz=1024 batch=-1 epochs=3000 patience=1000

yolo task=detect mode=train model=runs\detect\tiktok_v1.1\weights\best.pt data=config/tiktok.yaml imgsz=1024 batch=-1 epochs=200
yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/tiktok2.yaml imgsz=1024 batch=-1 epochs=200
yolo task=detect mode=train model=runs\detect\train3\weights\best.pt data=config/tiktok2.yaml imgsz=1024 batch=-1 epochs=500 patience=200

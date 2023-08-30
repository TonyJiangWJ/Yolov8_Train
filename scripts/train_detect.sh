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


yolo task=detect mode=train model=yolov8n data=config/manor.yaml imgsz=480 batch=-1 epochs=20

yolo task=detect mode=train model=runs\detect\manor_v2\weights\best.pt data=config/manor.yaml imgsz=480 batch=-1 epochs=120

yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/manor2.yaml imgsz=480 batch=-1 epochs=120
yolo task=detect mode=train model=runs\detect\train2\weights\best.pt data=config/manor3.yaml imgsz=480 batch=-1 epochs=120


yolo task=detect mode=train model=runs\detect\manor_v3\weights\best.pt data=config/manor_punish.yaml imgsz=480 batch=-1 epochs=120

yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/manor_punish.yaml imgsz=480 batch=-1 epochs=120

yolo task=detect mode=train model=runs\detect\train2\weights\best.pt data=config/manor.yaml imgsz=480 batch=-1 epochs=1200 patience=300


yolo task=detect mode=train model=yolov8s.pt data=config/feed.yaml imgsz=640 batch=25 epochs=120
yolo task=detect mode=train model=runs\detect\train4\weights\best.pt data=config/feed.yaml imgsz=640 batch=-1 epochs=240 patience=100

yolo task=detect mode=train model=runs\detect\feed_v1\weights\best.pt data=config/feed.yaml imgsz=640 batch=25 epochs=240 patience=100
yolo task=detect mode=train model=runs\detect\feed_v2\weights\best.pt data=config/feed.yaml imgsz=640 batch=20 epochs=400 patience=100

yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/feed2.yaml imgsz=640 batch=-1 epochs=200 patience=100

yolo task=detect mode=train model=runs\detect\train\weights\best.pt data=config/feed2.yaml imgsz=640 batch=25 epochs=2400 patience=0
yolo task=detect mode=train model=runs\detect\train3\weights\best.pt data=config/feed3.yaml imgsz=640 batch=-1 epochs=100
yolo task=detect mode=train model=runs\detect\train4\weights\best.pt data=config/feed4.yaml imgsz=640 batch=25 epochs=300 patience=100

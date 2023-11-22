from ultralytics import YOLO

if __name__ == '__main__':
    init_idx = 12
    # Load a model
    model = YOLO(rf'K:\YOLOV8_train_clean\train\runs\detect\train{init_idx}\weights\best.pt')  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(data='../config/yuanshen.yaml', batch=-1, epochs=2000, imgsz=800, device=0, patience=500)
    # results = model.train(data='../config/yuanshen_qiuqiu.yaml', batch=-1, epochs=300, imgsz=640, device=0, patience=100)
    print(f"train first result: {results}")
    # retrain 50 二次訓練，
    model = YOLO(fr'K:\YOLOV8_train_clean\train\runs\detect\train{init_idx+1}\weights\best.pt')  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(data='../config/yuanshen.yaml', batch=-1, epochs=150, imgsz=800, device=0, patience=100)
    print(f"train2 result: {results}")
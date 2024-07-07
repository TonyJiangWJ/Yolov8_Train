from ultralytics import YOLO
import os

if __name__ == '__main__':
    # Load a model
    # model = YOLO('yolov8n.pt')
    # model = YOLO('yolov8n.pt')
    pre_train_model = os.path.abspath(r'./runs/detect/train32/weights/best.pt')
    model = YOLO(pre_train_model)
    # Train the model
    # results = model.train(data='E:/Repository/YOLOV8_train/config/tiktok2.yaml', epochs=100, imgsz=1024, device=[0])
    results = model.train(data=os.path.abspath(r'../config/forest_rolling.yaml'), epochs=400, imgsz=320, device=0,
                          workers=32, batch=32,
                          patience=200)

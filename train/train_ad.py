from ultralytics import YOLO
import os

if __name__ == '__main__':
    # Load a model
    # model = YOLO('yolov8n.pt')
    model = YOLO('yolov8n.pt')
    # Train the model
    # results = model.train(data='E:/Repository/YOLOV8_train/config/tiktok2.yaml', epochs=100, imgsz=1024, device=[0])
    results = model.train(data=os.path.abspath(r'../config/ad.yaml'), epochs=400, imgsz=480, device=0,
                          workers=32, batch=32,
                          patience=200)

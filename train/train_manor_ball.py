from ultralytics import YOLO
import os

if __name__ == '__main__':
    # Load a model
    # model = YOLO(r'K:\YOLOV8_train_clean\runs\detect\manor_v4\weights\best.pt')
    # model = YOLO('yolov8n.pt')
    model = YOLO(os.path.abspath('../train/runs/detect/train26/weights/best.pt'))
    # model = YOLO(r'K:\YOLOV8_train_clean\train\runs\detect\train24\weights\best.pt')
    # Train the model
    results = model.train(data=os.path.abspath(r'..\config\manor_ball.yaml'), epochs=250, imgsz=320, device=0, patience=100)

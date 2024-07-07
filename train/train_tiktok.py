from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO('E:/Repository/YOLOV8_train/train/runs/detect/train7/weights/best.pt')

    # Train the model
    # results = model.train(data='E:/Repository/YOLOV8_train/config/tiktok2.yaml', epochs=100, imgsz=1024, device=[0])
    results = model.train(data='E:/Repository/YOLOV8_train/config/tiktok_process.yaml', epochs=500, imgsz=480, device=0)

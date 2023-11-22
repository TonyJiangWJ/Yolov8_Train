from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO('K:/YOLOV8_train_clean/runs/detect/forest_v5/weights/best.pt')

    # Train the model
    # results = model.train(data='K:/YOLOV8_train_clean/config/tiktok2.yaml', epochs=100, imgsz=1024, device=[0])
    results = model.train(data='K:/YOLOV8_train_clean/config/forest3.yaml', epochs=500, imgsz=320, device=0)

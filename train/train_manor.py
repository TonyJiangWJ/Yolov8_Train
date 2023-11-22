from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    # model = YOLO(r'K:\YOLOV8_train_clean\runs\detect\manor_v4\weights\best.pt')
    # model = YOLO('yolov8n.pt')
    model = YOLO(r'K:\YOLOV8_train_clean\train\runs\detect\train24\weights\best.pt')
    # Train the model
    results = model.train(data=r'K:\YOLOV8_train_clean\config\manor.yaml', epochs=500, imgsz=480, device=0, patience=100)

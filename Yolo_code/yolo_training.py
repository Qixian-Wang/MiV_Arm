from ultralytics import YOLO

best_weights = 'D:/Python/Projects/tool_labeling/runs/detect/yolo1117/weights/last.pt'

if __name__ == '__main__':

    # mode = "training"
    mode = "testing"

    if mode == "training":
        # training
        model = YOLO('yolo11.yaml')
        results = model.train(
            data='bio_tool.yaml',         # data yaml file
            epochs=3,                   # training epochs
            imgsz=960,                    # image size
            batch=6,                     # batch size
            device=[0],                   # GPU number
            name='yolo11',                # experiment name
            )
            
    elif mode == "testing":
        # testing
        model = YOLO(best_weights)
        results = model.predict(
            source='C:/Users/Qixian/Desktop/lab_tool_data/All_figures/images/val',  # validation image folder
            imgsz=960,
            conf=0.5,
            save=True,
            project='runs/val_preds',
            name='yolo11_on_val'
        )  

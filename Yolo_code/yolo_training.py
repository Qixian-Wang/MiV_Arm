from ultralytics import YOLO

path = 'D:/Python/Projects/tool_labeling'
best_weights = 'D:/Python/Projects/tool_labeling/runs/detect/yolo11/weights/best.pt'

train = 'images/images_train'
val =   'images/images_val'

if __name__ == '__main__':

    mode = "training"
    # mode = "testing"

    if mode == "training":
        # training
        model = YOLO('yolo11.yaml')
        results = model.train(
            data='bio_tool.yaml',         # data yaml file
            epochs=80,                   # training epochs
            imgsz=960,                    # image size
            batch=8,                     # batch size
            device=[0],                   # GPU number
            name='yolo11',                # experiment name
            )
    elif mode == "testing":
        # testing
        model = YOLO(best_weights)
        results = model.predict(
            source=val,  # validation image folder
            imgsz=1600,
            conf=0.5,
            save=True,
            project='runs/val_preds',
            name='yolo11_on_val'
        )  
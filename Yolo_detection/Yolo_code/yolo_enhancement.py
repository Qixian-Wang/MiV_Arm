import os

import cv2
import json
import albumentations as A
import numpy as np

from matplotlib import pyplot as plt
from pathlib import Path


def show_image(image):
    plt.imshow(image)
    plt.show()

transform = A.Compose([
    # Flip
    A.HorizontalFlip(p=0.5),

    # ColorJitter
    A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.4),
    A.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.3, p=1),

    # morphology
    A.OneOf([
    A.RandomShadow(shadow_roi=(0, 0, 1, 1), num_shadows_lower=3, num_shadows_upper=8, shadow_dimension=8, shadow_intensity_range=(0.2, 0.4), p=1),
    A.CoarseDropout(min_holes=5, max_holes=10, min_height=300, max_height=500, min_width=300, max_width=500, fill_value=0, p=1.0)
    ], p=1),

    # noise
    A.MultiplicativeNoise(multiplier=(0.5, 1.5), p=0.3),
    # resize
    A.ShiftScaleRotate(shift_limit=0.2, scale_limit=0.2, rotate_limit=0, border_mode=cv2.BORDER_CONSTANT, p=1),
    ],
    bbox_params=A.BboxParams(
        format='yolo',
        label_fields=['cls'],
        min_visibility=0.0
    ))


def generate_labelstudio_tasks(img_path, label_path, output_path):
    output_label_path = output_path / "label"
    output_img_path = output_path / "img"

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(output_label_path, exist_ok=True)
    os.makedirs(output_img_path, exist_ok=True)

    label_map = {
        0: "Beaker",
        1: "Large centri-tube",
        2: "MEA",
        3: "Middle centri-tube",
        4: "Mini centri-tube",
        5: "Petri dish",
        6: "Pipette",
        7: "Pipette tip holder",
        8: "Suction tip",
        9: "Tube holder",
        10: "rectangle bottle",
    }

    tasks = []

    for img_file in img_path.glob("*.jpg"):
        image = cv2.imread(str(img_file), cv2.IMREAD_COLOR_RGB)
        file_name = os.path.basename(img_file)

        lbl_file = label_path / f"{file_name.replace('.jpg', '.txt')}"
        bboxes, cls = [], []
        if lbl_file.exists():
            with open(lbl_file) as f:
                for line in f:
                    c, xc, yc, w, h = line.split()
                    cls.append(int(c))
                    bboxes.append((float(xc), float(yc), float(w), float(h)))
        else:
            raise FileNotFoundError(f"Label file not found: {lbl_file}")

        bboxes = np.array(bboxes, dtype=float)
        augmented = transform(image=image, bboxes=bboxes, cls=cls)
        aug_image = augmented['image']
        transformed_bboxes = augmented['bboxes']
        transformed_cls = augmented['cls']

        # save image
        new_name = f"Aug3_{file_name}"
        out_img = output_img_path / new_name
        cv2.imwrite(str(out_img), aug_image)
        print(f"{file_name} saved")

        # construct label studio format
        h, w = aug_image.shape[:2]
        results = []
        for cid, box in zip(transformed_cls, transformed_bboxes):
            xc, yc, bw, bh = box
            x_center = xc * w
            y_center = yc * h
            w_pix    = bw * w
            h_pix    = bh * h

            xmin = x_center - w_pix / 2
            ymin = y_center - h_pix / 2

            # convert to percentage which label studio needss
            x_pct = xmin / w * 100
            y_pct = ymin / h * 100
            w_pct = w_pix / w * 100
            h_pct = h_pix / h * 100

            results.append({
                "original_width": w,
                "original_height": h,
                "image_rotation": 0,
                "value": {
                    "x": x_pct,
                    "y": y_pct,
                    "width": w_pct,
                    "height": h_pct,
                    "rotation": 0,
                    "rectanglelabels": [ label_map[int(cid)] ]
                },
                "from_name": "rect",
                "to_name": "image",
                "type": "rectanglelabels",
                "origin": "manual"
            })

        task = {
            "data": {
                "image": f"/data/local-files/?d={output_img_path}/{new_name}"
            },
            "annotations": [
                {
                    "result": results
                }
            ]
        }
        tasks.append(task)

    output_file = output_label_path / "output_file.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    test_flag = False

    if test_flag:
        img = cv2.imread("test_img.jpg", cv2.IMREAD_COLOR_RGB)
        augmented = transform(image=img)
        transformed_image = augmented['image']
        show_image(transformed_image)

    else:
        img_path = Path("C:/Users/Qixian/Desktop/lab_tool_data/original_figures")
        label_path = Path("C:/Users/Qixian/Desktop/lab_tool_data/labels_original_figures")
        output_path = Path("C:/Users/Qixian/Desktop/lab_tool_data/aug4")

        os.makedirs(output_path, exist_ok=True)

        generate_labelstudio_tasks(img_path, label_path, output_path)

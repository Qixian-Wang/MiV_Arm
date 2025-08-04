import albumentations as A
from matplotlib import pyplot as plt
import cv2
from pathlib import Path
import os

def show_image(image):
    plt.imshow(image)
    plt.show()

transform = A.Compose([
    # Flip
    A.HorizontalFlip(p=0.5),

    # ColorJitter
    A.RGBShift(r_shift_limit=20, g_shift_limit=20, b_shift_limit=20, p=0.4),
    A.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.3, p=1),

    # morphology
    A.OneOf([
    A.RandomShadow(shadow_roi=(0, 0, 1, 1), num_shadows_lower=3, num_shadows_upper=8, shadow_dimension=8, shadow_intensity_range=(0.2, 0.4), p=1),
    A.CoarseDropout(min_holes=5, max_holes=10, min_height=300, max_height=500, min_width=300, max_width=500, fill_value=0, p=1.0)
    ], p=1),

    # noise
    A.OneOf([
    A.MultiplicativeNoise(multiplier=(0.5, 1.5), p=1),
    A.MotionBlur(blur_limit=(21, 31), p=1)], p=1),

    # resize
    A.ShiftScaleRotate(shift_limit=0.2, scale_limit=0.2, rotate_limit=70, border_mode=cv2.BORDER_CONSTANT, p=1)
])

if __name__ == "__main__":
    test_flag = False

    if test_flag:
        img = cv2.imread("test_img.jpg", cv2.IMREAD_COLOR_RGB)
        augmented = transform(image=img)
        transformed_image = augmented['image']
        show_image(transformed_image)

    else:
        img_path = Path("C:/Users/Qixian/Desktop/lab_tool_data/original_figures(927)")
        output_path = Path("C:/Users/Qixian/Desktop/lab_tool_data/augmented_figures_batch2")
        os.makedirs(output_path, exist_ok=True)

        for img in img_path.glob("*.jpg" or "*.jpeg" or "*.png"):
            new_name = f"Aug2_{os.path.basename(img)}"
            augmented = transform(image=cv2.imread(img, cv2.IMREAD_COLOR_RGB))
            transformed_image = augmented['image']
            cv2.imwrite(output_path / new_name, transformed_image)






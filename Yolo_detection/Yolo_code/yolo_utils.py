import os

import json
from PIL import Image
from pathlib import Path


def rename_file(file_path, split_str):
    """
    This function is used to rename the file name by splitting the string, the new name is the second part of the original name.
    It is used to solve the problem that the file name is not consistent with the desired name due to label_studio export.

    Parameters
    ----------
        file_path: the path of the file
        split_str: the string to split the file name
    """
    for file in file_path.iterdir():
        if file.is_file():
            name = file.name
            new_name = name.split(split_str, 1)[1]
            new_path = file.with_name(new_name)
            file.rename(new_path)


def check_label_name(img_path, label_path):
    """
    This function is used to check the label name is consistent with the image name.
    It is necessary because sometimes we need to delete some images since they are hard to label.

    Parameters
    ----------
        img_path: the path of the image
        label_path: the path of the label
    """
    img_path = Path(img_path)
    label_path = Path(label_path)

    error_flag = False
    for img in img_path.glob("*.jpg"):
        name = os.path.basename(img)
        label_name = name.replace(".jpg", ".txt")
        label_file_path = label_path / label_name
        if not label_file_path.exists():
            error_flag = True
            print(f"error: {label_name} not found")

    if error_flag:
        print("error: some label file not found")
    else:
        print("success: all label file found")


def update_json_paths(json_file_path, output_file_path, path_name):
    """
    This function is used to update the json paths.
    It is used to solve the problem that the json paths in exported json file need to be 
    updated in order to be imported in another PC.

    Parameters
    ----------
        json_file_path: the path of the json file   
        output_file_path: the path of the output json file
        path_name: the path of the image
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for task in data:
        if "data" in task and "image" in task["data"]:
            original_path = task["data"]["image"]
            filename = os.path.basename(original_path)
            filename = filename.rsplit("%5C", 1)[-1]
            task["data"]["image"] = f"/data/local-files/?d={path_name}/{filename}"

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def rename_image(img_path, starting_image_index=0):
    """
    This function is used to rename the image name.
    Names of images should be renamed because raw names taken by phones are too messy.
    The new name is "image_{image_index:06d}.jpg".

    Parameters
    ----------
        img_path: the path of the image
        starting_image_index: the starting image index, default is 0
    """
    for img in img_path.glob("*.jpg"):
        new_name = f"Aug4_image_{starting_image_index:06d}.jpg"
        img.rename(img_path / new_name)
        starting_image_index += 1

def resize_image(input_path, output_path, max_size=2048):
    """
    This function is used to resize the images so it will not be too large.

    Parameters
    ----------
        input_path: a folder containing raw images
        output_path: a folder to hold new resized images
        max_size: max limit for new images
    """
    os.makedirs(output_path, exist_ok=True)
    for image in os.listdir(input_path):
        with Image.open(os.path.join(input_path, image)) as img:
            original_size = img.size
            largest_size_idx = original_size.index(max(original_size))

            if largest_size_idx == 0:
                img_resized = img.resize(size=(max_size, int(max_size*original_size[1]/original_size[0])))
            elif largest_size_idx == 1:
                img_resized = img.resize(size=(int(max_size*original_size[0]/original_size[1]), max_size))
            else:
                img_resized = img
            img_resized.save(os.path.join(output_path, image))


if __name__ == "__main__":
    # Example for rename the image name
    # file_path = Path("C:/Users/Qixian/Downloads/project-8-at-2025-08-04-10-26-dcce85b8/labels")
    # split_str = "figures_batch2%5C"
    # rename_file(file_path, split_str)

    # Example for check the label name
    img_path = Path("C:/Users/Qixian/Desktop/lab_tool_data/All_figures/images/train")
    label_path = Path("C:/Users/Qixian/Desktop/lab_tool_data/All_figures/labels/train")
    check_label_name(img_path, label_path)

    # Example for update the json paths
    # json_path = Path("D:/Python/Projects/tool_labeling/output_file.json")
    # output_path_json = "D:/Python/Projects/tool_labeling/output_json.json"
    # path_name = "/home/zhantao/Bio_label/all_images/augmented_figures_batch3"
    # update_json_paths(json_path, output_path_json, path_name)

    # Example for rename the image name
    # img_path = Path("C:/Users/Qixian/Desktop/lab_tool_data/aug4/img")
    # rename_image(img_path, starting_image_index=0)

    # Example for resizing images
    # input_image = "/Users/aia/Downloads/pics"
    # output_image = "/Users/aia/Downloads/compressed_pics2"
    # resize_image(input_image, output_image, max_size=1920)





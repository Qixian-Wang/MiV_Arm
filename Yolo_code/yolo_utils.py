import os

import json
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
    for img in img_path.glob("*.jpeg" or "*.jpg" or "*.png"):
        name = os.path.basename(img)
        label_name = name.replace(".jpeg", ".txt").replace(".jpg", ".txt").replace(".png", ".txt")
        label_path = label_path / label_name
        if not label_path.exists():
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
        new_name = f"image_{starting_image_index:06d}.jpg"
        img.rename(img_path / new_name)
        starting_image_index += 1


if __name__ == "__main__":
    # example for rename the image name
    file_path = Path("C:/Users/Qixian/Downloads/project-8-at-2025-08-04-10-26-dcce85b8/labels")
    split_str = "figures_batch2%5C"
    rename_file(file_path, split_str)

    # example for check the label name
    img_path = Path("C:/Users/Qixian/Downloads/project-8-at-2025-08-04-10-26-dcce85b8/images")
    label_path = Path("C:/Users/Qixian/Desktop/lab_tool_data/labels")
    check_label_name(img_path, label_path)

    # example for update the json paths
    json_path = Path("D:/Python/Projects/tool_labeling/project-8-at-2025-08-03-15-39-0e5d6ccd.json")
    output_path_json = "D:/Python/Projects/tool_labeling/output_json.json"
    path_name = "C:/Users/Qixian/Desktop/lab_tool_data/original_figures(927)"
    update_json_paths(json_path, output_path_json, path_name)

    # example for rename the image name
    img_path = Path("C:/Users/Qixian/Desktop/lab_tool_data/original_figures(927)")
    rename_image(img_path)



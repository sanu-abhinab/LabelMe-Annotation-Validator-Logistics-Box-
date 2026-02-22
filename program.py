import os
import json
import shutil
import cv2


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = BASE_DIR
DEFECT_DIR = os.path.join(BASE_DIR, "defects")
MANUAL_VERIFICATION_DIR = os.path.join(BASE_DIR, "manual_verification")
NO_JSON_DIR = os.path.join(BASE_DIR, "no_json")

MIN_AREA_RATIO = 0.005
MAX_AREA_RATIO = 0.6
MIN_ASPECT_RATIO = 0.2
MAX_ASPECT_RATIO = 5.0
BOX_MIN_Y_RATIO = 0.35

os.makedirs(DEFECT_DIR, exist_ok=True)
os.makedirs(MANUAL_VERIFICATION_DIR, exist_ok=True)
os.makedirs(NO_JSON_DIR, exist_ok=True)



def get_base_name(filename):
    return os.path.splitext(filename)[0]


def move_file(path, target_dir):
    if path and os.path.exists(path):
        shutil.move(path, os.path.join(target_dir, os.path.basename(path)))




def validate_structure(data):
    required_keys = ["imagePath", "imageHeight", "imageWidth", "shapes"]

    for key in required_keys:
        if key not in data:
            return False

    if not isinstance(data["shapes"], list):
        return False

    for shape in data["shapes"]:
        if shape.get("shape_type") != "rectangle":
            return False
        if "points" not in shape or len(shape["points"]) != 2:
            return False
        if "label" not in shape or not shape["label"]:
            return False

    return True




def get_bbox(points):
    (x1, y1), (x2, y2) = points
    return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)


def box_area(box):
    x1, y1, x2, y2 = box
    return max(0, x2 - x1) * max(0, y2 - y1)


def boxes_overlap(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    return xB > xA and yB > yA


def is_partial_box(box, img_w, img_h):
    x1, y1, x2, y2 = box
    return x1 <= 0 or y1 <= 0 or x2 >= img_w or y2 >= img_h


def validate_box_relationships(boxes, img_w, img_h):
    full_boxes = []
    partial_boxes = []

    for box in boxes:
        if is_partial_box(box, img_w, img_h):
            partial_boxes.append(box)
        else:
            full_boxes.append(box)

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if boxes_overlap(boxes[i], boxes[j]):
                return False

    for p_box in partial_boxes:
        for f_box in full_boxes:
            if boxes_overlap(p_box, f_box):
                return False

    return True



def handle_images_without_json():
    files = os.listdir(INPUT_DIR)

    images = {get_base_name(f): f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))}
    jsons = {get_base_name(f): f for f in files if f.lower().endswith(".json")}

    for base, image_file in images.items():
        if base not in jsons:
            print(f"⚠ Image without JSON - NO_JSON: {image_file}")
            move_file(os.path.join(INPUT_DIR, image_file), NO_JSON_DIR)




def main():

    print("=== Annotation Validator Started ===\n")

    handle_images_without_json()

    for file in os.listdir(INPUT_DIR):
        if not file.endswith(".json"):
            continue

        json_path = os.path.join(INPUT_DIR, file)

        try:
            with open(json_path, "r") as f:
                data = json.load(f)
        except:
            print(f"❌ Invalid JSON: {file}")
            move_file(json_path, DEFECT_DIR)
            continue

        image_path = os.path.join(INPUT_DIR, data.get("imagePath", ""))

        if not os.path.exists(image_path):
            print(f"❌ Missing image: {file}")
            move_file(json_path, DEFECT_DIR)
            continue

        image = cv2.imread(image_path)
        img_h, img_w = image.shape[:2]
        image_area = img_w * img_h

        min_valid_area = image_area * MIN_AREA_RATIO
        max_valid_area = image_area * MAX_AREA_RATIO

        if not validate_structure(data):
            print(f"❌ Structural error: {file}")
            move_file(json_path, DEFECT_DIR)
            move_file(image_path, DEFECT_DIR)
            continue

        if len(data["shapes"]) == 0:
            print(f"⚠ Empty JSON - Manual verification: {file}")
            move_file(json_path, MANUAL_VERIFICATION_DIR)
            move_file(image_path, MANUAL_VERIFICATION_DIR)
            continue

        boxes = []
        geometry_error = False

        for shape in data["shapes"]:
            box = get_bbox(shape["points"])
            x1, y1, x2, y2 = box

            width = x2 - x1
            height = y2 - y1
            area = box_area(box)

            if area == 0 or area < min_valid_area or area > max_valid_area:
                geometry_error = True
                break

            aspect_ratio = width / height if height != 0 else 0

            if aspect_ratio < MIN_ASPECT_RATIO or aspect_ratio > MAX_ASPECT_RATIO:
                geometry_error = True
                break

            if y2 < img_h * BOX_MIN_Y_RATIO:
                geometry_error = True
                break

            boxes.append(box)

        if geometry_error:
            print(f"❌ Unrealistic box: {file}")
            move_file(json_path, DEFECT_DIR)
            move_file(image_path, DEFECT_DIR)
            continue

        if not validate_box_relationships(boxes, img_w, img_h):
            print(f"❌ Overlapping labels: {file}")
            move_file(json_path, DEFECT_DIR)
            move_file(image_path, DEFECT_DIR)
        else:
            print(f"✅ VALID: {file}")

    print("\n=== Validation Complete ===")
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()

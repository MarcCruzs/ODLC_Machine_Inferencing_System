import argparse
import os

import cv2
import torch
from PIL import Image


def load_model(weights_path, conf_threshold):
    model = torch.hub.load("ultralytics/yolov5", "custom", path=weights_path)
    model.conf = conf_threshold
    return model


def process_image(model, image, save_dir, filename_no_ext, ext, checklist_path):
    results = model(image)
    output_lines = []
    for i, obj in enumerate(results.xyxy[0]):
        x1, y1, x2, y2, conf, class_id = obj.tolist()
        cropped_image = image.crop((x1, y1, x2, y2))
        cropped_image_path = os.path.join(save_dir, f"{filename_no_ext}_cropped_{i}{ext}")
        cropped_image.save(cropped_image_path)
        output_line = f"Object {i}: Bounding Box: ({x1}, {y1}) - ({x2}, {y2}), confidence: {conf}, class: {class_id}, Cropped Image Path: {cropped_image_path}\n"
        output_lines.append(output_line)
        print(output_line.strip())

    # Save output to checklist file
    save_output_to_txt(output_lines, checklist_path)


def process_directory(model, path, save_dir, checklist_path):
    foldername = os.path.basename(path)
    folder_save_dir = os.path.join(save_dir, f"{foldername}_cropped_images")
    os.makedirs(folder_save_dir, exist_ok=True)
    for filename in os.listdir(path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            image_path = os.path.join(path, filename)
            image = Image.open(image_path)
            filename_no_ext, ext = os.path.splitext(filename)
            process_image(model, image, folder_save_dir, filename_no_ext, ext, checklist_path)


def live_view(model):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        cv2.imshow("YOLOv5 Object Detection", results.render()[0])
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


def save_output_to_txt(output_lines, checklist_path):
    with open(checklist_path, "w") as f:
        f.writelines(output_lines)


def detect_objects(
    source=None,
    image_dir=False,
    conf_threshold=0.25,
    save_dir=r"/usr/app/src/images",
    checklist_path="/usr/app/checklist/output.txt",
):
    weights_path = "./ShapeModel.pt"
    model = load_model(weights_path, conf_threshold)
    if str(source) == "0":
        live_view(model)
    else:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if image_dir:
            process_directory(model, source, save_dir, checklist_path)
        else:
            image = Image.open(source)
            filename = os.path.basename(source)
            filename_no_ext, ext = os.path.splitext(filename)
            process_image(model, image, save_dir, filename_no_ext, ext, checklist_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect objects using a YOLOv5 model.")
    parser.add_argument("--source", required=True, help="Path to the image, directory, or video (0 for live view)")
    parser.add_argument("--image_dir", action="store_true", help="Set this flag if the source is a directory of images")
    parser.add_argument("--conf_threshold", type=float, default=0.25, help="Confidence threshold for object detection")
    parser.add_argument("--save_dir", default="/usr/app/src/images", help="Directory to save the cropped images")
    parser.add_argument(
        "--checklist_path", default="/usr/app/checklist/output.txt", help="Path to save the output checklist"
    )

    args = parser.parse_args()
    detect_objects(
        source=args.source,
        image_dir=args.image_dir,
        conf_threshold=args.conf_threshold,
        save_dir=args.save_dir,
        checklist_path=args.checklist_path,
    )

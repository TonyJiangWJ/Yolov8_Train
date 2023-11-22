import argparse
import numpy as np
import onnxruntime
import time

import resnet50_data_reader
from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType, QuantFormat, CalibrationMethod, \
    quantize_static

import os
from PIL import Image
import cv2


def _preprocess_images(images_folder: str, height: int, width: int, size_limit=0):
    """
    Loads a batch of images and preprocess them
    parameter images_folder: path to folder storing images
    parameter height: image height in pixels
    parameter width: image width in pixels
    parameter size_limit: number of images to load. Default is 0 which means all images are picked.
    return: list of matrices characterizing multiple images
    """
    image_names = os.listdir(images_folder)
    if size_limit > 0 and len(image_names) >= size_limit:
        batch_filenames = [image_names[i] for i in range(size_limit)]
    else:
        batch_filenames = image_names
    unconcatenated_batch_data = []
    # print(image_names)

    for image_name in batch_filenames:
        # input_img = cv2.cvtColor(image_name, cv2.COLOR_BGR2RGB)
        input_img = Image.open(images_folder + "/" + image_name)
        # input_img = cv2.resize(input_img, (width, height))
        input_img = input_img.resize((width, height))
        input_img = np.array(input_img)
        input_img = input_img / 255.0

        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)
        input_tensor = np.ascontiguousarray(input_tensor, dtype=np.float32)

        # nchw_data = nhwc_data.transpose(0, 3, 1, 2)  # ONNX Runtime standard
        unconcatenated_batch_data.append(input_tensor)
    batch_data = np.concatenate(
        np.expand_dims(unconcatenated_batch_data, axis=0), axis=0
    )
    return batch_data


class ResNet50DataReader(CalibrationDataReader):
    def __init__(self, calibration_image_folder: str, model_path: str):
        self.enum_data = None

        # Use inference session to get input shape.
        session = onnxruntime.InferenceSession(model_path, None)
        (_, _, height, width) = session.get_inputs()[0].shape

        # Convert image to input data
        self.nhwc_data_list = _preprocess_images(
            calibration_image_folder, height, width, size_limit=1
        )
        self.input_name = session.get_inputs()[0].name
        # print(session.get_inputs())
        for n in session.get_inputs():
            print(n.name)
        self.datasize = len(self.nhwc_data_list)

    def get_next(self):
        if self.enum_data is None:
            self.enum_data = iter(
                [{self.input_name: nhwc_data} for nhwc_data in self.nhwc_data_list]
            )
        return next(self.enum_data, None)

    def rewind(self):
        self.enum_data = None


def main():
    input_model_path = '../runs/detect/forest_v4_320_try/weights/best-infer.onnx'
    output_model_path = input_model_path.replace('.onnx', '_lite.onnx')
    calibration_dataset_path = '../datasets/forest2/static'
    dr = ResNet50DataReader(
        calibration_dataset_path, input_model_path
    )

    quantize_static(
        input_model_path,
        output_model_path,
        dr,
        activation_type=QuantType.QUInt8,
        weight_type=QuantType.QInt8,
        per_channel=True,
        reduce_range=True,
        calibrate_method=CalibrationMethod.MinMax,
    )

    print("Calibrated and quantized model saved.")


if __name__ == "__main__":
    main()
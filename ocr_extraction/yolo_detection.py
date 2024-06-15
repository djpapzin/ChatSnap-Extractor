import os, sys
import traceback
from ultralytics import YOLO


class ObjectDetection():
    def __init__(self) -> None:
        self.__detector = YOLO("detection_model_99MAP.pt")

    def calculate_intersection_percentage(self, bbox1, bbox2):
        """
        The function calculates the percentage of intersection between two bounding boxes.
        
        :param bbox1: The `calculate_intersection_percentage` function calculates the percentage of
        intersection between two bounding boxes `bbox1` and `bbox2`. The function first extracts the
        coordinates of the two bounding boxes and then calculates the intersection area between them
        :param bbox2: The function `calculate_intersection_percentage` calculates the percentage of
        intersection between two bounding boxes `bbox1` and `bbox2`. The parameters `bbox1` and `bbox2`
        are dictionaries containing the coordinates of the bounding boxes in the format `{'x1': x1,
        'y1':
        :return: The function `calculate_intersection_percentage` returns the percentage of intersection
        between two bounding boxes `bbox1` and `bbox2`.
        """

        x1, y1, x2, y2 = bbox1['x1'], bbox1['y1'], bbox1['x2'], bbox1['y2']
        x3, y3, x4, y4 = bbox2['x1'], bbox2['y1'], bbox2['x2'], bbox2['y2']
                
        x_intersection = max(x1, x3)
        y_intersection = max(y1, y3)
        width_intersection = min(x2, x4) - x_intersection
        height_intersection = min(y2, y4) - y_intersection
        
        if width_intersection <= 0 or height_intersection <= 0:
            return 0
        
        area_b = (x4 - x3) * (y4 - y3)
        area_intersection = width_intersection * height_intersection
        intersection_percentage = area_intersection / area_b
        
        return intersection_percentage

    def detection_inference(self, screenshot_image):
        """
        This function performs object detection inference on a screenshot image using a detector model
        and returns the predicted classes with their confidence scores and bounding box coordinates.
        
        :param screenshot_image: The `detection_inference` method you provided seems to be performing
        object detection using a detector model. The method takes a `screenshot_image` as input and uses
        a detector to predict objects in the image
        :return: The `detection_inference` method returns a dictionary containing the predicted classes
        along with their confidence scores and bounding box coordinates for the given
        `screenshot_image`. If an exception occurs during the prediction process, an empty dictionary is
        returned.
        """
        try:
            results = self.__detector.predict(screenshot_image, stream= True, verbose=False, save=False, conf = 0.5)
            names = self.__detector.names
            predicted_class = {}
            for result in results:
                for idx, cls in enumerate(result.boxes.cls):
                    bbox = result.boxes.xyxy[idx].cpu().numpy().tolist()
                    if f"{names[int(cls)]}" not in predicted_class.keys():
                        predicted_class[f"{names[int(cls)]}"] = [{"confidence" : f"{result.boxes.conf[idx].cpu().numpy()}", "bbox" : {"x1" : bbox[0], "y1" : bbox[1], "x2" : bbox[2], "y2" : bbox[3]}}]
                    else:
                        predicted_class[f"{names[int(cls)]}"].append({"confidence" : f"{result.boxes.conf[idx].cpu().numpy()}", "bbox" : {"x1" : bbox[0], "y1" : bbox[1], "x2" : bbox[2], "y2" : bbox[3]}})
            return predicted_class
        except:
            print(f" Exception Occured {traceback.format_exc()}")
            return {}
        
    def organize_detection_result(self, detection_result):
        """
        This Python function organizes a detection result by grouping chat window elements based on
        their intersection percentage with sender, receiver, and emoji elements.
        
        :param detection_result: The `organize_detection_result` function takes a `detection_result` as
        input, which is expected to be a dictionary containing information about a screenshot,
        particularly a chat window and other elements like senders, receivers, and emojis within that
        chat window
        :return: The function `organize_detection_result` returns an organized list of chat windows with
        their corresponding content based on the detection result provided as input. If the input
        detection result does not contain a 'chat_window' key, the function returns the string "Not a
        Screenshot". Otherwise, it iterates through each chat window in the detection result, extracts
        the sender, receiver, and emoji content that intersects with
        """
        if 'chat_window' not in detection_result:
            return "Not a Screenshot"
        
        organized_result = []
        for chat_window in detection_result['chat_window']:
            organized_chat_window = {'bbox': chat_window['bbox'], 'content': []}
            
            for class_name in ['sender', 'receiver', 'emoji']:
                if class_name not in detection_result:
                    continue
                
                for item in detection_result[class_name]:
                    if 'bbox' not in item:
                        continue
                    
                    bbox = item['bbox']

                    if self.calculate_intersection_percentage(chat_window["bbox"], bbox) >= 0.8:
                        organized_chat_window['content'].append({class_name: item})
            
            organized_result.append(organized_chat_window)
        return organized_result   

    def driver_function(self, image_rgb):
        """
        The `driver_function` takes an RGB image as input, performs detection inference, organizes the
        predicted class, and returns the result.
        
        :param image_rgb: It looks like the code snippet you provided is a method called
        `driver_function` that takes `self` and `image_rgb` as parameters. The `image_rgb` parameter
        seems to be an RGB image that is passed to the `detection_inference` method to get a predicted
        class, and
        :return: the organized detection result after running the image through the detection inference
        and organizing the predicted class.
        """
        predicted_class = self.detection_inference(image_rgb)
        get_class = self.organize_detection_result(predicted_class)
        return get_class
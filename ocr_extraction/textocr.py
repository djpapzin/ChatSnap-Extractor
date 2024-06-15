import os
from paddleocr import PaddleOCR

class OCRExtraction:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls = True, lang = "en", show_log = False,
                                det_model_dir = os.path.join('paddlemodel', 'det'),
                                rec_model_dir = os.path.join('paddlemodel', 'rec'),
                                cls_model_dir = os.path.join('paddlemodel', 'cls'),
                                use_gpu = False, use_mp = True, total_process_num = 10, det_db_unclip_ration = 2) 
        print("OCR models are initialized")
        
    def points_to_xyxy(self, points):
        """
        The function `points_to_xyxy` converts a list of points to xyxy format by finding the minimum
        and maximum x and y values.
        
        :param points: The `points` parameter is a list of tuples representing coordinates in the format
        (x, y)
        :return: A dictionary containing the x1, y1, x2, and y2 values of the bounding box formed by the
        input points is being returned.
        """
        # Convert points to xyxy format
        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]

        x1 = min(x_values)
        y1 = min(y_values)
        x2 = max(x_values)
        y2 = max(y_values)
        # return [x1, y1, x2, y2]
        return {"x1" : x1,
                "y1" : y1,
                "x2" : x2,
                "y2" : y2}
    
    def read_text(self, img):
        """
        The function reads text from an image using OCR and returns the text along with its bounding box
        coordinates.
        
        :param img: The `img` parameter in the `read_text` method is typically an image input that you
        want to perform optical character recognition (OCR) on. The method uses the `self.ocr.ocr`
        function to extract text from the image
        :return: The `read_text` function returns a dictionary `ocr_points` containing a key "texts"
        with a list of text and bounding box information extracted from the input image using OCR
        (Optical Character Recognition) technology. If the OCR operation is successful, the function
        populates the "texts" list with text and bounding box data and returns the dictionary. If an
        exception occurs during the OCR operation, the
        """
        ocr_points = {"texts" : []}
        try:              
            paddle_result = self.ocr.ocr(img, cls = True)
            for x in paddle_result[0]:
                # print(points_to_xyxy(x[0]), x[1][0])
                ocr_points["texts"].append({"text" : x[1][0], "bbox" : self.points_to_xyxy(x[0])})
            return ocr_points
        except:
            return ocr_points
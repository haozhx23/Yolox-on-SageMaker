import numpy as np
import torch, os, json, io, cv2, time
# from ultralytics import YOLO


def model_fn(model_dir):
    model = torch.hub.load('code/', 'custom', path='code/best.pt', source='local')
    return model

def input_fn(request_body, request_content_type):
    print("Executing input_fn from inference.py ...")
    if request_content_type:
        jpg_original = np.load(io.BytesIO(request_body), allow_pickle=True)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=-1)
    else:
        raise Exception("Unsupported content type: " + request_content_type)
    return img

def predict_fn(input_data, model):
    result = model(input_data)
    return result

def output_fn(prediction_output, content_type):
    df = prediction_output.pandas().xyxy[0]
    return(df.to_json(orient="split"))
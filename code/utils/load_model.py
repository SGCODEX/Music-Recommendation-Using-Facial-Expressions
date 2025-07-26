import os
from keras.models import load_model

def load_trained_model():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model_path = os.path.join(base_dir, "model", "fer2013_mini_XCEPTION.102-0.66.hdf5")
    if not os.path.exists(model_path):
        raise FileNotFoundError("Trained model not found. Please add or train a model.")
    return load_model(model_path)

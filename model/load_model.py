"""
This is used to get classify a image of four breeds:
'french_bulldog','german_shepherd','golden_retriever','labrador_retriever',
into the right category. Currently the model gives 93%  accuracy
"""
import torchvision
from torchvision import models
from torchvision import transforms, datasets
import torch.nn as nn
import torch
import os
import sys
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

#path = os.path.dirname(os.path.realpath(__file__))

breeds_dict = {
    'french_bulldog': 0,
    'german_shepherd': 1,
    'golden_retriever': 2,
    'labrador_retriever': 3
}

def load_model(model_file_name):
    """
    Load the model

    Arguments:
        model_file_name {XXmodel.pth} -- saved trained model

    Returns:
        the loaded model
    """
    #path = os.getcwd()
    path = os.path.dirname(os.path.realpath(__file__))
    device = torch.device('cpu')
    model = torchvision.models.resnet18(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 4)
    model.load_state_dict(
        torch.load(os.path.join(path, model_file_name), map_location=device))
    model.eval()
    return model


def process_image(image_file):
    """
    Pre-processing the image

    Arguments:
        image_file {image.jpg} -- the image wants to get inference

    Returns:
        [tensor] -- [tensor to feed into the model]
    """
    simple_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.4910, 0.4593, 0.4196], [0.229, 0.224, 0.225])
    ])
    image = Image.open(Path(image_file))
    image_processed = simple_transform(image)
    image = image_processed.view(1, 3, 224, 224)
    return image


def predict(model, processed_image):
    """Get prediction

    Arguments:
        model -- the loaded model
        processed_image  -- image tensor

    Returns:
        int -- the index of the label dictionary
    """
    output = model(processed_image)
    prediction = int(torch.max(output.data, 1)[1].numpy())
    return prediction

def run_model(image_path):
    model = load_model('trained_model_Jun21.pth')
    image = process_image(image_path)
    prediction = predict(model, image)
    return list(breeds_dict.keys())[prediction]

def main():

    # breeds_dict = {
    #     'french_bulldog': 0,
    #     'german_shepherd': 1,
    #     'golden_retriever': 2,
    #     'labrador_retriever': 3
    # }
    model = load_model('trained_model_Jun21.pth')
    # image = process_image(
    #     '/Users/jing/Documents/school/2019Summer/software engineering/dog-breed-identification/test_images/image1.jpg'
    # )  ## Change here to be the image path.
    image = process_image(sys.argv[1])
    prediction = predict(model, image)
    #print(prediction)
    print(list(breeds_dict.keys())[prediction])


if __name__ == '__main__':
    main()
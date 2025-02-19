import torch
from torchvision import transforms, models
from PIL import Image
def object_classification(img_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = models.resnet18(pretrained=True) 
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 9) 
    model = model.to(device)

    model.load_state_dict(torch.load(r"classification_model.pth"))
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    def predict_image(image_path):
        image = Image.open(image_path).convert('RGB')
        image = transform(image).unsqueeze(0)  
        image = image.to(device)

        # Make prediction
        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output, 1)
            class_index = predicted.item()

        class_labels = {
            0: 'Banana',
            1: 'Lemon',
            2: 'Mango',
            3: 'Orange',
            4: 'Pineapple',
            5: 'Tomato',
            6: 'Watermelon',
            7: 'Apple',
            8: 'Images_Packed'
        }
        return class_labels[class_index]
    result = predict_image(img_path)
    return result


Automated Date Extraction and Product Classification

This repository provides a comprehensive solution for automating the extraction of manufacturing and expiry dates from product images, classifying objects into predefined categories, and evaluating product freshness. It integrates advanced OCR, machine learning, and deep learning techniques to ensure accuracy and efficiency.
Abstract
This project, PRODUCT DETAIL EXTRACTION, automates the extraction and classification of product-related information using advanced machine learning and neural network techniques. Key functionalities include Optical Character Recognition (OCR) for text extraction, freshness detection to determine product validity, and classification of objects into predefined categories. The system employs a ResNet-50 architecture for classification, a custom OCR pipeline for text recognition, and a logistic regression model for freshness evaluation. Designed for ease of use, the project features a web-based interface for seamless data processing and visualization. This document details the methodologies, network architectures, and workflows implemented, offering insights into the project's functionality and potential applications.
Overview
The PRODUCT DETAIL EXTRACTION project focuses on automating the process of extracting, analyzing, and classifying product-related information from images or scanned documents. It integrates advanced machine learning techniques, including deep learning architectures and neural networks, to process a range of tasks such as Optical Character Recognition (OCR), freshness detection, and product classification.
This system is designed for industries requiring high accuracy in product information processing, such as retail, inventory management, and supply chain logistics. By employing state-of-the-art models and intuitive interfaces, it offers a robust solution to streamline data extraction workflows, minimize manual errors, and enhance operational efficiency.
The system primarily comprises three core functionalities:
1.	OCR for Text Extraction: Extracting text from product labels, including critical details such as manufacturing dates, expiry dates, and serial numbers.
2.	Freshness Detection: Identifying product validity or shelf life using text analysis of extracted dates.
3.	Product Classification: Categorizing products into predefined classes based on visual features, utilizing a ResNet-50 architecture.
________________________________________
 Key Features
•	OCR for text extraction: Identify and extract text from images.
•	Freshness detection: Determine the shelf life or expiry of a product.
•	Object classification: Classify products into predefined categories using a deep learning model.
•	Automated classification of objects into six predefined categories using a ResNet-50 model.
•	Extraction of manufacturing and expiry dates using fine-tuned PaddleOCR.
•	Freshness evaluation based on the extracted dates.
•	MRP (Maximum Retail Price) extraction from product images.

________________________________________


Algorithm and Neural Network Details
Neural Network Architecture
The project utilizes:
•	ResNet-50: For object classification with six classes, leveraging its deep residual connections for feature extraction.
•	Custom OCR Pipeline: A combination of pre-trained models and fine-tuned layers to improve text detection and recognition accuracy.
Layers and Training Pipeline
Object Classification Model
1.	Input Layer: Processes resized images (224x224 pixels).
2.	Convolutional Layers:
o	The ResNet-50 backbone consists of 5 stages, each with multiple convolutional blocks.
o	Each block includes 3 convolutional layers with kernel sizes of 1x1, 3x3, and 1x1.
o	Batch normalization and ReLU activation are applied after each convolution.
o	Skip connections are added to ensure efficient gradient flow.
3.	Global Average Pooling Layer: Reduces the spatial dimensions of the feature maps.
4.	Fully Connected Layers: Outputs probabilities for six categories.
5.	Loss Function: Cross-entropy loss.
6.	Optimizer: Adam optimizer with learning rate scheduling.
OCR Pipeline
1.	Text Detection:
o	Uses a convolutional network to predict bounding boxes around text regions.
o	Employs a sliding window approach to localize characters.
2.	Text Recognition:
o	Character-level CNN combined with a BiLSTM layer for sequence modeling.
o	Outputs recognized text sequences using Connectionist Temporal Classification (CTC) loss.
Freshness Detection
•	A logistic regression model trained on extracted text features to identify valid dates.
•	Features include contextual embeddings from a pre-trained language model.
________________________________________
Detailed Workflow
1.	Object Classification:
o	Input images are passed through a ResNet-50 model (model_resnet50_6_classes.h5) to determine the product category.
o	The classification results are used to guide subsequent processing steps.
2.	Date Extraction:
o	text_extraction_ocr.py performs OCR using a fine-tuned PaddleOCR model (tuned_rec_det_model/) to extract text data from the images.
o	The PaddleOCR model was fine-tuned using a custom dataset of product images, achieving a character-level accuracy of 96% and a word-level accuracy of 94%.
o	Extracted text is analyzed and filtered to identify manufacturing and expiry dates using pattern-matching techniques.
3.	Freshness Evaluation:
o	Using the extracted dates, freshness_test.py calculates the product's freshness by comparing the expiry date with the current date.
o	The results indicate whether the product is fresh or expired.
4.	MRP Extraction:
o	extract_mrp.py uses a custom-trained model (mrp_extract_tained_model/) to identify and extract MRP and pricing details from product images.
o	The extracted pricing information is stored for further analysis or reporting.
________________________________________
Models Utilized
•	ResNet-50 Classification Model:
o	Model file: model_resnet50_6_classes.h5
o	Purpose: Classifies input images into one of six predefined categories.
•	MRP Extraction Model:
o	Location: mrp_extract_tained_model/
o	Purpose: Extracts MRP and pricing information from product images.
•	Fine-tuned PaddleOCR Model:
o	Location: tuned_rec_det_model/
o	Purpose: Fine-tuned OCR model for text recognition, achieving high accuracy for manufacturing and expiry dates.
________________________________________
Prerequisites
1.	Python Environment:
o	Python 3.8 or above is recommended.
2.	Dependencies:
o	Ensure the following libraries are installed:
	TensorFlow / Keras
	PyTorch
	OpenCV
	scikit-learn
	PaddleOCR
o	Install PaddleOCR:
pip install paddleocr
3.	Hardware Requirements:
o	A GPU is recommended for faster processing, especially for deep learning tasks.In our case we used NVIDIA RTX 4060
________________________________________
Installation
1.	Clone the repository:
2.	git clone <repository-url>
cd <repository-folder>
3.	Install dependencies (manually install if requirements.txt is not available):
pip install tensorflow keras torch torchvision opencv-python scikit-learn paddleocr
4.	Download or place pretrained models in their respective folders.
________________________________________
Usage Instructions
1.	Run the automated workflow script:
python automated_workflow.py
2.	Test specific features:
o	Object Classification:
python object_classification.py
o	Date Extraction:
python text_extraction_ocr.py
o	Freshness Testing:
python freshness_test.py
o	MRP Extraction:
python extract_mrp.py

________________________________________
Folder Structure
•	Scripts:
o	automated_workflow.py: Main script for the entire workflow.
o	extract_info.py: General information extraction.
o	extract_mrp.py: Extracts MRP details.
o	freshness_test.py: Calculates product freshness.
o	object_classification.py: Classifies objects into categories.
o	text_extraction_ocr.py: Performs OCR-based text extraction.
•	Models:
o	classification_model.pth: PyTorch model for classification.
o	model_resnet50_6_classes.h5: Keras/TF model for object classification.
o	tuned_rec_det_model/: Fine-tuned PaddleOCR models.
o	mrp_extract_tained_model/: Models for extracting pricing details.
•	Data:
o	product_data.xlsx: Metadata and related information about products.
o	test_images/: Sample test images.
o	Train/: Training dataset.
•	Logs:
o	extraction.log: Tracks extraction processes.
________________________________________
Limitations
•	The accuracy of OCR and extraction depends on image quality.
•	Models may require retraining or fine-tuning for additional categories or text formats.
________________________________________
License
This project is licensed under the WEACT TECH. See the @www.weacttech.com license file for more details.

For any clarification contact weacttech@gmail.com



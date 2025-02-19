from paddleocr import PaddleOCR

def ocr(image_path):
    det_model_dir = r"tuned_rec_det_model\best_accuracy_det"  
    rec_model_dir = r"tuned_rec_det_model\best_accuracy_rec"  

    ocr = PaddleOCR(
        det_model_dir=det_model_dir,
        rec_model_dir=rec_model_dir,
        use_gpu=True, 
        download_enabled=False,
        lang='en' 
    )

   
    result = ocr.ocr(image_path, det=True, rec=True)

  
    extracted_text = ""
    for line in result[0]: 
        extracted_text += f"{line[1][0]}\n"
    return extracted_text

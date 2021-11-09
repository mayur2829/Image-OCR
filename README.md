# Image-OCR
Aadhar Card, Pan Card, Voter ID, Driving License and Passport images OCR

Requirement: Extract data from Image using Tesseract OCR

1. Open sampleOCR.py file and add image path in respective image extraction model and excute.
eg:Aadhar card OCR 

extractor_aadhar = e.Aadhar_Info_Extractor()

extractor_aadhar.info_extractor("D:\\Mayur\\Aadhar_img.jpg")

2. All extratced data will be store in output_ocr.txt

3. Extracted content will be store in info1.json

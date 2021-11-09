import json
import cv2
import pytesseract
import regex as re
import io



# import easyocr
# READER = easyocr.Reader(['en'])
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class Pan_Info_Extractor:
    def __init__(self):
        # self.reader = reader
        self.extracted = {}

    def find_pan_number(self, ocr_text):
        #print(ocr_text)
        text_output = open('output_ocr.txt', 'w', encoding='utf-8')
        text_output.write(ocr_text)
        text_output.close()
        
        pan_number_patn = '[A-Z]{5}[0-9]{4}[A-Z]{1}'
        match = re.search(pan_number_patn, ocr_text)
        if match:
            return match.group()

    def find_name(self, ocr_text):
        """Function to find adhar name inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: name on the aadhar card
        """
        pan_name_patn =r'([A-Z]+)\s([A-Z]+)\s([A-Z]+)$|([A-Z]+)\s([A-Z]+)$' #r'^.{1}\b[A-Z]+\s[A-Z]'# or r'\b[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+$'
        split_ocr = ocr_text.split('\n\n')
        #print("Split data:",split_ocr)
        for ele in split_ocr:
            #print(ele)
            s1 = ele.split("\n")
            #print(s1[-1])
            match = re.search(pan_name_patn, s1[-1])
            if match:
                return match.group()
    
    def find_father_name(self, ocr_text):
        
        pan_father_patn = r'([A-Z]+)\s([A-Z]+)\s([A-Z]+)$|([A-Z]+)\s([A-Z]+)$'#r'([A-Z]+)\s+?'#r'\b[A-Z][a-z]+\s[A-Z][a-z]+$'
        split_ocr =  ocr_text.split('Signature')
        for ele in split_ocr:
            #print(ele)
            s1 = ele.split("\n\n")
            #print(s1)
            match = re.search(pan_father_patn,s1[3])
            if match:
                return match.group()
        
    
    def find_dob(self, ocr_text):
        """Function to find date of birth inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: Date of birth
        """
        dob_patn = '\d{2}+[-/]\d{2}+[-/]\d{4}+'
        #yob_patn = '[0-9]{4}'
        DateOfBirth = ''
        
        match = re.search(dob_patn, ocr_text)
        DateOfBirth = match.group()
 
            
        return DateOfBirth

    


    def info_extractor(self, front_image):
        """Function to extract information from the aadhaar card image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        json: Data extracted from Adhar photograph
        """
        self.fimage = front_image
        self.Name = 'NAN'
        self.Father = 'NAN'
        self.DateOB = 'NAN'
        self.Pan_No = 'NAN'
        # front image
        img = cv2.imread(self.fimage)
        # OCR_text = self.reader.readtext(img, detail=0,width_ths=0.9)
        ocr_text = pytesseract.image_to_string(img)
        

        self.Pan_No = self.find_pan_number(ocr_text)
        self.Name = self.find_name(ocr_text)
        #self.DateOB = self.find_dob(ocr_text)
        self.Father = self.find_father_name(ocr_text)
        self.DateOB = self.find_dob(ocr_text)

        
        self.extracted = {
        'Pan_number': self.Pan_No,
        'Name': self.Name,
        'Father_Name': self.Father,
        'DOB': self.DateOB
        }
        
        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str
            
        # return self.extracted
        with io.open('info1.json', 'w', encoding='utf-8') as outfile:
            data = json.dumps(self.extracted)
            outfile.write(to_unicode(data))
            

        

if __name__ == '__main__':
    ext = Pan_Info_Extractor()
    print(ext.info_extractor('front.jpeg'))
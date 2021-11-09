import json
import cv2
import pytesseract
import regex as re
import io



# import easyocr
# READER = easyocr.Reader(['en'])
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class Passport_Info_Extractor:
    def __init__(self):
        # self.reader = reader
        self.extracted = {}

    def find_passport_number(self, ocr_text):
        #print(ocr_text)
        text_output = open('output_ocr.txt', 'w', encoding='utf-8')
        text_output.write(ocr_text)
        text_output.close()
        """Function to find adhar number inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: 12 digit aadhaar number
        """
        passport_number_patn = '[A-Z]{1}[0-9]{7}'
        match = re.search(passport_number_patn, ocr_text)
        if match:
            return match.group()

    def find_name(self, ocr_text):
        """Function to find adhar name inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: name on the aadhar card
        """
        
        '''
        pass_name_patn = r'([A-Z]+)\s([A-Z]+)\s([A-Z]+)$|([A-Z]+)\s([A-Z]+)$|([A-Z]+)\s([A-Z]+)\s([A-Z]+)\s([A-Z]+)$|([A-Z]+)$'
        split_ocr = ocr_text.split('\n')
        #print("Split data:",split_ocr)
        for ele in split_ocr:
            print(ele)
            match = re.search(pass_name_patn, ele)
            if match:
                return match.group()
        '''
        with open('output_ocr.txt','r') as f:
            string =""
            for line in f:
                if "Given" in line or "Name" in line:
            #with open('output_ocr.txt','r') as f:
                
                #for line in f:
                    phrase = 'Given'
                    #newline_break =""
                    if phrase in line: 
                        for i in range(1):
                            address_data = f.readline()
                            string += address_data
                    
                        #print(string)    
                    return string
    
    def find_surname(self, ocr_text):
        '''
        pass_surname_patn = r'([A-Z]+)$|([A-Z]+)\s([A-Z]+)$'#r'([A-Z]+)\s+?'#r'\b[A-Z][a-z]+\s[A-Z][a-z]+$'
        split_ocr =  ocr_text.split(' ')
        for ele in split_ocr:
            print(ele)
        '''
            #s1 = ele.split(" ")
            #print(s1)
        '''
            match = re.search(pass_surname_patn,ele)
            if match:
                return match.group()
        '''
        with open('output_ocr.txt','r') as f:
            string =""
            for line in f:
                if "Surname" in line or "Suiname" in line:
            #with open('output_ocr.txt','r') as f:
                
                #for line in f:
                    phrase = 'Surname' or 'Suiname'
                    #newline_break =""
                    if phrase in line: 
                        for i in range(1):
                            address_data = f.readline()
                            string += address_data
                    
                        #print(string)    
                    return string

    def find_dob(self, ocr_text):
        """Function to find date of birth inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: Date of birth
        """
        dob_patn = '\d{2}+[-/]\d{2}+[-/]\d{4}+'
        
        DateOfBirth = ''
        
        match = re.search(dob_patn, ocr_text)
        DateOfBirth = match.group()
   
        return DateOfBirth

    def find_gender(self, ocr_text):
        """Function to find Gender inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: Gender
        """
        
        split_ocr = ocr_text.split('\n')
        #print("Split data:",split_ocr)
        #split_ocr = split_ocr.split(' ')
        #print("Split data:",split_ocr)
        text1=[]
        for i in split_ocr:
            text1+=i.split(" ")
            
        #print(text1)
        
        #print("Split data:",split_ocr)
        
        if 'M' in text1 or 'MALE' in text1 or "M." in text1:
            GENDER = 'Male'
        elif 'F' in text1 or 'FEMALE' in text1 or "F." in text1:
            GENDER = 'Female'
        else:
            GENDER = 'NAN'
        return GENDER

    def find_address(self, backimg):
        """Function to find address inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: address on the aadhaar card
        """
        pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        ocr_text = pytesseract.image_to_string(backimg, config=f'-l eng --psm 6 --oem 3 ')
        #print(ocr_text)
        
        
        #try:
            #address_start = text_output.find('Address')
            #address = ocr_text[address_start:]
        with open('output_ocr.txt','r') as f:
            string =""
            for line in f:
                if "Address" in line:
            #with open('output_ocr.txt','r') as f:
                
                #for line in f:
                    phrase = 'Address'
                    #newline_break =""
                    if phrase in line: 
                        for i in range(6):
                            address_data = f.readline()
                            string += address_data
                    
                        print(string)    
                    return string
                    '''
                    elif phrase1 in line:
                        for i in range(15):
                            line = f.readline()
                            #print(line)
                            line_strip = line.replace('\n', " ")
                            newline_break += line_strip
                            
                            data = " ".join(newline_break.split(" ", 3)[2:])
                            data1 = " ".join(data.split(" ", 3)[3:])
                            string += line
                     '''     
                        
                            
                  
                        
                        
                        #print(s)s = string.splitlines()[5:]
                        
                    
                    
        


    def info_extractor(self, front_image):
        """Function to extract information from the aadhaar card image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        json: Data extracted from Adhar photograph
        """
        self.fimage = front_image
        self.bimage = front_image
        self.Name = 'NAN'
        self.Surname = 'NAN'
        self.Gender = 'NAN'
        self.DateOB = 'NAN'
        self.Passport_No = 'NAN'
        self.Address = 'NAN'
        # front image
        img = cv2.imread(self.fimage)
        # OCR_text = self.reader.readtext(img, detail=0,width_ths=0.9)
        OCR_text = pytesseract.image_to_string(img)
        # print(OCR_text)

        self.Passport_No = self.find_passport_number(OCR_text)
        self.Name = self.find_name(OCR_text)
        self.Surname = self.find_surname(OCR_text)
        self.DateOB = self.find_dob(OCR_text)
        self.Gender = self.find_gender(OCR_text)

        # back image
        backimg = cv2.imread(self.bimage)
        backimg = cv2.cvtColor(backimg, cv2.COLOR_BGR2GRAY)
        self.Address = self.find_address(backimg)

        self.extracted = {
        'Passport_number': self.Passport_No,
        'Name': self.Name,
        'Surname': self.Surname,
        'Gender': self.Gender,
        'DOB': self.DateOB,
        'Address': self.Address
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
    ext = Passport_Info_Extractor()
    print(ext.info_extractor('front.jpeg'))
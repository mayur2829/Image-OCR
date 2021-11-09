import json
import cv2
import pytesseract
import regex as re
import io



# import easyocr
# READER = easyocr.Reader(['en'])
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class Aadhar_Info_Extractor:
    def __init__(self):
        # self.reader = reader
        self.extracted = {}

    def find_adhar_number(self, ocr_text):
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
        adhar_number_patn = '[0-9]{4}\s[0-9]{4}\s[0-9]{4}'
        match = re.search(adhar_number_patn, ocr_text)
        if match:
            return match.group()

    def find_name(self, ocr_text):
        """Function to find adhar name inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: name on the aadhar card
        """
        adhar_name_patn = r'\b[A-Z][a-z]+\s[A-Z][a-z]+$' or r'\b[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+$'
        split_ocr = ocr_text.split('\n')
        #print("Split data:",split_ocr)
        for ele in split_ocr:

            match = re.search(adhar_name_patn, ele)
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
        yob_patn = '[0-9]{4}'
        DateOfBirth = ''
        if 'DOB' in ocr_text:
            match = re.search(dob_patn, ocr_text)
            DateOfBirth = match.group()
        if 'Year of Birth' in ocr_text:
            match = re.search(yob_patn, ocr_text)
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
        
        if 'Male' in text1 or 'MALE' in text1:
            GENDER = 'Male'
        elif 'Female' in text1 or 'FEMALE' in text1:
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
                if "Address" in line or 'S/O' in line or 'D/O' in line or "To" in line:
            #with open('output_ocr.txt','r') as f:
                
                #for line in f:
                    phrase = 'Address'
                    phrase1 = 'To'
                    newline_break =""
                    if phrase in line: 
                        for i in range(6):
                            address_data = f.readline()
                            string += address_data
                    
                        print(string)    
                        return string
                    
                    elif phrase1 in line:
                        for i in range(15):
                            line = f.readline()
                            #print(line)
                            line_strip = line.replace('\n', " ")
                            newline_break += line_strip
                            
                            data = " ".join(newline_break.split(" ", 3)[2:])
                            data1 = " ".join(data.split(" ", 3)[3:])
                            string += line
                            
                        
                            
                        #print(line[1:4])
                        #print(string)
                        #print(newline_break)
                        print("This:",data1)

                        return data1
                        
                        
                        
                        #print(s)s = string.splitlines()[5:]
                        
                    
                    
            
        '''
        #pinpatn = r'[0-9]{6} '
        addresspatn = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+$'
        address_end = 0
        pinloc = re.search(addresspatn, address)
        
        if pinloc:
            address_end = pinloc.end() 
        else:
            print('Pin code not found in address')
            address = re.sub('\n', ' ', address[:address_end])
        address = address.split(':')[1]
    
        return address
        '''
        #except:
            
        '''
        address = re.sub('\n', ' ', ocr_text)
        #pinpatn = re.compile(r'[0-9]{6}')
        addresspatn = re.compile(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+$')
        pincode = re.search(addresspatn, address)
        # print(pincode.group())
        return pincode.group()
        '''


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
        self.Gender = 'NAN'
        self.DateOB = 'NAN'
        self.Aadhar_No = 'NAN'
        self.Address = 'NAN'
        # front image
        img = cv2.imread(self.fimage)
        # OCR_text = self.reader.readtext(img, detail=0,width_ths=0.9)
        OCR_text = pytesseract.image_to_string(img)
        # print(OCR_text)

        self.Aadhar_No = self.find_adhar_number(OCR_text)
        self.Name = self.find_name(OCR_text)
        self.DateOB = self.find_dob(OCR_text)
        self.Gender = self.find_gender(OCR_text)

        # back image
        backimg = cv2.imread(self.bimage)
        backimg = cv2.cvtColor(backimg, cv2.COLOR_BGR2GRAY)
        self.Address = self.find_address(backimg)

        self.extracted = {
        'Aadhar_number': self.Aadhar_No,
        'Name': self.Name,
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
    ext = Aadhar_Info_Extractor()
    print(ext.info_extractor('front.jpeg'))
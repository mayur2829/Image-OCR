import json
import cv2
import pytesseract
import regex as re
import io



# import easyocr
# READER = easyocr.Reader(['en'])
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class VoterID_Info_Extractor:
    def __init__(self):
        # self.reader = reader
        self.extracted = {}

    def find_voterid_number(self, ocr_text):
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
      
        voterid_number_patn = r'([A-Z]{3}[0-9]{7}+)'
            
        match = re.search(voterid_number_patn, ocr_text)
        print(match)
        if match:
            return match.group()
   

    def find_name(self, ocr_text):
        """Function to find adhar name inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: name on the aadhar card
        """
        with open('output_ocr.txt','r', encoding="utf8") as f:
            
            for line in f:
                if "Name" in line:
                    #with open('output_ocr.txt','r') as f:
        
                    voterid_name_patn = r'([A-Z]+)\s([A-Z]+)\s([A-Z]+)$|([A-Z]+)\s([A-Z]+)$|([A-Z]+)$'
                    split_ocr = line.split("Name")
                    #print(split_ocr)
                    #print("Split data:",split_ocr)
                    
                    string = split_ocr[1]
                
                    print(string)    
                    return string
                    
                    '''
                    for ele in split_ocr:
                        print(ele)
                        match = re.search(voterid_name_patn, ele)
                        if match:
                            return match.group()
                    '''
                    
    def find_father(self, ocr_text):
        """Function to find adhar name inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: name on the aadhar card
        """
        with open('output_ocr.txt','r', encoding="utf8") as f:
            
            for line in f:
                if "Father's" in line:
                    #with open('output_ocr.txt','r') as f:
        
                    voterid_name_patn = r'([A-Z]+)\s([A-Z]+)\s([A-Z]+)$|([A-Z]+)\s([A-Z]+)$|([A-Z]+)$'
                    split_ocr = line.split("Name")
                    #print(split_ocr)
                    #print("Split data:",split_ocr)
                    
                    string = split_ocr[1]
                
                    print(string)    
                    return string
                    
                    '''
                    for ele in split_ocr:
                        print(ele)
                        match = re.search(voterid_name_patn, ele)
                        if match:
                            return match.group()
                    '''

    def find_dob(self, ocr_text):
        """Function to find date of birth inside the image

        Args:
        ocr_text (list): text from the ocr

        Returns:
        str: Date of birth
        """
        with open('output_ocr.txt','r', encoding="utf8") as f:
            #string =""
            for line in f:
                
                    
                phrase = "DOB" or "Date of  Birth"
                dob_patn = '\d{2}+[-/]\d{2}+[-/]\d{4}+'
                split_ocr = line.split('\n')
                
                for ele in split_ocr:
                    #print(ele)
                    match = re.search(dob_patn, ele)
                    if match:
                        return match.group()
        '''
        DateOfBirth = ''
        
        if "DOB" in ocr_text or "Date of Birth" in ocr_text:
            match = re.search(dob_patn, ocr_text)
            DateOfBirth = match.group()
   
        return DateOfBirth
        '''
    

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
        with open('output_ocr.txt','r',encoding="utf8") as f:
            string =""
            for line in f:
                if "Address" in line or "Add" in line:
                    
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
        self.Father = 'NAN'
        self.DateOB = 'NAN'
        self.Voter_No = 'NAN'
        self.Address = 'NAN'
        # front image
        img = cv2.imread(self.fimage)
        # OCR_text = self.reader.readtext(img, detail=0,width_ths=0.9)
        OCR_text = pytesseract.image_to_string(img)
        # print(OCR_text)

        self.Voter_No = self.find_voterid_number(OCR_text)
        self.Name = self.find_name(OCR_text)
        self.Father = self.find_father(OCR_text)
        self.DateOB = self.find_dob(OCR_text)


        # back image
        backimg = cv2.imread(self.bimage)
        backimg = cv2.cvtColor(backimg, cv2.COLOR_BGR2GRAY)
        self.Address = self.find_address(backimg)

        self.extracted = {
        'VoterID_number': self.Voter_No,
        'Name': self.Name,
        'Father Name': self.Father,
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
    ext = VoterID_Info_Extractor()
    print(ext.info_extractor('front.jpeg'))
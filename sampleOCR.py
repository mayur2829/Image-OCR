import Aadhar_Extrator as e
import Pan_Extractor_new as pe
import Passport_Extractor as pae
import DL_Extractor as dl
import VoterID_Extractor as vi



# Aadhar card OCR 
# Add Image Path
extractor_aadhar = e.Aadhar_Info_Extractor()
extractor_aadhar.info_extractor("")

# Pan Card OCR
extractor_pan = pe.Pan_Info_Extractor()
extractor_pan.info_extractor("")

# Passport OCR
extractor_passport = pae.Passport_Info_Extractor()
extractor_passport.info_extractor("")

# Driving License OCR
extractor_driving_license = dl.Driving_License_Info_Extractor()
extractor_driving_license.info_extractor("")

# VoterID OCR
extractor_voterid = vi.VoterID_Info_Extractor()
extractor_voterid.info_extractor("")
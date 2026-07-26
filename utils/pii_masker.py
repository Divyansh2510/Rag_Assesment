from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

# Initialize Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# PERSON recognizer (labels, honorifics, form fields, and Indian surnames)
person_label_pattern = Pattern(
    name="person_label_pattern",
    regex=r"(?i)(?:(?:candidate|student|account\s*holder|holder|applicant|father|mother|parent|guardian|husband|spouse|beneficiary|customer|employee|member|user|insured|patient|client|examinee|examinant|nominee|person|individual|owner|payee|payer)(?:'s)?\s*(?:name|name\s*of\s*(?:the\s*)?(?:candidate|student|account\s*holder|holder|applicant|beneficiary|customer|employee|member|user|insured|patient|client|examinee|nominee|person|individual|owner|payee|payer))|name)\s*[:=\-]\s*([A-Za-z\.\'\-]{2,30}(?:\s+[A-Za-z\.\'\-]{2,30}){0,3})",
    score=1.0,
)
person_title_pattern = Pattern(
    name="person_title_pattern",
    regex=r"(?:(?:Mr|Mrs|Ms|Miss|Dr|Prof|Sh|Shri|Smt|Kumari|Md|Er|Adv|Shrimati)\.?\s+)([A-Z][a-zA-Z\.\'\-]*(?:\s+[A-Z][a-zA-Z\.\'\-]*){1,3})",
    score=1.0,
)
person_field_pattern = Pattern(
    name="person_field_pattern",
    regex=r"(?i)\b(?:candidate|student|account\s*holder|holder|applicant|beneficiary|customer|employee|member|user|insured|patient|client|examinee|examinant|nominee|payee|payer)\b\s*[:=\-]\s*([A-Za-z\.\'\-]{2,30}(?:\s+[A-Za-z\.\'\-]{2,30}){1,3})",
    score=1.0,
)
person_indian_pattern = Pattern(
    name="person_indian_pattern",
    regex=r"(?i)\b([A-Z][a-zA-Z\.\'\-]{2,20}\s+(?:Sharma|Verma|Patel|Kumar|Singh|Gupta|Devi|Mishra|Rao|Reddy|Chauhan|Yadav|Nair|Pillai|Iyer|Joshi|Mehta|Shah|Das|Roy|Ghosh|Dutta|Agarwal|Jain|Kaur|Bhat|Bhattacharya|Chatterjee|Banerjee|Sinha|Pandey|Saxena|Tiwari|Thakur|Pathak|Dubey|Chaudhary|Bhatt|Chavan|Gaikwad|Kulkarni|Deshmukh|Patil|Suryawanshi|More|Shinde|Pawar|Jadhav|Kale|Bhosale|Rathod|Rathore|Solanki|Parmar|Kapoor|Khanna|Chopra|Arora|Mehra|Soni|Malhotra|Sethi|Bansal|Mittal|Singhal|Goyal|Jindal|Mahajan|Ahuja|Bhatia|Dua|Gill|Lamba|Madan|Nangia|Oberoi|Puri|Sareen|Taneja|Vaidya|Wadhwa))\b",
    score=0.9,
)
person_recognizer = PatternRecognizer(
    supported_entity="PERSON",
    patterns=[person_label_pattern, person_title_pattern, person_field_pattern, person_indian_pattern],
    context=["name", "candidate", "student", "holder", "account holder", "applicant", "father", "mother", "beneficiary", "customer", "mr", "mrs", "ms", "dr", "shri", "smt"],
)

# ROLL_NUMBER recognizer
roll_number_pattern = Pattern(
    name="roll_number_pattern",
    regex=r"(?i)(?:(?:exam\s*|examination\s*)?roll\s*(?:no\.?|number|#|code)?|hall\s*ticket\s*(?:no\.?|number|#)?|seat\s*(?:no\.?|number|#)?|admit\s*card\s*(?:no\.?|number|id|#))\s*[:=\-]?\s*([A-Za-z0-9\-\/]*\d[A-Za-z0-9\-\/]{2,25})",
    score=1.0,
)
roll_standalone_pattern = Pattern(
    name="roll_standalone_pattern",
    regex=r"(?i)\b(?:roll\s*no|rollno|hall\s*ticket\s*no|seat\s*no)\b\s*[:=\-]?\s*([A-Za-z0-9\-\/]*\d[A-Za-z0-9\-\/]{2,25})",
    score=1.0,
)
roll_number_recognizer = PatternRecognizer(
    supported_entity="ROLL_NUMBER",
    patterns=[roll_number_pattern, roll_standalone_pattern],
    context=["roll", "roll no", "roll number", "hall ticket", "admit card", "exam", "seat"],
)

# ID_NUMBER recognizer (Application No, Registration No, Candidate ID, Center Code)
id_number_pattern1 = Pattern(
    name="id_number_pattern1",
    regex=r"(?i)(?:(?:application|app|registration|reg|enrollment|enrolment|enroll|candidate|student|exam|user|member|employee|customer|reference|ref|ticket|form|serial|sr|certificate|identity|id|unique|center|centre|school|college|university|batch|policy|loan)\s*(?:no\.?|number|id|#|code)|(?:id|id\s*no\.?|id\s*number))\s*[:=\-]?\s*([A-Za-z0-9\-\/]*\d[A-Za-z0-9\-\/]{2,30})",
    score=1.0,
)
id_number_pattern2 = Pattern(
    name="id_number_pattern2",
    regex=r"(?i)\b(?:[A-Za-z0-9_ -]{2,30}?\s+(?:ID|No\.?|Number|Code|Key|#))\s*[:=\-]\s*([A-Za-z0-9_/\-]*\d[A-Za-z0-9_/\-]{2,30})\b",
    score=0.8,
)
id_number_recognizer = PatternRecognizer(
    supported_entity="ID_NUMBER",
    patterns=[id_number_pattern1, id_number_pattern2],
    context=["id", "no", "number", "code", "application", "registration", "enrollment", "candidate", "student"],
)

# BANK_ACCOUNT recognizer (Bank Account No, A/c No, IBAN)
bank_account_pattern1 = Pattern(
    name="bank_account_pattern1",
    regex=r"(?i)(?:(?:bank|customer|beneficiary|savings|current)\s+)?(?:(?:account|acc|a/c|acct)\s*(?:no\.?|number|#|id|code)|iban|ac\s*no\.?)\s*[:=\-]?\s*([\d\-\s]{6,30}|[A-Za-z0-9\-\s]*\d[A-Za-z0-9\-\s]{5,30})",
    score=1.0,
)
bank_account_pattern2 = Pattern(
    name="bank_account_pattern2",
    regex=r"(?i)\b(?:a/c|acc|acct|account|iban)\b[\s:=-]*(\d{9,18})\b",
    score=0.9,
)
bank_account_recognizer = PatternRecognizer(
    supported_entity="BANK_ACCOUNT",
    patterns=[bank_account_pattern1, bank_account_pattern2],
    context=["account", "a/c", "acc", "bank", "iban", "savings", "current", "deposit", "holder"],
)

# FINANCIAL_CODE recognizer (IFSC, MICR, SWIFT, BIC, Routing, BSB)
ifsc_pattern = Pattern(
    name="ifsc_pattern",
    regex=r"(?i)(?:ifsc|ifsc\s*code)\s*[:=\-]?\s*([A-Z]{4}0[A-Z0-9]{6})",
    score=1.0,
)
micr_pattern = Pattern(
    name="micr_pattern",
    regex=r"(?i)(?:micr|micr\s*code)\s*[:=\-]?\s*(\d{9})",
    score=1.0,
)
swift_pattern = Pattern(
    name="swift_pattern",
    regex=r"(?i)(?:swift|bic|swift\s*code)\s*[:=\-]?\s*([A-Z]{6}[A-Z0-9]{2}(?:[A-Z0-9]{3})?)",
    score=1.0,
)
routing_pattern = Pattern(
    name="routing_pattern",
    regex=r"(?i)(?:cif\s*(?:no\.?|number|id)?|routing\s*(?:no\.?|number|#)?|sort\s*code|branch\s*code|bsb)\s*[:=\-]?\s*([A-Za-z0-9\-]{4,15})",
    score=1.0,
)
financial_code_recognizer = PatternRecognizer(
    supported_entity="FINANCIAL_CODE",
    patterns=[ifsc_pattern, micr_pattern, swift_pattern, routing_pattern],
    context=["ifsc", "micr", "swift", "bic", "routing", "cif", "branch", "code", "bank"],
)

# CREDIT_CARD recognizer (Card Numbers, CVV, PIN)
card_number_pattern = Pattern(
    name="card_number_pattern",
    regex=r"(?i)(?:(?:credit|debit|atm|master|visa|rupay)\s*)?card\s*(?:no\.?|number|#)?\s*[:=\-]?\s*(\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}|\d{15,19})",
    score=1.0,
)
card_standalone_pattern = Pattern(
    name="card_standalone_pattern",
    regex=r"\b(?:\d{4}[\s\-]){3}\d{4}\b",
    score=0.9,
)
cvv_pattern = Pattern(
    name="cvv_pattern",
    regex=r"(?i)(?:cvv|cvv2|cvc|security\s*code)\s*[:=\-]?\s*(\d{3,4})",
    score=1.0,
)
pin_pattern = Pattern(
    name="pin_pattern",
    regex=r"(?i)(?:atm\s*)?pin\s*(?:no\.?|number|code)?\s*[:=\-]?\s*(\d{4,6})",
    score=1.0,
)
card_recognizer = PatternRecognizer(
    supported_entity="CREDIT_CARD",
    patterns=[card_number_pattern, card_standalone_pattern, cvv_pattern, pin_pattern],
    context=["card", "credit", "debit", "cvv", "pin", "expiry", "atm", "visa", "mastercard"],
)

# NATIONAL_ID recognizer (Aadhaar, PAN Card, Passport, DL, Voter ID)
aadhaar_pattern1 = Pattern(
    name="aadhaar_pattern1",
    regex=r"(?i)(?:aadhaar|aadhar|uid|uidai)\s*(?:no\.?|number|#)?\s*[:=\-]?\s*(\d{4}[\s\-]?\d{4}[\s\-]?\d{4})",
    score=1.0,
)
aadhaar_pattern2 = Pattern(
    name="aadhaar_pattern2",
    regex=r"\b\d{4}\s\d{4}\s\d{4}\b",
    score=0.9,
)
pan_pattern1 = Pattern(
    name="pan_pattern1",
    regex=r"(?i)(?:pan|pan\s*card|pan\s*no\.?|permanent\s*account\s*number)\s*[:=\-]?\s*([A-Z]{5}[0-9]{4}[A-Z]{1})",
    score=1.0,
)
pan_pattern2 = Pattern(
    name="pan_pattern2",
    regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
    score=0.9,
)
passport_pattern = Pattern(
    name="passport_pattern",
    regex=r"(?i)(?:passport\s*(?:no\.?|number|#)?)\s*[:=\-]?\s*([A-PR-WYa-pr-wy][1-9]\d\s?\d{4}[1-9]|[A-Z0-9]{6,9})",
    score=0.9,
)
govt_id_pattern = Pattern(
    name="govt_id_pattern",
    regex=r"(?i)(?:dl|driving\s*licen[cs]e|voter\s*id|epic|gstin|gst|ssn|uan|ration\s*card)\s*(?:no\.?|number|#)?\s*[:=\-]?\s*([A-Za-z0-9\-\/]{6,18})",
    score=1.0,
)
national_id_recognizer = PatternRecognizer(
    supported_entity="NATIONAL_ID",
    patterns=[aadhaar_pattern1, aadhaar_pattern2, pan_pattern1, pan_pattern2, passport_pattern, govt_id_pattern],
    context=["aadhaar", "aadhar", "pan", "passport", "dl", "driving license", "voter id", "uid", "tax", "gstin"],
)

# DATE_OF_BIRTH & DEMOGRAPHICS recognizer (DOB, Age, Gender, Category)
dob_pattern = Pattern(
    name="dob_pattern",
    regex=r"(?i)(?:dob|date\s*of\s*birth|birth\s*date)\s*[:=\-]?\s*([0-9]{1,2}[/\-\.][0-9]{1,2}[/\-\.][0-9]{2,4}|[0-9]{4}[/\-\.][0-9]{1,2}[/\-\.][0-9]{1,2}|[0-3]?\d\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})",
    score=1.0,
)
dob_recognizer = PatternRecognizer(
    supported_entity="DATE_OF_BIRTH",
    patterns=[dob_pattern],
    context=["dob", "birth", "date of birth", "born"],
)
age_pattern = Pattern(
    name="age_pattern",
    regex=r"(?i)\b(?:age)\s*[:=\-]?\s*(\d{1,3}\s*(?:years?|yrs?|Y)?)\b",
    score=1.0,
)
gender_pattern = Pattern(
    name="gender_pattern",
    regex=r"(?i)(?:gender|sex)\s*[:=\-]?\s*(Male|Female|Other|Transgender|M|F)\b",
    score=1.0,
)
category_pattern = Pattern(
    name="category_pattern",
    regex=r"(?i)(?:category|caste|community)\s*[:=\-]?\s*(General|GEN|OBC|SC|ST|EWS|PWD|PH)\b",
    score=1.0,
)
demographic_recognizer = PatternRecognizer(
    supported_entity="DEMOGRAPHIC",
    patterns=[age_pattern, gender_pattern, category_pattern],
    context=["age", "gender", "sex", "category", "caste"],
)

# CONTACT DETAILS recognizer (Phone, Email, Address)
phone_pattern1 = Pattern(
    name="phone_pattern1",
    regex=r"(?i)(?:(?:phone|mobile|tel|telephone|contact|ph|cell|whatsapp|mob)\s*(?:no\.?|number|#)?)\s*[:=\-]?\s*(\+?\d[\d\s\-]{8,15}\d)",
    score=1.0,
)
phone_pattern2 = Pattern(
    name="phone_pattern2",
    regex=r"\b(?:\+?91[\s\-]?)?[6-9]\d{9}\b",
    score=0.9,
)
phone_recognizer = PatternRecognizer(
    supported_entity="PHONE_NUMBER",
    patterns=[phone_pattern1, phone_pattern2],
    context=["phone", "mobile", "tel", "contact", "call", "sms", "whatsapp"],
)
email_pattern = Pattern(
    name="email_pattern",
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    score=1.0,
)
email_recognizer = PatternRecognizer(
    supported_entity="EMAIL_ADDRESS",
    patterns=[email_pattern],
    context=["email", "mail", "e-mail", "contact"],
)
address_pattern1 = Pattern(
    name="address_pattern1",
    regex=r"(?i)(?:(?:permanent|current|residence|correspondence|residential|office|postal|mailing|home)?\s*address|addr)\s*[:=\-]?\s*([^\n\r]{5,120})",
    score=1.0,
)
address_pattern2 = Pattern(
    name="address_pattern2",
    regex=r"(?i)(?:pin\s*code|pincode|postal\s*code|zip\s*code|zip)\s*[:=\-]?\s*(\d{6}|\d{5}(?:-\d{4})?)",
    score=1.0,
)
address_recognizer = PatternRecognizer(
    supported_entity="ADDRESS",
    patterns=[address_pattern1, address_pattern2],
    context=["address", "city", "pincode", "zip", "state", "street", "road"],
)

# AUTH & CREDENTIALS recognizer (PASSWORD, CLIENT_ID)
password_pattern = Pattern(
    name="password_pattern",
    regex=r"(?i)(?:password|pwd|pass|secret|token)\s*(?:[:=]|is|-)\s*([A-Za-z0-9@#$%^&+=_!.-]+)",
    score=1.0,
)
password_recognizer = PatternRecognizer(supported_entity="PASSWORD", patterns=[password_pattern])

client_id_pattern = Pattern(
    name="client_id_pattern",
    regex=r"(?i)(?:client id|client_id|cid|tenant_id|tenant\s*id)\s*(?:[:=]|is|-)\s*([A-Za-z0-9_-]+)",
    score=1.0,
)
client_id_recognizer = PatternRecognizer(supported_entity="CLIENT_ID", patterns=[client_id_pattern])

# Register all custom recognizers with AnalyzerEngine
analyzer.registry.add_recognizer(person_recognizer)
analyzer.registry.add_recognizer(roll_number_recognizer)
analyzer.registry.add_recognizer(bank_account_recognizer)
analyzer.registry.add_recognizer(financial_code_recognizer)
analyzer.registry.add_recognizer(card_recognizer)
analyzer.registry.add_recognizer(national_id_recognizer)
analyzer.registry.add_recognizer(id_number_recognizer)
analyzer.registry.add_recognizer(dob_recognizer)
analyzer.registry.add_recognizer(demographic_recognizer)
analyzer.registry.add_recognizer(phone_recognizer)
analyzer.registry.add_recognizer(email_recognizer)
analyzer.registry.add_recognizer(address_recognizer)
analyzer.registry.add_recognizer(password_recognizer)
analyzer.registry.add_recognizer(client_id_recognizer)

def mask_text(text: str) -> str:
    """Mask sensitive information in text using Presidio."""
    results = analyzer.analyze(text=text, language="en")
    anonymized_result = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized_result.text

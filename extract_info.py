import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dateparser
from spellchecker import SpellChecker
import spacy


try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

date_pattern = r"""
    (                          
        \b\d{4}[-./]\d{1,2}[-./]\d{1,2}\b
    ) |
    (                          
        \b\d{1,2}[-./]\d{1,2}[-./]\d{2,4}\b
    ) |
    (                       
        \b\d{1,2}\s+
        (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|
        January|February|March|April|May|June|July|August|
        September|October|November|December)\s+
        \d{2,4}\b
    ) |
    (                       
        (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|
        January|February|March|April|May|June|July|August|
        September|October|November|December)\s+
        \d{1,2},?\s+\d{2,4}\b
    ) |
    (                       
        (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|
        JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|
        January|February|March|April|May|June|July|August|
        September|October|November|December)
        \d{4}\b
    )
"""

quantity_pattern = r"\b(\d+(?:\.\d+)?)\s*(g|grams?|kilograms?|kg|liters?|litres?|l|ml|pieces?|packs?|pack of|sachets?|cans?|oz|lbs?)\b"

month_map = {
    "jan": "Jan", "feb": "Feb", "mar": "Mar", "apr": "Apr", "may": "May", "jun": "Jun",
    "jul": "Jul", "aug": "Aug", "sep": "Sep", "oct": "Oct", "nov": "Nov", "dec": "Dec",
    "january": "January", "february": "February", "march": "March", "april": "April",
    "june": "June", "july": "July", "august": "August", "september": "September",
    "october": "October", "november": "November", "december": "December"
}

def preprocess_ocr_text(text):
    """Clean and normalize OCR text."""
    replacements = {
        'O': '0', 
        'o': '0',
        'I': '1', 
        'Z': '2',
        '@': 'a',
        '#': '',
        '$': 'S',
        '%': '',
        '^': '',
        '&': '',
        '*': '',
        '(': '',
        ')': '',
        '!': '',
        '?': '',
        '/': '-',  
        '\\': '-',  
        '|': '-',  
        '': '',
        '~': '',
        '{': '',
        '}': '',
        '[': '',
        ']': '',
        ':': '',
        ';': '',
        "'": '',
        '"': '',
        '<': '',
        '>': '',
        '+': '',
        '=': '',
        '_': ' ',
    }
    
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    
    text = re.sub(r'\bl\b', '1', text)
    
    text = re.sub(r'[^\w\s/.,\-]', ' ', text)
    
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def correct_spelling(text):
    """Correct spelling mistakes in OCR text."""
    spell = SpellChecker()
    words = text.split()
    corrected_words = []
    for word in words:
        word_lower = word.lower()
        if word_lower in month_map:
            corrected_words.append(month_map[word_lower])
            continue
        if spell.unknown([word]):
            corrected_word = spell.correction(word)
            if corrected_word:
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)
    return ' '.join(corrected_words)

def normalize_units(quantity, unit):
    """Normalize different units to a standard format: 'g' for solids and 'ml' for liquids."""
    unit = unit.lower()
    if unit in ['grams', 'g', 'gram']:
        normalized_unit = 'g'
    elif unit in ['kilograms', 'kilogram', 'kg']:
        normalized_unit = 'g'
        quantity = str(int(quantity) * 1000)  
    elif unit in ['liters', 'litre', 'l']:
        normalized_unit = 'ml'
        quantity = str(int(quantity) * 1000) 
    elif unit in ['milliliters', 'millilitre', 'ml']:
        normalized_unit = 'ml'
    elif unit in ['pieces', 'piece']:
        normalized_unit = 'pcs'
    elif unit in ['pack of']:
        normalized_unit = 'pack'
    elif unit in ['sachets', 'sachet']:
        normalized_unit = 'sachet'
    elif unit in ['cans', 'can']:
        normalized_unit = 'can'
    else:
        normalized_unit = unit 
    return quantity, normalized_unit

def is_valid_date(date_obj):
    """Check if a date is valid and not in the future."""
    if date_obj.year < 1900 or date_obj.year > 2030:
        return False
    return True

def calculate_expiry_date(mfg_date: datetime, duration: str):
    """Calculate the expiry date based on the manufacturing date and duration."""
    match = re.match(r'(\d+)\s*(years?|months?|weeks?|days?)', duration, re.IGNORECASE)
    if not match:
        return None

    amount, unit = match.groups()
    amount = int(amount)

    if 'year' in unit.lower():
        expiry_date = mfg_date + relativedelta(years=amount)
    elif 'month' in unit.lower():
        expiry_date = mfg_date + relativedelta(months=amount)
    elif 'week' in unit.lower():
        expiry_date = mfg_date + relativedelta(weeks=amount)
    elif 'day' in unit.lower():
        expiry_date = mfg_date + relativedelta(days=amount)
    else:
        return None

    return expiry_date

def extract_dates(text):
    """Extract dates from text and skip invalid ones."""

    matches = re.findall(date_pattern, text, re.VERBOSE | re.IGNORECASE)
    dates = []
    for match in matches:
        
        match = [m for m in match if m]
        
        if not match: 
            continue
        
        if len(match) == 1:
            date_str = match[0]
        elif len(match) == 3:
            date_str = ' '.join(match)
        elif len(match) == 2: 
            date_str = ' '.join(match)
        elif len(match) == 4:
            date_str = f"{match[0]}-{match[1]}-{match[2]}"
        else:
            continue
        
        parsed_date = dateparser.parse(date_str, settings={'PREFER_DAY_OF_MONTH': 'first'})
        
        if parsed_date and is_valid_date(parsed_date):
            if parsed_date.year == 0 or any(part == "00" for part in match):
                continue
            dates.append(parsed_date)
    

    return dates

def extract_quantities(text):
    """Extract and normalize multiple quantities and units."""
    quantities = re.findall(quantity_pattern, text, re.IGNORECASE)
   
    normalized_quantities = []
    for qty, unit in quantities:
        qty_norm, unit_norm = normalize_units(qty, unit)
        normalized_quantities.append((qty_norm, unit_norm))
    normalized_quantities=list(set(normalized_quantities))
    return max(normalized_quantities, key=lambda x: float(x[0]))

def extract_info_from_ocr(text):
    """Extract manufacturing date, expiry date, MRP, and quantities from OCR text."""
    try:
        text = preprocess_ocr_text(text)
        
      
        
        quantities = extract_quantities(text)
        
        dates = extract_dates(text)
        
        mfg_date = None
        expiry_date = None
        
        best_before_match = re.search(r'best before\s+(\d+\s*\w+)', text, re.IGNORECASE)
        if best_before_match and dates:
            duration_str = best_before_match.group(1).strip()
            mfg_date = min(dates)
            expiry_date = calculate_expiry_date(mfg_date, duration_str)
            dates = [date for date in dates if date != mfg_date]
        else:
            expiry_phrases = ['expiry date', 'expiry on', 'best before']
            for phrase in expiry_phrases:
                pattern = fr'{phrase}\s+([\dA-Za-z\s/.,-]+)'
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    expiry_date_str = match.group(1).strip()
                    expiry_date = dateparser.parse(expiry_date_str)
                    if expiry_date and is_valid_date(expiry_date):
                        dates = [date for date in dates if date != expiry_date]
                        break
            
            if dates:
                if len(dates) >= 2 and not mfg_date and not expiry_date:
                    mfg_date = dates[0]
                    expiry_date = dates[1]
                elif len(dates) == 1 and not mfg_date and not expiry_date:
                    mfg_date = dates[0]
        
        shelf_life = None
        if expiry_date:
            current_date = datetime.now()
            total_days = (expiry_date - current_date).days
            if total_days < 0:
                shelf_life = "expired"
            else:
                years, remaining_days = divmod(total_days, 365)
                months, days = divmod(remaining_days, 30)
                shelf_life = {"years": years, "months": months, "days": days}
        
        extracted_info = {
            "mfg_date": mfg_date.strftime("%d/%m/%Y") if mfg_date else None,
            "expiry_date": expiry_date.strftime("%d/%m/%Y") if expiry_date else None,
            "shelf_life": shelf_life,
            "quantities": quantities
        }
        
        return extracted_info
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None
def extract_info(text):
    result = extract_info_from_ocr(text)
    return result



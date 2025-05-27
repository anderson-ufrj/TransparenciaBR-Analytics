"""
Helper functions for data formatting, validation, and utilities.
"""

import re
from datetime import datetime, date, timedelta
from typing import Union, Optional, List, Any, Tuple
from decimal import Decimal, ROUND_HALF_UP
import unicodedata


def format_currency(value: Union[float, int, str, Decimal], 
                   symbol: str = "R$",
                   decimal_places: int = 2) -> str:
    """
    Format value as Brazilian currency.
    
    Args:
        value: Numeric value to format
        symbol: Currency symbol
        decimal_places: Number of decimal places
        
    Returns:
        Formatted currency string
    """
    try:
        # Convert to Decimal for precise handling
        if isinstance(value, str):
            value = value.replace(',', '.')
        
        decimal_value = Decimal(str(value))
        
        # Round to specified decimal places
        quantized = decimal_value.quantize(
            Decimal(f"0.{'0' * decimal_places}"),
            rounding=ROUND_HALF_UP
        )
        
        # Format with thousand separators
        parts = str(quantized).split('.')
        integer_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else '00'
        
        # Add thousand separators
        integer_formatted = ''
        for i, digit in enumerate(reversed(integer_part)):
            if i > 0 and i % 3 == 0:
                integer_formatted = '.' + integer_formatted
            integer_formatted = digit + integer_formatted
        
        # Combine parts
        formatted = f"{integer_formatted},{decimal_part.ljust(decimal_places, '0')}"
        
        return f"{symbol} {formatted}"
    
    except (ValueError, TypeError, ArithmeticError):
        return f"{symbol} 0,00"


def format_date(date_value: Union[str, datetime, date],
                output_format: str = "%d/%m/%Y") -> str:
    """
    Format date in Brazilian format.
    
    Args:
        date_value: Date to format
        output_format: Desired output format
        
    Returns:
        Formatted date string
    """
    try:
        if isinstance(date_value, str):
            # Try to parse ISO format first
            if 'T' in date_value:
                dt = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            else:
                # Try common date formats
                for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]:
                    try:
                        dt = datetime.strptime(date_value, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return date_value  # Return as-is if parsing fails
        elif isinstance(date_value, datetime):
            dt = date_value
        elif isinstance(date_value, date):
            dt = datetime.combine(date_value, datetime.min.time())
        else:
            return str(date_value)
        
        return dt.strftime(output_format)
    
    except Exception:
        return str(date_value)


def format_cpf_cnpj(document: str) -> str:
    """
    Format CPF or CNPJ with proper punctuation.
    
    Args:
        document: CPF or CNPJ number
        
    Returns:
        Formatted document
    """
    # Remove non-numeric characters
    clean_doc = re.sub(r'\D', '', str(document))
    
    if len(clean_doc) == 11:  # CPF
        return f"{clean_doc[:3]}.{clean_doc[3:6]}.{clean_doc[6:9]}-{clean_doc[9:]}"
    elif len(clean_doc) == 14:  # CNPJ
        return f"{clean_doc[:2]}.{clean_doc[2:5]}.{clean_doc[5:8]}/{clean_doc[8:12]}-{clean_doc[12:]}"
    else:
        return document


def validate_cpf(cpf: str) -> bool:
    """
    Validate Brazilian CPF number.
    
    Args:
        cpf: CPF number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Remove non-numeric characters
    cpf = re.sub(r'\D', '', str(cpf))
    
    # Check length
    if len(cpf) != 11:
        return False
    
    # Check for known invalid CPFs
    if cpf in ['00000000000', '11111111111', '22222222222', '33333333333',
               '44444444444', '55555555555', '66666666666', '77777777777',
               '88888888888', '99999999999']:
        return False
    
    # Calculate first digit
    sum_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit_1 = (sum_1 * 10) % 11
    if digit_1 == 10:
        digit_1 = 0
    
    if digit_1 != int(cpf[9]):
        return False
    
    # Calculate second digit
    sum_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit_2 = (sum_2 * 10) % 11
    if digit_2 == 10:
        digit_2 = 0
    
    return digit_2 == int(cpf[10])


def validate_cnpj(cnpj: str) -> bool:
    """
    Validate Brazilian CNPJ number.
    
    Args:
        cnpj: CNPJ number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Remove non-numeric characters
    cnpj = re.sub(r'\D', '', str(cnpj))
    
    # Check length
    if len(cnpj) != 14:
        return False
    
    # Check for known invalid CNPJs
    if cnpj == cnpj[0] * 14:
        return False
    
    # Validate first digit
    weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_1 = sum(int(cnpj[i]) * weights_1[i] for i in range(12))
    digit_1 = 11 - (sum_1 % 11)
    if digit_1 >= 10:
        digit_1 = 0
    
    if digit_1 != int(cnpj[12]):
        return False
    
    # Validate second digit
    weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_2 = sum(int(cnpj[i]) * weights_2[i] for i in range(13))
    digit_2 = 11 - (sum_2 % 11)
    if digit_2 >= 10:
        digit_2 = 0
    
    return digit_2 == int(cnpj[13])


def clean_text(text: str, 
               remove_accents: bool = False,
               lowercase: bool = False) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Text to clean
        remove_accents: Whether to remove accents
        lowercase: Whether to convert to lowercase
        
    Returns:
        Cleaned text
    """
    if not isinstance(text, str):
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove accents if requested
    if remove_accents:
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
    
    # Convert to lowercase if requested
    if lowercase:
        text = text.lower()
    
    return text.strip()


def parse_brazilian_date(date_str: str) -> Optional[datetime]:
    """
    Parse date in Brazilian format.
    
    Args:
        date_str: Date string to parse
        
    Returns:
        Parsed datetime or None
    """
    if not date_str:
        return None
    
    # Common Brazilian date formats
    formats = [
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%d-%m-%Y",
        "%d-%m-%Y %H:%M:%S",
        "%d.%m.%Y",
        "%d de %B de %Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    # Try ISO format as fallback
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        return None


def calculate_date_range(start_date: Union[str, datetime],
                        end_date: Union[str, datetime]) -> int:
    """
    Calculate number of days between two dates.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Number of days
    """
    if isinstance(start_date, str):
        start_date = parse_brazilian_date(start_date) or datetime.now()
    
    if isinstance(end_date, str):
        end_date = parse_brazilian_date(end_date) or datetime.now()
    
    return abs((end_date - start_date).days)


def get_fiscal_year(date_value: Union[str, datetime, date]) -> int:
    """
    Get Brazilian fiscal year for a given date.
    
    Args:
        date_value: Date to check
        
    Returns:
        Fiscal year
    """
    if isinstance(date_value, str):
        date_value = parse_brazilian_date(date_value)
    
    if isinstance(date_value, date) and not isinstance(date_value, datetime):
        date_value = datetime.combine(date_value, datetime.min.time())
    
    if date_value:
        return date_value.year
    else:
        return datetime.now().year


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.
    
    Args:
        lst: List to split
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize filename for safe file system usage.
    
    Args:
        filename: Original filename
        max_length: Maximum filename length
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove control characters
    filename = ''.join(char for char in filename if ord(char) >= 32)
    
    # Limit length
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_length = max_length - len(ext) - 1 if ext else max_length
        filename = name[:max_name_length] + ('.' + ext if ext else '')
    
    return filename.strip()


def calculate_percentage_change(old_value: Union[float, int],
                               new_value: Union[float, int]) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        old_value: Original value
        new_value: New value
        
    Returns:
        Percentage change
    """
    if old_value == 0:
        return 100.0 if new_value > 0 else 0.0
    
    return ((new_value - old_value) / old_value) * 100


def extract_year_month(date_value: Union[str, datetime, date]) -> Tuple[int, int]:
    """
    Extract year and month from date.
    
    Args:
        date_value: Date value
        
    Returns:
        Tuple of (year, month)
    """
    if isinstance(date_value, str):
        date_value = parse_brazilian_date(date_value)
    
    if isinstance(date_value, (datetime, date)):
        return date_value.year, date_value.month
    
    return datetime.now().year, datetime.now().month
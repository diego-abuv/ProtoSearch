# backend/utils/date_parser.py
import datetime

def parse_date_ddmmyyyy(date_str: str) -> datetime.datetime:
    """
    Parses a date string in 'DD/MM/AAAA' format to a datetime object.
    Raises ValueError if the format is invalid.
    """
    try:
        return datetime.datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        raise ValueError("Formato de data inválido. Use DD/MM/AAAA.")

def format_date_m_d_y(date_obj: datetime.datetime) -> str:
    """
    Formats a datetime object to 'MM/DD/YY' string.
    Useful for tkcalendar if it expects this format.
    """
    return date_obj.strftime('%m/%d/%y')

def format_date_d_m_yyyy(date_obj: datetime.datetime) -> str:
    """
    Formats a datetime object to 'DD/MM/YYYY' string.
    """
    return date_obj.strftime('%d/%m/%Y')
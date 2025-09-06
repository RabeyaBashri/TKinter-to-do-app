from datetime import datetime
from typing import Optional, Union

import sys
sys.path.append(r"E:\python\TKinter-to-do-app\utilities")
from app_state import AppState
from enums import ErrorHandler

state = AppState.get_instance()

class ConversionHelper :

    @staticmethod
    def convert_to_datetime(dt_str: Optional[str]) -> Optional[datetime]:
       
        if not dt_str:

            return None
        
        for format in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):

            try:

                return datetime.strptime(dt_str, format)
            
            except Exception as e:

                state.log_error(f"{ErrorHandler.ConversionHelperConvertToDatetimeError.value} {e}")
            
        return None

    def none_if_placeholder(value: str, placeholder: str) -> str | None:

        return None if value == placeholder else value
    
    def to_datetime(value: Union[str, datetime, None], fmt: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
       
        if isinstance(value, datetime):

            return value
        
        if isinstance(value, str) and value.strip():

            return datetime.strptime(value.strip(), fmt)
        
        return None

    def to_db_string(value: Union[str, datetime, None], fmt: str = "%Y-%m-%d %H:%M") -> Optional[str]:
        
        if isinstance(value, datetime):

            return value.strftime(fmt) if value else None
        
        if isinstance(value, str) and value.strip():

            return datetime.strptime(value.strip(), fmt)
        
        return None
    

    def to_db_timestamp(value: Optional[datetime]) -> Optional[str]:
       
        return value.strftime("%Y-%m-%d %H:%M:%S") if value else None
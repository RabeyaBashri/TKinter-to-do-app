from typing import  Optional

import sys
sys.path.append(r"E:\python\TKinter-to-do-app\utilities")
from enums import AppStatus

class AppState:

    _instance: Optional["AppState"] = None

    def __init__(self) -> None:

        if not hasattr(self, "errors"):
            self.errors: list[str] = []

        if not hasattr(self, "status"):
            self.status : str = AppStatus.OK

    @classmethod
    def get_instance(cls) -> "AppState":

        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def log_error(self, error_msg:str) -> None:

        self.status = AppStatus.Error
        self.errors.append(error_msg)

    def get_errors(self) -> list[str]:

        return self.errors

    def clear_errors(self) -> None:

        self.status = AppStatus.OK
        self.errors.clear()
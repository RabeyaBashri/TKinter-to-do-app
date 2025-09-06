import sqlite3
import json
from typing import  Optional
import os

import sys
sys.path.append(r"E:\python\TKinter-to-do-app\utilities")
from enums import ErrorHandler
from app_state import AppState

state = AppState.get_instance()

class SQLiteHelper:

    _instance = None

    def __init__(self) -> None:
        
        try:
        
            if not hasattr(self, "conn"):

                # with open("E:\python\TKinter-to-do-app\config.json") as f:
                #     cfg = json.load(f)

                base_dir = os.path.dirname(os.path.abspath(__file__))  # this file location
                base_dir = os.path.dirname(base_dir)  
                self.db_path = os.path.join(base_dir, "tkinter_to_do_app.db")

                #self.db_name: str = cfg.get("DB_NAME", "tkinter_to_do_app.db")
                #self.conn: sqlite3.Connection = sqlite3.connect(self.db_name, check_same_thread=False)
                self.conn: sqlite3.Connection = sqlite3.connect(self.db_path, check_same_thread=False)
                self.conn.row_factory = sqlite3.Row

        except Exception as e:

            state.log_error(f"{ErrorHandler.DB_Initialization.value} {e}")
    
    @classmethod
    def get_instance(cls) -> "SQLiteHelper":
       
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def execute_non_query(self, sql : str, params: Optional[list[any]]  = None ) -> bool :
       
        try:

            self.create_cursor(sql,params)
            self.conn.commit()
            
            return True
        
        except Exception as e:

            state.log_error(f"{ErrorHandler.DB_ExecuteNonQueryError.value} {e}")

            return False
    
    def execute_non_query_and_scalar(self, sql : str, params: Optional[list[any]]  = None ) -> Optional[int] :
       
        try:
           
            self.execute_non_query(sql,params)

            return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        except Exception as e:

            state.log_error(f"{ErrorHandler.DB_ExecuteNonQueryAndScalarError.value} {e}")

            return None
    
    def execute_query_and_list(self, sql : str, params: Optional[list[any]]  = None ) -> list[sqlite3.Row]:
        
        try:
            
            return self.create_cursor(sql,params).fetchall()
        
        except Exception as e:

            state.log_error(f"{ErrorHandler.DB_ExecuteQueryAndListError.value} {e}")

            return []
        
    def execute_query_and_Row(self, sql : str, params: Optional[list[any]]  = None ) -> Optional[sqlite3.Row]:
        
        try:
            
            return self.create_cursor(sql,params).fetchone()
        
        except Exception as e:

            state.log_error(f"{ErrorHandler.DB_ExecuteQueryAndRowError.value} {e}")

            return None
           
    def create_cursor(self, sql : str, params: Optional[list[any]]  = None) -> Optional[sqlite3.Cursor]:
         
         try :

            cur : sqlite3.Cursor = self.conn.cursor()
            cur.execute(sql, params or [])

            return cur
         
         except Exception as e :
             
             state.log_error(f"{ErrorHandler.DB_CreateCursorError.value} {e}")
             return None

from typing import  Optional
from datetime import datetime

import sys
sys.path.append(r"E:\python\TKinter-to-do-app\utilities")
sys.path.append(r"E:\python\TKinter-to-do-app\models")
from enums import TaskCategory,TaskPriority, TaskCompleted, ErrorHandler
from app_state import AppState
from task import Task
from sqlite_helper import SQLiteHelper
from conversion_helper import ConversionHelper

state = AppState.get_instance()
db_helper = SQLiteHelper.get_instance()

class TaskDataHelper :

    create_table_query : str = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'Medium',
                deadline TEXT,
                reminder TEXT,
                category TEXT DEFAULT 'General',
                tags TEXT,
                completed TEXT DEFAULT 'No',
                created_at TEXT,
                updated_at TEXT
            )
            """
        
    insert_query : str = """
            INSERT INTO tasks (title, description, priority, deadline, reminder, category, tags, completed, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
    update_query : str = """
            UPDATE tasks SET title=?, description=?, priority=?, deadline=?, reminder=?,
                             category=?, tags=?, completed=?, updated_at=?
            WHERE id=?
            """
    mark_completed_query : str = """
            UPDATE tasks SET completed=?, updated_at=?
            WHERE id=?
            """
    delete_query : str = "DELETE FROM tasks WHERE id=?"

    delete_all_query : str = "DELETE FROM tasks"

    get_query : str = "SELECT * FROM tasks WHERE id=?"

    get_all_query : str = "SELECT * FROM tasks ORDER BY deadline IS NULL, deadline"

    get_reminders_query : str = "SELECT * FROM tasks WHERE reminder IS NOT NULL"
   
    def __init__(self) -> None:
        pass
        

    def create_table(self) -> bool :

        try:
            
            return db_helper.execute_non_query(self.create_table_query)

        except Exception as e :

            state.log_error(f"{ErrorHandler.DB_CreateTableError.value} {e}")
            return False
    
    def insert(self, task: Task) -> Optional[int] :
        
        try:
            if self.create_table() :

                params : list[any] = [task.title, 
                                    task.description, 
                                    task.priority if task.priority else TaskPriority.Medium.value, 
                                    ConversionHelper.to_db_string(task.deadline),
                                    ConversionHelper.to_db_string(task.reminder),
                                    task.category if task.category else TaskCategory.General.value, 
                                    task.tags, 
                                    task.completed if task.completed else TaskCompleted.No.value,
                                    ConversionHelper.to_db_timestamp(task.created_at),
                                    ConversionHelper.to_db_timestamp(task.updated_at)]
                
                return db_helper.execute_non_query_and_scalar(self.insert_query, params)

        except Exception as e :

            state.log_error(f"{ErrorHandler.DB_InsertError.value} {e}")
            return None
        
    def update(self, task: Task) -> bool :

        try:

            params = [task.title, 
                      task.description, 
                      task.priority if task.priority else TaskPriority.Medium.value, 
                      ConversionHelper.to_db_string(task.deadline),
                      ConversionHelper.to_db_string(task.reminder),
                      task.category  if task.category else TaskCategory.General.value, 
                      task.tags, 
                      task.completed  if task.completed else TaskCompleted.No.value,
                      ConversionHelper.to_db_timestamp(task.updated_at), 
                      task.id]
                
            return db_helper.execute_non_query(self.update_query, params)

        except Exception as e :
            
            state.log_error(f"{ErrorHandler.DB_UpdateError.value} {e}")
            return False
    
    def mark_completed(self, task : Task) -> bool:

            try : 

                params = [task.completed  if task.completed else TaskCompleted.No.value,
                      ConversionHelper.to_db_timestamp(task.updated_at), 
                      task.id]
                
                return db_helper.execute_non_query(self.mark_completed_query, params)

            except Exception as e :

                state.log_error(f"{ErrorHandler.TaskServiceGetUpcomingRemindersError.value} {e}")
                return False

    def delete(self, task_id: int) -> bool:

        try:

            return db_helper.execute_non_query(self.delete_query, [task_id])
        
        except Exception as e :
            
            state.log_error(f"{ErrorHandler.DB_DeleteError.value} {e}")
            return False
        
    def delete_all(self) -> bool:

        try:

            return db_helper.execute_non_query(self.delete_all_query)
        
        except Exception as e :
            
            state.log_error(f"{ErrorHandler.DB_DeleteError.value} {e}")
            return False
    
    def get(self, task_id: int) -> Optional[Task]:

        try :

            row = db_helper.execute_query_and_Row(self.get_query, [task_id])
            return self.row_to_task(row) if row else None
        
        except Exception as e :
            
            state.log_error(f"{ErrorHandler.DB_GetError.value} {e}")
            return None
        
    def get_all(self) -> list[Task] :

        try : 

            rows = db_helper.execute_query_and_list(self.get_all_query)
            return [self.row_to_task(row) for row in rows]

        except Exception as e :
            
            state.log_error(f"{ErrorHandler.DB_GetAllError.value} {e}")
            return None
        
    def search_and_filter(self, keyword : Optional[str] = None, priority : Optional[str] = None ,category : Optional[str] = None, completed: Optional[int] = None) -> list[Task] :

        try : 

            search_query = "SELECT * FROM tasks "
            params = []
            where_clause : Optional[str] = None

            if keyword:

                where_clause = " WHERE (title LIKE ? OR description LIKE ? OR tags LIKE ?)"
                search_query += where_clause
                pattern = f"%{keyword}%"
                params.extend([pattern, pattern, pattern])

            if priority:

                if where_clause :

                    where_clause = " AND priority=?"

                else :

                    where_clause = " WHERE priority=?"
                    
                search_query += where_clause
                params.append(priority)

            if category:

                if where_clause :

                    where_clause = " AND category=?"

                else :

                    where_clause = " WHERE category=?"

                search_query += where_clause
                params.append(category)

            if completed is not None:

                if where_clause :

                    where_clause = " AND completed=?"

                else :

                    where_clause = " WHERE completed=?"

                search_query += where_clause
                params.append(completed)

            search_query += " ORDER BY created_at DESC"

            rows = db_helper.execute_query_and_list(search_query,params)
            return [self.row_to_task(row) for row in rows]

        except Exception as e :
            
            state.log_error(f"{ErrorHandler.DB_SearchAndFilterError.value} {e}")
            return []
        
    def get_upcoming_reminders(self) -> list[Task]:
       
        try:
         
            rows = db_helper.execute_query_and_list(self.get_reminders_query)
            return [self.row_to_task(row) for row in rows]
        
        except Exception as e:
           
            state.log_error(f"{ErrorHandler.DB_GetRemindersError.value} {e}")
            return []

    def row_to_task(self, row) -> Task:

        return Task(
            id = row["id"],
            title = row["title"],
            description = row["description"],
            priority = TaskPriority(row["priority"]).value if row["priority"] else TaskPriority.Medium.value,
            deadline = ConversionHelper.to_datetime(row["deadline"]),
            reminder = ConversionHelper.to_datetime(row["reminder"]),
            category = TaskCategory(row["category"]).value if row["category"] else TaskCategory.General.value,
            tags = row["tags"],
            completed = TaskCompleted(row["completed"]).value if row["completed"] else TaskCompleted.No.value,
            created_at = ConversionHelper.to_datetime(row["created_at"], "%Y-%m-%d %H:%M:%S"),
            updated_at = ConversionHelper.to_datetime(row["updated_at"], "%Y-%m-%d %H:%M:%S"),
        )


## CALLING METHODS TO TEST
# if __name__ == "__main__":

#     helper = TaskDataHelper()
#     print("\n helper.create_table() : " + str(helper.create_table()))
    
#     print("\n helper.delete_all() : " + str(helper.delete_all()))

#     task = Task()
#     task.title = "python learning project"
#     print("\n Task Obj : ",task)
#     print("\n helper.insert(task) : " + str(helper.insert(task)))

#     task.id = 12
#     task.deadline = "2025-09-02 20:20"
#     task.reminder = "2025-09-02 20:50"
#     task.category = TaskCategory.Work.value
#     print("\n helper.update(task) : " + str(helper.update(task)))

#     print("\n helper.get() : " + str(helper.get(1)))

#     print("\n helper.get_all() : " + str(helper.get_all()))

#     print("\n helper.search_and_filter() : " + str(helper.search_and_filter("try_to_search")))

#     print("\n helper.get_upcoming_reminders() : " + str(helper.get_upcoming_reminders()))

#     if len(state.errors) > 0 : print([f"{error}" for error in state.errors])  
#     else : print("\n\n no state error")

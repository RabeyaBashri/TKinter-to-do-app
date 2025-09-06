from typing import  Optional
from datetime import datetime, timedelta

import sys
sys.path.append(r"E:\python\TKinter-to-do-app\utilities")
sys.path.append(r"E:\python\TKinter-to-do-app\models")
sys.path.append(r"E:\python\TKinter-to-do-app\dal")
from task_data_helper import TaskDataHelper
from task import Task
from app_state import AppState
from enums import ErrorHandler, TaskCompleted, TaskCategory
from conversion_helper import ConversionHelper

state = AppState.get_instance()

class TaskService :

    def __init__ (self) :

        self.data_mapper = TaskDataHelper()

    def save(self, task: Task) -> Optional[Task] :
       
        try :

            task_id = self.data_mapper.insert(task)

            if task_id:

                task.id = task_id

            return task
        
        except Exception as e :

            state.log_error(f"{ErrorHandler.TaskServiceSaveError.value} {e}")
            return None
        
    def update(self, task: Task) -> bool :
       
        try :

            task.updated_at = datetime.now()
            return self.data_mapper.update(task)
        
        except Exception as e :

            state.log_error(f"{ErrorHandler.TaskServiceUpdateError.value} {e}")
            return False
        
    def delete(self, task_id: int) -> bool :
       
        try :

            return self.data_mapper.delete(task_id)
        
        except Exception as e :

            state.log_error(f"{ErrorHandler.TaskServiceDeleteError.value} {e}")
            return False
        
    def delete_all(self) -> bool :
       
        try :

            return self.data_mapper.delete_all()
        
        except Exception as e :

            state.log_error(f"{ErrorHandler.TaskServiceDeleteError.value} {e}")
            return False
        
    def get(self, task_id: int) -> Optional[Task] :
       
        try :

            return self.data_mapper.get(task_id)
        
        except Exception as e :

            state.log_error(f"{ErrorHandler.TaskServiceGetError.value} {e}")
            return None
        
    def get_all(self) -> list[Task] :
       
        try :

            return self.data_mapper.get_all()
        
        except Exception as e :

            state.log_error(f"{ErrorHandler.TaskServiceGetAllError.value} {e}")
            return []
        
    def search_and_filter(self, 
                          keyword: Optional[str] = None,
                          priority: Optional[str] = None,
                          category: Optional[str] = None,
                          completed: Optional[int] = None) -> list[Task] :
       
        try :

            return self.data_mapper.search_and_filter(keyword, priority, category,completed)
        
        except Exception as e :

            state.log_error(f"{ErrorHandler.TaskServiceSearchAndFilterError.value} {e}")
            return []

    def mark_completed(self, task : Task) -> bool:

            try : 

                task.updated_at = datetime.now()

                return self.data_mapper.mark_completed(task)

            except Exception as e :

                state.log_error(f"{ErrorHandler.TaskServiceGetUpcomingRemindersError.value} {e}")
                return False

    def get_upcoming_reminders(self, within_minutes: int = 60) -> list[Task] :
       
        try :

            tasklist : list[Task] = self.data_mapper.get_upcoming_reminders()
            now = datetime.now()
            horizon = now + timedelta(minutes=within_minutes)

            results = []
            
            for task in tasklist:

                if task.reminder and task.completed == TaskCompleted.No.value:

                    if now <= task.reminder <= horizon:
                        results.append(task)

            return results
        
        except Exception as e :

            state.log_error(f"{ErrorHandler.TaskServiceGetUpcomingRemindersError.value} {e}")
            return []

## CALLING METHODS TO TEST
# if __name__ == "__main__":

#     service = TaskService()

#     print("\n service.delete_all() : " + str(service.delete_all()))

#     task = Task()
#     task.title = "python learning project"
#     print("\n Task Obj : ",str(task))
#     print("\n service.save(task) : " + str(service.save(task)))
#     print("\n service.save(task) : " + str(task))

#     task = service.get(14)
#     print("\n service.get(task) : " + str(task))
#     task.deadline = "2025-09-07 21:14"
#     task.reminder = "2025-09-04 16:55"
#     task.category = TaskCategory.Work.value
#     print("\n service.update(task) : " + str(service.update(task)))

#     print("\n service.delete() : " + str(service.delete(2)))

#     print("\n service.get() : " + str(service.get(12)))
    
#     print("\n service.get_all() : " + str(service.get_all()))
#     print("\n service.get_all() : ".join(str(task) for n, task in enumerate(service.get_all(),0)))
    
#     print("\n service.search_and_filter() : " + str(service.search_and_filter("project")))

#     print("\n service.get_upcoming_reminders() : " + str(service.get_upcoming_reminders()))

#     if len(state.errors) > 0 : print([f"{error}" for error in state.errors])  
#     else : print("\n\n no state error")
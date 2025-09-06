from enum import Enum

class TaskCategory(Enum):
    Work = "Work"
    Personal = "Personal"
    Study = "Study"
    Health = "Health"
    Shopping = "Shopping"
    General = "General"

class TaskPriority(Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class TaskCompleted(Enum):
    Yes = "Yes"
    No = "No"

class ErrorHandler(Enum):

    DB_Initialization = "[Error] DB Initialization: "
    DB_ExecuteNonQueryError = "[DB Execute Non Query Error] : "
    DB_ExecuteQueryAndListError = "[DB Execute Query And List Error] : "
    DB_ExecuteQueryAndRowError = "[DB Execute Query And Row Error] : "
    DB_ExecuteNonQueryAndScalarError = "[DB Execute Non Query And Scalar Error] : "
    DB_CreateCursorError = "[DB Create Cursor Error] : "
    DB_CreateTableError = "[DB Create Table Error] : "
    DB_InsertError = "[DB Insert Error] : "
    DB_UpdateError = "[DB Update Error] : "
    DB_DeleteError = "[DB Delete Error] : "
    DB_GetError = "[DB Get Error] : "
    DB_GetAllError = "[DB Get All Error] : "
    DB_SearchError = "[DB Search Error] : "
    DB_GetRemindersError = "[DB Get Reminders Error] : "
    TaskServiceSaveError = "[Task Service Save Error] : "
    TaskServiceUpdateError = "[Task Service Update Error] : "
    TaskServiceDeleteError = "[Task Service Delete Error] : "
    DB_SearchAndFilterError = "[DB Search And Filter Error] : "
    TaskServiceSearchAndFilterError = "[Task Service Search And Filter Error] : "
    TaskServiceGetUpcomingRemindersError = "[Task Service Get Upcoming Reminders Error] : "
    ConversionHelperConvertToDatetimeError = "[Conversion Helper Convert To Datetime Error] : "
    TaskServiceGetError = "[Task Service Get Error] : "
    TaskServiceGetAllError = "[Task Service Get All Error] : "
    UISaveActionError = "[Save Task Error] : "

class AppStatus(Enum):
    OK = "OK"
    Error = "Error"
    

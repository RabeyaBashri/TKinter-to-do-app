import sys
sys.path.append(r"E:\python\TKinter-to-do-app\utilities")
from enums import TaskCategory,TaskPriority, TaskCompleted

from datetime import datetime
from typing import Optional
from dataclasses import dataclass,  field

@dataclass
class Task:
    
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    priority: str = TaskPriority.Medium.value
    deadline: Optional[datetime] = None
    reminder: Optional[datetime] = None
    category: Optional[str] = TaskCategory.General.value
    tags: str = ""
    completed : Optional[str]  = TaskCompleted.No.value
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_form(
        cls,
        title: str,
        desc: str,
        cat_value: str,
        prio_value: str,
        completed_value: str,
        deadline_value: str,
        reminder_value: str,
        tags_value : str,
        placeholder_category: str = "Select",
        placeholder_priority: str = "Select",
        placeholder_completed: str = "Select"
    ) -> "Task":
        
        ##Safely construct a Task object from form inputs
        
        # Category 
        if cat_value == placeholder_category:
            category = TaskCategory.General.value
        else:
            try:
                category = TaskCategory(cat_value).value
            except ValueError:
                category = TaskCategory.General.value

        # Priority 
        if prio_value == placeholder_priority:
            priority = TaskPriority.Medium.value
        else:
            try:
                priority = TaskPriority(prio_value).value
            except ValueError:
                priority = TaskPriority.Medium.value

        # Completed 
        if completed_value == placeholder_completed:
            completed = TaskCompleted.No.value
        else:
            try:
                completed = TaskCompleted(completed_value).value
            except ValueError:
                completed = TaskCompleted.No.value

        # Deadline 
        deadline = deadline_value.strip() if deadline_value.strip() else None

        # Reminder 
        reminder = reminder_value.strip() if reminder_value.strip() else None

        #  Tags 
        tags = tags_value.strip()

        return cls(
            title=title,
            description=desc,
            category=category,
            priority=priority,
            deadline=deadline,
            reminder=reminder,
            tags=tags,
            completed=completed
        )

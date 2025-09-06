import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Optional
from functools import partial

import sys
sys.path.append(r"E:\python\TKinter-to-do-app\utilities")
sys.path.append(r"E:\python\TKinter-to-do-app\models")
sys.path.append(r"E:\python\TKinter-to-do-app\services")
from task_service import TaskService
from task import Task
from app_state import AppState
from enums import TaskPriority, TaskCategory, TaskCompleted, ErrorHandler

class TKinterToDoApp(tk.Tk) :

    def __init__(self):

        super().__init__()

        # Theme Below
                
        style = ttk.Style(self)
        try:
            style.theme_use("clam")  # stable built-in theme
        except Exception:
            style.theme_use("default")  # fallback

        # Treeview custom style (striped, dark mode)
        style.configure(
            "Treeview",
            background="#F2EAE9",
            foreground="#403C3B",
            fieldbackground="#F2EAE9",
            rowheight=35,
            bordercolor="#BA5549",
            borderwidth=1
        )
        style.map("Treeview",
                  background=[("selected", "#E8D3CF")],
                  foreground=[("selected", "#37CDCD")])

        # Treeview heading style
        style.configure(
            "Treeview.Heading",
            background="#E8D3CF",
            foreground="#37CDCD",
            font=("Segoe UI", 10, "bold")
        )

        # Button style
        style.configure(
            "TButton",
            padding=6,
            relief="flat",
            background="#E8D3CF",
            foreground="#37CDCD",
            font=("Segoe UI", 10)
        )
        style.map("TButton",
                  background=[("active", "#37CDCD")],
                  foreground=[("active", "#E8D3CF")])

        # Combobox style
        style.configure(
            "TCombobox",
            fieldbackground="#E8D3CF",
            background="#E8D3CF",
            foreground="#37CDCD",
            arrowcolor="#37CDCD"
        )

        # Label style
        style.configure("TLabel",
                        background="#E8D3CF",
                        foreground="#37CDCD",
                        font=("Segoe UI", 10))

        self.configure(bg="#E8D3CF")  # app background

        ## Theme Above

        self.title("To-Do App")
        self.geometry("1200x800")

        self.service = TaskService()
        self.state = AppState.get_instance()

        ## Variables
        self.keyword_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.completed_var = tk.StringVar()
        self.action_buttons = {}

        self.all_completed = False

        ## UI Rendering and actions
        self.build_ui()
        self.load_tasks()
        self.setup_reminder_check()

    ##  UI  Below

    def build_ui(self):

        try : 
            ## Search And Filter - Frame Below

            top_frame = ttk.Frame(self)
            top_frame.pack(fill="x", padx=10, pady=5)

            ## Keyword Search Label And i/p
            ttk.Label(top_frame, text="Keyword:").grid(row=0, column=0, padx=5)
            ttk.Entry(top_frame, textvariable=self.keyword_var, width=20).grid(row=0, column=1)

            ## Priority filter
            ttk.Label(top_frame, text="Priority:").grid(row=0, column=2, padx=5)
            self.priority_cb = ttk.Combobox(
                top_frame,
                textvariable = self.priority_var,
                values=["Select"] + [p.value for p in TaskPriority],  
                width=10,
                state="readonly"
            )
            self.priority_cb.grid(row=0, column=3, padx=5)
            self.priority_cb.current(0)

            ## Category filter
            ttk.Label(top_frame, text="Category:").grid(row=0, column=4, padx=5)
            self.category_cb = ttk.Combobox(
                                    top_frame,
                                    textvariable=self.category_var,
                                    values=["Select"] + [c.value for c in TaskCategory],
                                    width=15,
                                    state="readonly"
                                    )
            self.category_cb.grid(row=0, column=5, padx=5)
            self.category_cb.current(0)

            ## Completed filter
            ttk.Label(top_frame, text="Completed:").grid(row=0, column=6, padx=5)
            self.completed_cb = ttk.Combobox(
                top_frame,
                textvariable=self.completed_var,
                values=["Select"] + [c.value for c in TaskCompleted],
                width=12,
                state="readonly"
            )
            self.completed_cb.grid(row=0, column=7, padx=5)
            self.completed_cb.current(0)

            ## Search button
            ttk.Button(top_frame, text="Search", command=self.on_search).grid(row=0, column=8, padx=10)
            ttk.Button(top_frame, text="Clear Search", command=self.on_clear_search).grid(row=0, column=9, padx=5)
            ## Search And Filter - Frame Above

            ttk.Button(top_frame, text="Add Task", command=self.open_add_form).grid(row=0, column=10, padx=5)

            ttk.Button(top_frame, text="Delete All", command=self.on_delete_all).grid(row=0, column=11, padx=5)

            # treeview Task Table
            columns = ("id", "completed_check", "title","description", "priority", "category", "completed", "deadline", "reminder", "action")
            
            self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20, selectmode="extended")

            self.tree["displaycolumns"] = ("completed_check", "title","description", "priority", "category", "completed", "deadline", "reminder", "action")

            for col in columns:

                if col == "completed_check" :

                    self.tree.heading(col, text="☐")  

                else : 
                    
                    self.tree.heading(col, text=col.capitalize())
                
                self.tree.column(col, width=120, anchor="center")

            self.tree.pack(fill="both", expand=True)

            # redraw action buttons when tree is resized or scrolled
            self.tree.bind("<Configure>", lambda e: self.draw_action_buttons())
            self.tree.bind("<Motion>", lambda e: self.draw_action_buttons())
            self.tree.bind("<ButtonRelease-1>", lambda e: self.draw_action_buttons())

            self.tree.bind("<Button-1>", self.on_tree_click)

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    ## Action Buttons 

    def on_tree_click(self, event):

        try : 

            item_id = self.tree.identify_row(event.y)
            col = self.tree.identify_column(event.x)

            if col == "#1" and item_id == "":

                tasks = self.service.get_all()
                new_state = TaskCompleted.Yes.value if not self.all_completed else TaskCompleted.No.value

                for task in tasks:

                    task.completed = new_state
                    self.service.mark_completed(task)

                self.load_tasks()  
                return

            
            if col == "#1" and item_id:

                task_id = self.tree.item(item_id, "values")[0]

                task = self.service.get(int(task_id))

                if task:

                    task.completed = TaskCompleted.No.value if task.completed == TaskCompleted.Yes.value else TaskCompleted.Yes.value

                    self.service.mark_completed(task)

                    self.load_tasks()

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    def draw_action_buttons(self):

        try : 

            self.clear_action_buttons()

            for item in self.tree.get_children():

                vals = self.tree.item(item, "values")
                
                if not vals:
                    continue
                task_id = vals[0]

                bbox = self.tree.bbox(item, column = 9)  # action column
                if not bbox:
                    continue
                x, y, w, h = bbox

                edit_btn = ttk.Button(self.tree, text="Edit",command = partial(self.open_edit_form, task_id))
                edit_btn.place(x=x, y=y, width=w // 2, height=h)

                del_btn = ttk.Button(self.tree, text="Delete", command = partial(self.on_delete, task_id))
                del_btn.place(x=x + w // 2, y=y, width=w // 2, height=h)

                self.action_buttons[item] = (edit_btn, del_btn)

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    def clear_action_buttons(self):

        try : 

            for btns in self.action_buttons.values():

                for btn in btns:

                    btn.destroy()

            self.action_buttons.clear()

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    ##  UI  Above

    ## CRUD Below

    def on_search(self):

        try : 

            self.populate_tasks(self.service.search_and_filter(
                keyword = self.keyword_var.get().strip() or None,
                priority = self.priority_var.get() if self.priority_var.get() != "Select" else None,
                category = self.category_var.get() if self.category_var.get() != "Select" else None,
                completed = self.completed_var.get() if self.completed_var.get() != "Select" else None
            ))

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    def on_clear_search(self) :

        try : 

            self.keyword_var.set("")
            self.priority_cb.current(0)
            self.category_cb.current(0)
            self.completed_cb.current(0)

            self.load_tasks()

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    def load_tasks(self) :

        try : 
            
            self.state.clear_errors()

            self.populate_tasks(self.service.get_all())

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    def populate_completed_checkbox(self, tasks : list[Task]) :

        try :

            if not tasks :

                tasks = self.task_service.get_all()

            self.all_completed = all(t.completed == TaskCompleted.Yes.value for t in tasks)
            header_text = "☑" if self.all_completed else "☐"
            self.tree.heading("completed_check", text=header_text)

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    def populate_tasks(self, tasks : list[Task]) :

        try : 

            for row in self.tree.get_children():
                    self.tree.delete(row)
            self.clear_action_buttons()

            if tasks :

                self.populate_completed_checkbox(tasks)
                
                for task in tasks:

                    checkbox = "☑" if task.completed == TaskCompleted.Yes.value else "☐"

                    self.tree.insert("", "end", values=(
                        task.id,
                        checkbox,
                        task.title,
                        task.description,
                        task.priority if task.priority else "",
                        task.category if task.category else "",
                        task.completed if task.completed else "",
                        task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "",
                        task.reminder.strftime("%Y-%m-%d %H:%M") if task.reminder else "",
                        ""  # action col
                    ))

                self.after(100, self.draw_action_buttons)

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()    

    def open_add_form(self):

        try :

            self.open_form()

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    def open_edit_form(self, task_id: int):

        try : 
             
            task = self.service.get(task_id)

            if not task:

                messagebox.showerror("Error", "Task not found")
                return
            
            self.open_form(task)

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    def open_form(self, task: Optional[Task] = None) :

        try : 

            ## i/p form (popup window) to add/edit
            form = tk.Toplevel(self)
            form.title("Edit Task" if task else "Add Task")
            form.geometry("400x450")

            ## form field data variables
            title_var = tk.StringVar(value=task.title if task else "")
            desc_var = tk.StringVar(value=task.description if task else "")
            prio_var = tk.StringVar(value=task.priority if task and task.priority else "Select")
            cat_var = tk.StringVar(value=task.category if task and task.category else "Select")
            comp_var = tk.StringVar(value=task.completed if task and task.completed else "Select")
            deadline_var = tk.StringVar(value=task.deadline.strftime("%Y-%m-%d %H:%M") if task and task.deadline else "")
            reminder_var = tk.StringVar(value=task.reminder.strftime("%Y-%m-%d %H:%M") if task and task.reminder else "")
            tags_var = tk.StringVar(value=task.tags if task else "")

            ## fields
            ttk.Label(form, text="Title:").pack()
            ttk.Entry(form, textvariable=title_var).pack(fill="x", padx=5, pady=2)

            ttk.Label(form, text="Description:").pack()
            ttk.Entry(form, textvariable=desc_var).pack(fill="x", padx=5, pady=2)

            ttk.Label(form, text="Priority:").pack()
            ttk.Combobox(form, textvariable=prio_var,
                        values=["Select"] + [p.value for p in TaskPriority],
                        state="readonly").pack(fill="x", padx=5, pady=2)

            ttk.Label(form, text="Category:").pack()
            ttk.Combobox(form, textvariable=cat_var,
                        values=["Select"] + [c.value for c in TaskCategory],
                        state="readonly").pack(fill="x", padx=5, pady=2)

            ttk.Label(form, text="Completed:").pack()
            ttk.Combobox(form, textvariable=comp_var,
                        values=["Select"] + [c.value for c in TaskCompleted],
                        state="readonly").pack(fill="x", padx=5, pady=2)

            ttk.Label(form, text="Deadline (YYYY-MM-DD HH:MM):").pack()
            ttk.Entry(form, textvariable=deadline_var).pack(fill="x", padx=5, pady=2)

            ttk.Label(form, text="Reminder (YYYY-MM-DD HH:MM):").pack()
            ttk.Entry(form, textvariable=reminder_var).pack(fill="x", padx=5, pady=2)

            ttk.Label(form, text="Tags:").pack()
            ttk.Entry(form, textvariable=tags_var).pack(fill="x", padx=5, pady=2)

            def save_task() :
                
                try :

                    task_obj = Task.from_form(
                        title_var.get(),
                        desc_var.get(),
                        cat_var.get(),
                        prio_var.get(),
                        comp_var.get(),
                        deadline_var.get(),
                        reminder_var.get(),
                        tags_var.get()
                    )

                    if task:

                        task_obj.id = task.id
                        self.service.update(task_obj)
                    else:
                        self.service.save(task_obj)

                    self.load_tasks()

                    form.destroy()

                except Exception as e:

                    self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
                
                self.show_error()
                
            ttk.Button(form, text="Save", command=save_task).pack(pady=10)

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    def show_error(self) :

        if len(self.state.errors) > 0 : messagebox.showerror("Error",[f"{error}" for error in self.state.errors])

        self.state.clear_errors()

    def on_delete(self, task_id: int):

        try : 

            if messagebox.askyesno("Confirm", "Delete this task?"):

                self.service.delete(task_id)
                self.load_tasks()

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()
        
    def on_delete_all(self) :

        try :  

            if messagebox.askyesno("Confirm", "Delete all task?"):

                self.service.delete_all()
                self.load_tasks()

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    ## CRUD Above

    def setup_reminder_check(self):

        try : 

            self.check_reminders()

            self.after(60000, self.setup_reminder_check)

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
               
            self.show_error()

    def check_reminders(self):

        try : 

            due = self.service.get_upcoming_reminders()

            for t in due:

                messagebox.showinfo("Reminder", f"{t.title} at {t.deadline}")

        except Exception as e :

            self.state.log_error(f"{ErrorHandler.UISaveActionError.value} {e}")
            self.show_error()
               
        

if __name__ == "__main__":

    app = TKinterToDoApp()
    app.mainloop()
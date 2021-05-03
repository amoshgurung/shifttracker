"""Shift Tracker App

This is the main code for the app. It consists of classes that represents the main window and the frames within the
window.
"""

import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk
from datetime import datetime, time, date
from manager import FileManager


class MainApp(tk.Tk):
    """
    This class is a tkinter window that loads all the frames in a stack. It provides a way for all the other classes to
    interact with each other.

    Attributes
    ----------
    shared_data : dict
        A dict to store current user's user id as a value which is available to all the other classes.
    frames : dict
        It contains the name of frames as the key and the corresponding frame object as its value.

    Methods
    -------
    show_frame(page_name)
        The page_name passed in as an argument is brought on top of the stack.
    get_page(page_class)
        Returns the page_class.
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Shift Tracker")

        self.shared_data = {
            "username": tk.StringVar()
        }

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Name of the frame(key) : Frame object(value)
        self.frames = {}
        for F in (LoginView, HomeView, AddWindow):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, page_name):
        """
        Switches to the frame passed in as an argument.

        Parameters
        ----------
        page_name : String
            Name of the frame to switch.
        """

        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()

    def get_page(self, page_name):
        """
        Returns the frame object passed in as an argument.

        Parameters
        ---------
        page_name : String
            Name of the frame.

        Returns
        -------
        tk.Frame
            The frame object whose name was passed in.
        """

        return self.frames[page_name]


class LoginView(tk.Frame):
    """
    This class is a frame designed to be the interface for login and registering users.

    Attributes
    ----------
    name : tk.StringVar
    surname : tk.StringVar
    userid : tk.StringVar
        The value for name, surname and userid when the user is registering.
    message : tk.StringVar
        The message displayed when user makes an error. Different message is displayed for different error.

    Methods
    -------
    only_strings_allowed(s, action)
        Validating the user's input and only allowing strings to be entered.
    login_user()
        Login the existing user if correct information is provided.
    create_user()
        Create an account for new users.
    """

    def __init__(self, parent, controller):
        """
        Parameters
        ----------
        parent : tk.Frame
            The root frame in the window which holds all the other frames.
        controller : tk.Tk
            The main window where all the frames are stacked. It also provides a way for all the other frames to
            interact with each other.
        """

        tk.Frame.__init__(self, parent)
        self.controller = controller
        header_font = tkFont.Font(family="TkDefaultFont", size=10, weight=tkFont.BOLD)

        self.name = tk.StringVar()
        self.surname = tk.StringVar()
        self.userid = tk.StringVar()

        # Login frame.
        self.frm_login_form = tk.Frame(master=self)
        self.frm_login_form.grid(row=0, column=0)
        self.lbl_login_header = tk.Label(master=self.frm_login_form, text="Sign in", font=header_font)
        self.lbl_login_header.grid(row=0, column=0)
        self.lbl_login_userid = tk.Label(master=self.frm_login_form, text="User ID ")
        self.ent_login_userid = tk.Entry(master=self.frm_login_form, width=50,
                                         textvariable=self.controller.shared_data["username"])
        self.lbl_login_userid.grid(row=1, column=0, sticky="e", pady=1)
        self.ent_login_userid.grid(row=1, column=1, sticky='nsew', pady=1)
        self.login_prompt = tk.StringVar()
        self.login_prompt.set("")
        self.lbl_login_prompt = tk.Label(master=self.frm_login_form, textvariable=self.login_prompt)
        self.lbl_login_prompt.grid(row=2, column=1)
        self.btn_login = tk.Button(master=self.frm_login_form, text="Login", width=8, height=1, command=self.login_user)
        self.btn_login.grid(row=3, column=1, pady=5)

        # Register frame.
        self.frm_register_form = tk.Frame(master=self, borderwidth=3)
        self.frm_register_form.grid(row=1, column=0)
        self.lbl_login_header = tk.Label(master=self.frm_register_form, text="Sign up", font=header_font)
        self.lbl_login_header.grid(row=1, column=0)
        self.lbl_name = tk.Label(master=self.frm_register_form, text="Name ")

        # Validation
        check_if_alpha_char = (self.register(self.only_strings_allowed), '%P', '%d')
        self.ent_name = tk.Entry(master=self.frm_register_form, width=50, textvariable=self.name, validate="key",
                                 validatecommand=check_if_alpha_char)
        self.lbl_name.grid(row=2, column=0, sticky="e", pady=1)
        self.ent_name.grid(row=2, column=1, sticky='nsew', pady=1)
        self.lbl_surname = tk.Label(master=self.frm_register_form, text="Surname ")
        self.ent_surname = tk.Entry(master=self.frm_register_form, width=50, textvariable=self.surname, validate="key",
                                    validatecommand=check_if_alpha_char)
        self.lbl_surname.grid(row=3, column=0, sticky="e", pady=1)
        self.ent_surname.grid(row=3, column=1, sticky='nsew', pady=1)
        self.lbl_userid = tk.Label(master=self.frm_register_form, text="User ID ")
        self.ent_userid = tk.Entry(master=self.frm_register_form, width=50, textvariable=self.userid)
        self.lbl_userid.grid(row=4, column=0, sticky="e", pady=1)
        self.ent_userid.grid(row=4, column=1, sticky='nsew', pady=1)

        # Frame for buttons at the bottom of the page.
        self.frm_buttons = tk.Frame(master=self)
        self.frm_buttons.grid(row=2, column=0, sticky="ew", pady=3, ipady=3)
        self.message = tk.StringVar()
        self.message.set("")
        self.lbl_prompt = tk.Label(master=self.frm_buttons, textvariable=self.message)
        self.lbl_prompt.pack()

        self.btn_create = tk.Button(master=self.frm_buttons, text="Create", command=self.create_user)
        self.btn_create.pack(side=tk.RIGHT, ipadx=10, padx=10)

    def only_strings_allowed(self, s, action):
        """
        Only allows string to be entered in the entry box.

        Parameters
        ----------
        s : String
            The string typed in by the user.
        action : Action code
            This is the code for users action, that is set to "1". The statement is true when the user's
            is inserting a value.
        Returns
        -------
        boolean
            True if it's a string and False otherwise.
        """

        if action == "1":
            if not s.isalpha():
                return False
        return True

    def login_user(self):
        """
        It checks if the user id already exists in the users_db. If it does, the display switches to home
        page, else it displays an error message.
        """

        fmanager = FileManager()
        self.login_prompt.set("")
        if not fmanager.check_if_userid_exists(self.ent_login_userid.get()):
            self.login_prompt.set("Invalid User ID. Please try again.")
        else:
            home_view = self.controller.get_page("HomeView")
            home_view.populate_tree(self.controller.shared_data["username"].get())
            self.controller.show_frame("HomeView")

    def create_user(self):
        """
        This function is assigned to the "create" button.
        If the entry box is empty an error message is displayed.
        If the user id exists, an error message is displayed to let the user know that duplicate user id is
        not accepted.
        Else, the users information: name, surname and user id is saved in users_db file to register the new user.
        """

        fmanager = FileManager()
        if self.name.get() == "" or self.surname.get() == "" or self.userid.get() == "":
            self.message.set("Please fill in all the boxes.")
        # To avoid duplicate user id(primary key).
        elif fmanager.check_if_userid_exists(self.userid.get()):
            self.ent_userid.delete(0, tk.END)
            self.message.set("This User ID already exists. Please enter a different User ID.")
        else:
            fmanager.save_to_userList(self.name.get(), self.surname.get(), self.userid.get())
            self.ent_name.delete(0, tk.END)
            self.ent_surname.delete(0, tk.END)
            self.ent_userid.delete(0, tk.END)
            self.message.set("Congratulation, your account has been created.")


class HomeView(tk.Frame):
    """
    This class is the main page of the app. The user is able to check their previous entry and also add and delete
    new and old ones respectively.

    Attributes
    ----------
    shift_db : list
        This is a dataframe of the "shift_db" file.
    tbl_headers : list
        List of columns in shift_db. They are: User id, Date, Start time, End time and No of hours.
    tv_shift_table : tk.TreeView
       To display user specific entries on the main page.

    Methods
    -------
    populate_tree(userid)
        Add shift entries to the tv_shift_table and update the shift_db file.
    clear_tree_data()
        Empty the tv_shift_table.
    delete_selected_entry()
        Delete the selected entry on the tv_shift_table and update the shift_db file.
    log_out_user()
        Log out the current user and switch the frame to login page.
    """

    def __init__(self, parent, controller):
        """
        Parameters
        ----------
        parent : tk.Frame
            The root frame in the window which holds contains all the other frames.
        controller : tk.Tk
            The window of the application. It provides a way for all the other frames to interact with each other.
        """

        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.frm_root = tk.Frame(master=self)
        self.frm_root.grid(row=0, column=0)

        self.fmanager = FileManager()

        self.lbl_username = tk.Label(master=self.frm_root, textvariable=self.controller.shared_data["username"],
                                     font=("*Font", 10), relief="groove")
        self.lbl_username.grid(row=0, column=0, padx=10, pady=10)
        self.frm_main = tk.Frame(master=self.frm_root)
        self.frm_main.grid(row=1, column=0)
        self.btn_add = tk.Button(master=self.frm_main, text="Add", width=10, command=self.open_add_window)
        self.btn_add.grid(row=1, column=1, pady=5, padx=5)
        self.btn_delete = tk.Button(master=self.frm_main, text="Delete", width=10, command=self.delete_selected_entry)
        self.btn_delete.grid(row=2, column=1, pady=5, padx=5)
        self.btn_cancel = tk.Button(master=self.frm_main, text="Logout", width=10, command=self.log_out_user)
        self.btn_cancel.grid(row=3, column=1, pady=5, padx=5)

        self.frm_shift_table = tk.Frame(master=self.frm_root)
        self.frm_shift_table.grid(row=1, column=1, padx=10)
        self.tv_shift_table = tk.ttk.Treeview(master=self.frm_shift_table)

        self.shift_db = self.fmanager.shift_db_df
        self.tbl_headers = self.shift_db.columns.tolist()

        self.tv_shift_table['columns'] = ('Date', 'Start time', 'End time', 'No of hours')
        self.tv_shift_table.column('#0', width=0, stretch=tk.NO)
        self.tv_shift_table.column('Date', anchor=tk.CENTER)
        self.tv_shift_table.column('Start time', anchor=tk.CENTER)
        self.tv_shift_table.column('End time', anchor=tk.CENTER)
        self.tv_shift_table.column('No of hours', anchor=tk.CENTER)

        self.tv_shift_table.heading('#0', text='', anchor=tk.CENTER)
        self.tv_shift_table.heading('Date', text=self.tbl_headers[1], anchor=tk.CENTER)
        self.tv_shift_table.heading('Start time', text=self.tbl_headers[2], anchor=tk.CENTER)
        self.tv_shift_table.heading('End time', text=self.tbl_headers[3], anchor=tk.CENTER)
        self.tv_shift_table.heading('No of hours', text=self.tbl_headers[4], anchor=tk.CENTER)

    def populate_tree(self, userid):
        """
        Populating the tree with current user's entries.

        Parameters
        ----------
        userid : String
            User id of current user.
        """

        tbl_values = self.fmanager.get_user_specific_entry(userid)

        for i in range(len(tbl_values)):
            self.tv_shift_table.insert(parent='', index=i, iid=i, text='', values=(tbl_values[i][2],
                                                                                   tbl_values[i][3],
                                                                                   tbl_values[i][4],
                                                                                   tbl_values[i][5]))
        self.tv_shift_table.grid(row=0, column=0)

    def update_shift_entry_table(self, date, start_time, end_time, no_of_hours):
        self.tv_shift_table.insert(parent='', index=len(self.tv_shift_table.get_children()) + 1,
                                   iid=len(self.tv_shift_table.get_children()) + 1, text='', values=(date,
                                                                                                     start_time,
                                                                                                     end_time,
                                                                                                     no_of_hours))

    def clear_tree_data(self):
        """
        Deleting all the data in tree.
        """

        for children in self.tv_shift_table.get_children():
            self.tv_shift_table.delete(children)

    def open_add_window(self):
        """
        Switch to add page.
        """

        self.controller.show_frame("AddWindow")

    def delete_selected_entry(self):
        """
        Deletes the selected entry from the table.
        If the delete button is clicked without selecting a target an error message is shown.
        The shift_db is also updated.
        """

        try:
            selected_entry = self.tv_shift_table.selection()[0]
            self.tv_shift_table.delete(int(selected_entry))
            self.shift_db = self.shift_db.drop(int(selected_entry))
        except IndexError:
            print("No entry selected.")
        except KeyError:
            print("Key Error")
        fmanager = FileManager()
        fmanager.updated_shift_db(self.shift_db)

    def log_out_user(self):
        """
        Log out the current user and switch to login page.
        """

        self.clear_tree_data()
        self.controller.show_frame("LoginView")
        login_view = self.controller.get_page("LoginView")
        login_view.ent_login_userid.delete(0, tk.END)
        login_view.ent_name.delete(0, tk.END)
        login_view.ent_surname.delete(0, tk.END)
        login_view.ent_userid.delete(0, tk.END)
        login_view.message.set("")


class AddWindow(tk.Frame):
    """
    This class is the frame for adding entries to the database. It provides entry boxes for entering dates and hour of
    a shift that the user has done.

    Attributes
    ----------
    message : tk.StringVar()
        The error message displayed for invalid input.
    date : tk.StringVar()
        The date of the shift.
    start_time : tk.StringVar()
        The time when the shift started.
    end_time : tk.StringVar()
        The time when the shift ended.
    self.no_of_hours : tk.StringVar()
        The total number of hours worked in a single shift.

    Methods
    -------
    add_button_action()
        The entered information is combined and added to the shift_db as an entry.
    cancel_add_entry()
        The frame switches back to home page.
    only_digits_allowed(s, action)
        Validation for date entry box, where the only value accepted as an input are digits.
    time_format_validate(s, action, index)
        The validation for time format(HH:MM).
    on_entry_click(event)
        The start and end time entry boxes is initially filled with "HH:MM" string. When clicked on any of the entry
        boxes the "HH:MM" is removed for the user to enter a valid input.
    on_focus_out(event)
        If the start and end time entry boxes are empty, fill it with "HH:MM" string.
    """

    def __init__(self, parent, controller):
        """
        Parameters
        ----------
        parent : tk.Frame
            The root frame in the window which holds contains all the other frames.
        controller : tk.Tk
            The window of the application. It provides a way for all the other frames to interact with each other.
        """

        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.message = tk.StringVar()

        self.date = tk.StringVar()
        self.start_time = tk.StringVar()
        self.end_time = tk.StringVar()
        self.no_of_hours = tk.StringVar()

        self.master.rowconfigure(index=0, weight=1)
        self.master.columnconfigure(index=0, weight=1)

        self.frm_entry_section = tk.Frame(master=self)
        self.frm_entry_section.grid(row=0, column=0)

        # Date entry field
        self.lbl_date = tk.Label(master=self.frm_entry_section, text="Date: ")
        self.lbl_date.grid(row=1, column=0)

        digit_only_vcmd = (self.register(self.only_digits_allowed), "%P", "%d")
        self.lbl_year = tk.Label(master=self.frm_entry_section, text="Year")
        self.lbl_year.grid(row=0, column=1)
        self.ent_date_year = tk.Entry(master=self.frm_entry_section, width=10, validate="key",
                                      validatecommand=digit_only_vcmd)
        self.ent_date_year.grid(row=1, column=1)

        self.lbl_fslash_1 = tk.Label(master=self.frm_entry_section, text="/")
        self.lbl_fslash_1.grid(row=1, column=2)
        self.lbl_month = tk.Label(master=self.frm_entry_section, text="Month")
        self.lbl_month.grid(row=0, column=3)
        self.ent_date_month = tk.Entry(master=self.frm_entry_section, width=10, validate="key",
                                       validatecommand=digit_only_vcmd)
        self.ent_date_month.grid(row=1, column=3)
        self.lbl_fslash_2 = tk.Label(master=self.frm_entry_section, text="/")
        self.lbl_fslash_2.grid(row=1, column=4, padx=5)
        self.lbl_day = tk.Label(master=self.frm_entry_section, text="Day")
        self.lbl_day.grid(row=0, column=5)
        self.ent_date_day = tk.Entry(master=self.frm_entry_section, width=10, validate="key",
                                     validatecommand=digit_only_vcmd)
        self.ent_date_day.grid(row=1, column=5, pady=1)

        # Time entry field.
        time_format_valid = (self.register(self.time_format_validate), "%P", "%d", "%i")
        self.lbl_from = tk.Label(master=self.frm_entry_section, text="From: ")
        self.lbl_from.grid(row=2, column=0)
        self.ent_from = tk.Entry(master=self.frm_entry_section, width=10, validate="key",
                                 validatecommand=time_format_valid)
        self.ent_from.insert(0, "HH:MM")
        self.ent_from.bind("<FocusIn>", self.on_entry_click)
        self.ent_from.bind("<FocusOut>", self.on_focus_out)
        self.ent_from.grid(row=2, column=1)
        self.lbl_to = tk.Label(master=self.frm_entry_section, text="To: ")
        self.lbl_to.grid(row=2, column=2)
        self.ent_to = tk.Entry(master=self.frm_entry_section, width=10, validate="key",
                               validatecommand=time_format_valid)
        self.ent_to.insert(0, "HH:MM")
        self.ent_to.bind("<FocusIn>", self.on_entry_click)
        self.ent_to.bind("<FocusOut>", self.on_focus_out)
        self.ent_to.grid(row=2, column=3)

        # Bottom frame for buttons.
        self.frm_buttons = tk.Frame(master=self)
        self.frm_buttons.grid(row=1, column=0, sticky="ew", pady=3, ipady=3)
        self.btn_add = tk.Button(master=self.frm_buttons, text="Add", command=self.add_button_action)
        self.btn_add.pack(side=tk.RIGHT, ipadx=10, padx=3)
        self.btn_cancel = tk.Button(master=self.frm_buttons, text="Cancel",
                                    command=self.cancel_add_entry)
        self.btn_cancel.pack(side=tk.RIGHT, padx=10, ipadx=3)

        self.frm_message = tk.Frame(master=self.master)
        self.frm_message.grid(row=1, column=0)
        self.lbl_message = tk.Label(master=self.frm_message, textvariable=self.message, fg="red")
        self.lbl_message.pack()

    def add_button_action(self):
        """
        Adding shift information(date and time) to shift_db.

        Raises
        ------
        ValueError
            If an empty value is passed in as date.
        TypeError
            If an invalid input is entered. For e.g. A string is passed in instead of an integer.
        """

        fmanager = FileManager()
        try:
            self.date = date(int(self.ent_date_year.get()),
                             int(self.ent_date_month.get()),
                             int(self.ent_date_day.get()))
            self.start_time = time(hour=int(self.ent_from.get().split(":")[0]),
                                   minute=int(self.ent_from.get().split(":")[1]))
            self.end_time = time(minute=int(self.ent_to.get().split(":")[1]),
                                 hour=int(self.ent_to.get().split(":")[0]))

            self.no_of_hours = (datetime.combine(self.date, self.end_time) -
                                datetime.combine(self.date, self.start_time))
            self.no_of_hours = round(self.no_of_hours.seconds / 3600, 2)

            fmanager.add_entry_to_shift_db(self.controller.shared_data["username"].get(), self.date, self.start_time,
                                           self.end_time, self.no_of_hours)
            hview = self.controller.get_page("HomeView")
            hview.update_shift_entry_table(self.date, self.start_time, self.end_time, self.no_of_hours)
            self.controller.show_frame("HomeView")
        except ValueError:
            self.message.set("Value Error! Please fill in the boxes with appropriate entry.")
        except TypeError:
            self.message.set("Type Error! Please fill in the boxes with appropriate entry.")
        self.ent_date_day.delete(0, tk.END)
        self.ent_date_month.delete(0, tk.END)
        self.ent_date_year.delete(0, tk.END)
        self.ent_from.delete(0, tk.END)
        self.ent_from.insert(0, "HH:MM")
        self.ent_to.delete(0, tk.END)
        self.ent_to.insert(0, "HH:MM")

    def cancel_add_entry(self):
        """
        Switches the frame back to home view.
        """

        self.controller.show_frame("HomeView")
        self.message.set("")

    def only_digits_allowed(self, s, action):
        """
        Only allow integers to be entered in the date fields.

        Parameters
        ----------
        s : String
            The user's input.
        action : Action code
            This is the code for users action, that is set to "1". The "1" is if the user is inserting a value.

        Returns
        -------
        If "s" is not a digit returns False, else returns True.
        """

        if action == "1":
            if not s.isdigit():
                return False
        return True

    def time_format_validate(self, s, action, index):
        """
        Validation for the time format(HH:MM).

        Parameters
        ----------
        s : String
            The user's input.
        action : Action code
            This is the code for users action, that is set to "1". The "1" is if the user is inserting a value.
        index : Integer
        """

        if action == "1":
            if index == "2" and s[int(index)] != ":":
                return False
            if len(s) > 5:
                return False
        return True

    def on_entry_click(self, event):
        """
        On clicking on either of the fields will remove the initial text.

        Parameter
        --------
        event : tkinter Event
            Mouse click event.
        """

        if self.ent_from.get() == "HH:MM":
            self.ent_from.delete(0, tk.END)
        if self.ent_to.get() == "HH:MM":
            self.ent_to.delete(0, tk.END)

    def on_focus_out(self, event):
        """
        If either the start and end time field is empty, fill it with "HH:MM" text.

        Parameter
        --------
        event : tkinter Event
            Focus out event.
        """

        if self.ent_from.get() == "":
            self.ent_from.insert(0, "HH:MM")
        if self.ent_to.get() == "":
            self.ent_to.insert(0, "HH:MM")


if __name__ == "__main__":
    root = MainApp()
    root.mainloop()

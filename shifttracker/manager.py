""" File manager

This is a file manager class that handle the opening and editing of the cvs files. It contains function that allows the
main application to interact with the shift_db and user_db file.
"""

from pathlib import Path
import pandas as pd


class FileManager:
    """
    A class for interacting with the csv files. Addition to open and editing of the csv files, it also allows easy
    access to contents within the files.

    Attributes
    ----------
    current_path : Path
        Path to the current working directory or the root directory where this file is located.
    path_to_users_db : Path
        Path to the users_db file.
    path_to_shift_db : Path
        Path to the shift_db file.
    user_db_df : DataFrame
        The users_db file as dataframe.
    shift_db_df : DataFrame
        The shift_db file as dataframe.

    Methods
    -------
    check_if_userid_exists(userid)
        Checks if the passed in userid is in users_db file.
    save_to_userList(name, surname, userid)
        Saves the passed in user detail in users_db file.
    add_entry_to_shift_db(userid, date, start_time, end_time, no_of_hours)
        The passed in shift detail is added to the shift_db file.
    delete_shift_entry(userid, date)
        The entry with the same userid and date is deleted from the shift_db file.
    updated_shift_db(df)
        The df is saved as the csv file to save the changes.
    get_user_specific_entry(userid)
        Returns all the entries for the user with the passed in userid.
    """

    def __init__(self):
        # setting path to data directory
        self.current_path = Path('') #TODO: Add path to the root folder before running the program.
        self.path_to_users_db = Path(self.current_path, 'data', 'users_db.csv')
        self.path_to_shift_db = Path(self.current_path, 'data', 'shift_db.csv')
        self.user_db_df = pd.read_csv(self.path_to_users_db)
        self.shift_db_df = pd.read_csv(self.path_to_shift_db)

    def check_if_userid_exists(self, userid):
        """
        Check if the passed in userid has a duplicate.

        Parameters
        ----------
        userid : String
            The userid of the current user.

        Returns
        -------
        boolean
            Returns True if the userid already exists in the users_db file, else returns False.
        """

        user_id_list = pd.read_csv(self.path_to_users_db)["User id"].tolist()
        if userid not in user_id_list:
            return False
        return True

    def save_to_userList(self, name, surname, userid):
        """
        The passed in user's detail is save to users_db.

        Parameters
        ----------
        name : String
            The name of the user.
        surname : String
            The surname of the user.
        userid : String
            The unique userid of the user.
        """

        new_user = {'Name': name, "Surname": surname, "User id": userid}
        updated_user_db_df = pd.read_csv(self.path_to_users_db).append(new_user, ignore_index=True)
        updated_user_db_df.to_csv(self.path_to_users_db, index=False)

    def add_entry_to_shift_db(self, userid, date, start_time, end_time, no_of_hours):
        """
        The passed in shift details is saved to the shift_db file.

        Parameters
        ----------
        userid : String
            The unique user id of the user.
        date : datetime.Date
            The exact date of the shift carried out.
        start_time : String
            The start time of the shift.
        end_time : String
            The end time of the shift.
        no_of_hours : Integer
            Total number of hours worked in that shift.
        """

        shift_db_df = pd.read_csv(self.path_to_shift_db)
        new_shift_entry = {"User id": userid, "Date": date, "Start time": start_time, "End time": end_time,
                           "No of hours": no_of_hours}
        shift_db_df = shift_db_df.append(new_shift_entry, ignore_index=True)
        self.updated_shift_db(shift_db_df)

    def updated_shift_db(self, df):
        """
        Save the passed in dataframe(shift_db_df) as a csv file.

        Parameters
        ----------
        df : DataFrame
            The shift_db dataframe.
        """

        df.to_csv(self.path_to_shift_db, index=False)

    def get_user_specific_entry(self, userid):
        """
        Returns all the shift entry specific to the userid passed in.

        Parameters
        ----------
        userid : String
            The userid of the current user.

        Returns
        -------
        list
            List containing all the shift entry specific to the userid.
        """

        current_user_entry = []
        for row in pd.read_csv(self.path_to_shift_db).itertuples():
            if userid == row[1]:
                current_user_entry.append(row)
        return current_user_entry

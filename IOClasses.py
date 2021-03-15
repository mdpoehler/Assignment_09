#------------------------------------------#
# Title: IO Classes
# Desc: A Module for IO Classes
# Change Log: (Who, When, What)
# MPoehler, 2021-Mar-11, Retrieved file created by DBiesinger
# MPoehler, 2021-Mar-12, Cleaned up TODOS and added code to the save_inventory and load_inventory to handle track data in and out of a file.
# MPoehler, 2021-Mar-13, Added the greeting section and modified sections in th ScreenIO class to include the addition of the CD/Album deleting section
#------------------------------------------#

if __name__ == '__main__':
    raise Exception('This file is not meant to run by itself')

import DataClasses as DC
import ProcessingClasses as PC

class FileIO:
    """Processes data to and from file:

    properties:

    methods:
        save_inventory(file_name, lst_Inventory): -> None
        load_inventory(file_name): -> (a list of CD objects)

    """
    @staticmethod
    def save_inventory(file_name: list, lst_Inventory: list) -> None:
        """


        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory] that hold the data.
            lst_Inventory (list): list of CD objects.

        Returns:
            None.

        """
        file_name_CDs = file_name[0]
        file_name_trks = file_name[1]
        try:
            with open(file_name_CDs, 'w') as objFile:
                for disc in lst_Inventory:
                    objFile.write(disc.get_record())
                objFile.close()
            with open(file_name_trks, 'w') as objFile:
                for disc in lst_Inventory:
                    tracks = disc.cd_tracks
                    disc_id = disc.cd_id
                    for trk in tracks:
                        if trk is not None:
                            record = '{},{}'.format(disc_id, trk.get_record())
                            objFile.write(record)
                objFile.close()
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')

    @staticmethod
    def load_inventory(file_name: list) -> list:
        """


        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory] that hold the data.

        Returns:
            list: list of CD objects.

        """

        lst_Inventory = []
        file_name_CDs = file_name[0]
        file_name_trks = file_name[1]
        try:
            with open(file_name_CDs, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    row = DC.CD(data[0], data[1], data[2])
                    lst_Inventory.append(row)
                file.close()
            with open(file_name_trks, 'r')as file:
                for line in file:
                    data = line.strip().split(',')
                    cd = PC.DataProcessor.select_cd(lst_Inventory, int(data[0]))
                    track = DC.Track(int(data[1]), data[2], data[3])
                    cd.add_track(track)
                file.close()
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')
        return lst_Inventory

class ScreenIO:
    """Handling Input / Output"""

    @staticmethod
    def greeting():
        """Displays a greeting and total number of CDs currently in inventory"""
        print('\nWelcome to the CD Inventory Program!\n')
        print(DC.CD.total_entry())

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\nMain Menu\n\n[l] Load Inventory from file\n[a] Add CD / Album\n[i] Display Current Inventory')
        print('[c] Choose CD / Album\n[s] Save Inventory to file\n[d] Delete CD / Album\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, d, c, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'c', 's','d','x']:
            choice = input('Which operation would you like to perform? [l, a, i, c, s, d or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def print_CD_menu(cd):
        """Displays a sub menu of choices for CD / Album to the user

        Args:
            cd: cd object information to display in the sub menu.

        Returns:
            None.
        """
        print('\n======================================')
        print('\n{} Tracks Menu\n{}\n\n[a] Add track\n[d] Display cd / Album details\n[r] Remove track\n[x] exit to Main Menu'.format(cd.cd_title, cd.total_tracks(cd)))

    @staticmethod
    def menu_CD_choice():
        """Gets user input for CD sub menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices a, d, r or x

        """
        choice = ' '
        while choice not in ['a', 'd', 'r', 'x']:
            choice = input('Which operation would you like to perform? [a, d, r or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print(row)
        print('======================================')

    @staticmethod
    def show_tracks(cd):
        """Displays the Tracks on a CD / Album

        Args:
            cd (CD): CD object.

        Returns:
            None.

        """
        print('====== Current CD / Album: ==========')
        print(cd)
        print('=====================================')
        print(cd.get_tracks())
        print('=====================================')

    @staticmethod
    def get_CD_info():
        """function to request CD information from User to add CD to inventory


        Returns:
            cdId (string): Holds the ID of the CD dataset.
            cdTitle (string): Holds the title of the CD.
            cdArtist (string): Holds the artist of the CD.

        """

        cdId = input('Enter ID: ').strip()
        cdTitle = input('What is the CD\'s title? ').strip()
        cdArtist = input('What is the Artist\'s name? ').strip()
        return cdId, cdTitle, cdArtist

    @staticmethod
    def get_track_info():
        """function to request Track information from User to add Track to CD / Album


        Returns:
            trkId (string): Holds the ID of the Track dataset.
            trkTitle (string): Holds the title of the Track.
            trkLength (string): Holds the length (time) of the Track.

        """

        trkId = input('Enter Position on CD / Album: ').strip()
        trkTitle = input('What is the Track\'s title? ').strip()
        trkLength = input('What is the Track\'s length? ').strip()
        return trkId, trkTitle, trkLength

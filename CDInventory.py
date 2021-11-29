#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes,functions, error handling, and binary files.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# NWoodward, 2021-Nov-21, Added functions for Data Processing and IO
# NWoodward, 2021-Nov-28, Added Error Handling. Changed data storage from text to binary. Removed #DONE notations. Update Desc.
#------------------------------------------#
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # binary data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """ Functions for processing data """
    
    @staticmethod
    def add_cd(intID, strTitle, strArtist, table):
        """ Function that allows user to add a CD to the inventory in memory. The CD must be 
            saved, choice 's', in order for the CD to be written to a binary file.
        
        Args:
            intID (string): ID number entered by user
            strArtist (string): Artist name input by user
            strTitle (string): CD title input by user
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            table (list of dict): Updated list of dictionaries that contains CD data. Each dictionary represents one CD.
        """

        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dicRow)
        return table
       

    @staticmethod
    def del_cd(table, ID):
        """ Function that allows user to delete a CD from the inventory in memory.
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            ID: ID number of the CD the user would like to delete
        
        Returns:
            message: Message to the user to tell them if their attempt to delete a CD was successful
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == ID:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            message = print('The CD was removed')
        else:
            message = print('Could not find this CD!')
        return message

class FileProcessor:
    """Processing the data to and from binary file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from binary file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table (list of dicts).
        Each dictionary represents one CD.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table (list of dict): Updated list of dictionaries that contains CD data. Each dictionary represents one CD.
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            objFile = open(file_name, 'rb')
            table = pickle.load(objFile)
        except FileNotFoundError:
            print('Creating file.')
            objFile = open(file_name, 'ab')
            table = []
        except EOFError as e:
            print('File is blank. Please add CD\'s')
            print(type(e))
            table = []
        finally:
            objFile.close()
            return table
               
    @staticmethod
    def write_file(file_name, table):
        """Function to write data from a 2D list to a binary file
        
        Writes data from 2D list (list of dictionaries) identified by table into a binary file indentified
        by file_name.
        
        Args:
            file_name (string): name fo file used to write data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
            
        Returns:
            None.
        """
        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Functions handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
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
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
    
    @staticmethod
    def get_cd():
        """ Function to enable user to add a new CD to in memory to a list of dictionaries 
        
        Args:
            None.
        
        Returns:        
            strID (sting): ID number entered by user
            strArtist (string): Artist name input by user
            strTitle (string): CD title input by user
        
        """
        try:
            strID = input('Enter ID: ').strip()
            strID = int(strID)
            strTitle = input('What is the CD\'s title? ').strip()
            strArtist = input('What is the Artist\'s name? ').strip()
            return strID, strTitle, strArtist
        except ValueError as e:
            print('Please enter a whole number. You entered {}'.format(strID))
            print(type(e))
           

# 1. When program starts, read in the currently saved Inventory
try:
    lstTbl = FileProcessor.read_file(strFileName, lstTbl)
    print(lstTbl)
except Exception as e:
    print(type(e))

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        try:
            strID, strArtist, strTitle = IO.get_cd()
            # 3.3.2 Add item to the table
            lstTbl = DataProcessor.add_cd(strID, strArtist, strTitle, lstTbl)
            IO.show_inventory(lstTbl)
        except TypeError as e:
            print('Please enter valid CD inputs. Select \'a\' again to retry.')
            print(type(e))
        finally:  
            continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        try:
            IO.show_inventory(lstTbl)
        except TypeError as e:
            print('The CD Inventory is blank. Please add content.')
            print(type(e))
        finally:
            continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # 3.5.2 search thru table and delete CD
            DataProcessor.del_cd(lstTbl,intIDDel)
            print() # Add extra space for layout
            IO.show_inventory(lstTbl)
        except ValueError as e:
            print('Please enter a whole number listed as ID in inventory. Select \'d\' again to retry.')
            print(type(e))
        finally:
            continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.') 
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')





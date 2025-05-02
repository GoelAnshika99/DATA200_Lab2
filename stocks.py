# Summary: This module is just a shorter name for the program that can start either the Console or GUI version of the program.
import stock_console
import stock_GUI
def main():
    while True:
        print("\nWelcome to the Stock Manager Program!")
        print("Please choose an option: ")
        print("1 - Start Console Version")
        print("2 - Start GUI Version")
        print("0 - Exit Program")
        option = input("Enter your choice: ")
        if option == "1":
            stock_console.main()
        elif option == "2":
            stock_GUI.main()
        elif option == "0":
            print("Goodbye!")
            break
        else:
            print("*** Invalid option, please try again. ***")
# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a script
    main()
def main():


    while True:

        print("\n==============================")
        print("   JOB APPLICATION TRACKER")
        print("==============================")

        print("1. Add Job Application")
        print("2. View Applications")
        print("3. Search Application")
        print("4. Update Status")
        print("5. Delete Application")
        print("6. Statistics")
        print("7. Analytics")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            print("Add application selected.")

        elif choice == "2":
            print("View applications selected.")

        elif choice == "3":
            print("Search selected.")

        elif choice == "4":
            print("Update status selected.")

        elif choice == "5":
            print("Delete selected.")

        elif choice == "6":
            print("Statistics selected.")

        elif choice == "7":
            print("Analytics selected.")

        elif choice == "8":
            print("Thank you for using Job Application Tracker!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

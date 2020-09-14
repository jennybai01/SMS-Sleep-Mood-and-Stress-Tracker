    # while True:
    #         email = input("Enter your email: ")
    #         regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    #         if (re.search(regex, email)): # email validation with regexp
    #             break
    #         else:
    #             print("Invalid email.")
    #
    # while True: # get mood
    #     try:
    #         mood = input("Rate your mood today from 1 to 10 (inclusive): ")
    #         mood = int(mood)
    #         if (mood > 0 and mood < 11):
    #             break
    #     except ValueError:
    #         print("Please enter an integer.")
    #
    # while True: # get stress
    #     try:
    #         stress = input("Rate your stress today from 1 to 10 (inclusive): ")
    #         stress = int(stress)
    #         if (stress > 0 and stress < 11):
    #             break
    #     except ValueError:
    #         print("Please enter an integer.")
    #
    # while True: # get sleep
    #     try:
    #         sleep = input("How many hours of sleep did you get last night? ")
    #         sleep = int(sleep)
    #         if (sleep > -1 and sleep < 25):
    #             break
    #     except ValueError:
    #         print("Please enter an integer.")
import pandas as pd
import sys

def CheckSimilarity(hotelName):
    hotel_matrix = df.pivot_table(index='hotel_name', columns='user_name', values='rating')

    # Pearson correlation
    corr = hotel_matrix.corr(method = 'pearson')
    userRatings = hotel_matrix.loc[hotelName].dropna()

    simUsers = pd.Series()

    for i in range(0, len(userRatings.index)):
        sims = corr[userRatings.index[i]]
        sims = sims.map(lambda x: x * userRatings[i])
        simUsers = simUsers.append(sims)


    # Similar users
    simUsers = simUsers.groupby(simUsers.index).max()
    simUsers.sort_values(inplace = True, ascending = False)

    return simUsers

def UserStatus():
    while True:
        choice = input("\nDo you want to continue(Y/N)? ")
            
        if choice.upper()=="Y":
            break
        elif choice.upper()=="N":
            print("Thankyou!!!")
            sys.exit()
        else:
            print("Improper Input.")


choice="Y"

try:
    # Import CSV files
    Ratings =pd.read_csv('ratings.csv',encoding="latin-1")
    Hotels =pd.read_csv('hotels.csv',encoding="latin-1")

    Ratings['user_name'] = Ratings['user_name'].str.capitalize()
    Hotels['hotel_name'] = Hotels['hotel_name'].str.capitalize()

    # Merge both files
    df=pd.merge(Ratings, Hotels)
except:
    print ('Error. Required files are missing.')
    sys.exit()

# List of available hotels
print ("\nHere are the lists of available hotels:")
print (Hotels.hotel_name.to_string(index=False))

while (choice.upper()=="Y"):
    while True:
        try:
            hotelName = input("\nEnter name of the hotel: ").capitalize()
            simUsers = CheckSimilarity(hotelName)
            # Checkings for ratings greater than 3
            d = simUsers[simUsers>3]
            break
            
        except:
            print("\nImproper Input")
            UserStatus()

            
    if len(d) == 0:
        print("Nothing To Recommend. Sorry")
    else:
        print("\nHotel " + hotelName + " can be recommended to the following users.\n")
        # df_new = d.to_frame().reset_index()
        # print(df_new['index'])
        print(d)

    UserStatus()
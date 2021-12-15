API Documentation

ITEMS API

/items/item

Supports Get,Put,Delete Requests (require itemID as arg eg items/item?itemID=2, GET can filter by itemName also)

Can just include parts u want to edit will assume the non included parts as keep the same

For PUT request (ie editing of item post) will check whether current user in session is owner of itemID, however current implementation means only one user can be logged in at a time else won’t work properly

/items

Support Get (Returns all items), Post (Add new item to DB need json body)

        body = {
            "itemID": itemID,
            "itemName": itemName,
            "userName": userName,
            "userID" : userID,
            "description" : description,
            "remarks" : remarks,
            "photo" : photo,
     "status" : 0,
            “tags" : ["appliances"]
        }

/items/category

Filter by category

USERS AND PROFILES API

/users and /profiles (GET)

Support Get request, if userID arg is included will return user data/ profile data for particular userID, else return all users/ profiles


/profiles/edit (PUT)

Edit user profile info (see representation for what info needed)
For PUT request (ie editing of  user profile) will check whether current user in session is the same as user profile however current implementation means only one user can be logged in at a time else won’t work properly

User representation in DB

{
    "userID": "A0123456X",
    "passwordHash": "RandomStr",
    "email": "eXXXXX@u.nus.edu"
}

Profiles Representation in DB

{
    "userID": "A0XXXXXXE",
    "room": "7-102",
    "telegramHandle": "a",
    "profilePictureURI": "b",
    "userName": "John"
}

AUTH API

/auth/register (POST)

Register user, requires data below
Splits data into profiles and user collections in DB (see above)

Form Data Example
{
    "userID": "A0XXXXXXE",
    "passwordHash": "RandomStr",
    "email": "eXXXXX@u.nus.edu",
    "displayName": "UserName",
    "room": "7-101",
    "telegramHandle": "telehandle",
“userPhoto” : optional if not added uses a default uri
}


/auth/login (POST)

Login user, returns token and status = success
Session is updated to include user 

{
    "userID": "A0XXXXXXE",
    "passwordHash": "RandomStr"
}

/auth/logout (GET)

Logout user,
Returns user have successfully logged out message
Session removes user


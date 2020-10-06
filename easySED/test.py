from cryptography.fernet import Fernet
import onetimepad
import copy


def isSubString(string, subString):
    lengthOfSubString = len(subString)
    try:
        for i, j in enumerate(string):
            if(j == subString[0]):
                if(subString == string[i:i+lengthOfSubString]):
                    return True
                else:
                    pass
        return False
    except Exception as e:
        return False



class ED:

    def __init__(self):

        # pin for salting password key
        self.__pin = None

        self.__password = None

        # salting list
        self.saltList = ["This" , "is" , "an" , "industry" , "level" , "encryption"]

        # for salting fernet key
        self.keySalt1 = None
        self.keySalt2 = None

        self.securityLevelHigh = True
        self.outpass = False

    
    # function to output the encrypted password as well in the outputted string
    def setOutPutPass(self):
        self.outpass = True

    def setOwnSaltList(self , saltList):
        if(len(saltList) != 6):
            raise Exception("please pass 6 strings in list")

        else:
            self.saltList = saltList



    # function for checking if a password contain all lower , upper , nums and special case characters and also if is of 12 digit or not 
    def checkPass(self , string):

        # checking for 12 digit length 
        if(len(string) != 12):
            return False

        # lower case list
        lowerCase = ['a','s','d','f','g','h','j','k','l','z','x',
                    'c','v','b','n','m','q','w','e','r','t','y','u'
                    ,'i','o','p']

        # upper case list 
        upperCase = []
        for i in lowerCase:
            upperCase.append(i.upper())


        # nums and special characters
        spChar = ['~','!','@','$','%','^','&','*','(',')','_','-','=',
                '`','/','+','/','<','>','[',']','{','}','.',':',';',
                '|','#']

        nums = ['1','2','3','4','5','6','7','8','9','0']

        # tempList for checking if contains lowers uppers etc
        tempList = []

        for s in string:
            # if lower is present
            if(s in lowerCase):
                tempList.append("l")
            
            # if upper is present
            elif(s in upperCase):
                tempList.append("u")

            # if num is present
            elif(s in spChar):
                tempList.append("s")

            # if special char is present
            elif(s in nums):
                tempList.append("n")

        count = 0
        if("l" in tempList):
            count = count + 1
        
        if("u" in tempList):
            count = count + 1

        if("s" in tempList):
            count = count + 1

        if("n" in  tempList):
            count = count + 1 

        if(count >=  4):
            return True
        else:
            return False


    
    # function for checking if the pin is of 6 digit or not 
    def checkPin(self , pin):

        if(len(pin) != 6):
            return False

        return True

    
    def setSecurityLevel_toLow(self):
        self.securityLevelHigh = False
        

    # fucntion for setting the password , pin , keysalt
    # password must contain all lower , upper , nums , sp chars
    # pin must be of 6 digit
    def setPassword_Pin_keySalt(self , password , pin = 123456 , keySalt = "harshnative"):

        password = str(password)
        pin = str(pin)
        keySalt = str(keySalt)
        
        if(self.securityLevelHigh):
            if(self.checkPass(password)):
                self.__password = str(copy.copy(password))
            else:
                raise Exception("please set a 12 digit pass containing at least lower , upper , nums , special character \nOr you can set the security level to low")
        
        else:
            self.__password = str(copy.copy(password))
        
        if(self.checkPin(pin)):
            self.__pin = str(copy.copy(pin))
        else:
            raise Exception("please set a 6 digit pin \nOr you can set the security level to low")


        
        lenKeySalt = len(keySalt)
        self.keySalt1 = keySalt[:lenKeySalt]
        self.keySalt2 = keySalt[lenKeySalt:]



    # function to add salt to the password
    def convPassword(self):
        if(self.__password == None):
            raise Exception("please set the password")

        count = 0
        
        newPass = self.__password

        for i in self.__pin:
            digit = int(i)
            newPass = newPass[:digit] + self.saltList[count] + newPass[digit:]
            count += 1

        return newPass


    # function to check if everything is set up
    def checkIfPossible(self):
        if(self.__password == None):
            raise Exception("please set password")
            
        if(self.__pin == None):
            raise Exception("please set pin")

        if((self.keySalt1 == None) and (self.keySalt2 == None)):
            raise Exception("please set key salt")
    
    # function to encrypt things
    def encrypter(self , stringToEncrypt):

        self.checkIfPossible()
            
        stringToReturn = ""

        convPass = self.convPassword()

        if(self.outpass):

            # key
            key = Fernet.generate_key()
            
            # conv key from bytes to str 
            newKey = key.decode("utf-8")

            # encryting the key using the conv pass and keysalts
            keyToAdd = onetimepad.encrypt(newKey , self.keySalt1 + convPass + self.keySalt2)


            # conv string to bytes
            stringToPass = bytes(stringToEncrypt , "utf-8")

            cipher_suite = Fernet(key)
            encoded_text = cipher_suite.encrypt(stringToPass)
            stringToAdd = encoded_text.decode("utf-8")

            stringToReturn = keyToAdd + stringToAdd


        else:

            # password that will be added is encrypted by the convPass
            passwordToAdd = onetimepad.encrypt(self.__password , convPass)

            # key
            key = Fernet.generate_key()
            
            # conv key from bytes to str 
            newKey = key.decode("utf-8")

            # encryting the key using the conv pass and keysalts
            keyToAdd = onetimepad.encrypt(newKey , self.keySalt1 + convPass + self.keySalt2)


            # conv string to bytes
            stringToPass = bytes(stringToEncrypt , "utf-8")

            cipher_suite = Fernet(key)
            encoded_text = cipher_suite.encrypt(stringToPass)
            stringToAdd = encoded_text.decode("utf-8")


            stringToReturn = passwordToAdd + "////////////" + keyToAdd + "////////////" + stringToAdd

        return stringToReturn

    
    def decrypter(self , stringToDecrypt):

        self.checkIfPossible()

        convPass = self.convPassword()

        if(isSubString(stringToDecrypt , "////////////")):

            myList = stringToDecrypt.split("////////////")

            if(len(myList) != 3):
                raise Exception("could not decrypt")

            # checking if the password is correct or not
            toComparePass = onetimepad.decrypt(myList[0] , convPass)
            if(toComparePass != self.__password):
                raise Exception("could not decrypt , password does not match")

            # getting the key
            newKey = onetimepad.decrypt(myList[1] , self.keySalt1 + convPass + self.keySalt2)

            # conv strings to bytes
            key = bytes(newKey , "utf-8")

            cipher_suite = Fernet(key)
            decoded_text = cipher_suite.decrypt(bytes(myList[2] , "utf-8"))

            return decoded_text.decode("utf-8")

        else:

            # getting the key
            newKey = onetimepad.decrypt(stringToDecrypt[:88] , self.keySalt1 + convPass + self.keySalt2)

            # conv strings to bytes
            key = bytes(newKey , "utf-8")

            cipher_suite = Fernet(key)
            decoded_text = cipher_suite.decrypt(bytes(stringToDecrypt[88:] , "utf-8"))

            return decoded_text.decode("utf-8")
        


        

        



import random



myListLower = ['a','s','d','f','g','h','j','k','l','z','x',
          'c','v','b','n','m','q','w','e','r','t','y','u'
          ,'i','o','p'] 

myListUpper = []
for i in myListLower:
    myListUpper.append(i.upper())

myListEtc =  ['~','!','@','$','%','^','&','*','(',')','_','-','=',
             '`','/','+','/','<','>','[',']','{','}','.',':',';',
             '|','#' , ' ', ' ' , ' ' , ' ']  

nums = ['1','2','3','4','5','6','7','8','9','0']

myList = []

for i in myListLower:
    myList.append(i)

for i in myListUpper:
    myList.append(i)

for i in myListEtc:
    myList.append(i)

for i in nums:
    myList.append(i)



toDo = int(input("Enter the number of test : "))

error = 0
errorList = []
exList = []

e = ED()


for i in range(toDo):
    print("on - " , i)

    string = ""

    rand = random.randint(256 , 1024)
    rand2 = random.randint(4 , 16)

    for j in range(rand):
        string = string + str(random.choice(myList))

    password = ""
    for j in range(3):
        password = password + str(random.choice(myListLower))
    
    for j in range(3):
        password = password + str(random.choice(myListUpper))
    
    for j in range(3):
        password = password + str(random.choice(myListEtc))
    
    for j in range(3):
        password = password + str(random.choice(nums))

    salt = ""

    for i in range(rand2):
        salt = salt + str(random.choice(myList))

    
    pin = random.randint(100000 , 999999)

    saltList = []

    for i in range(6):
        saltstring = ""
        for j in range(random.randint(4 , 16)):
            saltstring = saltstring + str(random.choice(myList)) 
        saltList.append(saltstring)

    try:
        e.setPassword_Pin_keySalt(password , pin , salt)
        e.setOwnSaltList(saltList)

        enc = e.encrypter(string)

        dec = e.decrypter(enc)

        if(dec != string):
            error += 1
            tempList = []
            tempList.append(string)
            tempList.append(dec)
            errorList.append(tempList)

    except Exception as ex:
        tempList = []
        tempList.append(ex)
        tempList.append(password)
        tempList.append(pin)
        tempList.append(salt)
        tempList.append(string)
        exList.append(tempList)

    



print("error = ",  error)

with open("result.txt" , "w") as fil:

    fil.write("error = {}\n\n\n".format(error))
    fil.write("errorList = \n")

    for i in errorList:
        for j in i:
            fil.write(str(j))
            fil.write("\n")
        fil.write("\n")

    for i in exList:
        for j in i:
            fil.write(str(j))
            fil.write("\n")
        fil.write("\n")


    



#!/usr/bin/python3
input_string = ""
key_text = ""

#This program allows the user to encrypt and decrypt text based on an inputted key.


#Function to strip spaces and punctuation from inputted text. Takes the variable 'text' as an argument. Creates a list
#'characters' containing the uppercase letters of the alphabet.
#Iterates through each character in text, checking for items not found in list characters (i.e. characters besides the
#uppercase alphabet). If one is found, it is replaced in the text with an empty substring. Returns the string.

def strip_punct(text):
    #punctuation = [" ",".",",","\'","@","!","#","$","%","^","&","*","(",")","-","_","=","+","?",">","<","[","]","{","}","\""]
    characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    for item in text:
        if item not in characters:
            text = text.replace(item,"")
    return text


#Gets an input from the user for text to encrypt or decrypt. Converts to uppercase to streamline
#substitution.

#Strip_punct() is used to eliminate spaces, punctuation/special characters, and non-alphabetic characters from the input text.
#A while loop is used to ensure some text is inputted. Returns the uppercase, punctuation-stripped input_string.


def get_text():
    global input_string
    input_string = ""
    #input_string = "1"
    #while strip_punct(input_string).isalpha() == False:
    while len(input_string) < 1:
        input_string = strip_punct(input("Please enter the text to encrypt or decrypt: ").upper())
        continue
    return input_string

#Gets an input from the user to use as the cipher key. Converts to uppercase to streamline substitution.
#Strips any non-alphabetical characters before proceeding. A while loop is used to ensure some text is inputted.
#Takes variable 'text' as an argument; the length of the key_text is compared with the length of text to ensure
#a valid key has been entered. Returns the (punctuation-stripped) key string (key_text).


def get_key(text):
    global key_text
    key_text = ""
    #key_text = text + "abcd"
    #while key_text.isalpha() == False and len(key_text) > text:
    while len(key_text)<1:
        key_text = strip_punct(input("Enter a substitution key: ").upper())
        continue
        if (len(key_text) > len(text)):
            print("Invalid substitution key.")
            continue
        else:
            break
    #print(key_text)
    return key_text


#Function to find new character assignments based on the repositioned values of the alphabetized key. Takes an original key string
#and its alphabetized counterpart (key_sorted) as arguments. 
#Creates an empty list 'new_index' to store these values. Iterates through the original (unsorted) key
#text, appending each character's position (using key_sorted.index()) in the sorted key to new_index. If a value is a duplicate
#the function enters a while loop, where the counter i is set to zero and added to the value. i is incremented until the value+i is no longer
#already present in new_index, at which point it is appended to the list. New_index is then returned.

def find_index(key_text,key_sorted):
    #global key_text, key_sorted
    new_index = []
    for character in key_text:
        #print(character)
        if ((key_sorted.index(character) not in new_index)):
            new_index.append(key_sorted.index(character))
            #print(key_sorted.index(character))
        else:
            i=0
            duplicates = True
            while duplicates:
                if(key_sorted.index(character)+i) in new_index:
                    i+=1
                    continue
                else:
                    new_index.append(key_sorted.index(character)+i)
                    break
            #print(key_sorted.index(character)+1)
    return new_index
        
#Function to break text down into chunks (corresponding to the length of the key) in order to be transposed. Takes the text
#and the key as arguments. The size of each chunk is determined by finding the value of len(key).
#A list total_slice is created to store each chunk of the text.

#A mod operation is used to determine if any chunks are smaller than the length of the key. If so, they are 'padded' with the
#character 'X.'

#Until the total slice list is equal to the total number of possible chunks in the original text (obtained by dividing the length
#of the text by the size of the key), the function uses a while loop to iterate through the original text and create a new slice
#which is then appended to the total_slice list. The variable num is used (and incremented by the key size) to determine the
#start and stop locations for each slice. The list total_slice is returned.
def slice_it(text,key):
    #text = strip_punct(text)
    num = 0
    key_size = len(key)
    total_slice = []
    while(len(text)%key_size != 0):
        text = text + "X"
        continue
    
    #print(text)
    while len(total_slice)<len(text)/key_size:
        #print(len(total_slice),len(text))
        new_slice = text[num:num+key_size]
        num = num+key_size
        #print(new_slice)
        total_slice.append(new_slice)
    return total_slice



#Encryption function used to transpose individual characters in a chunk according to the positional values defined by the key. Takes a target
#chunk and the key as arguments.
#Creates two empty lists, one for the target string and one for the end result. The end result list (swap_list) is initially
#populated with placeholder characters corresponding to the length of the key. Each character in the target text
#is then appended to target_list. The function then iterates through each item in target_list, moving it to the key-defined
#position in the swap_list (the placeholder value is replaced by the new character). Finally, the function parses through each item
#in swap_list and concatenates it to the (initially empty) swap_string, which is then returned.
def swap_char(target,key):
    target_list = []
    swap_list = []
    swap_string = ""

    while len(swap_list) < len(key):
        swap_list.append("X")
        
    for character in target:
        target_list.append(character)

    #print(target_list)
    
    num = 0
    for item in target_list:
        #print(item, key[num])
        swap_list[key[num]] = item
        num += 1
        #print(swap_list)

    for item in swap_list:
        swap_string += item
    #print(len(swap_list))

    return swap_string

#Encryption function used to encrypt chunks and combine them. Takes a target (chunked) list and the key as arguments. An empty list and empty string are created. For each
#chunk in the target list, the function swap_char (defined above) is called to transpose its characters according to the key; the variable num is incremented to work through
#each character. Each encrypted chunk is added as an item to the list new_list. When every chunk has been transposed, they (as items in new_list)
#are concatenated to the empty string with a space to preserve text blocking. This string is then returned.

def encrypt(target,key):
    num = 0
    new_list = []
    new_string = ""
    for item in target:
        new_list.append(swap_char(target[num],key))
        num += 1

    for item in new_list:
        new_string += item + " "
        
    return new_string

#Decryption function used to transpose individual characters in a chunk according to the positional values defined by the key. Takes a target chunk and the key as arguments.
#The empty string new_item is created. The function works through each character in the target chunk; at each, the character found at the target index (determined by incrementing
#the value of key[num]) is concatenated to new_item. Returns the decrypted chunk new_item as a string. 

def decrypt_char(target,key):
    num = 0
    new_item = ""
    new_list = []
    
    for character in target:
        #for character in item:
        #new_list.append(swap_char(target[num], key[num]))
        new_item += (target[key[num]])
        num += 1
        #print(num,key.index(num))
        #new_list.append(new_item)
        #print(new_list)
    return new_item

#Decryption function used to decrypt chunks and combine them. Takes a target (chunked) list and the key as arguments. An empty list and empty string are created. For each
#chunk in the target list, the function decrypt_char (defined above) is called to transpose its characters according to the key; the variable num is incremented to work through
#each character. Each chunk is appended to the list decrypt_list. When every chunk has been transposed, they (as items in decrypt_list) are
#concatenated to the empty string with a space to preserve text blocking. This string is then returned.

def decrypt_list(target,key):
    decrypt_list = []
    decrypt_string = ""
    for item in target:
        #print(item)
        decrypt_list.append(decrypt_char(item,key))
        
    for item in decrypt_list:
        decrypt_string += item + " "
    return decrypt_string
    #print(decrypt_list)
        
#Main program execution. First initializes text and key strings (target_string and target_key) by calling get_text() and get_key(target_string).
#Target_key is then alphabetically arranged using the sorted() function. An index of the key's values is created using the find_index() function.
#The target string is then sliced into key-dependent chunks. These operations are all performed in a while loop, allowing the program to be restarted
#if desired.

#In a second while loop, the user is prompted to enter the desired command to perform on the text. If 'ENCRYPT' is selected, encrypt() is called
#using sliced_string and index. If 'DECRYPT' is selected, decrypt() is called with the same arguments. Output is printed to console and the program
#breaks out of the loop. After the operation has been performed, the user is prompted to quit or encrypt/decrypt a new text. If 'NEW' is entered, the program will reinitialize
#and continue.

if __name__ == '__main__':
    program_state = 1
    while program_state == 1:
        #print("init")
        target_string = get_text()
        target_key = get_key(target_string)
        #Using the sorted() function, rearrange key characters in alphabetical order. Returns the sorted characters in a list.
        sorted_key = sorted(key_text)
        index = find_index(target_key,sorted_key)
        sliced_string = slice_it(target_string,target_key)
        #print(index)
        running = True

        while running == True:
            command = input("Please enter encrypt to encrypt the text, or decrypt to decrypt the text: ").upper()
            if(command == "ENCRYPT"):
                print(encrypt(sliced_string,index))
                break
            elif(command == "DECRYPT"):
                print(decrypt_list(sliced_string,index))
                break
            else:
                print("Invalid command. Please try again.")
                continue
        commands = ["NEW","QUIT"]
        retry = ""
        while retry not in commands:
            retry = input("Enter 'NEW' to work on another text, or 'QUIT' to exit: ").upper()
            if(retry == "NEW"):
                break
        
            elif(retry == "QUIT"):
                print("Goodbye.")
                program_state = 0
                break
        
        

        
        #print(encrypt(sliced_string,index))
        #print(key_text)
        #print(index)
            
           
        
        
        



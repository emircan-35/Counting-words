"""

#ntlk is used for only getting stop words
#it could be done by hand but it would not be a professional job

#urllib is used only for reaching the web-site 

#beatifulsoup(bs4) is used to get the text of the book

#If you do not have to run this program on the IDLE (it is working on CMD or many linux terminal), please do not do that.
#Because tqdm is not efficient on the IDLE.

"""
try:
    import bs4 as bs
    from tqdm import tqdm 
    import urllib.request
    from nltk.corpus import stopwords
except ImportError:
    print("There is a problem about the modules"+
          "Your system has these modules"+
          "1-) BeatifulSoup"+
          "2-) tqdm"+
          "3-) urllib"+
          "4-) nltk (Only english stop words)")




#Getting stop words
stop_words=stopwords.words('english')

#Creating the list includes all of names of the books will be selected by the user
name_books=["book1","book2"]

#Creating a function to edit the text for starting to count
def Editing(document_coming,choice_counting):
    #Firstly, making all leters lower
    document_coming=document_coming.lower()
    
    #Creating a empty string variable to return edited text
    text_edited=""
    
    #because of working on the every letters, an list is created
    document_outcoming=[]
    
    #for reaching every letter, for loop
    for i in tqdm (range(len(document_coming)), desc="STEP 1/3 Editing book.."): 
        #Taking letter as its form in decimal
        #Decimal format is used for reachingmore readable code and a faster program
        letter=document_coming[i].lower() 
        decimal_ascii=ord(document_coming[i])
        
        #Depending on input coming the user, editing text
        if choice_counting=="1":
            if  ((decimal_ascii>96 and decimal_ascii<123)):
                document_outcoming.append(letter)
            else:
                document_outcoming.append(" ")
        if choice_counting=="3":
            if  ((decimal_ascii>96 and decimal_ascii<123)or(decimal_ascii>47 and decimal_ascii<58)):
                document_outcoming.append(letter)
            else:
                document_outcoming.append(" ")
        if choice_counting=="2":
            if  ((decimal_ascii>96 and decimal_ascii<123)or(decimal_ascii>32 and decimal_ascii<48)
                 or (decimal_ascii>57 and decimal_ascii<65)):
                document_outcoming.append(letter)
            else:
                document_outcoming.append(" ")
        if choice_counting=="4":
            if  ((decimal_ascii>96 and decimal_ascii<123)or(decimal_ascii>32 and decimal_ascii<64)):
                document_outcoming.append(letter)
            else    :
                document_outcoming.append(" ")

    
    #Checking spaces
    #Because it can be occur one more time because of \n or a table etc.
    for i in tqdm (range(len(document_outcoming)-1), desc="STEP 2/3 Editing book.."): 
        if document_outcoming[i]==" " and document_outcoming[i+1]== " ":
            #the trash letters are not deleted directly so that,
            #There is no the index out of range problem
            document_outcoming[i]=-1

    #Appending letters to text_edited variable
    for i in tqdm (range(len(document_outcoming)), desc="STEP 3/3 Editing book.."): 
        if document_outcoming[i]!=-1:
            text_edited+=document_outcoming[i]
    
    #Returning edited text
    return text_edited

#Creating a function to get the books as a text by searching
def GetBookBySearch(index_name_book):
    #A flag is created to check errors
    error=True
    while (error):
        #A list containing results of searching
        titles=[]
        main_url="https://en.wikibooks.org/wiki/Special:Search?search="
        book1_name = input("Please enter your searching for book: ")
        #Starting to make main url in a acceptable format
        for book_name_words in book1_name.split():
            main_url+=book_name_words
            main_url+="_" 
        #Try except structure is used to prevent some errors caused of the user
        try:
            #Connecting the website
            source = urllib.request.urlopen(main_url).read()
            error=False
        except UnicodeEncodeError:
            print("Do not use Turkish characters!")
            error=True
            continue
        except urllib.error.URLError:
            print("You have an internet problem, please fix it and try again")
            continue
            error=True
            
        print("Please wait, loading...")
        #Getting html codes of the web-site
        soup = bs.BeautifulSoup(source, 'lxml')        

        #Appending the result of searching to the list according to the parser class
        for title in soup.find_all(class_="mw-search-result-heading"        ):
            titles.append(title.text)        

        #In the case of nothing found
        if (len(titles)==0):
            print("\nI did not found a book its name like you said\n\nPlease do not suspect whether i am working!\n\nIf you do not believe me, go and try yourself\n")
            error=True
    
    #Showing the results to the user        
    print("\tTHE BOOK FOUNDED ARE LISTED BELOW\n\n")
    print("INDEX".ljust(30), end="")
    print("NAME\n")
    index=1
    for names_books in titles:
        print(str(index).ljust(15),end="")
        print(names_books)
        index=index+1

    #Taking the index of the book from the user
    index_book1=int(input("\nPlease enter the index of your book: "))
    index_book1=index_book1-1
    print("Please wait, loading...")
    
    #Converting main url to its initial form
    main_url="https://en.wikibooks.org/wiki/"

    #Adding the name of book wanted by the user to the list named book_name_words
    for book_name_words in titles[index_book1].split():
        main_url+=book_name_words
        main_url+="_" 
    
    #Creating the name of txt file
    text_name=""
    for book_name_words in titles[index_book1].split():
        text_name=text_name+book_name_words+"_"
        
    #Replacing / character to prevent some error 
    text_name=text_name.replace("/","_")    
    #The names of books are also added the list named all_book_names above
    name_books[index_name_book] = text_name
    
    #Opening (Creating if it does not exists) the txt file
    f=open("{0}.txt".format(text_name),"a",encoding="utf-8")
    
    #Connecting the website
    source = urllib.request.urlopen(main_url).read()
    
    #Getting the HTML codes of the website
    soup = bs.BeautifulSoup(source, 'lxml')
    
    #Taking all text to in a string variable
    text_coming=soup.find(class_="mw-parser-output")
    text_writing=text_coming.text 
    #text is used so no dealing html or css tags codes
    #But if it were not allowed, it can be done by hand thanks to syntax of html and css
    
    #Writing the book to txt file    
    f.writelines(text_writing)
    
    #Closing the txt file after writing process is done
    f.close()
    
    #Nothing returned because of no need


#Creating a function to get the books as a text
#by directly taking the name of book from the user
def GetBookByName(index_name_book):
    #A flag is created to check errors
    error=True
    #an int variable is used to understand who is next to used
    #For example printable_version, print_version or Print_version
    numb_error=0
    while(error):
        main_url="https://en.wikibooks.org/wiki/"
        if numb_error%4==0:
            book1_name_first=input("\nPleasen enter the name of your book: ")
            text_print="/Printable_version"
            book1_name=book1_name_first
            book1_name+=text_print
            print("Searching in the form of {0}\n".format(text_print))
        elif numb_error%4==1:
            book1_name=book1_name_first
            text_print="/Print_version"
            book1_name+=text_print
            print("Searching in the form of {0}\n".format(text_print))
        elif numb_error%4==2:
            book1_name=book1_name_first
            text_print="/Print_Version"
            book1_name+=text_print
            print("Searching in the form of {0}\n".format(text_print))
        elif numb_error%4==3:
            book1_name=book1_name_first
            text_print="/print_version"
            book1_name+=text_print
            print("Searching in the form of {0}\n".format(text_print))
            
            
            
        #Replacing / character to prevent some error
        book1_name.replace("/","_")

        #Starting to make main url in an acceptable format
        for book_name_words in book1_name.split(' '):
            main_url+=book_name_words
            main_url+="_" 

        #Try except structure is used to prevent some errors caused of the user
        try:
            #Connecting to web-site
            print(main_url)
            source = urllib.request.urlopen(main_url).read()
            print("Found in this format!")
            error=False
        except urllib.error.HTTPError:
            print("{0} is failed".format(text_print))
            numb_error+=1
            error=True
        except UnicodeEncodeError:
            print("Do not use Turkish characters!")
            error=True
        except urllib.error.URLError:
            print("You have an internet problem, please fix it and try again")
            error=True           
    #Getting HTML codes of website        
    soup = bs.BeautifulSoup(source, 'lxml')

    #Creating the name of txt file
    text_name=""
    for book_name_words in book1_name.split():
        text_name=text_name+book_name_words+"_"
        pass
            
    #Replacing / character to prevent some error   
    text_name=text_name.replace("/","_")
    #The name of books are also added the list named all_book_names ab
    name_books[index_name_book] = text_name
            
    #Opening (Creating if it does not exist) the txt file
    f=open("{0}.txt".format(text_name),"a",encoding="utf-8")
            
    #Writing book to the txt file
    web_site=soup.find(class_="mw-parser-output")
    f.writelines(web_site.text)
    f.close
        
    #Nothing returned because of no need    
#A function is created to count words by reading text file
def Creating_frequencies(name_book,choice_counting):
    #Creating a list for words        
    words_list=[]                
    #Creating a list for a word's how many wroten        
    words_list_numb=[]                
    #Opening the text         
    f=open("{0}.txt".format(name_book),'r',encoding="utf-8")                
    #Reading the text        
    f_read=f.read()
    f_read=Editing(f_read,choice_counting)
    

    #Taking every words in a list by using split method                    
    words_line=f_read.split(' ')                    
    #Creating a loop for reaching every words                    
    for i in tqdm (range (len(words_line)), desc="STEP 1/2 Creatin frequencies"):
        if words_line[i] not in stop_words: #meaning it not a stop words                   
            if  words_line[i] not in words_list: #meaning it is not wroten before             
                words_list.append(words_line[i])                    
                words_list_numb.append(0)   
                         
    f.close()        
    f=open("{0}.txt".format(name_book),'r',encoding="utf-8")        
    f_read=f.read()        

    #Counting every words how mant times is it used in the text
    for i in tqdm (range (len(words_line)), desc="STEP 2/2 Creating frequencies"):
        for j in range(len(words_list)):        
            if (words_line[i]==words_list[j]):        
                words_list_numb[j]+=1        
                break
            
    f.close()
    # Calling the Sorting function to put it an ordered list 
    sorted_list=Sorting(words_list_numb,words_list)
    #because it returns a tuple, assigning every list in tuple in the sorted form 
    words_list_numb=sorted_list[0]                
    words_list=sorted_list[1]

    #Returning two list, so a tuple, in the sorted format      
    return words_list, words_list_numb
    
#Creating a function to sorting two related list
#For example names and how many times is it used
def Sorting(list_numb,list_word):
    #a basic sorting algorithm, x^^2 
    for i in tqdm (range (len(list_numb)), desc="Sorting words..."):
        for j in range(len(list_numb)):
            if(list_numb[i]>list_numb[j]):        
                temp_numb=list_numb[i]        
                list_numb[i]=list_numb[j]        
                list_numb[j]=temp_numb        
                #for name        
                temp_name=list_word[i]        
                list_word[i]=list_word[j]        
                list_word[j]=temp_name  
    #Returning two list, so a tuple
    return list_numb,list_word

#Creating a function for comparing process    
def Comparing(choice,choice_counting):
        #Firstly taking how many word frequencies will be used frm the user
        how_freq=input("How many word frequencies you want to see\nIf you enter anything out of the numbers, it will taken 20 as default  ")
        try:
            how_freq=int(how_freq)
        except ValueError:
            how_freq=20
            print("it is taken 20 as default")
        how_freq+=1
        print("word counting can take a time, please wait!")
        
        #In every case, book 1 is calculated, so
        book_0 = Creating_frequencies(name_books[0],choice_counting)

        if choice=="1":
            #Comparing user input and length of list
            #so that preventing index out of bound errors
            if how_freq>len(book_0[0]):
                how_freq=len(book_0[0])
                
            print("\nBOOK 1: {0}".format(name_books[0]))
            print("NO".ljust(15),end="")
            print("WORDS".ljust(25),end="")
            print("FREQ_1".ljust(0))
            for i in range(how_freq):
                print(str(i).ljust(15),end="")
                print(book_0[0][i].ljust(25),end="") 
                print(str(book_0[1][i]).ljust(0))
    
    
        if choice=="2":
            #Now, book 2 will be calculated
            book_1=Creating_frequencies(name_books[1],choice_counting)
            
            #Comparing two list
            common_freq=[]
            common_freq_numb=[]
            for i in tqdm (range (len(book_0[0])), desc="Comparing two book, please wait.."):
                for j in range(len(book_1[0])):
                    if  book_0[0][i]==book_1[0][j]:
                        common_freq.append(book_0[0][i])
                        common_freq_numb.append(book_0[1][i]+book_1[1][j])
                        
            #Sorting common
            sorted_common=Sorting(common_freq_numb,common_freq)
            common_freq_numb=sorted_common[0]
            common_freq=sorted_common[1]
            
            #For distinct words, creating a list
            distinc=[]
            distinc_numb=[]
            for i in tqdm (range (len(book_0[0])), desc="Comparing two book, please wait.."):
                if book_0[0][i] not in book_1[0]:
                    distinc.append(book_0[0][i])
                    distinc_numb.append(book_0[1][i])

            #For other distinct words, creating other list
            distinc_1=[]
            distinc_numb_1=[]
            for i in tqdm (range (len(book_1[0])), desc="Last steps, please wait..."):
                if book_1[0][i] not in book_0[0]:
                    distinc_1.append(book_1[0][i])
                    distinc_numb_1.append(book_1[1][i])
                    
            #Attention! Distinct lists were not sorted, because they had already sorted...
                    
            #Comparing user input and length of list
            #so that preventing index out of bound errors
            if how_freq>len(common_freq):
                how_freq=len(common_freq)
                print("The length of list is limited as {0}".format(len(common_freq)))

                    
            print("\nBOOK 1: {0}".format(name_books[0]))
            print("BOOK 2: {0}".format(name_books[1]))
            print("COMMON WORDS\n",end="")
            print("NO".ljust(5),end="")
            print("WORD".ljust(10),end="")
            print("FREQ_1".ljust(10),end="")
            print("FREQ_2".ljust(10),end="")
            print("FREQ_SUM".ljust(5))
            
            for i in range(how_freq):
                print(str(i).ljust(5),end="") 
                print(common_freq[i].ljust(11),end="")
                print(str(book_0[1][i]).ljust(11),end="")
                print(str(book_1[1][i]).ljust(11),end="")
                print(str(common_freq_numb[i]).ljust(5))

                
            #Comparing user input and length of list
            #so that preventing index out of bound errors
            if how_freq>len(distinct):
                how_freq=len(distinct)
                print("The length of list is limited as {0}".format(len(distinct)))



            print("\n\nBOOK 1: {0}".format(name_books[0]))
            print("DISTINCT WORDS")
            print("NO".ljust(5),end="")
            print("WORD".ljust(17),end="")
            print("FREQ_1")
            for i in range(how_freq):
                print(str(i).ljust(5), end="")
                print(distinc[i].ljust(18),end="")
                print(str(distinc_numb[i]))

            #Comparing user input and length of list
            #so that preventing index out of bound errors
            if how_freq>len(distinct_1):
                how_freq=len(distinct_1)
                print("The length of list is limited as {0}".format(len(distinct_1)))
 
            print("\n\nBOOK 2: {0}".format(name_books[1]))
            print("NO".ljust(5),end="")
            print("WORD".ljust(17),end="")
            print("FREQ_1")
            for i in range(how_freq):
                print(str(i).ljust(5),end="")
                print(distinc_1[i].ljust(19),end="")
                print(str(distinc_numb_1[i]))          
        
    
#Creating main function to control everyting
def Main():
    print("! ! !WELCOME TO THE E-BOOK ANALYSIS PROGRAM! ! !\n".center(100," "))
    while(True):
        print("\n1-) Analyze 1 bok\n"+
            "2-) Analyze 2 books and compare them\n"+
            "3-) Exit\n")
        #Taking what does user want in a numeric form
        #There and below, when takin an input from the user
        #string type is used to prevent some error
        choice=input("Please enter what do you want as numerically:")
        
        #Checking coming input is right 
        while (choice!="1" and choice!="2" and choice!="3"):
            choice=input("Please enter a valid number: ") 
        if choice=="3":
            exit()
        
        print("\n1-) Only Words > RECOMMENDED\n"+
            "2-) Words and Symbols\n"+
            "3-) Words and numbers \n"+
            "4-) Words, numbers and symbols\n"+
            "\nATTENTION: Every options counts also words\n")
        #An option depends the user, taking it from the user
        choice_counting=input("Please enter what do you want as numerically:")
        
        #Checking coming input is right 
        while choice_counting!="1" and choice_counting!="2" and choice_counting!="3" and choice_counting!="4":
            choice_counting=input("Please enter a valid number:")

    
        if choice=="1":
            print("\n1-)Get The Book By Searching In WikiBooks\n"+
                "2-)Get The Book by directly the name of book\n")
            choice_2=input("Please enter what do you want as numerically:")
            while (choice_2!="1" and choice_2!="2"):
                choice_2=input("Please enter a valid number: ")

            if (choice_2=="1"):
                #Calling a function created above to get the book as a txt file
                GetBookBySearch(0)
            elif(choice_2=="2"):
                #Calling a function created above to get the book as a txt file
                GetBookByName(0)
                
            #Calling comparing function to show the user the results
            Comparing(choice,choice_counting)    
        elif choice=="2":
            #A for loop, to get 2 book
            for i in range(2):
                print("\n1-)Get The Book By Searching In WikiBooks\n2-)Get The Book by directly the name of book")
                choice_2=input("Please enter your choice: ")
                while (choice_2!="1" and choice_2!="2"):
                    choice_2=input("Please enter a valid number: ")    
                if (choice_2=="1"):
                    #Calling a function created above to get the book as a txt file
                    GetBookBySearch(i)
                elif(choice_2=="2"):
                    #Calling a function created above to get the book as a txt file
                    GetBookByName(i)  
            #Calling comparing function to show the user the results
            Comparing(choice,choice_counting)


#The program starts
#and does not end unless user wants 
Main()

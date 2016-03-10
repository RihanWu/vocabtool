# VocabTool developer documentation

This program consists a core module and other peripheral modules. We try to make all the modules interchangeable and extendable so that we can have different user interfaces, different dictionary-source modules, and different database/latex interfaces.

## Program logic

### Initialize
When the program starts, the core module reads configurations from the config file and use them accordingly. It then load dictionary sources that are enabled according to the setting.

### Look up words
* The user interface passes requests to the core module.  
* The core passes the requests to all the loaded dictionary sources(Web page, API, Local dictionary, local database).  
* The dictionary modules return dictionary entries along with methods to generate formated text with or without tags.  
* The core collect the results and passes them to the user interfaces  
* The user interfaces display the result according to their need.

### Store result to database
* The user interface initialize a request and tell core.
* Core passes the current word to database interface module.
* Database interface module uses the method included in the data to generate database friendly entries and store them into database.

### Generate \(\LaTeX\) files and create PDF
* The user interface starts a request and tell core.
* According to the request, core tells the database to extract stored data.
* Core passes the data to the generate module.
* The generate module generate \(\LaTeX\) files and create PDF accordingly.

## Basic data structure

**Entry**  
Store info of a word that is one part of speech.
* pronouciation (*string*)
* sound (*string*) -- containing URL or path of sound file
* pos (*string*) -- part of speech
* separation_storage (*bool*) -- Whether the explantion and the example sentences are stored side by side or separately
* explanation (*list*)

**SuperEntry**  
Store explanations of a word that may be different part of speech.
* valid (*bool*) -- Whether the result is valid
* source (*string*) -- ID of the source
* source_name (*string*) -- Name of the source
* word_text (*string*) -- The word or expression contained
* entries (*list*) -- List of entries (*Entry*)

# A'mas'kan to English Live Translator
This repository includes all of the code for our live translator that converts speech in A'mas'kan to text in English.  

To get the translator up and running, there are some dependecies you will need to install.  

These include the following packages:  
1. datasets  
2. transformers  
3. torch  
4. tkinter  
5. threading  
6. sounddevice  
7. numpy  
8. queue  
9. PIL  

You can install these by typing them directly into terminal/cmd or through an IDE (like Pycharm)  

To run our prototype translator:  
1. Install the fiftyWordTunedWhisper model in this repository as well as the GUI (Graphical User Interface) file  
2. Open the GUI file in Pycharm (or other IDE) and set the model path to YOUR path for the model (where it downloaded)  
3. Run the GUI file and if all dependencies are there, you should have a 25 word A'mas'kan to English Translator!  

If you wish to train Whisper on all A'mas'kan words or even your own conlang's lexicon:  
1. Install the FINALTRAIN file and GUI file from this repository and open them in Pycharm  
2. In cd Desktop, create a folder named data, in this, you will put both audio recordings and their mapping to english translations  
   Your folder should be formatted accordingly:  
   Data  
     |--- Audio1.wav (audio files)  
     |--- Audio2.wav  
     |--- Metadata.jsonl (a txt file that maps audio to translations), This should look like the 50 word example we have posted in this repository  
3. Make sure all paths refer to YOUR CUSTOM paths in the training file (it is very obvious which path goes where) and run the script  
   This step consumes a lot of power, depending on how many words, but having a strong GPU is highly recommended  
4. After you do this, a model should pop up in cd Desktop and you can input its path into the GUI file  
5. Run the GUI file and you should have a custom translator!  

On a side note, if anyone out of genuine curiosity or interest decides to create a tuned Whisper model for all A'mas'kan words, please create a pull request asking that model to be added to MASTER, so anyone can use it

To learn about our English to A'mas'kan translator, click on the EnglishToA'mas'kan.md file!

Thank you and have fun conlanging!


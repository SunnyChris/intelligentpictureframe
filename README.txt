Code sample of an intelligent picture frame:

The digital picture frame is a windows based tablet screen that enables following functions using scripts to control the front camera:

•	Motion detection to activate the screen
•	Face detection
•	Voice output to greet recognized people at defined times of the day

The source code comes from various internet sources and has been modified for the present application example of the picture frame. Since it is a hobby project, 
no source information is given here. The code is mainly written in python and can be divided in four parts that enable the screen to run properly:

•	Training script to train the model, here a CV2 algorithm is used as face recognizer, training images must be saved in the local folder "images" (Python)
•	Windows control script to control and run the main script (Python)
•	Main script to run the described functions (Python)
•	Helper script to activate the screen using windows keyboard keys (VBS)

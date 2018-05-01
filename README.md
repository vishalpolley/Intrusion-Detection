# Intrusion Detection System

Implementation of Intrusion Detection System based on Python and OpenCV.

## Requirements

* [Python 3.3+](https://www.python.org/downloads/)

* [dlib library](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)

## Set Up

* Firstly clone/download the project from [here](https://github.com/vishalpolley/Intrusion-Detection/archive/master.zip)

* Open terminal / cmd and navigate to the project folder.

* Install all the dependencies required for the project.

  (If you are on Linux/MacOS platform run the command with `sudo` privileges)
```
pip install -r requirements.txt
```

## Running the Project

### **Step 1: Training the Model**

* To train the model with your face images, run
```
python3 capture.py
```

* Now to capture your face press `c` key.

  (If no face detected you will be prompted on the terminal / cmd)

* Now, you will be prompt to enter your name, on the terminal / cmd.

  (If the image name is already present / exists, you will be prompt to enter another name or overwrite the existing entry for the image)

* After this, training the model for your image gets completed.

### **Step 2: Detection of any Intrusion**

* For detecting any instrusion, run the script
```
python3 script.py
```

* The image window will display the person's name, if that face exits in the database, and the system will prompt `Permission Granted !!` message.

* Else if the face does not exits in the database, the image window will display `Unknown` with the face, and will prompt `Permission Denied !!` message.

* To exit the process press `q` key.

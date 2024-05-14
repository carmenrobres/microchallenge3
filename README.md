# Microchallenge III: Embodying Surveillance
![IMG_4076](https://hackmd.io/_uploads/BkBu4ebX0.jpg)


Contributors: 
Carmen - https://carmenrobres.github.io/portfolio/
Anna - https://annafedele.github.io/mdef/

## Initial idea / Concept of the Project

Our project aims to create a comprehensive experience centered around embodying surveillance through a wearable device. We seek to develop a tool capable of monitoring others and detecting signs of aggression from individuals in close proximity.

In the era of surveillance capitalism, cameras are ubiquitous. Various nations utilize these cameras to surveil and monitor citizens, tracking behaviors such as walking patterns and aggression to maintain urban safety. While these data-driven analyses through machine learning hold potential societal benefits, they remain inherently reliant on statistical behavior and lack 100% reliability.

Despite constant surveillance, many individuals have normalized it and exhibit apathy towards it. However, what if the roles were reversed, and we became the surveillers? What if they were aware of us watching them? This is the concept underlying our wearable technology.

Our wearable aims to raise awareness about surveillance and prompt others to recognize that they are being observed. Moreover, it serves as a protective tool. By wearing a device that monitors our surroundings and alerts us to nearby individuals displaying aggression or encroaching on our personal space, can we feel safer? Is this the optimal solution for our needs?


### Interaction Description
The idea is to make a personification of a 'human' surveillance camera that detects other bodies or potentially aggressive attitudes.

The wearable is going to have a camera and a proximity sensor that detects other bodies and potential attitudes and then reacts through sound and an LED. It will also have an artistic display where all the inputs connect and showcase what the wearable si sensing live.

![system (1)](https://hackmd.io/_uploads/BkQPD9yQC.jpg)

### Research References

> []ANNA

### Purpose

- Create a comprehensive experience centered around embodying surveillance through a wearable device.
- Raise awareness about surveillance and prompt others to recognize that they are being observed.
- Serve as a protective tool by alerting the wearer to nearby individuals displaying aggression or encroaching on personal space.
- Utilize a combination of a camera and proximity sensor to detect other bodies and potential aggressive attitudes.
- React to detected behaviors through sound and LED indicators.
- Develop a wearable capable of monitoring others and detecting signs of aggression from individuals in close proximity.
- Train a model to detect body language and if the body is being aggressive.
- Incorporate an artistic display to showcase real-time sensory inputs and enhance the wearable's aesthetic appeal.


### Integrated Design
> []ANNA


### Honest Design
This project leverages technology in a meaningful and socially conscious manner. By addressing the pervasive issue of surveillance in modern society, the wearable device serves as a thought-provoking intervention, making critical reflection on the implications of constant monitoring and observation. Rather than perpetuating the status quo of passive acceptance towards surveillance, this project empowers individuals to actively engage with and question the dynamics of surveillance capitalism.

Moreover, the design of the wearable device is inherently transparent and user-centric. Through the integration of a camera and proximity sensor, the device provides real-time feedback about surrounding individuals and potential threats, fostering a sense of agency and awareness in the wearer. By employing sound and LED indicators, the device communicates detected behaviors in a clear and accessible manner, ensuring that users can make informed decisions about their safety and well-being. This transparency and user empowerment facilitates meaningful interactions with technology that prioritize human values and ethical considerations.


### Design Boundaries
This project presented several challenges due to the integration of Machine Learning and TouchDesigner. We had no prior experience training a model or utilizing Python with mediapipe, making this aspect of the project particularly demanding. Additionally, our lack of familiarity with TouchDesigner posed its own set of difficulties, requiring us to quickly learn and adapt to a new software platform.

Furthermore, the physical construction of the wearable device, such as sewing the vest and integrating electronics, proved to be a formidable task. Despite our prior experience with Arduino and OSC communications from previous microchallenges, the complexity of creating a fully functional wearable piece added another layer of difficulty. Despite these challenges, we approached each obstacle with determination and perseverance, ultimately overcoming them through collaborative problem-solving and continuous learning.


##  Project planning

![image](https://hackmd.io/_uploads/rJzC-h1mA.png)

---

## Process

### Design Process

We divided our work into two main inputs: Anna focused on developing the wearable and Arduino circuit, while Carmen tackled the machine learning and model training. We collaborated closely on TouchDesigner to craft the appropriate artistic representation, pooling our expertise to create a cohesive and impactful final product.

**Testing Different Cameras**

Our first focus of the Design Process was to find a wearable camera that could send good quality live feed to our computer. So the requirements for the camera had to be:

- Good quality
- Small enough that it could fit in a wearable
- Give live video that could be used on python

Our first trial was with the ESP32 Xiao Camera that was able to give us a good quality image and was small enough for the wearable. Unfortunately, when we connected the camera to the Machine Learning code, the camera would freeze.

*ESP32 XIAO CAMERA:*
![IMG_4030](https://hackmd.io/_uploads/Skn0BxW7R.jpg)

After exploring various Arduino cameras, we ultimately opted to utilize our own phones as webcams for this project. The other cameras we considered either had very low quality or were difficult to program.

To achieve this setup, we employed two programs: CamoStudio and OBS Studio. CamoStudio is a mobile app that needs to be installed on both the phone and the computer. Its function is to connect the phone's camera as a webcam on the computer. Subsequently, with OBS, we configured the live feed from the phone to be accessible as a camera source, allowing our Python code to utilize it for drawing skeletons and analyzing poses through Mediapipe.

*CamoStudio & OBS Studio Platforms:*
![Captura de pantalla 2024-05-14 163450](https://hackmd.io/_uploads/BkchLebmA.png)



**Explored Machine Learning**
After setting up our camera, we delved into Machine Learning tools. Following various YouTube tutorials (linked in the references), we experimented with face, hand, and body recognition using Python and Mediapipe.

Our initial focus was on analyzing body movements to detect different actions. To accomplish this, we began by researching body language and signs of aggressiveness:

The tells of aggressive body language include:
>- Hands and Arms: Always keep a close eye on the hands, as they can indicate a potential threat. Balled fists show aggression, but also watch for crossed arms or hands in pockets, which can signal hidden intentions.
>- Legs and Feet: Pay attention to the person's stance, especially if they blade themselves towards a perceived threat. This combat-style stance, with one foot behind the other, can indicate readiness for action, especially if they are concealing a weapon on the bladed side.
> - The Whole Package: Be alert for movement warning signs like pacing or standing on the balls of their feet. Pacing may precede an attack, while standing on the balls of their feet could signal readiness for flight or escape.


After conducting our research, our initial approach was to develop a model that could detect specific hand and arm movements associated with aggressiveness, such as open or closed hands, arm angles, and arm positions relative to the torso. This served as our first attempt to determine aggressiveness based on body language, providing a general probability score.

![Machinelearning1](https://hackmd.io/_uploads/rk19HgbQ0.jpg)

However, we encountered several challenges. The model proved to be overly general, often misinterpreting harmless gestures as aggressive behavior. Additionally, when we prompted individuals to display aggressive behavior, their actions did not always align with the predefined criteria outlined in our research.

From this initial exploration, we drew two key conclusions:

- Assessing aggressiveness based on individual frames is inherently difficult, and a more holistic approach considering actions over time may be more effective.
- Training a model using videos of various actions to distinguish between aggressive and non-aggressive behavior would likely yield more accurate results.
- Our first code is not enough to generate a right conclusion of aggressiveness.


That led us to our second approach: **Machine Learning**. We created two videos capturing various instances of aggressive and non-aggressive behavior, each approximately 2 minutes long. The process involved the following steps:

1. Utilize our "importcsv.py" code to analyze each video frame-by-frame using MediaPipe. This code saved the position of the body skeleton in each frame to a CSV file, categorizing them as either "AGGRESSIVE" or "NORMAL".


![image](https://hackmd.io/_uploads/H1ZO5MZQR.png)


2. Train our machine learning model to distinguish between the two categories using the "training.py" script.
3. Implement our model into the "FINAL.py" code, which reads the camera feed and determines whether the body movements detected are aggressive or not, providing an accuracy measure.


![GIF-2024-05-13-17-41-46](https://github.com/carmenrobres/microchallenge3/assets/145042059/efe91741-4a3f-4c4d-8098-9ddc15b735c7)


Our final conclusion resulted in a prototype model capable of determining whether a person's actions were aggressive or not. This model was trained to recognize specific aggressive gestures such as giving the finger, slapping, or punching, as well as normal behaviors like having hands open and walking normally.

However, three main challenges remained with the model:

- The training data was collected using a steady camera in a fixed position. This meant that when the model was applied to real-world scenarios where the camera or wearer was in motion, its accuracy decreased.
- Aggressiveness is not solely determined by individual frames but rather by the overall action. Consequently, the model occasionally misclassified poses because it could not predict subsequent movements, only identifying potentially aggressive poses.
- Aggressiveness is subjective, making it challenging to detect accurately, as it varies depending on context and interpretation.
  
![GIF-2024-05-13-17-42-27](https://github.com/carmenrobres/microchallenge3/assets/145042059/420c11d3-fa3d-427e-b344-db5eb708ccb5)


Finally we sent the data recollected as AGGRESSIVE or NORMAL and % accuracy through osc to TouchDesigner.

![GIF-2024-05-13-17-43-24](https://github.com/carmenrobres/microchallenge3/assets/145042059/0291c934-8650-43cd-91c8-010a6729b813)


**TouchDesigner**

Once we had all of the INPUTS designed and working, we sent all the info through OSC to touchDesigner....
**GIF 3** - All together
GIF-2024-05-13-17-43-24


**Arduino**
Day 1:
Create arduino circuit

Day 2:
Test wearable

Day 3: Wearable 
> []ANNA - explain the process (?)



---

### Fabrication process: Wearable
(How did you fabricate)
> []ANNA


### Digital System
> []ANNA

(illustration explaining function parts and protocols)

### Code: Machine Learning

For the final product we used 3 specific codes made with python. These codes are used to make the Machine Learning Model with pose and hand recognition.

**Reading skeleton**
The script performs real-time pose estimation and gesture recognition on a video file, extracting landmark coordinates and visualizing them, while also allowing user interaction to quit the processing loop.

What it does is read every frame, it processes each frame of the video using the MediaPipe Holistic model to detect landmarks for the face, pose, left hand, and right hand. It extracts landmark coordinates and exports them to a CSV file for further analysis.


**Training Model**
This code was not authored by us; it utilizes a pre-trained machine learning model, specifically a Random Forest Classifier. Here's an overview of how it works:

- Setting up the prediction model: Initially, a logistic regression model is established for prediction.

- Data processing: The script reads data from a CSV file, extracting only the numeric coordinates. This data is then split into two parts: one for training the model and the other for testing its performance.

- Training the model: Different methods (or pipelines) are set up to train the model. Each method involves preparation steps and a specific learning approach. The model is trained using these methods to determine their effectiveness.

- Evaluation: The trained models are tested to assess their performance. The method that yields the best results is selected as the base learning model and saved for future us

**Diagnostic**
The last code is the Detection Model. It performs real-time body language prediction using hand and body landmarks detected from the live camera feed, visualizes the detected landmarks and predicted body language, and allows the user to quit the processing loop.

*Diagrams of each code*
![CODE (1)](https://hackmd.io/_uploads/S1-vKQb7C.jpg)



### TouchDesigner
> []ANNA




### Materials and technologies needed (BOM)
> []ANNA - make it cuter?

Speaker which one?
Barduino
Proximity Sensor
LED stripe

Computer
Phone
APPS:
 - TouchDesigner  - with MediaPipe
 - Camo Studio
 - OBS Studio
 - Python - with MediaPipe

---


## Learning outcomes

### Results & Problems Ecountered

In our project, we encountered several issues. 
- Firstly, the Arduino cameras didn't function properly, which was frustrating. We had to test 4 different cameras until we finally decided to use the phone as a webcam.
- Additionally, while the Arduino circuit worked initially, it failed to operate when connected to a powerbank. We spent a whole day troubleshooting, trying different Arduinos and components, only to realize it was a simple coding issue. The Arduino was programmed to send messages, but the power bank couldn't interpret them, causing a continuous loop of the same output.
- Moreover, we faced challenges with machine learning, as it's a complex field, especially for beginners like us. We realized the need to enhance our models by adding more datasets.
- Another hurdle was encountered with TouchDesigner, where documents weren't saving correctly. This became evident during our presentation when the document failed to open properly. We suspect that the abundance of OSC messages disrupted the program, preventing it from saving correctly.

### Reflection
We believe this project encapsulates what we've learned in MDEF so far. It showcases our exploration of wearables, delves into Arduino, and highlights our efforts in device communication—a skill we've been honing throughout the year. This project not only reflects our workflow but also improves certain aspects we hadn't fully addressed in previous microchallenges.

However, there are areas for improvement. While our wearable prototype is a good start, it doesn't evoke the sense of being under surveillance, as some feedback suggested. Additionally, delving into machine learning proved challenging. Understanding it better is crucial, as it's a tool often used in surveillance and thus integral to our critique. Yet, creating a reliable dataset, especially for subjective concepts like aggression, remains difficult.

Despite these challenges, we're satisfied with our exploration. We've learned a great deal, culminating in this final microchallenge where we expanded our knowledge of familiar elements and delved into machine learning, wearables and Touchdesigner.


### Future outcomes & what we could improve

1. Enhance Machine Learning: Instead of determining aggression based on individual frames, the tool should understand it as a collective of frames. This would require providing the model with a broader dataset that captures the progression of aggression over multiple frames. Currently, the tool struggles to differentiate between a greeting gesture and a potential threat.
*These are both considered as aggressive*
![EXMAPLE](https://hackmd.io/_uploads/BJwevEZ70.jpg)

2. Integrate Facial Recognition: Adding facial recognition would provide valuable context to the assessment of aggression. By analyzing facial expressions, the system could better discern intent. For example, detecting an angry facial expression alongside aggressive body language would raise the likelihood of an imminent attack.

3. Make the Wearable More Impactful: We aim to make the wearable device more dynamic and engaging. One enhancement would be to enable it to receive messages from the machine learning system and change color accordingly when detecting aggression. Additionally, we'd like to augment its visual impact, possibly by adding more cameras or reactive elements to evoke a heightened sense of surveillance and overwhelm. While primarily an artistic reflection tool, the wearable could also serve as a means of self-protection. For instance, it could dispense water as a dissuasion against perceived threats.

4. Improve TouchDesigner Implementation: As relative beginners with TouchDesigner, we acknowledge the need to refine our design to better convey the desired impact. Our goal is to create a more aggressive and impactful visual presentation that aligns with the overarching theme of surveillance and reflection.




### Final Product
> []ANNA - picture wearable on
![IMG_4076](https://hackmd.io/_uploads/BkBu4ebX0.jpg)




### References and Resources
PoseNet
https://github.com/tensorflow/tfjs-models/tree/master/posenet


MediaPipe
https://github.com/nicknochnack/MediaPipePoseEstimation/blob/main/Media%20Pipe%20Pose%20Tutorial.ipynb
https://github.com/nicknochnack/Full-Body-Estimation-using-Media-Pipe-Holistic

https://www.youtube.com/watch?v=We1uB79Ci-w
https://www.youtube.com/watch?v=06TE_U21FK4
https://github.com/nicknochnack


OpenPose
https://medium.com/@samim/human-pose-detection-51268e95ddc2
https://github.com/CMU-Perceptual-Computing-Lab/openpose

TOUCHDESIGNER
https://www.youtube.com/watch?v=iynrn58-sXc
https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python
https://www.youtube.com/watch?v=WS2Ww6zYgJw
https://www.youtube.com/watch?v=NnrWjQ_zO-s
https://www.youtube.com/watch?v=qRTRJziqoJk
https://www.youtube.com/watch?v=X4rlC6y1ahw

ESP32 CAMERA
https://www.youtube.com/watch?v=8h0iweM5Ngo
https://www.instructables.com/XIAO-ESP32-S3-Handheld-Camera-Pocket-Edition/

AGGRESSIVE BODY LANGUAGE
https://www.ftcollinsmartialarts.com/5-body-language-signs-that-indicate-aggression/
https://www.scienceofpeople.com/aggressive-body-language/#:~:text=Do%20you%20know%20the%20telltale,nostril%20flaring%20can%20indicate%20anger.

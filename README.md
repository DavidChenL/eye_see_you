# eye_see_you
A face recognition security system

## Inspiration
Make MLDA@EEE more AI-savvy! We had dreamed of a computer vision for door access control for a long time. Now it's time to implement it!

## What it does
We built a hardware system that could detect (and classify) multiple faces in one frame.

## This model can detect multiple person in the same frame
Door will only open with the right person detected
High accuracy with 90 % True Positive and less than 2 % False Positive
Can easily tune the model for security or convenience
How we built it
We proposed a hardware system based on Raspberry Pi running on Python to detect (and classify) faces. The Raspberry Pi board was connected to a motor that presses door switch to release access. A LED light band is connected to the board, to indicate the validity of the detected faces.

## Challenges we ran into
The computing capacity of a single Raspberry Pi is quite limited, which doesn't support high refresh rate detection. We resolved this issue by restricting the resolution to free the computing power.

## Accomplishments that we're proud of
This real-time detection model runs on Raspberry Pi
High accuracy with 90 % True Positive and less than 2 % False Positive
Secure model that can be iterated to finetune further
What's next for Eye See You
We plan to finetune the model to make it fit for more scenarios of various light ambience.

## Built With
python
raspberry-pi

## Run it on your raspberry-pi board
You need a raspberry-pi board, with a high-res webcam, a motor, and a LED light band to implement the system.
Copy open.py to your raspberry-pi board, and run
'sudo python3 open.py'

## Learn more at our Devpost page! (https://devpost.com/software/eye-see-you-28nb1x)

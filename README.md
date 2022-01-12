# TSA Bot
This repo contains sample code for TSA bot at Reinvent 2021- AWS Builder's Fair. The project sample code is intended to help you replicate what you may have seen in a Builder's Fair project demo at an event, and to set up AWS infrastructure for further experimentation.

## Overview 
T. S. A. Bot is a humanoid robot, that can **assist** with the security screening process at the airport. The bot is powered by AWS to showcase how you can use AWS services to solve everyday challenges. 

Below is the demo from reinvent 2021 on how TSA bot can help with airport screening process:

https://user-images.githubusercontent.com/19521063/149061793-9b15dce8-66a6-467c-b3db-26b4bbcc3083.mov

### Workflow
The TSA bot continously provides instructions on the correct screening procedure (what items can you carry vs need to put in a bin). Passenger can ask questions like "Do I need to remove my jacket?" or  "Do I need to remove my belt?" "When is the next flight to Boston?" and bot responds with an answer. Passenger can also ask if they can carry a specific object and bot recognizes the object and respond.

For question and answers, the bot uses Amazon Lex service. For getting flight info, bot fetches the results from DynamoDB that is storing daily flight from an external API. For detecting object , the bot uses Amazon Rekognition

Exhaustive list of questions available on the git repository in the List of QnA/Questions-EN-ES.md file.


## Architecture

<img src="images/TSABot-FinalArchitecture.png">



### Hardware

| Item      | Description |
| ----------- | ----------- |
| <p align="center"><img src="https://m.media-amazon.com/images/I/81rm-QULFpS._AC_SL1500_.jpg" width="15%"> </p>    | The Bot is currently based on the [STEM Robot-Building Kit made by Meccano<sup>&reg;</sup>](https://www.amazon.com/Meccano-Meccanoid-Robot-Building-Education-Exclusive/dp/B019K8KMHS/ref=asc_df_B019K8KMHS/) and we customized it by using our own servo motors and LEDs |
- I2C board for servo motors:  [https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c) I2C is used to connect 8 servo motors to move hands and neck  
| <p align="center"><img src="https://m.media-amazon.com/images/I/71IOISwSYZL._AC_SL1400_.jpg" width="25%"> </p> | We use a [Raspberry Pi 4](https://chicagodist.com/products/raspberry-pi-4-model-b-4gb?src=raspberrypi) that will be our edge compute resource to control the robot and scripts, and will communicate back to the AWS cloud for text to speech, speech to text, computer vision, and the QnA solution.   |
- USB serial for lidar sensor:  [https://www.amazon.com/gp/product/B00LODGRV8/ref=ppx\_yo\_dt\_b\_asin\_title\_o02\_s00?ie=UTF8&psc=1](https://www.amazon.com/gp/product/B00LODGRV8/ref=ppx\_yo\_dt\_b\_asin\_title\_o02\_s00?ie=UTF8&psc=1)    
- Microphone (support Cardioid for directional use case):  [https://www.amazon.com/Blue-Yeti-USB-Microphone-Blackout/dp/B00N1YPXW2/ref=sr\_1\_26?keywords=microphone+directional&qid=1637296149&sr=8-26](https://www.amazon.com/Blue-Yeti-USB-Microphone-Blackout/dp/B00N1YPXW2/ref=sr\_1\_26?keywords=microphone+directional&qid=1637296149&sr=8-26)    
- Speaker: [https://www.amazon.com/JBL-Waterproof-Portable-Bluetooth-Speaker/dp/B07Q6ZWMLR/ref=sr\_1\_14?keywords=speaker+with+jack+jbl&qid=1637296361&sr=8-14](https://www.amazon.com/JBL-Waterproof-Portable-Bluetooth-Speaker/dp/B07Q6ZWMLR/ref=sr\_1\_14?keywords=speaker+with+jack+jbl&qid=1637296361&sr=8-14)  
- LidaR sensor: [https://www.amazon.com/gp/product/B075V5TZRY/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1](https://www.amazon.com/gp/product/B075V5TZRY/ref=ppx\_yo\_dt\_b\_asin\_title\_o03\_s00?ie=UTF8&psc=1)  
- Raspberry cam: [https://www.amazon.com/Raspberry-Pi-NoIR-Camera-Module/dp/B01ER2SMHY/ref=sr_1_3?keywords=raspberry+cam+noir&qid=1637296656&sr=8-3](https://www.amazon.com/Raspberry-Pi-NoIR-Camera-Module/dp/B01ER2SMHY/ref=sr_1_3?keywords=raspberry+cam+noir&qid=1637296656&sr=8-3)  


## Repository structure

| Folder | Purpose | 
| --- | ---
| /docs/   | Project Documentation |
| /images/   | Project Images |
| /QnA/   | List of questions and answers to import |
| /cloudformation-templates/ | Deployment templates for TSA Bot components|
| /tsa-full/ | TSA Bot scripts and configurations to be deployed on the Raspberry Pi |

# Install the TSA Bot solution
## Getting started (step by step)

Follow the step by step deployment instructions in this [getting started documentation](Docs/GettingStarted.md). This describes how to deploy the resources locally on the bot, and resources in the cloud.
  
More details about servo motors and configuration [here](Docs/TSA-Bot-ServoMotors-details.md)


## Security
See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.

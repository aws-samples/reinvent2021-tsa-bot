# TSA Bot - AWS Builders Fair 2021 

## Overview of the AWS TSA-Bot solution

T. S. A. Bot is a humanoid robot that can **assist** with the security screening process at the airport. Before you pass through the checkpoint, the bot provides instructions on what items you can’t carry and remind you on the correct procedure. This enhance the travelers' experience by asking questions and allows the T.S.A agent to focus on screening and more than anything increase security.

The main user interaction is done with TSA Bot as soon as the user comes in front of it within 6 feets. Then the passenger can ask questions that are taken from the TSA FAQs and also ask if they can bring specific item.

Examples : *Hi, I am T.S.A. Bot, How can I help you?*  
- Do I need to remove my jacket?  *Bot anwsers*  
- Do I need to remove my belt?  *Bot anwsers*  
- Can I bring a water bottle?  *Bot anwsers*  
- When is the next flight to Boston?  *Will fetch results from DynamoDB that is storing daily flight from an external API*  
- Can I bring this? *Will trigger an image capture and start labels recognition*

Exhaustive list of questions available on the git repository in the List of QnA/Questions-EN-ES.md file.

**TSA Bot is an example of what can be done. The bot can be adapted to any use case, helping customers at re:Invent 2022, or at a retail store, hospital, or within any other industry vertical**

### TSABot videos (re:Invent 2021)
 - [Promo video for TSA Bot pre re:Invent](https://2021-tsabot.s3.amazonaws.com/TSABot-PromotionVideo-reInvent21.mp4)
 - [Interactive Demo at re:Invent Builders Fair booth](https://2021-tsabot.s3.amazonaws.com/TSABot-InteractiveDemo-reInvent21.mp4)


## The TSA Bot Architecture

<img src="images/TSABot-FinalArchitecture.png">



### Requirements

| Item      | Description |
| ----------- | ----------- |
| <p align="center"><img src="https://m.media-amazon.com/images/I/81rm-QULFpS._AC_SL1500_.jpg" width="15%"> </p>    | The Bot is currently based on the [STEM Robot-Building Kit made by Meccano<sup>&reg;</sup>](https://www.amazon.com/Meccano-Meccanoid-Robot-Building-Education-Exclusive/dp/B019K8KMHS/ref=asc_df_B019K8KMHS/) and accessible online. It is 4ft tall and can move head and arms. |
| <p align="center"><img src="https://m.media-amazon.com/images/I/71IOISwSYZL._AC_SL1400_.jpg" width="25%"> </p> | We use a [Raspberry Pi 4](https://chicagodist.com/products/raspberry-pi-4-model-b-4gb?src=raspberrypi) that will be our edge compute resource to control the robot and scripts, and will communicate back to the AWS cloud for text to speech, speech to text, computer vision, and the QnA solution.   |


### Connectivity

- I2C board for servo motors:  [https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)   
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

Follow the step by step deployment instructions in this [getting started documentation](docs/GettingStarted.md). This describes how to deploy the resources locally on the bot, and resources in the cloud.
  
More details about servo motors and configuration [here](docs/TSA-Bot-ServoMotors-details.md)


## Security
See [CONTRIBUTING](contributing.md) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.
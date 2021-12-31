# Install the TSA Bot solution
## Getting started (step by step)

### Deploy QnA Bot solution in AWS

[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?&templateURL=https://solutions-reference.s3.amazonaws.com/aws-qnabot/latest/aws-qnabot-main.template)

*(if button does not work, access directly from the solution page)*

1. Install QnA Bot : Now an official [AWS Solution Implementation](https://aws.amazon.com/solutions/implementations/aws-qnabot/) (5 min to deploy through CloudFormation)
 - Select ElasticSearch 2 nodes, 
 - Do not use Kendra (be frugal but might an option if ),
 - Select Lex v2 only
2. Once status is CREATE_COMPLETE, go to the outputs tab in the CFN console:
	- Copy from output tab the following values: `LexV2BotId` & `LexV2BotAliasId`
	- Clic on ContentDesignerURL link. This should look like *https://xxxxxxx.execute-api.us-east-1.amazonaws.com/prod/pages/designer*
	- Check your email for the temporary password sent, and use it for the Admin user. 
	- Set up new password
	- To import the TSA Bot questions: Select the tools menu ( ☰ ) and select Import. Select the qna-reinvent.json file from the git repository (see first step in next chapter)
	- To import pre-defined setting: Select the tools menu ( ☰ ), and then choose Settings. At the bottom of the page, select 'Import Settings', and select the qna\_settings.json file from the git repository.   
	A lot of optimization can be done here, including changing ES_USE_KEYWORD_FILTERS to FALSE. Scroll to the bottom and select Save

> You can further customize how the keyword filters feature works by changing the following settings (more details in [documentation](https://docs.aws.amazon.com/solutions/latest/aws-qnabot/modifying-configuration-settings.html):

>| Key        | Value           |
| ------------- | ------------- |
| ES_KEYWORD_SYNTAX_TYPES: | A list of tokens representing parts of speech identified by Amazon Comprehend |
| ES_MINIMUM_SHOULD_MATCH: | A query rule used to determine how many keywords must match an item question in a valid answer.|

### Deploy resources in the cloud using CloudFormation template

[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=buildkite&templateURL=https://github.com/aws-samples/reinvent2021-tsa-bot/cloudformation-templates/cdk.out/TSABotStack.template.json)


Use the [Cloudformation template](https://github.com/aws-samples/reinvent2021-tsa-bot/cloudformation-templates/cdk.out/TSABotStack.template.json) or cdk script are available to deploy resources in your AWS account. These allow you to:

* Create the DynamoDB "flights" table used for the daily flights leaving from specific airport (Done)  
* Create the DynamoDB "tsa-images" table used for the image recognition and labels (Done)
* Populate the "tsa-images" table with most common items that are not allowed (drinks, phone)
* Create the Lambda function that fetches external API for flights  (Done - if needed you can manually add an EventBridge scheduled trigger)  
* Update the Lambda that routes QnA (update the one from the QnA solution) (NOT DONE : Manual for now - replace the router file in the QnA Lambda function)



### Deploy TSA Bot on Raspberry Pi 4

1. Download repository from AWS CodeCommit:   
`git clone https://github.com/aws-samples/reinvent2021-tsa-bot`
2. Install packages and libraries required:  
`apt install jq`  
`python3 -m pip install pyserial`  
`python3 -m pip install adafruit-circuitpython-servokit`  
`python3 -m pip install pyaudio`  
`python3 -m pip install boto3`  
`python3 -m pip install awscrt`  
`python3 -m pip install awsiotsdk`  
`python3 -m pip install python-dotenv`  
`python3 -m pip install awscli --upgrade --user`  
3. Configure your AWS credentials with access and secret key with limited priviledges  
`aws configure`  (enter your AWS access and secret key, and AWS default region to be used by boto3 library. IAM user should have permissions to use Lexv2 - See IAM recommended permissions as example here)  
4. Install remaining libraries
`sudo apt-get install portaudio19-dev libatlas-base-dev`  
`python3 -m pip install pvporcupine`  
`python3 -m pip install ppnrespeakerdemo`  
`python3 -m pip install awscli --upgrade --user`   
`export PATH=/home/pi/.local/bin:$PATH`  
5. `cd reinvent2021-tsa-bot/TSA-demo/TSA_voice_assistant`
6. Update Lex parameters bot_id & bot\_alias_id  
`vim raspberry_voice_assistant.py` (Edit and change to reflect the bot and alias you created through the QnA Bot solution)
7. Edit the 'env' file that will use all variables to match your AWS account (credentials, IoT Core endpoint and configuration).   
`cd reinvent2021-tsa-bot/TSA-demo/TSA_mecha`  
`vim .env`

```
AWS_KEY_ID=<REPLACE_WITH_YOUR_AWS_ACCESS_KEY>
AWS_SECRET_KEY=<REPLACE_WITH_YOUR_AWS_SECRET_KEY>
ENDPOINT=akg4sd9hskq73-ats.iot.us-east-1.amazonaws.com  #required=True, help="Your AWS IoT custom endpoint, not including a port. " + "Ex: \"abcd123456wxyz-ats.iot.us-east-1.amazonaws.com\"")
PORT=8883   #Specify port. AWS IoT supports 443 and 8883.
CERT_FILEPATH=certs/<REPLACE WITH YOUR CERT FILE NAME>  #File path to your client certificate, in PEM format.
PRI_KEY_FILEPATH=certs/<REPLACE WITH YOUR PRIVATE KEY FILE NAME> #File path to your private key, in PEM format.
CA_FILEPATH=certs/AmazonRootCA1.cer #File path to root certificate authority, in PEM format.
on_connection_interrupted=on_connection_interrupted
on_connection_resumed=on_connection_resumed
CLIENT_ID=TSA-Bot- #Client ID for MQTT connection.
TOPIC=lcd-message
CLEAN_SESSION=False
KEEP_ALIVE_SECS=30
HTTP_PROXY_OPTIONS=None
```
8. Start the main script  
`cd reinvent2021-tsa-bot/TSA-demo/TSA_mecha`  
`python3 finalflow-mqtt-dev-rasp.py`
9.  Add the following line for autostart :  
`sudo vim /etc/rc.local`    
`cd /home/pi/TSA/ava && /usr/bin/npm start &;
sleep 20; su pi -c '/usr/bin/python3 /home/pi/TSA/TSA-demo/TSA_voice_assistant/raspberry_voice_assistant.py &> /tmp/log.txt 2>&1'`


## Servo motors

More details about servo motors and configuration [here](TSA-Bot-ServoMotors-details.md)

## Microphone configuration

On the RaspberryPi, list the different speaker that are connected to the Raspberry Pi by running:  
`aplay -l`

Open /etc/pulse/default.pa. in editor and change this line

`
load-module module-alsa-sink`  
into this   
`load-module module-alsa-sink device=hw:2,7`  
*(replace hw:CARD,DEVICE with the card and device numbers from speaker you want to use in the aplay command output.)*

Finally, select through the raspberry Pi UI the output device in the task bar.

## How to interact with wake word (optional)

1. We are using a wake word to start the interaction. To do so, we are using the free librarie picovoice and their porcupine local light implementation. More details [here](https://picovoice.ai/platform/porcupine/).

2. QnA / TSA FAQ
	- Say: `Picovoice`
	- Say: (Questions imported in QnA bot)  
		1 `Can I bring a water bottle?`  
		2 `Can I keep my jacket?`   
		3 `Can I bring my laptop?`  
		4 `Do I need to remove my belt?`    
		
3. Image recognition
	- Say: `Picovoice`  
	- Say:	 `Can I wear / bring this?` (will trigger the image recognition to see if you have anything that should be put in bin)


 	
## For screen application installation

1. On the Raspberry Pi:
	1. $`git clone https://github.com/eddie2070/ava.git`
	2. $`npm install -g @aws-amplify/cli`
	3. delete amplify directory from the root directory.
	4. delete aws-exports.js from the src directory.
	5. $`amplify configure`
	6. $`amplify init`
	7. $`amplify add auth`. Select "Default configuration", "Email" for user sign in, "No" for advanced settings?.
	8. $`amplify push`

	Create a file .env.local in the root folder
> REACT_APP_IDENTITY_POOL_ID='xxx'  
REACT_APP_USER_POOL_ID='xxx'  
REACT_APP_USER_POOL_WEB_CLIENT_ID='xxx'  
REACT_APP_REGION='us-east-1'  
REACT_APP_MQTT_ID='xxx'

Copy values from the file in src/aws.-exports.js generated after amplify push.  
  For the MQTT ID, go to settings in the IoT Core Console.

In the cognito identity pool console, edit the TSA Bot ID POOL. Edit the role for the unauthenticated requests and check the box to allow unauth requests:
> {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cognito-identity:",
                "transcribe:",
                "iot:",
                "mobileanalytics:PutEvents",
                "cognito-sync:"
            ],
            "Resource": "*"
        }
    ]
}


## (Optional) Install Seeeed ReSpeaker mic board
The ReSpeaker 4-Mic Array for Raspberry Pi（Pi 3/Pi 4 B +) is a 4 microphone expansion board for Raspberry Pi designed for AI and voice applications. This means that you can build a more powerful and flexible voice product 

* This is what it looks like: [Image](https://files.seeedstudio.com/wiki/ReSpeaker-4-Mic-Array-for-Raspberry-Pi/img/rainbow.jpg)

* Installation instructions: [Step by step](https://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/)

* Buy it on Amazon: [here](https://www.amazon.com/seeed-Studio-ReSpeaker-4-Mic-Raspberry/dp/B076SSR1W1)

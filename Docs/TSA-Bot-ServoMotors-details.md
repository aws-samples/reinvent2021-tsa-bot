# Information about servo-motors movements:

For the TSA Bot project, we have replaced the original Meccano<sup>&reg;</sup> motors with ones that we can easily command from the Raspberry Pi.

1.	The servo used for eye, neck and hand movement is the [ANNIMOS 20KG Digital Servo High Torque Full Metal Gear, DS3218MG, Angle 270°](https://www.amazon.com/gp/product/B076CNKQX4/). You can use any similar servo at your convenience.

2.	We will be setting it to 7.5 voltage for free movement

3.	We are using 8 servos in total.
<ol type="a">
<li>1 for neck movement (channel 10) -- Initial position at angle 90</li>
<li>1 for eye movement (channel 8) -- Initial position at angle 90</li>
<li>Left shoulder-1 movement (channel 3) -- Initial position at angle 180</li>
<li>Left elbow movement (channel 2) -- Initial position at angle 0</li>
<li>Left shoulder-2 movement (channel 0) ---Initial position at angle 0</li>
<li>Right shoulder-1 movement (channel 15) -- Initial position at angle 40</li>
<li>Right elbow movement (channel 12) -- Initial position at angle 180</li>
<li>Right shoulder-2 movement (channel 13) ---Initial position at angle 160</li>
</ol> 
Shoulder 1 Hand up and down  
Shoulder 2 Fly (hand far and near)  

4.	Since we have 8 servos, we cannot connect directly to raspi, as raspi don’t have enough GPIO pins. That’s why we are using I2C serial connector where in we can use 16 channel to connect 16 servos. More details [here](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

5.	If you have to move for example neck, all we need to do is provide angle For neck initial angle is at 90 degrees. You can move to 180 or 0 and it will move left and right.

**If voltage is below, you might have slow movements. If voltage is too high, you might have fast movements that we recommend to break into smaller movements with pauses between these)**

# Pacemaker  
Pacemaker model designed through Simulink and code generation to flash onto a NXP FRDM K64 board, which then interfaces with an artificial heart.  
The DCM then interfaces with the pacemaker through serial to update parameters and operating modes, in addition to displaying real time electrocardiograms of the heart.  

Tunable parameters include hysteresis intervals, refractory periods, and other parameters relevant to the operating mode of the pacemaker.  
Current operating modes include AOO, AAI, VVO, VVI, DOO, DDD, and the rate adaptive versions (AOOR, AAIR, etc).  
Rate adaptive works by using the on board accelerometer to gauge the activity level of the heart, and slows/speeds up the heart rate accordingly.  
The electrocardiogram in the DCM displays the pulses of the heart, and labels the pulse as either a natural pulse or an artificial pace from the pacemaker.   

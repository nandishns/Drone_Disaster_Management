# Drone_Disaster_Management

Disasters, including man-made ones, are an ever-present threat and are occurring at an increasing rate worldwide. Disaster response is one of the critical phases in the Disaster Management System life cycle. People affected must be given immediate relief and support which is impossible to do manually and at large scale. An automated, easy-to-deploy system is required to survey the affected regionand for the delivery and detection of the trapped people and totake the necessary action.

## Solution :

## 1.Accepting coordinates.

![image](https://i.ibb.co/HqW3hPB/Screenshot-20221002-074656.jpg)
   
   
   The drone accepts set of approximate coordinates of the trapped persons from the operator using ```Flutter App```.
## 2.Mapping
   The drone maps its trip according to the coordinates using A* algorithm.
## 3.Navigate to checkpoints
   The drone will navigate to coordinates in auto-mode and stop at each checkpoint to detect humans visually at that      place.
## 4.Detect humans
   Once the drone reaches the set destination, it searches for humans in the vicinity and navigates towards them.
## 5.Delivery
   The drone waits for signalling from receiver and delivers the required package and sets off for its next checkpoint.
## 6.On-Air Scanning
   The drone, once in air, also starts scanning for potentially undetected humans trapped while its on its way to next    checkpoints and report it back to ground control

## Technologies Used :
```1.Python```

```2.Image processing(OpenCV)```

```3.Open source APIs```

```3.Linux OS```

```4.Ardu Pilot (drone simulation software)```

```5.DroneKit API Python```



## Glimpse 
 
 1.  ![image](https://i.ibb.co/PDbVsJ6/png-20221004-153902-0000.png)
 
 
 2.  ![image](https://i.ibb.co/Qb48rgD/20221001-225628.jpg)

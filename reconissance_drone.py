from dronekit import *
from DistanceEstimation_edit import dist
import time
import cv2
import mysql.connector as mc
from mysql.connector import Error

try:
    mycon = mc.connect(host='HOST_NAME',user='USER_NAME', 
                        passwd='PASSWORD',
                        database='DB_NAME')
    if  mycon.is_connected():
        db_Info = mycon.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        # curr = mycon.cursor()
        # curr.execute("select database();")

except Error as e:
    print("Error while connecting to MySQL", e)


# curr = mycon.cursor()
curr = mycon.cursor()

'''

curr.execute('insert into lat_lon values(-35.3641764, 149.1608988),(-35.3641764, 149.1608988),(-35.3641769, 149.1608963)')
mycon.commit()
mycon.close()

'''

detector = cv2.QRCodeDetector()

cap = cv2.VideoCapture(0)

found_lst = [] #To store coordinate data of humans found

while True:
    _, image = cap.read()

    cv2.imshow("Output", image)
    if cv2.waitKey(1) == ord('q'):
        # release the webcam and destroy all active windows
        cv2.destroyAllWindows()
        cap.release()

    res, _, _ = detector.detectAndDecode(image)
    if res:
        try:
            lst = res.split(',')
            lst = [float(i) for i in lst]
            cv2.destroyAllWindows()
            cap.release()
            break
        except IndexError:
            print("Invalid QR code")
        except Exception as e:
            print(e)

vehicle = connect('127.0.0.1:14551', baud=921600, wait_ready=True)

#takeoff function
def arm_takeoff(height):
    #check if drone is ready
    while not vehicle.is_armable:
        print("waiting for drone")
        time.sleep(1)
    
    #change mode and arm
    print("Arming")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    #check if drone is armed
    while not vehicle.armed:
        print("Waiting for arm")
        time.sleep(1)

    #takeoff
    print("Takeoff")
    vehicle.simple_takeoff(height)
    
    #report values back every 1s and finally break out
    while vehicle.location.global_relative_frame.alt<=(height*0.95):
        print("Reached", vehicle.location.global_relative_frame.alt, "m")
        time.sleep(0.5)
    print("Reached target altitude")

def get_location_metres(original_location, dNorth, dEast):
    earth_radius = 6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    if type(original_location) is LocationGlobal:
        targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt)
    else:
        raise Exception("Invalid Location object passed")
        
    return targetlocation

def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def goto(dNorth,dEast, gotoFunction=vehicle.simple_goto):
    currentLocation=vehicle.location.global_relative_frame
    targetLocation= get_location_metres(currentLocation,dNorth,dEast)
    targetDistance = get_distance_metres(currentLocation,targetLocation)
    # print(targetLocation)
    gotoFunction(targetLocation)

    while vehicle.mode.name=="GUIDED":
        remainingDistance=get_distance_metres(vehicle.location.global_frame,targetLocation)
        # print("Distance to target:",remainingDistance) 
        if abs(remainingDistance)<=abs(targetDistance*0.05):
            print("REached target")
            break;
        human_dist = dist(cap)
        # print(human_dist)
        if(human_dist == -1 or human_dist>10):
            continue
        dr_cr_loc = vehicle.location.global_relative_frame
        if not found_lst:
            found_lst.append((dr_cr_loc.lat, dr_cr_loc.lon))
            continue
        for i in found_lst:
            oldlocation = LocationGlobal(i[0], i[1], 10)
            flag = 0
            # print(abs(get_distance_metres(dr_cr_loc,oldlocation)),abs(get_distance_metres(dr_cr_loc,oldlocation))>=150, len(found_lst))
            if abs(get_distance_metres(dr_cr_loc,oldlocation))<=75:
                flag = 1
                break
        if not flag:
            found_lst.append((dr_cr_loc.lat, dr_cr_loc.lon))
            print("Human Dectected", len(found_lst))
        
        # time.sleep(.5)

arm_takeoff(10)

vehicle.simple_goto(LocationGlobalRelative(float(lst[0]), float(lst[1]), 10))

target_dist = get_distance_metres(LocationGlobalRelative(lst[0],lst[1],15),vehicle.location.global_relative_frame)
while vehicle.mode.name == "GUIDED":
    rem_dist = get_distance_metres(vehicle.location.global_relative_frame,LocationGlobalRelative(lst[0],lst[1],15))
    print(f"Distance to target : {round(rem_dist,2)}m")
    if (abs(rem_dist)<=abs(target_dist*0.01)):
        print("Reached target")
        break
    time.sleep(2.5)

print('Mission')
cap = cv2.VideoCapture(0)
# vehicle.mode = VehicleMode('AUTO')
# time.sleep(300)


#Vehicle.simple_goto()
i=0
while(i<2):
    goto(-50,-100)
    goto(0,100)
    i+=1

while(i<4):
    goto(50,-100)
    goto(0,100)
    i+=1
key = cv2.waitKey(1)
if key == ord('q'):
    cv2.destroyAllWindows()
cv2.destroyAllWindows()

#landing
print("Landing")
vehicle.mode = VehicleMode('RTL')
while vehicle.location.global_relative_frame.alt>=(0.5):
    print("Vehilce at",vehicle.location.global_relative_frame.alt,"m")
    time.sleep(1)

print("Landed")

strr=''
for i in found_lst:
    strr+=str(i)+','
curr.execute(f'insert into lat_lon values{strr[:-1]}')
mycon.commit()



time.sleep(10)

#close vehicle
vehicle.close()
print('uploded to database')

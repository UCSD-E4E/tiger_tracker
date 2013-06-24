#include "ros/ros.h"
#include "std_msgs/String.h"
#include "time.h"
#include <fstream>
#include <iostream>
#include <string>
#include "CamTrap_Viper/LogPacket.h"

using namespace std;


void movementCallback(const CamTrap_Viper::LogPacket msg)
{

	/*****Log CSV Structure*****
	Video Name, pan posiion, tilt position
	***************************/
	char logLine[100];
	ofstream logfile;
	ifstream logfile2;
   stringstream pan_pos (stringstream::in | stringstream::out);
   stringstream tilt_pos (stringstream::in | stringstream::out);
	
	//opening the logfile to write on it
  	logfile.open("/home/viki/catkin_ws/src/tiger_tracker/src/node_log/log.csv", ios::app);
  
	 //convert message data to strings
	 pan_pos << msg.x_pos;
    tilt_pos << msg.y_pos;
	sprintf(logLine, "%s,%f,%f\n",msg.file_name.c_str(), msg.x_pos, msg.y_pos);
   ROS_INFO("LOG X:%f Y:%f", msg.x_pos, msg.y_pos);
   logfile << logLine; 
	//logfile << msg.file_name.c_str() << ',' << pan_pos << ',' << tilt_pos << std::endl; //writing data from msg to log file
    logfile.close();
    
	//block of code I used to check if the text was copied to the log file
	/* logfile2.open("/home/viki/groovy_workspace/CamTrap_Viper/src/node_log/log.txt");
    getline (logfile2, logLine);
    cout << logLine << std::endl;
    logfile.close();
*/
}

int main(int argc, char **argv)
{
   //Initialize ROS node setup
   ros::init(argc, argv, "log");
   ros::NodeHandle n;

   ros::Subscriber sub = n.subscribe("Motor_Movement",10, movementCallback);

   while(ros::ok())
   {
      //Do stuff until someone presses ctrl-c
      ros::spin();
   }
   return 0;
}


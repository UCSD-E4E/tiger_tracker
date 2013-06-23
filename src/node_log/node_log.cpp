#include "ros/ros.h"
#include "std_msgs/String.h"
#include "time.h"
#include <fstream>
#include <iostream>
#include <string>
using namespace std;


void movementCallback(const std_msgs::String::ConstPtr& msg)
{
	string logLine;
	ofstream logfile;
	ifstream logfile2;
  
	//opening the logfile to write on it
  	logfile.open("/home/viki/groovy_workspace/CamTrap_Viper/src/node_log/log.csv", ios::app);
  
    logfile << msg->data.c_str() << std::endl; //writing data from msg to log file
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


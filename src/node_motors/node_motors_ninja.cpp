#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include <iostream>
#include <time.h>
#include <string.h>
#include <sys/statvfs.h>
#include "CamTrap_Viper/CvService.h"
#include "CamTrap_Viper/LogPacket.h"
#include "motor_controller.h"
#include <boost/asio.hpp>

//using namespace boost::asio;

void hvCallback(const std_msgs::String::ConstPtr& msg)
{
	//Do stuff when the hypervisor says so
}

void comCallback(const std_msgs::String::ConstPtr& msg)
{
	//Do stuff when the com node says so
}

int main(int argc, char** argv){
	ros::init(argc, argv, "motors");
	ros::NodeHandle n;
	ROS_INFO("Running THIS Ninja Controller");
	//connect to Hypervisor and com nodes
	ros::Subscriber hv_sub = n.subscribe("Hypervisor_Output", 10, hvCallback);	
	ros::Subscriber com_sub = n.subscribe("Com_Commands", 10, comCallback);
	
	//Open connection for Log node to connect to
	ros::Publisher pub = n.advertise<CamTrap_Viper::LogPacket>("Motor_Movement",10);
	
	//Connect to CV service
	ros::ServiceClient client = n.serviceClient<CamTrap_Viper::CvService>("cv_service");
	CamTrap_Viper::CvService srv;

	MotorController mctrl("/dev/ttyUSB0", 19200, 0.0, 0.0);
	
	std::string response;
	std_msgs::String file_name;
	
	CamTrap_Viper::LogPacket msg;
//	ROS_INFO("Checking position");

	mctrl.updatePanTilt();	
	
	while (ros::ok())
	{  
	 //Query new coordinates
      srv.request.localization_request = 0;
      if (client.call(srv))
      {
			mctrl.new_pan = mctrl.pan_pos + srv.response.x_degree;  
			mctrl.new_tilt = mctrl.tilt_pos + srv.response.y_degree;
			//file_name = srv.response.file_name;
			
			msg.file_name = srv.response.file_name;
			msg.x_pos = mctrl.new_pan;
			msg.y_pos = mctrl.new_tilt;
       	
			mctrl.updatePosition();

			pub.publish(msg);
			
      }   
      else
      {   
         ROS_ERROR("service call failed :(");
      }
		ros::spinOnce();
//`		ros::Duration(0.5).sleep();
	}
}

#include <stdio.h>
#include <cv.h>
#include <opencv2/highgui/highgui.hpp>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <termios.h>
#include <iostream>
#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv/cxcore.h>
#include <opencv/cvblob.h>
#include <opencv2/core/core.hpp>
#include "CamTrap_Viper/CvService.h"
#include "cv_localizer.h"
 
using namespace cvb;
using namespace std;
 
int main(int argc, char * argv[])
{
    struct timeval tv;
    
    const double TICK_FREQ = cv::getTickFrequency();
    const int WEB_FOV_X = 36;
    const int WEB_FOV_Y = 27;
    //const int WEB_WRITER_FRAME_RATE = 30;
    ros::init(argc, argv, "cv_service");
	 ros::NodeHandle n;
   
    int duration_sec = 60 * 1;

	/* Initialize the camera */
    CvCapture *capture = cvCreateCameraCapture(1);
	cvQueryFrame(capture);
	

	const int WEB_FRAME_WIDTH = (int)cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH);
	const int WEB_FRAME_HEIGHT = (int)cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT);
	const double WEB_WRITER_FRAME_RATE = 15;
	
	/* Initialize the WebCam */
    cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, WEB_FRAME_HEIGHT);
 
    /* Always check if the program can find a device */
    if (!capture)
    {
       ROS_ERROR("Can not open webcam");
       return -1;
    }
 /* creating display window */
    //use only for testing
    cvNamedWindow("WEBCAM", CV_WINDOW_AUTOSIZE);
 
    /* Create required images once */
    IplImage *img = cvQueryFrame(capture);
	
	/* Time init */
    time_t rawTime = time (NULL);
    tm *pTime = localtime(&rawTime);

    char video_name[100];
	/* initialize video writer */
   
    CvVideoWriter *WebWriter;
    sprintf(video_name, "%s%d-%d-%d:%d:%d%s", "/home/viki/Videos/webcam/", pTime->tm_mon + 1, pTime->tm_mday, pTime->tm_hour, pTime->tm_min, pTime->tm_sec, ".avi");

    WebWriter = cvCreateVideoWriter(video_name, CV_FOURCC('D','I','V','X'), WEB_WRITER_FRAME_RATE, cvSize(WEB_FRAME_WIDTH, WEB_FRAME_HEIGHT), 1);	
   
	
   	double tick_duration = (TICK_FREQ/WEB_WRITER_FRAME_RATE);//1000.0/(WEB_WRITER_FRAME_RATE*TICK_FREQ);
	ROS_INFO("Tick Frequency: %f\nDuration in ticks: %f", TICK_FREQ, tick_duration);
	/* main loop */
    long int timecnt = time(&rawTime) + duration_sec;

	while(ros::ok())
	{

        double start_ticks = (double)cv::getTickCount();
		//ROS_INFO("Start ticks = %f", start_ticks);
 	    /* Obtain a frame from the device */
        img = cvQueryFrame(capture);
 
    	/* Always check if the device returns a frame */
    	if( !img )
    	{
      		ROS_ERROR("Error retrieving webcam frame\n");
       		return -1;
    	}
    
	 	rawTime = time (NULL);
 
    	/* reset video writer for every X second */
    	if (timecnt <= time(&rawTime))
    	{
       		cvReleaseVideoWriter(&WebWriter);
      	 	pTime = localtime(&rawTime);
       		sprintf(video_name, "%s%d-%d-%d:%d:%d%s", "/home/viki/Videos/webcam/", pTime->tm_mon+1, pTime->tm_mday, pTime->tm_hour, pTime->tm_min, pTime->tm_sec, ".avi");
       		WebWriter = cvCreateVideoWriter(video_name, CV_FOURCC('D','I','V','X'), WEB_WRITER_FRAME_RATE, cvSize(WEB_FRAME_WIDTH, WEB_FRAME_HEIGHT), 1);
			timecnt = time(&rawTime) + duration_sec;
	 	}
	
		//cvWriteFrame(WebWriter, cvQueryFrame(capture));
		cvWriteFrame(WebWriter, img);
 		
    	/* Publish videos */
    	cvShowImage("WEBCAM", img);
    	/* cleaning memory */
    	cvWaitKey(1);
    	//cvZero(img);
    
    	double stop_ticks = (double)cv::getTickCount();    
    
//   		ROS_INFO("start-stop=%f", stop_ticks - start_ticks); 
    	while (stop_ticks - start_ticks < tick_duration)
    	{
        	stop_ticks = (double)cv::getTickCount();    
			//ROS_INFO("waiting for correct frame timing");
    	}
    	ros::spinOnce();

	}
     
	/* Clean up memory */
	cvReleaseCapture ( &capture );
	cvReleaseVideoWriter(&WebWriter);
}

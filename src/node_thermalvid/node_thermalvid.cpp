#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <termios.h>
#include <iostream>
#include <sys/time.h>

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

int main(int argc, char **argv)
{
    const double TICK_FREQ = cv::getTickFrequency();
    const int FLIR_FOV_X = 36;
    const int FLIR_FOV_Y = 27;
	 const double FLIR_WRITER_FRAME_RATE = 29.5;

	int duration_sec = 60 * 1;

	ros::init(argc, argv, "cv_service");
	ros::NodeHandle n;
    
	// Initialize Cameras:	
	// set the norm to NTSC for FLIR - and input to 1 for capture device  
	system("v4l2-ctl -s NTSC -i 1");   //if FLIR is video0
	// system("v4l2-ctl -d /dev/video1 -s NTSC -i 1"); if FLIR is video1
	
	// Initialize the IRCam 
	CvCapture *capture = cvCreateCameraCapture(0);
   cvQueryFrame(capture);
	
    const int FLIR_FRAME_WIDTH = 700;//(int) cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH);

    const int FLIR_FRAME_HEIGHT = 576;//(int) cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT);
    cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, FLIR_FRAME_WIDTH);
	 cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, FLIR_FRAME_HEIGHT);  

	/* Always check if the program can find a device */
	if (!capture)
	{
		ROS_ERROR("Can not open flir");
		return -1;
	}
    
    
	CVLocalizer object_tracker(0, 0, FLIR_FRAME_WIDTH, FLIR_FRAME_HEIGHT, FLIR_FOV_X, FLIR_FOV_Y);
	object_tracker.setTimestamp(0);
    
    ros::ServiceServer service = n.advertiseService("cv_service", &CVLocalizer::newCoords, &object_tracker);
	
/* creating display window */
	//use only for testing
	cvNamedWindow( "FLIR",CV_WINDOW_AUTOSIZE);

	/* Create required images once */
	IplImage *img = cvQueryFrame(capture);

	double tick_duration = (TICK_FREQ/FLIR_WRITER_FRAME_RATE);

	/* Time init */
	time_t rawTime = time (NULL);
	tm *pTime = localtime(&rawTime);
	
	/* initialize video writer */
	CvVideoWriter *flirWriter;
	sprintf(object_tracker.video_name, "%s%d-%d-%d:%d:%d%s", "/home/viki/Videos/thermal/", pTime->tm_mon+1, pTime->tm_mday, pTime->tm_hour, pTime->tm_min, pTime->tm_sec, ".avi");
	flirWriter = cvCreateVideoWriter(object_tracker.video_name, CV_FOURCC('D','I','V','X'), FLIR_WRITER_FRAME_RATE, cvSize(FLIR_FRAME_WIDTH, FLIR_FRAME_HEIGHT), 1);
	
	/* main loop */
	long int timecnt = time(&rawTime) + duration_sec;
    
while (ros::ok())
{
	// Obtain a frame from the device 
	img = cvQueryFrame(capture);
	double start_ticks = (double)cv::getTickCount();

	/* Always check if the device returns a frame */
	if( !img )
	{
		ROS_ERROR("Error retrieving FLIR frame\n");
		return -1;
	}

	/* remove the watermark */
	cvSetImageROI(img, cvRect((FLIR_FRAME_WIDTH*367)/480,(FLIR_FRAME_HEIGHT*14)/320,(FLIR_FRAME_WIDTH*90)/480,(FLIR_FRAME_HEIGHT*28)/320));
	cvZero(img);
	cvResetImageROI(img);

	/* Time get */
	rawTime = time (NULL);

	/* reset video writer for every X second */
	if (timecnt <= time(&rawTime))
	{
		cvReleaseVideoWriter(&flirWriter);
		pTime = localtime(&rawTime);
		
		//object_tracker.video_name;
		int sprint_test = sprintf(object_tracker.video_name, "%s%d-%d-%d:%d:%d%s", "/home/viki/Videos/thermal/", pTime->tm_mon+1, pTime->tm_mday, pTime->tm_hour, pTime->tm_min, pTime->tm_sec, ".avi");

		if (sprint_test < 0)
			ROS_ERROR("sprintf error");
		
		flirWriter = cvCreateVideoWriter(object_tracker.video_name, CV_FOURCC('D','I','V','X'), FLIR_WRITER_FRAME_RATE, cvSize(FLIR_FRAME_WIDTH, FLIR_FRAME_HEIGHT), 1);
		timecnt = time(&rawTime) + duration_sec;
	}

	// Flipping the img if needed with motor node
	cvFlip(img, img,-1);

	/* Write images to file */
	cvWriteFrame(flirWriter, img);

	/* Publish videos */
	cvShowImage( "FLIR", img);

	//for use in node if cvShowImage didn't work
	/*	cv::Mat flir (img);
		cv::namedWindow (FLIR, CV_WINDOW_AUTOSIZE);
		cv::imshow ("FLIR", flir);*/

	/* cleaning memory */
	cvWaitKey(1);

	double stop_ticks = (double)cv::getTickCount();

	while (stop_ticks - start_ticks < tick_duration)
	{
		stop_ticks = (double)cv::getTickCount();
	}

	ros::spinOnce();
	}
 	
	/* Clean up memory */
	//since the loop will break by ros::ok this part is not useable
	/*	cvReleaseCapture( &capture );
	cvDestroyAllWindows();*/
	
	return 0;
}



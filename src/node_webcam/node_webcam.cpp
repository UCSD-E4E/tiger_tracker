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
#include "CamTrap_Viper/CvService.h"
#include "cv_localizer.h"
 
using namespace cvb;
using namespace std;
 
int main(int argc, char * argv[])
{
    const int WEB_FOV_X = 36;
    const int WEB_FOV_Y = 27;
    //const int WEB_WRITER_FRAME_RATE = 30;
    ros::init(argc, argv, "cv_service");
	 ros::NodeHandle n;
   
    int duration_sec = 60 * 5;

	/* Initialize the camera */
   CvCapture *capture = cvCreateCameraCapture(1);
	cvQueryFrame(capture);


	const int WEB_FRAME_WIDTH = (int)cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH);
	const int WEB_FRAME_HEIGHT = (int)cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT);
	const double WEB_WRITER_FRAME_RATE = 13.33;//(double)cvGetCaptureProperty(capture, CV_CAP_PROP_FPS);
	//ROS_INFO("img fps:%f", WEB_WRITER_FRAME_RATE);
   //cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, WEB_FRAME_WIDTH);
   //cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, WEB_FRAME_HEIGHT);
//CamCapture = cvCreateFileCapture("http://192.168.2.135:81/videostream.asf?user=viki&pwd=viki&resolution=640*480");
 //  system("v4l2-ctl -d /dev/video1 -s NTSC -i 1");// if FLIR is video1
	/* Initialize the WebCam */
    //cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, WEB_FRAME_HEIGHT);
 
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
    tm *pTime = gmtime(&rawTime);

    char video_name[100];
	/* initialize video writer */
   
    CvVideoWriter *WebWriter;
    sprintf(video_name, "%s%d-%d-%d:%d:%d%s", "/home/viki/Videos/webcam/", pTime->tm_mon, pTime->tm_mday, pTime->tm_hour, pTime->tm_min, pTime->tm_sec, ".avi");

    WebWriter = cvCreateVideoWriter(video_name, CV_FOURCC('D','I','V','X'), WEB_WRITER_FRAME_RATE, cvSize(WEB_FRAME_WIDTH, WEB_FRAME_HEIGHT), 1);	
   
	/* time */
	time_t current_time;
	current_time = time (NULL);
	long int stop_time = current_time + 10;
	
	/* main loop */
    long int timecnt = time(&rawTime) + duration_sec;

	while( current_time < stop_time )
	{
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
       pTime = gmtime(&rawTime);
       int sprint_test = sprintf(video_name, "%s%d-%d-%d:%d:%d%s", "/home/viki/Videos/webcam/", pTime->tm_mon, pTime->tm_mday, pTime->tm_hour, pTime->tm_min, pTime->tm_sec, ".avi");
       WebWriter = cvCreateVideoWriter(video_name, CV_FOURCC('D','I','V','X'), WEB_WRITER_FRAME_RATE, cvSize(WEB_FRAME_WIDTH, WEB_FRAME_HEIGHT), 1);
		timecnt = time(&rawTime) + duration_sec;
	 }
	
	cvWriteFrame(WebWriter, cvQueryFrame( capture ));
 		
    /* Publish videos */
    cvShowImage( "WEBCAM", img);
    /* cleaning memory */
    cvWaitKey(1);
    cvZero(img);
  
    ros::spinOnce();

	}
 
	/* Clean up memory */
	cvReleaseCapture ( &capture );
	cvReleaseVideoWriter(&WebWriter);
}

/**
 * @file objectDetection.cpp
 * @author A. Huaman ( based in the classic facedetect.cpp in samples/c )
 * @brief A simplified version of facedetect.cpp, show how to load a 
 * cascade classifier and how to find objects (Face + eyes) in a video stream
 */
#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "cv.h"
#include "highgui.h"
 
//#include "opencv2/core/utility.hpp"

#include "opencv2/highgui/highgui_c.h"

#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

/** Function Headers */
void detectAndDisplay( Mat frame );

/** Global variables */
/*-- Note, either copy these two files from opencv/data/haarscascades to your 
 * current folder, or change these locations*/
string cascade_name = "cascade.xml";
//string eyes_cascade_name = "haarcascade_eye_tree_eyeglasses.xml";
CascadeClassifier cascade;
//CascadeClassifier eyes_cascade;
string window_name = "Capture - Animal detection";
RNG rng(12345);

/**
 * @function main
 */
int main( void )
{
    CvCapture* capture;
    Mat frame;

    Size frameSize =  Size(480, 320);

    VideoWriter writer; 
    writer.open("./classifier_output.avi", 
                 CV_FOURCC('D', 'I', 'V', 'X'), 
                 15., frameSize, true);
    if (!writer.isOpened())
    {
        printf("Video writer is not open\n");
        return -1;
    }
    //-- 1. Load the cascades
    if (!cascade.load(cascade_name))
    {
        printf("--(!)Error loading\n"); 
        return -1; 
    };
    capture = cvCaptureFromAVI("wolf_test.avi");
    if( capture )
    {
        for(;;)
        {
            frame = cv::cvarrToMat(cvQueryFrame( capture ));

            //-- 3. Apply the classifier to the frame
            if (!frame.empty())
            { 
                detectAndDisplay( frame ); 
            }
            else
            { 
                printf(" --(!) No captured frame\n"); 
                break; 
            }
            writer << frame;
            int c = waitKey(10);
            if ((char)c == 'c') 
            { 
                break; 
            }

        }
    }
    return 0;
}

/**
 * @function detectAndDisplay
 */
void detectAndDisplay( Mat frame )
{
   std::vector<Rect> animals;
   Mat frame_gray;

   cvtColor( frame, frame_gray, COLOR_BGR2GRAY );
   equalizeHist( frame_gray, frame_gray );
   //-- Detect faces
   cascade.detectMultiScale( frame_gray, animals, 1.1, 2, 0|CASCADE_SCALE_IMAGE, Size(30, 30) );

   for( size_t i = 0; i < animals.size(); i++ )
    {
      Point center( animals[i].x + animals[i].width/2, animals[i].y + animals[i].height/2 );
      ellipse( frame, center, Size( animals[i].width/2, animals[i].height/2), 0, 0, 360, Scalar( 255, 0, 255 ), 2, 8, 0 );

      Mat animalROI = frame_gray(animals[i] );
      /*std::vector<Rect> eyes;

      //-- In each face, detect eyes
      eyes_cascade.detectMultiScale( faceROI, eyes, 1.1, 2, 0 |CASCADE_SCALE_IMAGE, Size(30, 30) );

      for( size_t j = 0; j < eyes.size(); j++ )
       {
         Point eye_center( faces[i].x + eyes[j].x + eyes[j].width/2, faces[i].y + eyes[j].y + eyes[j].height/2 );
         int radius = cvRound( (eyes[j].width + eyes[j].height)*0.25 );
         circle( frame, eye_center, radius, Scalar( 255, 0, 0 ), 3, 8, 0 );
       }*/
    }
   //-- Show what you got
   imshow( window_name, frame );
}

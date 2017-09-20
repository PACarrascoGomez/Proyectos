
#include <unistd.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;


void use (char * programName){

  cerr << "Usage: "<<programName << " options " << endl;
  cerr << "      options:" << endl;
  cerr << "             -i inputNameFile" << endl;
  cerr << "             -p #int periode" << endl;
  cerr << "             -f #int fase" << endl;
  cerr << "             [-o outputNameFile] " << endl;
}

int main(int argc,  char ** argv) {
 string inFileName="", outFileName="";
 int option,periode=-1,fase=0;

  while ((option=getopt(argc,argv,"i:o:p:f:"))!=-1)
    switch (option)  {
    case 'i':
      inFileName = optarg;
      break;
    case 'o':
      outFileName = optarg;
      break;
    case 'p':
      periode = atoi(optarg);
      break;
    case 'f':
      fase = atoi(optarg);
      break;
    default:
      use(argv[0]);
      return(-1);
    }

  if (inFileName.size()==0){
    cerr << argv[0] << " Error: input file name must be provided" << endl;
    use(argv[0]);
    return (-1);
  }
  
  if (periode == -1){
    cerr << argv[0] << " periode name must be provided" << endl;
    use(argv[0]);
    return (-1);
  }
  Mat img=imread(inFileName);

/*
  // Por columnas
  for (fase; fase < img.cols; fase+=periode) 
    //if (fase % periode == 0)
      line(img, Point(fase,0), Point(fase,img.rows-1), Scalar(160, 130, 240), 2,4,false); 
*/

  // Por filas
  for (int i=fase; i < img.rows; i+=periode)
    line(img, Point(0,i), Point(img.cols-1,i), Scalar(255, 0, 0), 1,4,false);

  if( outFileName.size() > 0)
    imwrite( outFileName, img);
  else {
    namedWindow("Imagen segmentada",WINDOW_NORMAL);
    imshow("Imagen segmentada",img);
    cv::waitKey();
  }

  return 0;
}

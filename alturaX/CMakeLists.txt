cmake_minimum_required(VERSION 2.8)
project( alturaX )
find_package( OpenCV REQUIRED )
add_executable( alturaX alturaX.cpp )
target_link_libraries( alturaX ${OpenCV_LIBS} -lboost_system -lboost_iostreams)

project( segmentar )
find_package( OpenCV REQUIRED )
add_executable( segmentar segmentarImagen.cpp )
target_link_libraries( segmentar ${OpenCV_LIBS})


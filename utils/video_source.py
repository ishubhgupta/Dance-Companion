"""
Video Source Module for Dance Companion

This module provides a class for handling video input from files or webcams.
It abstracts the details of video capture and provides a simple interface
for reading frames.

Author: Shubh Gupta
Version: 1.0.0
License: MIT
Date: 2025
"""

import cv2

class VideoSource:
    """
    A class for handling video input from files or webcams.
    
    This class wraps OpenCV's VideoCapture to provide a unified interface
    for reading frames from different sources.
    """
    
    def __init__(self, source):
        """
        Initialize a video source.
        
        Args:
            source (str or int): Path to video file (str) or webcam index (int).
                                Integer values (0, 1, etc.) refer to connected cameras.
                                
        Raises:
            ValueError: If the video source cannot be opened.
        """
        # Initialize video capture with the specified source
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise ValueError(f"Error: Could not open video source {source}.")
            
    def read_frame(self):
        """
        Read a frame from the video source.
        
        Returns:
            Tuple[bool, numpy.ndarray]: 
                - First element is a boolean indicating success (True) or failure (False)
                - Second element is the frame (numpy array) if successful, otherwise empty
        """
        return self.cap.read()
    
    def release(self):
        """
        Release the video source resources.
        
        This method should be called when the video source is no longer needed
        to free up resources.
        """
        self.cap.release()

"""
Pose Detector Module for Dance Companion

This module provides a class for detecting human pose landmarks using MediaPipe.
It handles the initialization of the pose detection model and processes frames
to extract pose landmarks.

Author: Shubh Gupta
Version: 1.0.0
License: MIT
Date: 2025
"""

import mediapipe as mp
import cv2

class PoseDetector:
    """
    A class for detecting human pose landmarks in images or video frames.
    
    This class wraps the MediaPipe Pose solution and provides methods for
    initializing the detector and processing frames to extract pose landmarks.
    """
    
    def __init__(self, static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initialize the MediaPipe pose detector.
        
        Args:
            static_image_mode (bool): Whether to treat the input images as a batch or as a video stream.
                                     Set to True for processing individual images, False for video.
            min_detection_confidence (float): Minimum confidence for the person detection to be considered successful.
                                             Value range: [0.0, 1.0]
            min_tracking_confidence (float): Minimum confidence for the pose landmarks to be considered tracked successfully.
                                           Value range: [0.0, 1.0]
        """
        # Initialize MediaPipe Pose components
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
    def detect_landmarks(self, frame):
        """
        Detect pose landmarks in the given frame.
        
        Args:
            frame (numpy.ndarray): BGR image to detect pose landmarks on.
            
        Returns:
            mp.solutions.pose.PoseLandmarkList: Pose detection results containing landmarks.
                                               Each landmark has x, y, z coordinates and visibility.
        """
        # Convert BGR to RGB as MediaPipe requires RGB input
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the frame and return the results
        return self.pose.process(rgb_frame)
    
    def get_pose_connections(self):
        """
        Get the pose landmark connections defined by MediaPipe.
        
        These connections define which landmarks should be connected by lines
        when visualizing the pose.
        
        Returns:
            List[Tuple[int, int]]: List of landmark index pairs representing connections.
        """
        return self.mp_pose.POSE_CONNECTIONS

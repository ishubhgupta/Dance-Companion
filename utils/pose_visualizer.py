"""
Pose Visualizer Module for Dance Companion

This module provides a class for visualizing pose landmarks and their connections.
It handles the creation of mirrored landmarks and drawing them on the frame.

Author: Shubh Gupta
Version: 1.0.0
License: MIT
Date: 2025
"""

import cv2
import numpy as np

class PoseVisualizer:
    """
    A class for visualizing pose landmarks and their connections.
    
    This class provides methods for creating mirrored landmarks and
    drawing them on frames for visualization.
    """
    
    def __init__(self, landmark_color=(255, 0, 0), connection_color=(0, 0, 255), 
                 circle_radius=3, line_thickness=2, offset_x=150):
        """
        Initialize the pose visualizer with customizable visual parameters.
        
        Args:
            landmark_color (tuple): Color for landmark points in BGR format (B,G,R).
            connection_color (tuple): Color for connections between landmarks in BGR format (B,G,R).
            circle_radius (int): Radius of the circles representing landmarks in pixels.
            line_thickness (int): Thickness of the lines connecting landmarks in pixels.
            offset_x (int): Horizontal offset for the mirrored pose in pixels.
        """
        self.landmark_color = landmark_color
        self.connection_color = connection_color
        self.circle_radius = circle_radius
        self.line_thickness = line_thickness
        self.offset_x = offset_x
        
    def create_mirrored_landmarks(self, landmarks, frame_shape):
        """
        Create mirrored landmarks from the detected pose landmarks.
        
        This method flips the detected landmarks horizontally and applies
        an offset to create a mirrored pose representation.
        
        Args:
            landmarks (mp.solutions.pose.PoseLandmarkList): Detected pose landmarks.
            frame_shape (tuple): Shape of the frame (height, width, channels).
            
        Returns:
            dict: Dictionary of mirrored landmark indices and their positions as (x, y) tuples.
        """
        h, w, _ = frame_shape
        mirrored_landmarks = {}
        
        # Process each landmark from the detection results
        for idx, lm in enumerate(landmarks.landmark):
            # Convert normalized coordinates to pixel coordinates
            x = int(lm.x * w)
            y = int(lm.y * h)
            # Mirror the x-coordinate and add the extra offset
            mirror_x = w - x + self.offset_x
            mirrored_landmarks[idx] = (mirror_x, y)
            
        return mirrored_landmarks
    
    def draw_mirrored_pose(self, frame, mirrored_landmarks, connections):
        """
        Draw mirrored pose landmarks and connections on a blank canvas.
        
        Args:
            frame (numpy.ndarray): Original frame to match dimensions.
            mirrored_landmarks (dict): Dictionary of mirrored landmark indices and positions.
            connections (list): List of landmark connections defined as index pairs.
            
        Returns:
            numpy.ndarray: Canvas with drawn mirrored pose.
        """
        # Create a blank canvas for drawing replicated landmarks
        replica = np.zeros_like(frame)
        
        # Draw landmark points as circles
        for position in mirrored_landmarks.values():
            cv2.circle(replica, position, self.circle_radius, self.landmark_color, -1)
        
        # Draw connections between landmarks as lines
        for connection in connections:
            start_idx, end_idx = connection
            if start_idx in mirrored_landmarks and end_idx in mirrored_landmarks:
                cv2.line(replica, mirrored_landmarks[start_idx], mirrored_landmarks[end_idx],
                         self.connection_color, self.line_thickness)
                
        return replica
    
    def create_composite(self, frame, replica):
        """
        Create a composite image by overlaying the replica on the original frame.
        
        This method combines the original frame with the mirrored pose visualization
        to create a side-by-side comparison.
        
        Args:
            frame (numpy.ndarray): Original frame.
            replica (numpy.ndarray): Canvas with mirrored pose.
            
        Returns:
            numpy.ndarray: Composite frame with original and mirrored pose.
        """
        return cv2.add(frame, replica)

"""
Dance Companion - Real-time Pose Mirroring Application

This script provides a visualization tool for dancers to see their movements mirrored in real-time.
It detects pose landmarks from a video source and creates a mirrored overlay to help with
self-assessment and technique improvement.

Author: Shubh Gupta
Version: 1.0.0
License: MIT
Date: 2025
"""

import cv2
from utils.pose_detector import PoseDetector
from utils.video_source import VideoSource
from utils.pose_visualizer import PoseVisualizer

# Initialize components with the same parameters as the original
pose_detector = PoseDetector()
video_source = VideoSource("videoplayback.mp4") # Replace with your video source
# Initialize the pose visualizer with specific parameters
pose_visualizer = PoseVisualizer(
    landmark_color=(255, 0, 0),  # Blue color for landmarks
    connection_color=(0, 0, 255),  # Red color for connections
    circle_radius=3,  # Size of landmark circles in pixels
    line_thickness=2,  # Thickness of connection lines in pixels
    offset_x=150  # Horizontal offset for the mirrored pose in pixels
)

# Main loop to process video frames
while True:
    # Read a frame from the video source
    ret, frame = video_source.read_frame()
    if not ret:
        # End of video or error reading frame
        break

    # Detect pose landmarks in the current frame
    pose_results = pose_detector.detect_landmarks(frame)
    
    if pose_results.pose_landmarks:
        # Landmarks detected - create mirrored visualization
        
        # Generate mirrored landmark positions
        mirrored_landmarks = pose_visualizer.create_mirrored_landmarks(
            pose_results.pose_landmarks, frame.shape
        )
        
        # Draw mirrored pose on a separate canvas
        replica = pose_visualizer.draw_mirrored_pose(
            frame, mirrored_landmarks, pose_detector.get_pose_connections()
        )
        
        # Create composite image by combining original frame and mirrored pose
        composite = pose_visualizer.create_composite(frame, replica)
        
        # Display the result
        cv2.imshow("Video with Replicated Landmarks Overlay", composite)
    else:
        # No landmarks detected - show original frame only
        cv2.imshow("Video with Replicated Landmarks Overlay", frame)
    
    # Exit on 'q' key press    
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Clean up resources
video_source.release()
cv2.destroyAllWindows()
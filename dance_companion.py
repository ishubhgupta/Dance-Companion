"""
Dance Companion - Command-line Interface Version

This script provides a command-line interface for the Dance Companion application,
allowing users to specify video sources and customize visualization parameters.
It detects pose landmarks from a video source and creates a mirrored overlay
to help dancers with self-assessment and technique improvement.

Author: Shubh Gupta
Version: 1.0.0
License: MIT 
Date: 2025
"""

import cv2
import argparse
from utils.pose_detector import PoseDetector
from utils.video_source import VideoSource
from utils.pose_visualizer import PoseVisualizer

def parse_arguments():
    """
    Parse command line arguments for the Dance Companion application.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Dance Companion - Pose Mirroring Tool')
    
    # Create a mutually exclusive group for video source
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('--input', type=str, help='Path to video file')
    source_group.add_argument('--webcam', type=int, help='Webcam device index')
    
    # Add visualization customization parameters
    parser.add_argument('--offset', type=int, default=150, 
                        help='Horizontal offset for mirrored pose (default: 150)')
    parser.add_argument('--radius', type=int, default=3, 
                        help='Radius of landmark circles (default: 3)')
    parser.add_argument('--thickness', type=int, default=2, 
                        help='Thickness of connection lines (default: 2)')
    
    return parser.parse_args()

def main():
    """
    Main function to run the Dance Companion application.
    Handles initialization, processing loop, and cleanup.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Determine the video source (file path or webcam index)
    source = args.input if args.input else args.webcam
    
    try:
        # Initialize components
        video_source = VideoSource(source)
        pose_detector = PoseDetector()
        pose_visualizer = PoseVisualizer(
            circle_radius=args.radius,
            line_thickness=args.thickness,
            offset_x=args.offset
        )
        
        # Create and configure display window
        window_name = "Dance Companion - Pose Mirroring"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        # Main processing loop
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
                cv2.imshow(window_name, composite)
            else:
                # No landmarks detected - show original frame only
                cv2.imshow(window_name, frame)
                
            # Exit on 'q' key press
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up resources
        video_source.release()
        cv2.destroyAllWindows()
        print("Dance Companion closed.")

if __name__ == "__main__":
    main()

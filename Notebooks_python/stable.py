import cv2

def save_frames(video_path, output_path, frame_interval):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if the video is successfully opened
    if not video.isOpened():
        print("Error opening video file")
        return

    # Initialize variables
    frame_count = 0

    # Read and save frames from the video
    while video.isOpened():
        # Read a single frame from the video
        ret, frame = video.read()

        # If the frame is successfully read
        if ret:
            # Save the frame
            if frame_count % frame_interval == 0:
                frame_filename = f"{output_path}/frame_{frame_count}.jpg"
                cv2.imwrite(frame_filename, frame)
                print(f"Saved frame {frame_count}")

            frame_count += 1
        else:
            # If there are no more frames to read, break the loop
            break

    # Release the video object
    video.release()

    print("Frame extraction completed!")

# Example usage
video_path = "D:\SEM 2\DL\stable.mp4"
output_path = "D:\SEM 2\DL\images"
frame_interval = 10  # Save every 30th frame

save_frames(video_path, output_path, frame_interval)

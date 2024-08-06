def calculate_frame_rate(total_frames, minutes, seconds):
    # Convert total duration to seconds
    total_seconds = (minutes * 60) + seconds
    
    # Calculate frame rate
    frame_rate = total_frames / total_seconds
    
    return frame_rate

# Example usage:
total_frames = 124
minutes = 2
seconds = 44

frame_rate = calculate_frame_rate(total_frames, minutes, seconds)
print(f"Required frame rate: {frame_rate:.2f} fps")

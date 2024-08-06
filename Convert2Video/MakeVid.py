import cv2
import os
import argparse
import logging
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, concatenate_videoclips

def images_to_video(input_dir, temp_video_file, frame_rate):
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Get all image files in the input directory
        image_files = [f for f in sorted(os.listdir(input_dir)) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not image_files:
            logging.error("No images found in the directory.")
            return

        # Read the first image to get the dimensions
        first_image_path = os.path.join(input_dir, image_files[0])
        frame = cv2.imread(first_image_path)
        if frame is None:
            logging.error("Failed to read the first image.")
            return

        height, width, layers = frame.shape
        size = (width, height)

        # Initialize the video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(temp_video_file, fourcc, frame_rate, size)

        for image_file in image_files:
            image_path = os.path.join(input_dir, image_file)
            frame = cv2.imread(image_path)
            if frame is not None:
                video.write(frame)
            else:
                logging.warning(f"Failed to read image: {image_path}")

        video.release()
        logging.info(f"Temporary video saved as {temp_video_file}")

    except Exception as e:
        logging.error(f"Error in images_to_video: {e}")

def collate_audio_tracks(input_dir, output_file):
    try:
        audio_files = [f for f in sorted(os.listdir(input_dir)) if f.lower().endswith('.mp3')]
        if not audio_files:
            logging.error("No audio files found in the directory.")
            return 0

        combined = AudioSegment.empty()
        for audio_file in audio_files:
            audio_path = os.path.join(input_dir, audio_file)
            audio = AudioSegment.from_mp3(audio_path)
            combined += audio

        combined.export(output_file, format="mp3")
        logging.info(f"Combined audio saved as {output_file}")

        return combined.duration_seconds

    except Exception as e:
        logging.error(f"Error in collate_audio_tracks: {e}")
        return 0

def create_text_clip(text, duration, size, fontsize=70, color='white'):
    try:
        return TextClip(text, fontsize=fontsize, color=color, size=size, bg_color='black', method='caption').set_duration(duration)
    except Exception as e:
        logging.error(f"Error in create_text_clip: {e}")
        return None

def add_audio_to_video(video_file, audio_file, output_file, title, author, title_duration, credits_duration, fontsize, color):
    try:
        video = VideoFileClip(video_file)
        audio = AudioFileClip(audio_file)
        
        width, height = video.size

        title_clip = create_text_clip(title, title_duration, (width, height), fontsize, color)
        credits_clip = create_text_clip(f"Author: {author}\n© {author}", credits_duration, (width, height), fontsize, color)

        final_video = concatenate_videoclips([title_clip, video.set_audio(audio), credits_clip])
        final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')
        logging.info(f"Final video with audio saved as {output_file}")

        # Clean up temporary files
        os.remove(video_file)
        os.remove(audio_file)

    except Exception as e:
        logging.error(f"Error in add_audio_to_video: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a sequence of images into a video, add audio, title, and credits.")
    parser.add_argument("image_directory", help="Directory containing the images")
    parser.add_argument("audio_directory", help="Directory containing the MP3 files")
    parser.add_argument("output_video_file", help="Output video file path")
    parser.add_argument("title", help="Title text for the title sequence")
    parser.add_argument("author", help="Author text for the credits sequence")
    parser.add_argument("--title_duration", type=int, default=5, help="Duration of the title sequence in seconds")
    parser.add_argument("--credits_duration", type=int, default=5, help="Duration of the credits sequence in seconds")
    parser.add_argument("--fontsize", type=int, default=70, help="Font size for the title and credits text")
    parser.add_argument("--color", default='white', help="Font color for the title and credits text")

    args = parser.parse_args()

    temp_video_path = "temp_video.mp4"
    combined_audio_path = "combined_audio.mp3"

    # Collate audio tracks
    audio_duration = collate_audio_tracks(args.audio_directory, combined_audio_path)

    # Get all image files in the input directory
    image_files = [f for f in sorted(os.listdir(args.image_directory)) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if image_files and audio_duration > 0:
        frame_rate = len(image_files) / audio_duration
        logging.info(f"Calculated frame rate: {frame_rate}")

        images_to_video(args.image_directory, temp_video_path, frame_rate)
        add_audio_to_video(temp_video_path, combined_audio_path, args.output_video_file, args.title, args.author, args.title_duration, args.credits_duration, args.fontsize, args.color)
    else:
        logging.error("No images found or audio duration is zero.")

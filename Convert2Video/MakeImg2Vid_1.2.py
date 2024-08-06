import cv2
import os
import logging
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, concatenate_videoclips
from moviepy.config import change_settings

# Specify the path to ImageMagick
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}) #!!! path will vary

def images_to_video(input_dir, temp_video_file, frame_rate):
    try:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        image_files = [f for f in sorted(os.listdir(input_dir)) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not image_files:
            logging.error("No images found in the directory.")
            return

        first_image_path = os.path.join(input_dir, image_files[0])
        frame = cv2.imread(first_image_path)
        if frame is None:
            logging.error("Failed to read the first image.")
            return

        height, width, layers = frame.shape
        size = (width, height)

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

        if title_clip is None or credits_clip is None:
            logging.error("Failed to create title or credits clip.")
            return

        final_video = concatenate_videoclips([title_clip, video.set_audio(audio), credits_clip])
        final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')
        logging.info(f"Final video with audio saved as {output_file}")

        os.remove(video_file)
        os.remove(audio_file)

    except Exception as e:
        logging.error(f"Error in add_audio_to_video: {e}")

if __name__ == "__main__":
    # Define variables for inputs and outputs
    image_directory = "/images"
    audio_directory = "/audio"
    output_video_file = "video.mp4"
    title = "My Video Title"
    author = "Author Name"
    title_duration = 5  # Duration of the title sequence in seconds
    credits_duration = 5  # Duration of the credits sequence in seconds
    fontsize = 70  # Font size for the title and credits text
    color = 'white'  # Font color for the title and credits text

    temp_video_path = "temp_video.mp4"
    combined_audio_path = "combined_audio.mp3"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    audio_duration = collate_audio_tracks(audio_directory, combined_audio_path)

    image_files = [f for f in sorted(os.listdir(image_directory)) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if image_files and audio_duration > 0:
        frame_rate = len(image_files) / audio_duration
        logging.info(f"Calculated frame rate: {frame_rate}")

        images_to_video(image_directory, temp_video_path, frame_rate)
        add_audio_to_video(temp_video_path, combined_audio_path, output_video_file, title, author, title_duration, credits_duration, fontsize, color)
    else:
        logging.error("No images found or audio duration is zero.")


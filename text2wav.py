
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import numpy as np
import torch
import soundfile as sf

speaker_embeddings = {
    "BDL": "spkemb/cmu_us_bdl_arctic-wav-arctic_a0009.npy",
    "CLB": "spkemb/cmu_us_clb_arctic-wav-arctic_a0144.npy",
    "KSP": "spkemb/cmu_us_ksp_arctic-wav-arctic_b0087.npy",
    "RMS": "spkemb/cmu_us_rms_arctic-wav-arctic_b0353.npy",
    "SLT": "spkemb/cmu_us_slt_arctic-wav-arctic_a0508.npy",
}

# Function to generate speech from text
def generate_speech(text, speaker, output_file="speech.wav"):
    try:
        # Load the processor and models
        processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

        if len(text.strip()) == 0:
            return (16000, np.zeros(0).astype(np.int16))

        # Process the input text
        inputs = processor(text=text, return_tensors="pt")

            # limit input length
        input_ids = inputs["input_ids"]
        input_ids = input_ids[..., :model.config.max_text_positions]

        # Load speaker embeddings from a dataset
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        speaker_embeddings = np.load(speaker_embeddings[speaker[:3]])
        speaker_embeddings = torch.tensor(embeddings_dataset[speaker_embedding_index]["xvector"]).unsqueeze(0)
        speaker_embeddings = torch.tensor(speaker_embeddings).unsqueeze(0)

        # Generate speech
        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        #speech = model.generate_speech(input_ids, speaker_embeddings, vocoder=vocoder)

        # Save the generated speech to a file
        speech = (speech.numpy() * 32767).astype(np.int16)
        sf.write(output_file, speech.numpy(), samplerate=16000)
        print(f"Speech generated and saved to {output_file}")
        #return (16000, speech)

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
text_to_synthesize = "Bringing the A.I. back to life was a challenge that consumed me."
# speaker_embedding_idx = 7306
speaker_embeddings = "BDL (male)"
output_filename = "sample3.wav"

generate_speech(text_to_synthesize, speaker_embeddings, output_filename)

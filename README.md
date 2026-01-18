# Samplette

Samplette is a Python application that analyzes audio samples from a YouTube playlist, extracts musical features like BPM, key, and genre tags, and stores the metadata in a Supabase database.

## Features

- Downloads audio from YouTube playlists
- Analyzes audio for:
  - BPM (Beats Per Minute)
  - Musical key and scale detection
  - Genre tags based on audio features (upbeat, chill, groovy, funky, jazzy, etc.)
- Stores sample metadata in Supabase database
- Processes up to 100 videos from a playlist

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd samplette
   ```

2. Install dependencies:

   ```bash
   pip install pytubefix librosa numpy supabase
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Supabase credentials:
     ```
     SUPABASE_KEY=your_supabase_anon_key_here
     ```

## Usage

1. Update the playlist URL in `src/main.py` if needed
2. Run the application:
   ```bash
   python src/main.py
   ```

The script will:

- Download audio from the specified YouTube playlist
- Analyze each track for musical properties
- Upload the metadata to your Supabase database
- Clean up temporary audio files

## Dependencies

- `pytubefix`: For downloading YouTube audio
- `librosa`: For audio analysis and feature extraction
- `numpy`: For numerical computations
- `supabase`: For database operations

## Configuration

- **Playlist URL**: Modify the `url` variable in `main.py` to point to your desired YouTube playlist
- **Supabase Setup**: Ensure your Supabase project has a `samples` table with appropriate columns for the metadata fields

## Database Schema

The application expects a Supabase table named `samples` with columns for:

- title
- url
- views
- likes
- bpm
- tags
- key
- scale
- duration
- author

## Key Detection

Uses the Krumhansl-Schmuckler key-finding algorithm implemented in the `Tonal_Fragment` class to determine the musical key and scale of each sample.

## Tag Generation

Generates genre tags based on audio features including:

- Tempo analysis
- Spectral centroid, bandwidth, and rolloff
- Zero-crossing rate
- RMS energy
- MFCC variance
- Chroma features
- Onset strength

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license here]

## Disclaimer

This tool downloads content from YouTube. Ensure you comply with YouTube's Terms of Service and respect copyright laws. Use responsibly and only for personal, educational, or research purposes.

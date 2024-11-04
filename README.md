# Local Network Video Player

A Flask-based web application that allows you to stream your video collection across your local network. Perfect for accessing your videos from any device on your home network through a web browser, with a clean and modern interface.

![Video Player Screenshot](screenshots/player.png)

## Features

- 🎥 Stream MP4 videos from multiple local directories
- 📁 Automatic subdirectory scanning
- 🎬 Modern video player interface (using Plyr)
- 📝 Subtitle support (.srt and .vtt)
- 🗑️ Delete videos directly from the interface
- 📱 Responsive design
- ⌨️ Keyboard shortcuts
- 🔊 Volume memory
- ⚡ Fast loading with directory caching

## Prerequisites

- Python 3.x installed
- Web browser (Chrome recommended)
- Videos in MP4 format

## Installation

1. Clone the repository: 
git clone https://github.com/mohamed-shiha/local-network-video-player.git
cd local-network-video-player

2. Install required packages:
pip install flask

## Configuration

### Setting Up Video Directories

Open `app.py` and modify the `VIDEO_DIRECTORIES` dictionary to include your video folders:

VIDEO_DIRECTORIES = {
'content': os.path.join('static', 'content'), # Default directory
'movies': r'C:\Users\YourName\Movies', # Custom directory
'series': r'D:\TV Series' # Another directory
}

### Changing Port Number

To change the default port (5000), modify the last line in `app.py`:

    app.run(host='0.0.0.0', port=YOUR_PORT, debug=True)
    
## Quick Start

### Using Run Scripts

#### Windows (run.bat):
Double-click `run.bat` or run in command prompt:

run.bat

After starting, access the app at:
- Local: `http://localhost:5000`
- Network: `http://your-ip:5000`

### Network Access
To access from other devices on your network:
1. Find your computer's IP address (use `ipconfig` in command prompt)
2. On other devices, open browser and go to: `http://YOUR_IP:5000`
3. Make sure your firewall allows incoming connections on the chosen port

## Directory Structure

local-network-video-player/
├── app.py # Main application
├── run.bat # Windows batch runner
├── static/
│ └── content/ # Default video directory
└── templates/
├── index.html # Video list page
├── player.html # Video player page
└── error.html # Error page


## Browser Support

- Google Chrome (Recommended)
- Firefox
- Microsoft Edge
- Safari
- Opera

## Troubleshooting

1. **Port Already in Use**
   - Change the port number in `app.py`
   - Kill the process using the current port

2. **Videos Not Showing**
   - Verify directory paths in `VIDEO_DIRECTORIES`
   - Ensure video files are MP4 format
   - Check directory permissions

3. **Access from Other Devices**
   - Ensure host is set to `0.0.0.0` in `app.py`
   - Allow Flask through firewall
   - Use machine's IP address instead of localhost

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Mohamed Shiha - [@mohamed-shiha](https://github.com/mohamed-shiha)

---

For more information or support, please open an issue in the GitHub repository.

## Keyboard Controls

- Space: Play/Pause
- M: Mute/Unmute
- F: Fullscreen
- ↑/↓: Volume
- ←/→: Seek
- 0-9: Seek to percentage
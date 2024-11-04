from flask import Flask, render_template, send_from_directory, abort, redirect, url_for, flash, request, jsonify
import os
import glob
from pathlib import Path
import shutil

app = Flask(__name__)
# Add a secret key for flash messages
app.secret_key = 'your_secret_key_here'  

# Define root video directories
VIDEO_DIRECTORIES = {
    'content': os.path.join('static', 'content'),
    'downloads': r'C:\Users\Mohamed\Downloads\Video'
}
SUBTITLE_FOLDER = os.path.join('static', 'subtitles')
ALLOWED_VIDEO_EXTENSIONS = {'.mp4'}
ALLOWED_SUBTITLE_EXTENSIONS = {'.srt', '.vtt'}

# Create necessary directories
os.makedirs(VIDEO_DIRECTORIES['content'], exist_ok=True)
os.makedirs(SUBTITLE_FOLDER, exist_ok=True)

def get_all_videos():
    """Get videos from all directories including subdirectories"""
    videos = []
    
    for source, root_dir in VIDEO_DIRECTORIES.items():
        if not os.path.exists(root_dir):
            continue
            
        # Walk through directory and all subdirectories
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if os.path.splitext(filename)[1].lower() in ALLOWED_VIDEO_EXTENSIONS:
                    # Get relative path from root directory
                    rel_path = os.path.relpath(dirpath, root_dir)
                    if rel_path == '.':
                        rel_path = ''
                    
                    # Full path for file operations
                    full_path = os.path.join(dirpath, filename)
                    
                    # Create video entry
                    videos.append({
                        'filename': filename,
                        'source': source,
                        'path': full_path,
                        'rel_path': rel_path,
                        'size': format_size(os.path.getsize(full_path)),
                        'folder': os.path.basename(dirpath) if rel_path else 'Root',
                        'modified': format_date(os.path.getmtime(full_path))
                    })
    
    return sorted(videos, key=lambda x: (x['source'], x['rel_path'], x['filename'].lower()))

def format_size(size):
    """Convert size to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

def format_date(timestamp):
    """Convert timestamp to readable date"""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

def get_subtitles(video_filename):
    """Get all available subtitle files for a video"""
    base_name = os.path.splitext(video_filename)[0]
    subtitles = []
    
    # Look for subtitle files
    for ext in ALLOWED_SUBTITLE_EXTENSIONS:
        pattern = os.path.join(SUBTITLE_FOLDER, f"{base_name}*{ext}")
        for subtitle_path in glob.glob(pattern):
            subtitle_file = os.path.basename(subtitle_path)
            # Try to extract language from filename (e.g., movie.en.srt -> en)
            lang = subtitle_file.replace(base_name, '').replace(ext, '').strip('.')
            if not lang:
                lang = 'Unknown'
            
            subtitles.append({
                'file': subtitle_file,
                'label': lang.upper(),
                'srclang': lang.lower()
            })
    
    return subtitles

@app.route('/')
def index():
    videos = get_all_videos()
    # Group videos by source and folder
    organized_videos = {}
    for video in videos:
        source = video['source']
        folder = os.path.join(video['rel_path']) if video['rel_path'] else 'Root'
        
        if source not in organized_videos:
            organized_videos[source] = {}
        if folder not in organized_videos[source]:
            organized_videos[source][folder] = []
            
        organized_videos[source][folder].append(video)
    
    return render_template('index.html', organized_videos=organized_videos, os=os)

@app.route('/play/<source>/<path:filepath>')
def play_video(source, filepath):
    if source not in VIDEO_DIRECTORIES:
        abort(404)
    filename = os.path.basename(filepath)
    rel_path = os.path.dirname(filepath)
    subtitles = get_subtitles(filename)
    return render_template('player.html', 
                         video=filename, 
                         source=source, 
                         rel_path=rel_path,
                         subtitles=subtitles,
                         os=os)

@app.route('/video/<source>/<path:filepath>')
def serve_video(source, filepath):
    if source not in VIDEO_DIRECTORIES:
        abort(404)
    directory = os.path.join(VIDEO_DIRECTORIES[source], os.path.dirname(filepath))
    return send_from_directory(directory, os.path.basename(filepath))

@app.route('/subtitle/<filename>')
def serve_subtitle(filename):
    return send_from_directory(SUBTITLE_FOLDER, filename)

@app.route('/delete/<source>/<path:filepath>')
def delete_video(source, filepath):
    if source not in VIDEO_DIRECTORIES:
        return jsonify({"success": False, "message": "Invalid source"}), 404
    
    try:
        # Safely join paths to prevent directory traversal
        base_dir = VIDEO_DIRECTORIES[source]
        full_path = os.path.abspath(os.path.join(base_dir, filepath))
        
        # Verify the path is within the allowed directory
        if not full_path.startswith(os.path.abspath(base_dir)):
            return jsonify({"success": False, "message": "Invalid path"}), 403
        
        if os.path.exists(full_path):
            if os.path.isfile(full_path):
                os.remove(full_path)
                print(f"Successfully deleted: {full_path}")
                
                # Optional: Remove empty directories
                try:
                    parent_dir = os.path.dirname(full_path)
                    if not os.listdir(parent_dir) and parent_dir != base_dir:
                        shutil.rmtree(parent_dir)
                        print(f"Removed empty directory: {parent_dir}")
                except Exception as e:
                    print(f"Error cleaning empty directory: {e}")
                
                return jsonify({"success": True, "message": "File deleted successfully"})
            else:
                return jsonify({"success": False, "message": "Not a file"}), 400
        else:
            return jsonify({"success": False, "message": "File not found"}), 404
            
    except Exception as e:
        print(f"Error deleting file: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

# Add error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                         error_code=404,
                         error_message="File or directory not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', 
                         error_code=500,
                         error_message="An internal error occurred"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
import os

def check_video_files():
    video_folder = os.path.join('static', 'content')
    
    # Check if folder exists
    if not os.path.exists(video_folder):
        print(f"Creating folder: {video_folder}")
        os.makedirs(video_folder)
    
    # List all files
    files = os.listdir(video_folder)
    print("\nFiles in video folder:")
    for file in files:
        full_path = os.path.join(video_folder, file)
        size = os.path.getsize(full_path) / (1024 * 1024)  # Size in MB
        print(f"- {file} ({size:.2f} MB)")

if __name__ == "__main__":
    check_video_files() 
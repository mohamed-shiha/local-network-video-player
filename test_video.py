import os
import shutil

# Create directories if they don't exist
os.makedirs('static/content', exist_ok=True)

# Create a simple text file to test the path
test_path = os.path.join('static', 'content', 'test.txt')
with open(test_path, 'w') as f:
    f.write('test')

print(f"Created test file at: {os.path.abspath(test_path)}")
print(f"Directory contents: {os.listdir(os.path.join('static', 'content'))}") 
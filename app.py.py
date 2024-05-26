from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Define your data processing functions here
def split_data_with_tracking(large_data, tracking_data, chunk_size, interval):
    chunks = []

    for i in range(0, len(large_data), chunk_size):
        chunk = large_data[i:i + chunk_size]
        for j in range(interval, len(chunk) + len(tracking_data), interval):
            if tracking_data:
                for track in tracking_data:
                    chunk.insert(j, track)
                    j += 1
        
        chunks.append(chunk)
    
    return chunks

def save_chunks_to_files(chunks, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for i, chunk in enumerate(chunks):
        file_path = os.path.join(directory, f"chunk_{i + 1}.txt")
        with open(file_path, "w") as file:
            for item in chunk:
                file.write(f"{item}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    large_data_file = request.files['large_data']
    tracking_data_file = request.files['tracking_data']
    chunk_size = int(request.form['chunk_size'])
    interval = int(request.form['interval'])

    # Read data from uploaded files
    large_data = large_data_file.read().decode('utf-8').splitlines()
    tracking_data = tracking_data_file.read().decode('utf-8').splitlines()

    # Process data
    chunks_with_tracking = split_data_with_tracking(large_data, tracking_data, chunk_size, interval)

    # Save chunks to files (optional)
    output_directory = 'output_chunks'
    save_chunks_to_files(chunks_with_tracking, output_directory)

    # Return result (for simplicity, returning plain text result)
    result = '\n'.join(['\n'.join(chunk) for chunk in chunks_with_tracking])
    return result

if __name__ == '__main__':
    app.run(debug=True)

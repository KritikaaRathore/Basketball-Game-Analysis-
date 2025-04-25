from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from analysis_script import analyze_video

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/output'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return "No file part", 400

    file = request.files['video']
    if file.filename == '':
        return "No selected file", 400

    if file:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = f"output_{filename}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        print(f"Saving uploaded video to: {input_path}")
        file.save(input_path)

        try:
            print(f"Processing video and saving to: {output_path}")
            analyze_video(input_path, output_path)
            return redirect(url_for('show_result', filename=filename))
        except Exception as e:
            return f"Error processing video: {str(e)}", 500

@app.route('/result/<filename>')
def show_result(filename):
    # Construct the output filename as done in upload_file
    output_filename = f"output_{filename}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    print(f"Checking if output video exists at: {output_path}")
    
    if os.path.exists(output_path):
        # Generate the correct static URL for the video, ensuring forward slashes
        static_path = f"output/{output_filename}".replace("\\", "/")
        video_url = url_for('static', filename=static_path)
        print(f"Video URL passed to template: {video_url}")
        return render_template('result.html', video_path=video_url)
    else:
        print(f"Output video not found at: {output_path}")
    return "Output video not found", 404

if __name__ == '__main__':
    app.run(debug=True)

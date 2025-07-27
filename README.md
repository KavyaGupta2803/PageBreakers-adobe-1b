PDF Analyzer (Adobe Hackathon)

📁 Folder Structure

├── Collection 1/              # Contains PDFs and input JSON

│   ├── challenge1b_input.json

│   ├── challenge1b_output.json

│   └── PDFs/

│       └── *.pdf

├── Collection 2/

├── Collection 3/

├── main.py                    # Main universal script

├── Dockerfile

├── requirements.txt

├── .gitignore

└── README.md


🚀 How to Use

Place each collection's challenge1b_input.json and PDFs inside Collection X folders.

Run locally or inside Docker.

Output will be saved as challenge1b_output.json inside each Collection folder.

🐳 Run with Docker

Build the Docker image:

>docker build -t adobe-pdf-analyzer .

Run the container:

On Windows (replace with full path):

docker run --rm -v %cd%/input:/app/input -v %cd%/output:/app/output adobe-pdf-analyzer

🛠 Requirements

Python 3.9+

PyMuPDF

Docker (optional for containerization)

To install dependencies locally:

pip install -r requirements.txt

👨‍💻 Contributors

This project was developed as part of Adobe’s Hackathon.

Team Name: PageBreakers

Members:

Arpita Rawat

Devanshi Jain

Kavya Gupta

✅ Credits

Thanks to the organizing team at Adobe for this challenge.

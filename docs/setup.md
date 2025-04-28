📄 setup.md

Setup Instructions

Clone the Repository:

git clone https://github.com/your-username/your-repo.git
cd your-repo

Create and Activate Virtual Environment:

python3 -m venv .venv
source .venv/bin/activate
# OR (Windows)
.venv\Scripts\activate

Install Required Packages:

pip install -r requirements.txt

Set Environment Variables:

export OPENAI_API_KEY=your-api-key
# Optional: DEEPSEEK_URL if using DeepSeek locally

Running:

python3 run_cli.py --workflow workflows/wf_example.yaml
streamlit run ui.py

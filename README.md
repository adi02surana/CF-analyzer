# Codeforces Performance Analyzer

## Overview
A Python-based tool that analyzes a user's Codeforces performance using the Codeforces API and provides actionable insights through data analysis and visualization.

## Features
- Fetches user data (ratings, submissions, profile info)
- Visualizes rating progression over time
- Analyzes problem-solving patterns by tags and difficulty
- Detects weak topics based on submission performance
- Provides basic recommendations for improvement

## Tech Stack
- Python
- pandas
- matplotlib
- seaborn
- requests

## Project Structure

```text
cf-analyzer/
│
├── 📄 main.py
├── 📄 api.py
├── 📄 analysis.py
├── 📄 visualization.py
├── 📄 utils.py
├── 📋 requirements.txt
├── 📖 README.md
└── 📁 data/
```


## How to Run
1. Clone the repository:
git clone https://github.com/adi02surana/CF-analyzer.git
cd cf-analyzer

2. Install dependencies:
pip install -r requirements.txt

3. Run the program: 
python main.py

4. Enter your Codeforces handle when prompted.

The program generates:

    Rating graph 
    Tag-wise performance chart
    Difficulty distribution
    Activity analysis

Future Improvements:

    Web interface (Streamlit)
    More advanced recommendation system
    Real-time contest performance tracking

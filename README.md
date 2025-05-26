# Health and Fitness Chatbot

A personalized diet and workout recommendation system using Google Gemini Pro.

## Features

- Personalized diet and workout recommendations
- Interactive user interface
- Weekly activity overview
- PDF report generation
- Responsive design

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repository-url>
cd health-and-fitness-chatbot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and don't share them publicly
- The `.gitignore` file is configured to exclude sensitive files

## Environment Variables

- `GOOGLE_API_KEY`: Your Google Gemini Pro API key

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

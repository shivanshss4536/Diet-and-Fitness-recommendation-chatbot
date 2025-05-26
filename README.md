# Health and Fitness Chatbot

A personalized diet and workout recommendation system using Cohere's AI API.

## Features

- Personalized diet and workout recommendations
- Interactive user interface
- Weekly activity overview
- PDF report generation
- Responsive design

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd health-and-fitness-chatbot
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get your Cohere API key:**
   - Sign up at [Cohere Dashboard](https://dashboard.cohere.com/)
   - Copy your API key from the dashboard

5. **Set your API key:**
   - For local development, create a `.env` file in the root directory:
     ```env
     COHERE_API_KEY=your_cohere_api_key_here
     ```
   - **For Streamlit Cloud deployment:**
     - Go to your app's **Settings → Secrets**
     - Add your key in TOML format:
       ```toml
       COHERE_API_KEY = "your_cohere_api_key_here"
       ```

6. **Run the application locally:**
   ```bash
   streamlit run app.py
   ```

## Security Notes

- Never commit your `.env` file or API keys to version control
- The `.gitignore` file is configured to exclude sensitive files
- Use Streamlit Cloud's Secrets management for deployment

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

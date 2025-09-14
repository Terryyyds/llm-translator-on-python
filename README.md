# AI LLM Translation Tool

A pioneering AI-powered text translation tool. Simple, fast, handy, cross-Platform LLM Text Translator Interface for everyday use, demonstrating early exploration of LLM for practical translation applications.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-green.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Year](https://img.shields.io/badge/Year-2023-purple.svg)

## 🎓 Project Background

This project emerged from the personal needs of an international student pursuing a MBIS degree. As English was a second language, frequent translation requirements during studies and programming hobbies motivated the creation of this tool. Built in 2023 when GPT-3.5 represented the pinnacle of AI technology, this project demonstrates early practical application of large language models in desktop applications.

## ✨ Project Highlights

### 🎯 Core Features
- **Intelligent Translation**: Powered by OpenAI GPT-3.5-turbo, delivering high-quality multilingual translation
- **Automatic Language Detection**: Supports automatic source language recognition without manual specification
- **Multilingual Support**: Supports English, Chinese, Spanish, Japanese, Russian, Italian, German, French, and other languages
- **Real-time Character Counting**: Live display of character counts for both source and translated text

### 🎨 User Experience
- **Intuitive Interface**: Clean left-right panel layout with clear source and translation display
- **Asynchronous Processing**: Multi-threaded architecture ensuring non-blocking user interface during translation
- **Robust Error Handling**: Comprehensive error messaging and exception handling mechanisms
- **Secure API Key Management**: Safe storage and validation of OpenAI API credentials

### 📊 Advanced Features
- **Translation History**: Automatic saving and retrieval of translation records
- **Usage Analytics**: Visual charts displaying translation usage patterns
- **Character Statistics**: Real-time non-whitespace character counting
- **Cross-platform Compatibility**: Supports Windows, macOS, and Linux operating systems


## 👀 Interface Preview

<img width="762" height="590" alt="image" src="https://github.com/user-attachments/assets/38c22f89-3205-4055-bbf9-cac27aa735b4" />

## 📖 Usage Guide

### Basic Translation
1. Enter the text to be translated in the left text panel
2. Select the target language (source language is auto-detected by default)
3. Click the "Translate" button to initiate translation
4. View the translated result in the right text panel

### Translation History
- Click the "History" button to access all translation records
- History entries include timestamps, character counts, and translation content

### Usage Analytics
- Click the "Usage Chart" button to view visual representations of your translation usage patterns

## 🛠️ Technical Architecture

### Core Technology Stack
- **GUI Framework**: Tkinter - Python's standard library graphical interface
- **AI Model**: OpenAI GPT-3.5-turbo - State-of-the-art language model (as of 2023)
- **Asynchronous Processing**: asyncio + threading - Non-blocking user experience
- **Data Visualisation**: Matplotlib - Usage statistics and analytics charts

### Project Structure
```
translator/
├── translator.py          # Main application file
├── api_key.txt           # API key storage file
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## 🔧 Configuration Options

### Supported Languages
- English
- Chinese (Simplified)
- Spanish
- Japanese
- Russian
- Italian
- German
- French
- Custom languages (user-defined)


## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- OpenAI API key

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python translator.py
```

### API Key Configuration
1. Launch the application and click the "Set API Key" button
2. Enter your OpenAI API key
3. Click "Test Key" to verify the key's validity
4. Click "Save Key" to store the key securely


## 📝 Development Information

- **Author**: Yu Deng
- **Creation Date**: 1st September 2023
- **Version**: 1.0.0

### Development Challenges Addressed
- **API Integration**: Successfully implemented OpenAI API integration with proper error handling
- **Cross-platform Compatibility**: Designed to run seamlessly on macOS, Windows, and Linux
- **User Experience**: Created an intuitive interface balancing simplicity with functionality
- **Performance Optimisation**: Implemented asynchronous processing to prevent UI blocking
- **Data Management**: Developed secure API key storage and translation history tracking

### 🔮 Future Enhancements

- [ ] Support for additional language models
- [ ] Batch translation functionality
- [ ] Translation quality assessment
- [ ] Custom translation prompts
- [ ] Voice translation capabilities
- [ ] Document format translation support


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


# Blackjack AI Assistant
# Co-author test line
Co-author test #2
Pull shark test line
Pull shark test line #2


## Overview

**Blackjack AI Assistant** is an advanced, educational blackjack tool that combines a React-based web interface with a Python backend powered by FastAPI. It features a sophisticated AI decision engine that uses basic strategy, true count card counting (Hi-Lo system), and professional-level deviations to provide optimal play recommendations. The project is designed for learning, training, and exploring advanced blackjack strategy.

## Strategy Used

This project uses a **hybrid blackjack strategy** that combines:

- **Basic Strategy:**  
  The mathematically optimal way to play every possible hand in blackjack, based on the player's cards and the dealer's upcard. This is the foundation for all decisions and is implemented in the backend as a set of rules.

- **Hi-Lo Card Counting System:**  
  The AI tracks the running count and true count using the Hi-Lo system, where:
  - 2–6 = +1
  - 7–9 = 0
  - 10, J, Q, K, A = -1  
  The true count is calculated by dividing the running count by the estimated decks remaining.

- **True Count Deviations (Index Plays):**  
  For certain hands, the AI will deviate from basic strategy if the true count reaches a specific threshold. For example:
  - **16 vs 10:** Stand instead of hit/surrender if the true count is 4 or higher.
  - **15 vs 10:** Stand at true count 4+.
  - **Insurance:** Only take insurance if the true count is 3 or higher.
  - Many other professional-level deviations are included.

- **Confidence & Risk Analytics:**  
  The AI provides a confidence score and advantage estimate for each recommendation, based on the true count and hand context.

---

## Development Approach 

1. **Backend (Python, FastAPI):**
   - Implemented the basic strategy as a Python class.
   - Built an enhanced card counter that tracks running count, true count, and deck penetration.
   - Developed a decision engine that applies basic strategy and then checks for true count deviations using a table of index plays.
   - Exposed the AI logic as a REST API using FastAPI.

2. **Frontend (React):**
   - Created a user-friendly interface for entering player and dealer cards, tracking the count, and displaying AI recommendations.
   - Integrated with the backend API to fetch real-time advice.
   - Visualized confidence, deviation, and reasoning for each decision.

3. **Testing & Simulation:**
   - Wrote unit tests to verify the AI’s decisions, including edge cases, splits, doubles, and soft hands.
   - Simulated thousands of hands to validate the strategy and counting accuracy.

4. **(Optional) Vision System:**
   - Prototyped card recognition using OpenCV and Tesseract OCR to automate card counting from screenshots.

---

**This approach allows users to learn not just basic strategy, but also advanced card counting and professional deviations, all with clear explanations and analytics.**


## Features

- **AI Decision Engine:** Python backend with enhanced basic strategy, true count deviations, and risk/confidence analytics.
- **Card Counting:** Hi-Lo system with true count calculation, deck penetration, and running count tracking.
- **Deviations:** Professional-level index plays (e.g., 16 vs 10 stand at TC 4+, insurance at TC 3+).
- **API:** FastAPI backend exposes endpoints for AI recommendations, ready for integration with any frontend.
- **Vision System (optional):** Prototype scripts for recognizing cards from screenshots using OpenCV and Tesseract OCR.
- **Unit Tests:** Robust test suite for AI logic, including edge cases, splits, doubles, and soft hands.

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/blackjack-ai-assistant.git
cd blackjack-ai-assistant
```

### 2. Install Python Dependencies

```sh
pip install -r requirements.txt
```
- Make sure you have Python 3.8+ and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed if using vision features.

### 3. Start the Backend API

```sh
uvicorn api:app --reload
```
- The API will be available at [http://localhost:8000](http://localhost:8000)
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Start the React Frontend

```sh
cd frontend
npm install
npm start
```
- The web app will be available at [http://localhost:3000](http://localhost:3000)

---

## Usage

- **Enter your hand and the dealer’s upcard** in the web interface.
- **Track the running count** as cards are dealt.
- **Get AI recommendations** for each hand, including confidence, deviation, and reasoning.
- **(Optional) Use the vision system** to detect cards from screenshots and automate counting.

---

## Project Structure

```
blackjack-ai-assistant/
│
├── api.py                      # FastAPI backend entry point
├── src/
│   └── ai_brain/
│       ├── EnhancedCardCounter.py
│       ├── basic_strategy.py
│       └── enhanced_counting_decision_engine.py
│   └── simulation/
│       └── ai_vs_ai_training.py
├── tests/
│   └── test_decision_engine.py
├── frontend/                   # React web app
│   └── src/
│       └── BlackjackAIApp.jsx
├── vision_card_detect.py       # (Optional) Card detection prototype
└── README.md
```

---

## API Example

**POST** `/ai_decision`

**Request:**
```json
{
  "player_hand": [10, 6],
  "dealer_upcard": 10,
  "running_count": 4,
  "cards_dealt": 20,
  "num_decks": 6
}
```

**Response:**
```json
{
  "action": "stand",
  "true_count": 2.5,
  "clamped_tc": 2.5,
  "confidence": 0.85,
  "deviation": false,
  "advantage": 0.01,
  "risk_level": "medium"
}
```

---

## Vision System (Prototype)

- See `vision_card_detect.py` for a starting point using OpenCV and Tesseract OCR.
- Capture screenshots of your game, crop card images, and run detection to automate counting.

---

## Testing

Run unit tests with:
```sh
python -m unittest discover tests
```

---

## Disclaimer

This project is for **educational purposes only**.  
Do not use for real-money gambling.  
Gamble responsibly.

---

## License

MIT License

---

## Contributing

Pull requests and suggestions are welcome!  
Open an issue or submit a PR to help improve the project.

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenCV](https://opencv.org/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Blackjack strategy resources from [Wizard of Odds](https://wizardofodds.com/)

---
=======
# Blackjack AI Assistant

## Overview

**Blackjack AI Assistant** is an advanced, educational blackjack tool that combines a React-based web interface with a Python backend powered by FastAPI. It features a sophisticated AI decision engine that uses basic strategy, true count card counting (Hi-Lo system), and professional-level deviations to provide optimal play recommendations. The project is designed for learning, training, and exploring advanced blackjack strategy.

---

## Features

- **Web Interface:** Intuitive React app for entering hands, tracking the count, and viewing AI recommendations.
- **AI Decision Engine:** Python backend with enhanced basic strategy, true count deviations, and risk/confidence analytics.
- **Card Counting:** Hi-Lo system with true count calculation, deck penetration, and running count tracking.
- **Deviations:** Professional-level index plays (e.g., 16 vs 10 stand at TC 4+, insurance at TC 3+).
- **API:** FastAPI backend exposes endpoints for AI recommendations, ready for integration with any frontend.
- **Vision System (optional):** Prototype scripts for recognizing cards from screenshots using OpenCV and Tesseract OCR.
- **Unit Tests:** Robust test suite for AI logic, including edge cases, splits, doubles, and soft hands.

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/blackjack-ai-assistant.git
cd blackjack-ai-assistant
```

### 2. Install Python Dependencies

```sh
pip install -r requirements.txt
```
- Make sure you have Python 3.8+ and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed if using vision features.

### 3. Start the Backend API

```sh
uvicorn api:app --reload
```
- The API will be available at [http://localhost:8000](http://localhost:8000)
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Start the React Frontend

```sh
cd frontend
npm install
npm start
```
- The web app will be available at [http://localhost:3000](http://localhost:3000)

---

## Usage

- **Enter your hand and the dealer’s upcard** in the web interface.
- **Track the running count** as cards are dealt.
- **Get AI recommendations** for each hand, including confidence, deviation, and reasoning.
- **(Optional) Use the vision system** to detect cards from screenshots and automate counting.

---

## Project Structure

```
blackjack-ai-assistant/
│
├── api.py                      # FastAPI backend entry point
├── src/
│   └── ai_brain/
│       ├── EnhancedCardCounter.py
│       ├── basic_strategy.py
│       └── enhanced_counting_decision_engine.py
│   └── simulation/
│       └── ai_vs_ai_training.py
├── tests/
│   └── test_decision_engine.py
├── frontend/                   # React web app
│   └── src/
│       └── BlackjackAIApp.jsx
├── vision_card_detect.py       # (Optional) Card detection prototype
└── README.md
```

---

## API Example

**POST** `/ai_decision`

**Request:**
```json
{
  "player_hand": [10, 6],
  "dealer_upcard": 10,
  "running_count": 4,
  "cards_dealt": 20,
  "num_decks": 6
}
```

**Response:**
```json
{
  "action": "stand",
  "true_count": 2.5,
  "clamped_tc": 2.5,
  "confidence": 0.85,
  "deviation": false,
  "advantage": 0.01,
  "risk_level": "medium"
}
```

---

## Vision System (Prototype)

- See `vision_card_detect.py` for a starting point using OpenCV and Tesseract OCR.
- Capture screenshots of your game, crop card images, and run detection to automate counting.

---

## Testing

Run unit tests with:
```sh
python -m unittest discover tests
```

---

## Disclaimer

This project is for **educational purposes only**.  
Do not use for real-money gambling.  
Gamble responsibly.

---

## License

MIT License

---

## Contributing

Pull requests and suggestions are welcome!  
Open an issue or submit a PR to help improve the project.

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [OpenCV](https://opencv.org/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Blackjack strategy resources from [Wizard of Odds](https://wizardofodds.com/)
>>>>>>> 7ec446f (yolo)


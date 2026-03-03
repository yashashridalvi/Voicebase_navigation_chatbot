🚗Voice Navigation Chatbot

A multilingual, voice-controlled navigation assistant built using Python and open-source mapping services.
This chatbot allows users to speak or type their starting location and destination, then provides real-world distance, estimated travel time, and step-by-step driving directions.

🌟 Project Overview

The Voice Navigation Chatbot works like a mini voice-based Google Maps.
Instead of typing and reading directions, users can simply speak and receive navigation instructions through voice output.

This project demonstrates integration of:

Voice processing

Real-time geocoding

Route calculation

Turn-by-turn navigation

Multilingual interaction

🎯 Key Features

✅ Voice or Text Input
✅ Voice Output (Text-to-Speech)
✅ Supports 3 Languages:
      1. English 2. Hindi #. Marathi
✅ Real-time route calculation
✅ Distance and travel time estimation
✅ Step-by-step driving directions
✅ Input cleaning for better speech accuracy
✅ Modular project structure

⚙️ How It Works
Step 1: Language Selection
User selects preferred language (English / Hindi / Marathi).
Step 2: Input Mode Selection
User chooses: 1. Type input, 2. Speak input
Step 3: Location Processing
User provides starting location and destination.
Speech is converted to text (if voice mode).
Input is cleaned to remove unnecessary words.
Step 4: Geocoding
The project uses OpenStreetMap Nominatim API to convert place names into GPS coordinates (latitude and longitude).
Step 5: Route Calculation
The coordinates are sent to the OSRM Routing API, which calculates:

Total road distance

Estimated travel time

Turn-by-turn driving instructions

Step 6: Voice Output

The chatbot speaks:

Distance

Estimated time

Step-by-step directions

🛠️ Technologies Used: 
1. Python
2. SpeechRecognition
3. gTTS (Google Text-to-Speech)
4. OpenStreetMap (Nominatim API)
5. OSRM (Open Source Routing Machine)

Example input: 
Start: Pune
Destination: Delhi

Example Output
Distance is 148 kilometers.
Estimated time is 210 minutes.
Steps: 
Turn right onto XYZ Road.
Continue straight for 2 kilometers.
Turn left at ABC Junction.

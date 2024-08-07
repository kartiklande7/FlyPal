# FlyPal

FlyPal is a Streamlit application that provides real-time flight updates at your fingertips. By leveraging the ADS-B API and LangChain's capabilities, FlyPal fetches flight data, processes it into understandable sentences, and stores it in a vector database for easy querying and retrieval. The application generates informative responses based on user queries about specific flights.

## Features

- Real-time flight data retrieval using the ADS-B API.
- Storage of flight data in a vector database using ChromaDB.
- Intelligent querying of flight data based on user input.
- Contextual conversation handling with memory using LangChain.
- Interactive user interface built with Streamlit.

## Tools and Libraries Used

- **Streamlit**: For building the interactive web application.
- **LangChain**: For managing the conversational context and generating responses.
- **ChromaDB**: For storing and querying vectorized flight data.
- **ADS-B API**: For fetching real-time flight data.
- **Ollama**: For generating embeddings and handling language model tasks.
- **Requests**: For making HTTP requests to the ADS-B API.

## Models Used

- **Language Model**: `llama3.1 8B` parameter model for generating responses.
- **Embedding Model**: `mxbai-embed-large` model for creating embeddings of flight data.

## Getting Started

### Prerequisites

- Python 3.8 or later
- Ollama installed for running the models

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/kartiklande7/flypal.git
    cd flypal
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Install Ollama: https://ollama.com/download

### Running the Models

1. Download and run the `llama3.1 8B` parameter model and the `mxbai-embed-large` embedding model using Ollama:

    ```bash
    ollama run llama3.1:8b
    ollama run mxbai-embed-large
    ```

### Running the Application

1. Start the Streamlit application:

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501` to interact with FlyPal.

## Project Structure

- `app.py`: The main Streamlit application file.
- `main.py`: Contains the core functions for fetching, processing, and querying flight data.
- `requirements.txt`: Lists the required Python packages for the project.

## How It Works

1. **User Input**: The user inputs a query about a flight in the Streamlit interface.
2. **Flight Number Extraction**: The application extracts the flight number from the user input.
3. **Flight Data Retrieval**: If a flight number is detected, the application fetches real-time flight data from the ADS-B API.
4. **Data Storage**: The processed flight data is stored in a vector database (ChromaDB).
5. **Query Handling**: If the flight number is not detected in the current input, the application searches for it in the chat history.
6. **Response Generation**: The application queries the vector database and generates a response based on the user input and the retrieved data.

Enjoy using FlyPal for all your real-time flight updates!

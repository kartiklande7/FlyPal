from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.chains import LLMChain
import chromadb
import requests
import ollama

def fetch_flight_data(callsign):
    """
    Fetches flight data from the ADS-B API.
    """
    url = f"https://opendata.adsb.fi/api/v2/callsign/{callsign}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Failed to retrieve data: {e}")

def extract_flight_number(userInput):
    """
    Extracts the flight number from the user input.
    """
    try:
        flight_number = next((word for word in userInput.split() if any(c.isalpha() for c in word) and any(c.isdigit() for c in word)), None)
        return flight_number
    except Exception as e:
        return None

def find_flight_number_in_history(history):
    """
    Searches through the chat history to find any flight number.
    """
    for message in history:
        flight_number = extract_flight_number(message['human'])
        if flight_number:
            return flight_number
    return None

def convert_to_sentences(data):
    """
    Converts flight data into understandable sentences.
    """
    try:
        ac_data = data.get('ac', [{}])[0]
        
        def safe_get(key, default="NA"):
            return ac_data.get(key, default)
        
        sentences = [
            f"The flight number {safe_get('flight').strip()} has aircraft registration {safe_get('r')}.",
            f"The aircraft for flight number {safe_get('flight').strip()} is a {safe_get('desc')}.",
            f"Flight number {safe_get('flight').strip()} is operated by {safe_get('ownOp')}.",
            f"Flight number {safe_get('flight').strip()} was manufactured in the year {safe_get('year')}.",
            f"Flight number {safe_get('flight').strip()} is currently at a barometric altitude of {safe_get('alt_baro')} feet.",
            f"Flight number {safe_get('flight').strip()} is currently at a geometric altitude of {safe_get('alt_geom')} feet.",
            f"Flight number {safe_get('flight').strip()} has a ground speed of {safe_get('gs')} knots.",
            f"Flight number {safe_get('flight').strip()} is heading {safe_get('track')} degrees.",
            f"Flight number {safe_get('flight').strip()} is descending at a rate of {safe_get('baro_rate')} feet per minute.",
            f"Flight number {safe_get('flight').strip()} has a squawk code of {safe_get('squawk')}.",
            f"Flight number {safe_get('flight').strip()} has no emergency indications.",
            f"Flight number {safe_get('flight').strip()} belongs to category {safe_get('category')}.",
            f"The latitude and longitude coordinates for flight number {safe_get('flight').strip()} are {safe_get('lat')} and {safe_get('lon')}, respectively.",
            f"Flight number {safe_get('flight').strip()} was last seen {safe_get('seen')} seconds ago.",
            f"The RSSI for flight number {safe_get('flight').strip()} is {safe_get('rssi')} dB."
        ]
        return sentences
    
    except Exception as e:
        print(f"An error occurred while converting data to sentences: {e}")
        return []

def store_documents_in_db(documents, collection_name):
    """
    Stores the documents in a vector database using ChromaDB.
    """
    client = chromadb.Client()
    
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = client.create_collection(name=collection_name)

    for i, d in enumerate(documents):
        try:
            response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
            embedding = response["embedding"]
            collection.add(
                ids=[str(i)],
                embeddings=[embedding],
                documents=[d]
            )
        except Exception as e:
            print(f"Failed to add document {i} to the collection: {e}")

    return collection

def query_document(collection_name, prompt, flight_number):
    """
    Queries the vector database for the specific prompt.
    """
    if flight_number:
        client = chromadb.Client()
        collection = client.get_collection(name=collection_name)

        try:
            response = ollama.embeddings(prompt=prompt, model="mxbai-embed-large")
            embedding = response["embedding"]
            results = collection.query(
                query_embeddings=[embedding],
                n_results=1
            )
            if results['documents']:
                data = results['documents'][0]
                return data
            else:
                return "No results found."
            
        except Exception as e:
            raise Exception(f"Failed to query document: {e}")
    else:
        return ""

def generate_response(userInput, memory):
    """
    Generates a response using the LLM chain with memory.
    """
    try:
        promptTemplate = PromptTemplate(
            input_variables=['history', 'input'],
            template="""
            You are a helpful AI assistant that provides information about flights. Keep your answers concise and informative.
            Conversation History: {history}
            human: {input}
            AI:
            """
        )

        llm = OllamaLLM(model="llama3.1", temperature=0)

        conversationChain = LLMChain(
            memory=memory,
            prompt=promptTemplate,
            llm=llm,
            verbose=True
        )

        response = conversationChain(userInput)
        return response
    
    except Exception as e:
        raise Exception(f"Failed to generate response: {e}")

import streamlit as st
from main import fetch_flight_data, store_documents_in_db, query_document, generate_response, convert_to_sentences, extract_flight_number, find_flight_number_in_history
from langchain.memory import ConversationBufferMemory
    
def main():
    memory = ConversationBufferMemory()
    st.title("FlyPal")
    st.write("Real time Flight Updates at Your Fingertips")
    userInput = st.text_input("")

    if 'chatHistory' not in st.session_state:
        st.session_state.chatHistory = []
    else:
        for message in st.session_state.chatHistory:
            memory.save_context({'input': message['human']}, {'output': message['AI']})
    
    if st.button("Submit"):
        if userInput:
            flight_number = extract_flight_number(userInput)
            if flight_number:
                print("Flight number detected:", flight_number + "\n")

            collection_name = "flight_docs"
            if flight_number:
                # Fetch flight data
                print("Fetching flight data...")
                data = fetch_flight_data(flight_number)
                print("Raw Flight Data:", data)
                print("\n")

                # Convert and print the understandable text
                print("Processing data...")
                documents = convert_to_sentences(data) 
                print("Successfully processed flight data!\n")

                st.write("Flight data retrieved successfully!")
                print("Flight Data:", documents)
                print("\n")

                # Store documents in the database
                print("Storing documents in the vector database...")
                collection = store_documents_in_db(documents, collection_name)
                print("Documents stored in the vector database.\n")
                st.write("Documents stored in the database!")

            #Find flight number in history
            if not flight_number:
                flight_number = find_flight_number_in_history(st.session_state.chatHistory)

            # Query for the specific prompt
            print("Querying the vector database for the specific prompt...")
            retrievedData = query_document(collection_name, userInput, flight_number)
            print("Data retrieved:", retrievedData)
                
            # Generate response
            if retrievedData:
                userInput = "Flight information: " + " ".join(retrievedData) +" "+ userInput
            print("Final user input:", userInput)
            
            response = generate_response(userInput, memory)
            message = {'human': userInput, 'AI': response['text']}
            st.session_state.chatHistory.append(message)
            st.write(response['text'])

if __name__ == "__main__":
    main()

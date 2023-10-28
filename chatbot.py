import numpy as np
import tensorflow as tf
import json
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load and preprocess data
# Load data
with open('C:\chatbot\murad.txt.txt', 'r') as f:
    data = json.load(f)

# Function to extract question-answer pairs from the data
def extract_qa_pairs(data, path=""):
    qa_pairs = []
    for key, value in data.items():
        if isinstance(value, dict):
            new_path = f"{path}{key} "
            qa_pairs.extend(extract_qa_pairs(value, new_path))
        else:
            question = f"{path}{key}"
            answer = value
            qa_pairs.append((question, answer))
    return qa_pairs

qa_pairs = extract_qa_pairs(data)

# Separate input texts and target texts
input_texts = [qa[0] for qa in qa_pairs]
target_texts = ['\t' + qa[1] + '\n' for qa in qa_pairs]

# Tokenize and pad sequences
tokenizer = Tokenizer(filters='')
tokenizer.fit_on_texts(input_texts + target_texts)
input_sequences = tokenizer.texts_to_sequences(input_texts)
target_sequences = tokenizer.texts_to_sequences(target_texts)
input_padded = pad_sequences(input_sequences, padding='post')
target_padded = pad_sequences(target_sequences, padding='post')

vocab_size = len(tokenizer.word_index) + 1
max_seq_length = max(max(len(seq) for seq in input_sequences), max(len(seq) for seq in target_sequences))

# Prepare data for training
history = model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
                    batch_size=64,
                    epochs=100,
                    validation_split=0.2,
                    verbose=1)

encoder_input_data = np.zeros((len(input_padded), max_seq_length, vocab_size), dtype='float32')
decoder_input_data = np.zeros((len(target_padded), max_seq_length, vocab_size), dtype='float32')
decoder_target_data = np.zeros((len(target_padded), max_seq_length, vocab_size), dtype='float32')

for i, (input_text, target_text) in enumerate(zip(input_padded, target_padded)):
    for t, word_index in enumerate(input_text):
        encoder_input_data[i, t, word_index] = 1.
    for t, word_index in enumerate(target_text):
        decoder_input_data[i, t, word_index] = 1.
        if t > 0:
            decoder_target_data[i, t - 1, word_index] = 1.

# Build the model
encoder_inputs = Input(shape=(None, vocab_size))
encoder = LSTM(256, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]

decoder_inputs = Input(shape=(None, vocab_size))
decoder_lstm = LSTM(256, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = Dense(vocab_size, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Compile and train the model
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit([encoder_input_data, decoder_input_data], decoder_target_data, batch_size=64, epochs=100, validation_split=0.2)

# Build the encoder model for prediction
encoder_model = Model(encoder_inputs, encoder_states)

# Build the decoder model for prediction
decoder_state_input_h = Input(shape=(256,))
decoder_state_input_c = Input(shape=(256,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)

# Define function to generate response
def decode_sequence(input_seq):
    states_value = encoder_model.predict(input_seq)

    target_seq = np.zeros((1, 1, vocab_size))
    target_seq[0, 0, tokenizer.word_index['\t']] = 1.

    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = tokenizer.index_word[sampled_token_index]
        decoded_sentence += sampled_char

        if sampled_char == '\n' or len(decoded_sentence) > max_seq_length:
            stop_condition = True

        target_seq = np.zeros((1, 1, vocab_size))
        target_seq[0, 0, sampled_token_index] = 1.

        states_value = [h, c]

    return decoded_sentence

# Function to chat with the bot
def chat():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        user_seq = tokenizer.texts_to_sequences([user_input])
        user_padded = pad_sequences(user_seq, maxlen=max_seq_length, padding='post')
        user_input_data = np.zeros((1, max_seq_length, vocab_size), dtype='float32')
        for t, word_index in enumerate(user_padded[0]):
            if word_index > 0:
                user_input_data[0, t, word_index] = 1.

        bot_response = decode_sequence(user_input_data)
        print("Bot:", bot_response)

if __name__ == "__main__":
    chat()

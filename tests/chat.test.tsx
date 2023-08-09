// Import the required testing libraries
import React from 'react';
import "@nivo/bar"; 
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // For custom matchers like toHaveTextContent
import Chat from '../src/components/Chat'; // Assuming this is the correct path to your Chat component

describe('<Chat />', () => {
  // Test case for checking if messages are displayed correctly
  it('displays chat messages correctly', () => {
    const messages = [
      { sender: 'user', text: 'Hello' },
      { sender: 'chatbot', text: 'Hi there, I am a chatbot' },
      { sender: 'user', text: 'How are you?' },
    ];

    render(<Chat messages={messages} />);

    // Check if all messages are displayed correctly
    messages.forEach((message) => {
      const displayedMessage = screen.getByText(message.text);
      expect(displayedMessage).toBeInTheDocument();
      expect(displayedMessage).toHaveClass(
        message.sender === 'user' ? 'text-right' : 'text-left'
      );
    });
  });

  // Test case for sending a message
  it('sends a message when the send button is clicked', () => {
    render(<Chat />);
    const input = screen.getByRole('textbox');
    const sendButton = screen.getByText('Send');

    // Type a message in the input field
    fireEvent.change(input, { target: { value: 'Hello, chatbot' } });

    // Click the send button
    fireEvent.click(sendButton);

    // Check if the message is displayed in the chat
    const sentMessage = screen.getByText('Hello, chatbot');
    expect(sentMessage).toBeInTheDocument();
    expect(sentMessage).toHaveClass('text-right');
  });

  // Test case for handling Enter key press
  it('sends a message when Enter key is pressed', () => {
    render(<Chat />);
    const input = screen.getByRole('textbox');

    // Type a message in the input field
    fireEvent.change(input, { target: { value: 'Hello, chatbot' } });

    // Press the Enter key
    fireEvent.keyPress(input, { key: 'Enter', code: 13, charCode: 13 });

    // Check if the message is displayed in the chat
    const sentMessage = screen.getByText('Hello, chatbot');
    expect(sentMessage).toBeInTheDocument();
    expect(sentMessage).toHaveClass('text-right');   
  });
});

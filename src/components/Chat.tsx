import React, { useState } from "react";
import Graph from "./graph/Graph";
import ChatService from "../service/chat";
import NewChatForm from "./NewChatForm";
import { v4 as uuidv4 } from 'uuid';
import Cookies from 'js-cookie';

export default function Chats({ chatService }: { chatService: ChatService }) {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>(
    []
  );
  const [showGraph, setShowGraph] = useState(false);
  const [isGraphLoading, setIsGraphLoading] = useState(false);

  const handleMessages = async (newMessage: any) => {
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    if (newMessage.sender === "user") {
      // 사용자 메시지를 서버로 전송하고 챗봇 응답을 반환
      try {
        // SessionID 생성 
        const sessionID = Cookies.get('sessionID') || uuidv4();
        Cookies.set('sessionID', sessionID, { expires: 1 });
        
        const response = await chatService.sendMessage(sessionID, newMessage.text);
        
        const chatbotResponse = {
          sender: "chatbot",
          text: response.answer, // 서버 응답의 answer 필드를 채팅창에 표시
        };


        setMessages((prevMessages) => [...prevMessages, chatbotResponse]);
      } catch (error) {
        console.error("Error sending message:", error);
      }
    }
  };

  const handleToggleGraph = () => {
    setShowGraph((prevState) => !prevState);
    setIsGraphLoading(true);

    setTimeout(() => {
      setIsGraphLoading(false);
    }, 1000);
  };

  return (
    <div className="flex-1 p-4">
      <div
        style={{ display: "flex", height: "90vh", backgroundColor: "white" }}
      >
        <div
          style={{ flex: 42, padding: "20px", borderRight: "1px solid #ccc" }}
        >
          <div
            style={{
              height: "580px",
              overflowY: "scroll",
              border: "1px solid #ccc",
              borderRadius: "5px",
              padding: "10px",
              position: "relative",
            }}
          >
            {messages.map((message, index) => (
              <div
                key={index}
                className={`text-${
                  message.sender === "user" ? "right" : "left"
                } mb-10`}
              >
                {message.sender === "chatbot" && (
                  <div>
                    <div className="bg-gray-200 text-black p-4 rounded-lg inline-flex items-center justify-end relative">
                      {message.text}
                    </div>
                    <div className="mt-2 flex items-center">
                      <span
                        onClick={handleToggleGraph}
                        className="cursor-pointer underline text-sm mr-2"
                      >
                        상세보기
                      </span>
                      <span
                        //onClick={handleSendMessage}
                        className="cursor-pointer underline text-sm"
                      >
                        선택하기
                      </span>
                    </div>
                  </div>
                )}
                {message.sender === "user" && (
                  <div className="bg-gray-300 text-black p-4 rounded-lg inline-block text-right">
                    {message.text}
                  </div>
                )}
              </div>
            ))}

          </div>
          <NewChatForm
            onQuestionClick={handleMessages}
            chatService={chatService}
          />
        </div>
        {showGraph && <Graph isGraphLoading={isGraphLoading} />}
      </div>
    </div>
  );
}

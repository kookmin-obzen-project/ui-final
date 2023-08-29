import React, { useState } from "react";
import Graph from "./Graph";
import ChatService from "../service/chat";
import NewChatForm from "./NewChatForm";
import "../App.css"; //수정된 App.css 파일을 불러옴

export default function Chats({ chatService }: { chatService: ChatService }) {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>(
    []
  );
  const [showGraph, setShowGraph] = useState(false);
  const [isGraphLoading, setIsGraphLoading] = useState(false);
  // 로딩 상태 추가 const [isLoading, setIsLoading] = useState(false); 

  const handleMessages = (newMessage: any) => {
    setMessages((prevMessages) => [...prevMessages, newMessage]);
  };

  const handleToggleGraph = () => {
    setShowGraph((prevState) => !prevState);
    setIsGraphLoading(true);

    setTimeout(() => {
      setIsGraphLoading(false);
    }, 1000);
  };

  return (
    <div className="flex-1 p-4 chat-container"> {/* App.css 스타일 */}
      <div className="chat-messages"> {/* App.css 스타일 사용 */}
        <div className="message-box"> {/* App.css 스타일 사용 */}
          {messages.map((message, index) => (
            <div
              key={index}
              className={`text-${message.sender === "user" ? "right" : "left"} mb-10`}
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
                    <span className="cursor-pointer underline text-sm">
                      선택하기
                    </span>
                  </div>
                </div>
              )}
              {message.sender === "user" && (
                <div className="bg-violet-100 text-black p-4 rounded-lg inline-block text-right">
                  {message.text}
                </div>
              )}
            </div>
          ))}
        </div>
        <NewChatForm onQuestionClick={handleMessages} chatService={chatService} />
      </div>
      {showGraph && <Graph isGraphLoading={isGraphLoading} />}
    </div>
  );
}

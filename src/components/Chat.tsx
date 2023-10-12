import React, { useState } from "react";
import Graph from "./graph/Graph";
import ChatService from "../service/chat";
import NewChatForm from "./NewChatForm";

export default function Chats({
  chatService,
  userSessionID, 
  chatSessionID,
}: {
  chatService: ChatService;
  userSessionID: string | null;
  chatSessionID: string | null; 
}) {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>(
    []
  );
  const [showGraph, setShowGraph] = useState(false);
  const [isGraphLoading, setIsGraphLoading] = useState(false);

  const [initialExplanationShown, setInitialExplanationShown] = useState(true);

  if (userSessionID === null || chatSessionID === null) {
    return <div className="text-red-500">유효한 세션 ID가 필요합니다.</div>;
  }  


  const handleMessages = async (newMessage: any) => {
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    if (newMessage.sender === "user" && initialExplanationShown) {
      setInitialExplanationShown(false);
    }

    if (newMessage.sender === "user") {
      // 사용자 메시지를 서버로 전송하고 챗봇 응답을 반환
      try {
        const response = await chatService.sendMessage(userSessionID, newMessage.text);
        
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
        style={{
          display: "flex",
          height: "90vh",
          backgroundColor: "white",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            flex: 42,
            padding: "20px",
            borderRight: "1px solid #ccc",
            width: "80%",
          }}
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
            {initialExplanationShown && (
              <div
                className="mb-4"
                style={{ textAlign: "center", marginTop: "480px" }}
              >
                <div
                  className="bg-gray-100 text-black p-4 rounded-lg"
                  style={{ width: "40%", float: "left", marginLeft: "8%" }}
                >
                  You can change the chat name.
                </div>
                <div className="mb-4">
                  <div
                    className="bg-gray-100 text-black p-4 rounded-lg"
                    style={{ width: "40%", float: "right", marginRight: "8%" }}
                  >
                    when you have a question, ask me.
                  </div>
                </div>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                key={index}
                className={`text-${
                  message.sender === "user" ? "right" : "left"
                } mb-10`}
              >
                {message.sender === "chatbot" && (
                  <div className="bg-pastel-blue text-black p-4 rounded-lg inline-flex items-center justify-end relative">
                    {message.text}
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
                  <div className="bg-pastel-light-blue text-black p-4 rounded-lg inline-block text-right">
                    {message.text}
                  </div>
                )}
              </div>
            ))}
          </div>
          <NewChatForm onQuestionClick={handleMessages} />
        </div>
        {showGraph && <Graph isGraphLoading={isGraphLoading} />}
      </div>
    </div>
  );
}

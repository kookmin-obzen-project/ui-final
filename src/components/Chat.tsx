import React, { useState } from "react";
import Graph from "./graph/Graph";
import ChatService from "../service/chat";
import NewChatForm from "./NewChatForm";
import { v4 as uuidv4 } from 'uuid';
import Cookies from 'js-cookie';

export default function Chats({ chatService }: { chatService: ChatService }) {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
  const [showGraph, setShowGraph] = useState(false);
  const [isGraphLoading, setIsGraphLoading] = useState(false);
  const [initialExplanationShown, setInitialExplanationShown] = useState(true);
  const [modalContent, setModalContent] = useState<string | null>(null);

  const handleMessages = async (newMessage: any) => {
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    if (newMessage.sender === "user" && initialExplanationShown) {
      setInitialExplanationShown(false);
    }

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

  const handleExplanationClick = (content: string) => {
    setModalContent(content);
  };

  const closeModal = () => {
    setModalContent(null);
  };

  return (
    <div className="flex-1 p-4">
      <div style={{ display: "flex", height: "90vh", backgroundColor: "white", justifyContent: "center" }}>
        <div style={{ flex: 42, padding: "20px", borderRight: "1px solid #ccc", width: "80%" }}>
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
              <div className="mb-4" style={{ textAlign: 'center', marginTop: '480px' }}>
                <div className="bg-gray-100 text-black p-4 rounded-lg" style={{ width: '40%', float: 'left', marginLeft: '8%' }} onClick={() => handleExplanationClick(`
                  <div class="text-xl font-bold mb-4">How to change the chat name</div>
                  <div>
                    To change the chat name, do the following:
                    <ul class="list-disc pl-6">
                      <li>Click on the "New Chat" button.</li>
                      <li>Type the new chat name and click "확인".</li>
                    </ul>
                  </div>`)}>
                  You can change the chat name.
                </div>
                <div className="mb-4">
                  <div className="bg-gray-100 text-black p-4 rounded-lg" style={{ width: '40%', float: 'right', marginRight: '8%' }} onClick={() => handleExplanationClick(`
                     <div class="text-xl font-bold mb-4">How to ask a question </div>
                     <div>
                       To ask a question, do the following:
                       <ul class="list-disc pl-6">
                         <li>Simply type your question in the chatbox </li>
                         <li>And hit Enter or click the send button.</li>
                       </ul>
                     </div>`)}>
                    When you have a question, ask me.
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
                <div>
                  <div className="bg-pastel-blue text-black p-4 rounded-lg inline-flex items-center justify-end relative">
                    {message.text}
                    </div>
                    <div className="mt-2 flex items-center">
                      <span onClick={handleToggleGraph} 
                      className="cursor-pointer underline text-sm mr-2">
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
          <NewChatForm onQuestionClick={handleMessages} chatService={chatService} />
        </div>
        {showGraph && <Graph isGraphLoading={isGraphLoading} />}
      </div>

      {modalContent && (
        <div className="fixed inset-0 flex items-center justify-end z-50"> 
          <div className="bg-white rounded-lg p-8" style={{ marginRight: '27%' }}> 
            <div className="flex justify-end">
              <button className="text-xl font-bold" onClick={closeModal}>X</button>
            </div>
            <div dangerouslySetInnerHTML={{ __html: modalContent }}></div>
          </div>
        </div>
      )}
    </div>
  );
  
}

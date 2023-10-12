import React, { useState } from "react";
import ChatListItem from "./ChatListItem";
import AddChatButton from "./AddChatButton";
import { v4 as uuidv4 } from 'uuid';
import "../../App.css";

export default function ChatList({
  isChatListVisible, 
  onChatListToggle, 
  userSessionID,
  chatSessionID,
  onUpdateChatSessionID,
}: {
  isChatListVisible: boolean;
  onChatListToggle: () => void;
  userSessionID: string | null; 
  chatSessionID: string | null;
  onUpdateChatSessionID: (selectedSessionID: string) => void; 
}) {
  const [chats, setChats] = useState<{ chatName: string; chatSessionID: string }[]>([]);
  const [selectedChat, setSelectedChat] = useState<string>("1번 채팅창");
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [newChatName, setNewChatName] = useState<string>("");
 
  const handleChatClick = (chatName: string, chatSessionID: string) => {
    setSelectedChat(chatName);
    onUpdateChatSessionID(chatSessionID); 
  };  

  const handleAddChat = () => {
    setIsModalOpen(true); // 모달 열기
  };

  const handleModalClose = () => {
    setIsModalOpen(false); // 모달 닫기
    setNewChatName(""); // 입력 필드 초기화
  };

  // 사용자가 재정의한 채팅방 이름만 저장
  const handleModalConfirm = () => {
    if (newChatName.trim() !== "") {
      // 고유한 세션 ID 생성
      const chatSessionID = uuidv4();
  
      // 채팅방 목록에 채팅방과 세션 ID 추가
      setChats((prevChats) => [...prevChats, { chatName: newChatName, chatSessionID }]);
      setSelectedChat(newChatName);
    }
    setIsModalOpen(false);
    setNewChatName("");
  };
 

  const handleRemoveChat = (chatName: string) => {
    const updatedChats = chats.filter((chat) => chat.chatName !== chatName);
    setChats(updatedChats);
  
    if (selectedChat === chatName) {
      setSelectedChat("");
    }
  };
  

  return (
    <div className={`overflow-auto w-1/5 py-4 px-2 border-r border-default-border bg-list-background ${!isChatListVisible ? 'hidden' : ''}`}>
      <AddChatButton onAddChat={handleAddChat} onChatListToggle={onChatListToggle} isChatListVisible={isChatListVisible} />
      {chats.map((chat) => (
        <ChatListItem 
          key={chat.chatName}
          chatName={chat.chatName}
          isSelected={selectedChat === chat.chatName}
          chatSessionID={chatSessionID}
          onChatClick={(chatName) => handleChatClick(chatName, chat.chatSessionID)}
          onTrashClick={handleRemoveChat}
        />
      ))}
      {isModalOpen && (
            <>
              <div className="fixed inset-0 flex items-center justify-center z-10">
                <div className="fixed inset-0 bg-black opacity-40"></div> 
                <div className="bg-white p-4 rounded-lg shadow-lg relative z-20">
                  <input
                    type="text"
                    placeholder="새 채팅 이름 입력"
                    value={newChatName}
                    onChange={(e) => setNewChatName(e.target.value)}
                  />
                  <button onClick={handleModalConfirm}style={{ marginRight: '10px' }}>확인</button>
                  <button onClick={handleModalClose}>취소</button>
                </div>
              </div>
            </>
          )}
    </div>
  );
}

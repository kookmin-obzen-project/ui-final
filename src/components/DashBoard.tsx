import React, { useState } from "react";
import Chats from "./Chat";
import ChatService from "../service/chat";
import ChatList from "./chat_list/ChatList";
import ShowChatListButton from "./chat_list/ShowChatListButton";

export default function DashBoard({
  chatService,
}: {
  chatService: ChatService;
}) {
  const [isChatListVisible, setIsChatListVisible] = useState(true);
  const [chatSessionID, setChatSessionID] = useState<string | null>(null);

  const handleToggleChatList = () => {
    setIsChatListVisible((prevState) => {
      const newState = !prevState;
      console.log(`Chat list visibility toggled: ${newState}`);
      return newState;
    });
  };

  // chatSessionID를 업데이트하는 함수
  const updateChatSessionID = (selectedSessionID: string) => {
    setChatSessionID(selectedSessionID);
  };

  return (
    <div className="flex h-screen border-obzen-purple border-solid">
      <ShowChatListButton
        onShowChatList={handleToggleChatList}
        isChatListVisible={isChatListVisible}
      />
      <ChatList
        isChatListVisible={isChatListVisible}
        onChatListToggle={handleToggleChatList}
        chatSessionID={chatSessionID} // chatSessionID를 전달
        onUpdateChatSessionID={updateChatSessionID} // chatSessionID를 업데이트하는 함수를 전달
        chatService={chatService}      />      
      <Chats chatService={chatService} chatSessionID={chatSessionID}/>
    </div>
  );
}

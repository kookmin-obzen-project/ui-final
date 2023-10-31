import { useState } from "react";
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

  const handleToggleChatList = () => {
    setIsChatListVisible((prevState) => {
      const newState = !prevState;
      console.log(`Chat list visibility toggled: ${newState}`);
      return newState;
    });
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
      />
      <Chats chatService={chatService} />
    </div>
  );
}

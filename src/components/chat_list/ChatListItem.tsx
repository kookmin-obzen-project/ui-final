import React, { useState } from "react";
import { BiComment, BiTrash } from "react-icons/bi";

interface ChatListItemProps {
  chatName: string;
  isSelected: boolean;
  chatSessionID: string | null; 
  onChatClick: (chatName: string, sessionID: string | null) => void;
  onTrashClick: (chatName: string) => void;
}

const ChatListItem: React.FC<ChatListItemProps> = ({
  chatName,
  isSelected,
  chatSessionID, 
  onChatClick,
  onTrashClick,
}) => {
  const [isHovered, setIsHovered] = useState(false); // State to track hover

  const chatBackgroundClass = isSelected
    ? "bg-list-selected rounded-lg"
    : "bg-list-background rounded-lg";

  const gradientBackgroundClass = (isSelected || isHovered)
    ? "from-list-selected rounded-lg"
    : "from-list-background rounded-lg";

  return (
    <div
      role="button"
      className={`flex py-3 px-3 items-center gap-3 relative rounded-md cursor-pointer break-all pr-14 hover:bg-list-selected group ${chatBackgroundClass}`}
      onClick={() => onChatClick(chatName, chatSessionID)}
      onMouseEnter={() => setIsHovered(true)} // Set hover state to true
      onMouseLeave={() => setIsHovered(false)} // Set hover state to false
      style={{ marginBottom: "8px" }}
    >
      <BiComment className="h-4 w-4 text-white opacity-50 mr-2" />
      <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all relative text-gray-300">
        {chatName}
        <div
          className={`absolute inset-y-0 right-0 w-8 z-10 bg-gradient-to-l ${gradientBackgroundClass}`}
        ></div>
      </div>
      <div className="absolute flex right-1 z-10 text-gray-300 visible mr-2">
        <button
          className="p-1 hover:text-white"
          onClick={(e) => {
            e.stopPropagation();
            onTrashClick(chatName);
          }}
        >
          <BiTrash className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};

export default ChatListItem;

import React from "react";
import { BiPlus } from "react-icons/bi";
import { TbLayoutSidebar, TbLayoutSidebarRight } from "react-icons/tb";

interface AddChatButtonProps {
  onAddChat: () => void;
  onChatListToggle: () => void; // isChatListVisible를 토글하기 위한 함수
  isChatListVisible: boolean;
}

const AddChatButton: React.FC<AddChatButtonProps> = ({
  onAddChat,
  onChatListToggle,
  isChatListVisible,
}) => {
  return (
    <div className="mb-3 flex flex-col gap-2">
      <div className="flex items-center gap-2">
        <button
          onClick={onAddChat}
          className="flex items-center gap-2 px-3 min-h-[44px] py-1 text-white text-sm rounded-md border border-white/20 hover:bg-gray-500/10 h-11 w-full transition-colors duration-200 cursor-pointer"
        >
          <BiPlus className="h-5 w-5" />
          <span className="truncate">New chat</span>
        </button>
        {/* Chat list toggle button */}
        <button
          onClick={onChatListToggle}
          className="flex items-center justify-center gap-2 px-3 min-h-[44px] py-1 text-white text-sm rounded-md border border-white/20 hover:bg-gray-500/10 h-11 w-11 transition-colors duration-200 cursor-pointer"
        >
          {/* Toggle icon based on isChatListVisible state */}
          {isChatListVisible ? (
            <TbLayoutSidebarRight className="h-5 w-5" />
          ) : (
            <TbLayoutSidebar className="h-5 w-5" />
          )}
        </button>
      </div>
    </div>
  );
};

export default AddChatButton;

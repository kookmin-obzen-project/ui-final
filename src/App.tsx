import "./App.css";
import Header from "./components/Header";
import ChatList from "./components/DashBoard";
import ChatService from "./service/chat";
import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import { v4 as uuidv4 } from 'uuid';


function App({ chatService }: { chatService: ChatService }) {
  const [userSessionID, setUserSessionID] = useState<string | null>(null);

  useEffect(() => {
    // 사용자의 초기 세션 ID를 가져오거나 생성합니다.
    const sessionID = Cookies.get('userSessionID') || uuidv4();
    Cookies.set('userSessionID', sessionID, { expires: 1 });
    setUserSessionID(sessionID);
  }, []);
  
  return (
    <>
      <Header />
      <ChatList chatService={chatService} userSessionID={userSessionID} />
    </>
  );
}

export default App;

import "./App.css";
import Header from "./components/Header";
import ChatService from "./service/chat";
import { useEffect, useState } from "react";
import DashBoard from "./components/DashBoard";


function App({ chatService }: { chatService: ChatService }) {
  const [userSessionID, setUserSessionID] = useState<string | null>(null);

  useEffect(() => {
    const fetchSessionID = async () => {
      const sessionID = await chatService.createSessionID();
      setUserSessionID(sessionID["data"]["session_ID"]);
      console.log(sessionID["data"]["session_ID"]);
    };
  
    fetchSessionID();
  }, []);
  


  return (
    <>
      <Header />
      <DashBoard chatService={chatService} userSessionID={userSessionID}/>
    </>
  );
}

export default App;

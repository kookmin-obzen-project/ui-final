import "./App.css";
import Cookies from "js-cookie";
import { v4 as uuidv4 } from 'uuid';
import Header from "./components/Header";
import ChatService from "./service/chat";
import { useEffect, useState } from "react";
import DashBoard from "./components/DashBoard";


function App({ chatService }: { chatService: ChatService }) {
  const [userSessionID, setUserSessionID] = useState<string | null>(null);

  useEffect(() => {
    const sessionID = Cookies.get('userSessionID') || uuidv4();
    Cookies.set('userSessionID', sessionID, { expires: 1 });
    setUserSessionID(sessionID);
  }, []);


  return (
    <>
      <Header />
      <DashBoard chatService={chatService} userSessionID={userSessionID}/>
    </>
  );
}

export default App;

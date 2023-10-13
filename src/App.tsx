import "./App.css";
import Header from "./components/Header";
import ChatService from "./service/chat";
import { useState } from "react";
import DashBoard from "./components/DashBoard";


function App({ chatService }: { chatService: ChatService }) {



  return (
    <>
      <Header />
      <DashBoard chatService={chatService}/>
    </>
  );
}

export default App;

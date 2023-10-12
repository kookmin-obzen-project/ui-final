import "./App.css";
import Header from "./components/Header";
import ChatList from "./components/DashBoard";
import ChatService from "./service/chat";
import { useQuery, useQueryClient, QueryClientProvider } from "react-query";
import Cookies from "js-cookie";
import { v4 as uuidv4 } from 'uuid';

function App({ chatService }: { chatService: ChatService }) {
  const queryClient = useQueryClient();

  const { data: userSessionID = null } = useQuery<string>("userSessionID", async () => {
    // 사용자의 초기 세션 ID를 가져오거나 생성합니다.
    const sessionID = Cookies.get('userSessionID') || uuidv4();
    Cookies.set('userSessionID', sessionID, { expires: 1 });
    return sessionID;
  });  

  return (
    <QueryClientProvider client={queryClient}>
      <Header />
      <ChatList chatService={chatService} userSessionID={userSessionID} />
    </QueryClientProvider>
  );
}

export default App;

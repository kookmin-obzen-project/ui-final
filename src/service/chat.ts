import HttpClient from "../network/http";

export default class ChatService {
  private http: HttpClient;

  constructor(http: HttpClient) {
    this.http = http;
  }

  async getChats() {
    return this.http.fetch(`/chats`, {
      method: "GET",
    });
  }

  async sendMessage(sessionID: string, message: string) {
    return this.http.fetch(`/chats/reflect`, {
      method: "POST",
      body: JSON.stringify({ sessionID: sessionID, text: message }), // 메시지를 서버로 전송
    });
  }

  async deleteChat(chatId: number) {
    return this.http.fetch(`/chats/${chatId}`, {
      method: "DELETE",
    });
  }

  async updateChat(chatId: number, text: string) {
    return this.http.fetch(`/chats/${chatId}`, {
      method: "PUT",
      body: JSON.stringify({ text }),
    });
  }

  // Session -----------------------------------------------

  async getSessionDB() {
    return this.http.fetch(`/session`, {
      method: "GET",
      body: JSON.stringify({}), // 메시지를 서버로 전송
    });
  }

  async getSessionID() {
    return this.http.fetch(`/session/session_id`, {
      method: "GET",
      body: JSON.stringify({}),
    });
  }

  async createSessionID() {
    return this.http.fetch(`/session`, {
      method: "POST",
      body: JSON.stringify({}),
    });
  }

  async deleteSessionDB() {
    return this.http.fetch(`/session`, {
      method: "DELETE",
      body: JSON.stringify({}),
    });
  }

  async deleteSessionID() {
    return this.http.fetch(`/session/session_id`, {
      method: "DELETE",
      body: JSON.stringify({}),
    });
  }

    // chatRoom -----------------------------------------------

  async getChatRoomDB() {
    return this.http.fetch(`/chatRoom`, {
      method: "GET",
      body: JSON.stringify({}),
    });
  }

  async getChatRoomUser() {
    return this.http.fetch(`/chatRoom/user`, {
      method: "GET",
      body: JSON.stringify({}),
    });
  }

  async getChatRoomID(chatRoom_ID: string) {
    return this.http.fetch(`/chatRoom/${chatRoom_ID}`, {
      method: "GET",
      body: JSON.stringify({}),
    });
  }

  async createChatRoom() {
    return this.http.fetch(`/chatRoom`, {
      method: "POST",
      body: JSON.stringify({}),
    });
  }

  async createChatRoomID(chatRoom_ID: string) {
    return this.http.fetch(`/chatRoom/{chatRoom_ID}`, {
      method: "POST",
      body: JSON.stringify({}),
    });
  }

  async createChatRoomIDandName(chatRoom_ID: string, name: string) {
    return this.http.fetch(`/chatRoom/${chatRoom_ID}/${name}`, {
      method: "POST",
      body: JSON.stringify({}),
    });
  }

  async deleteChatRoomDB() {
    return this.http.fetch(`/chatRoom`, {
      method: "DELETE",
      body: JSON.stringify({}),
    });
  }

  async deleteChatRoomID(chatRoom_ID: string) {
    return this.http.fetch(`/chatRoom/${chatRoom_ID}`, {
      method: "DELETE",
      body: JSON.stringify({}),
    });
  }

  async updateChatRoomName(chatRoom_ID: string, name: string) {
    return this.http.fetch(`/chatRoom/${chatRoom_ID}/${name}`, {
      method: "PUT",
      body: JSON.stringify({}),
    });
  }
  // chatQuestion -----------------------------------------------
  async getChatQuestionDB() {
    return this.http.fetch(`/chatQuestion`, {
      method: "GET",
      body: JSON.stringify({}),
    });
  }

  async getChatQuestionID(chatRoom_ID: string) {
    return this.http.fetch(`/chatQuestion/${chatRoom_ID}`, {
      method: "GET",
      body: JSON.stringify({}),
    });
  }

  async getChatQuestionIDandChatID(chatRoom_ID: string, chat_id: string) {
    return this.http.fetch(`/chatQuestion/${chatRoom_ID}/${chat_id} `, {
      method: "GET",
      body: JSON.stringify({}),
    });
  }

  async createChatQuestion_chatRoomID(chatRoom_ID: string) {
    return this.http.fetch(`/chatQuestion/${chatRoom_ID}`, {
      method: "POST",
      body: JSON.stringify({}),
    });
  }

  async deleteChatQuestion_chatRoomID(chatRoom_ID: string) {
    return this.http.fetch(`/chatQuestion/${chatRoom_ID}`, {
      method: "DELETE",
      body: JSON.stringify({}),
    });
  }

  async deleteChatQuestion_chatRoomID_chatID(chatRoom_ID: string, chat_id: string) {
    return this.http.fetch(`/chatQuestion/${chatRoom_ID}/${chat_id}`, {
      method: "DELETE",
      body: JSON.stringify({}),
    });
  }

  async updateChatQuestion_text(chatRoom_ID: string, chat_id: string, text: string) {
    return this.http.fetch(`/chatQuestion/${chatRoom_ID}/${chat_id}`, {
      method: "PUT",
      body: JSON.stringify({text: text}),
    });
  }
  // chatAnswer -----------------------------------------------

  async getChatAnswerDB() {
    return this.http.fetch(`/chatAnswer`, {
      method: "GET",
      body: JSON.stringify({}),
    });
  }

  async getChatAnswerID(chatRoom_ID: string) {
    return this.http.fetch(`/chatAnswer/${chatRoom_ID}`, {
      method: "GET",
      body: JSON.stringify({}),
    });
  }

  async getChatAnswerIDandChatID(chatRoom_ID: string, chat_id: number) {
    return this.http.fetch(`/chatAnswer/${chatRoom_ID}/${chat_id} `, {
      method: "GET",
      body: JSON.stringify({}),
    });
  }

  async createChatAnswer_chatRoomID(chatRoom_ID: string) {
    return this.http.fetch(`/chatAnswer/${chatRoom_ID}`, {
      method: "POST",
      body: JSON.stringify({}),
    });
  }

  async deleteChatAnswer_chatRoomID(chatRoom_ID: string) {
    return this.http.fetch(`/chatAnswer/${chatRoom_ID}`, {
      method: "DELETE",
      body: JSON.stringify({}),
    });
  }

  async deleteChatAnswer_chatRoomID_chatID(chatRoom_ID: string, chat_id: string) {
    return this.http.fetch(`/chatAnswer/${chatRoom_ID}/${chat_id}`, {
      method: "DELETE",
      body: JSON.stringify({}),
    });
  }

  async updateChatAnswer_text(chatRoom_ID: string, chat_id: string, text: string) {
    return this.http.fetch(`/chatAnswer/${chatRoom_ID}/${chat_id}`, {
      method: "PUT",
      body: JSON.stringify({text: text}),
    });
  }
}

export type ChatServiceType = typeof ChatService;

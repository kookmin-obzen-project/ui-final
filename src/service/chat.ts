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

  async sendMessage(message: string) {
    return this.http.fetch(`/chats/reflect`, {
      method: "POST",
      body: JSON.stringify({ text: message }), // 메시지를 서버로 전송
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
}

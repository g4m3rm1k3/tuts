export class APIClient {
  constructor(baseURL = "") {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: { "Content-type": "application/json", ...options.headers },
    };
    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`API Error on ${endpoint}:`, error);
      throw error;
    }
  }
  async getFiles() {
    return this.request("/api/files", { method: "GET" });
  }
}

export const apiClient = new APIClient();

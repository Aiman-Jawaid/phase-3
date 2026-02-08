// API Client for JWT-secured API calls

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  success: boolean;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      // Additional security: Check if token is expired
      if (token) {
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          const currentTime = Math.floor(Date.now() / 1000);
          if (payload.exp && payload.exp < currentTime) {
            // Token is expired, remove it
            localStorage.removeItem('token');
            return null;
          }
        } catch (e) {
          // If we can't parse the token, remove it
          localStorage.removeItem('token');
          return null;
        }
      }
      return token;
    }
    return null;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;

    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        // Add CSRF protection header if needed
        ...(typeof window !== 'undefined' && this.getAuthToken()
          ? { Authorization: `Bearer ${this.getAuthToken()}` }
          : {}),
      },
    };

    const mergedOptions = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...(options.headers as Record<string, string>),
      },
    };

    try {
      const response = await fetch(url, mergedOptions);

      // Handle 401 Unauthorized - token might be invalid
      if (response.status === 401) {
        if (typeof window !== 'undefined') {
          localStorage.removeItem('token');
        }
        throw new Error('Unauthorized: Please log in again');
      }

      // Handle network errors by checking if response is ok
      if (!response.ok) {
        const contentType = response.headers.get('content-type');
        let errorMessage = `HTTP error! status: ${response.status}`;

        // Try to get error message from response if available
        if (contentType && contentType.includes('application/json')) {
          try {
            const errorData = await response.json();
            errorMessage = errorData.error || errorMessage;
          } catch (e) {
            // If we can't parse the error response, use the status code
          }
        } else {
          // For non-JSON responses, just use status text
          errorMessage = response.statusText || errorMessage;
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();

      return {
        data,
        success: true,
      };
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error (server unreachable, DNS failure, etc.)
        return {
          error: 'Network error: Unable to connect to the server. Please check if the backend server is running.',
          success: false,
        };
      }

      return {
        error: error instanceof Error ? error.message : 'Unknown error occurred',
        success: false,
      };
    }
  }

  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  async put<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  async patch<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(body),
    });
  }

  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

// Export getAuthToken as a standalone function for use by other modules
export function getAuthToken(): string | null {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    // Additional security: Check if token is expired
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const currentTime = Math.floor(Date.now() / 1000);
        if (payload.exp && payload.exp < currentTime) {
          // Token is expired, remove it
          localStorage.removeItem('token');
          return null;
        }
      } catch (e) {
        // If we can't parse the token, remove it
        localStorage.removeItem('token');
        return null;
      }
    }
    return token;
  }
  return null;
}

export const apiClient = new ApiClient();
export default ApiClient;
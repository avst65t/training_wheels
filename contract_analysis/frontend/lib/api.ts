// API utility functions for FastAPI backend

export interface AnalysisResult {
  id: number
  filename: string
  file_hash: string
  company_name: string
  address: string
  services: {
    [serviceName: string]: string[]
  }
  costing: {
    [serviceName: string]:
      | {
          "Cost (Monthly)": string
          "Billing Cycle": string
        }
      | string
    "Total Estimated Annual Cost": string
    "Payment Terms": string
  }
  signer: {
    Company: {
      Name: string
      Title: string
    }
    Client: {
      Name: string
      Title: string
    }
  }
  end_date: string
  termination_clause: string
}

const API_BASE_URL = "http://localhost:8000"

export class ContractAPI {
  // Upload and analyze a contract
  static async analyzeContract(file: File): Promise<AnalysisResult> {
    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        const errorText = await response.text()
        let errorMessage = `HTTP error! status: ${response.status}`

        try {
          const errorData = JSON.parse(errorText)
          errorMessage = errorData.detail || errorMessage
        } catch {
          // If not JSON, use the text as error message
          errorMessage = errorText || errorMessage
        }

        throw new Error(errorMessage)
      }

      const result = await response.json()
      console.log("API Response:", result) // Debug log
      return result
    } catch (error) {
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error(
          "Cannot connect to backend server. Please ensure your FastAPI server is running on http://localhost:8000",
        )
      }
      throw error
    }
  }

  // Get all contracts from database
  static async getAllContracts(): Promise<AnalysisResult[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/contracts`, {
        method: "GET",
      })

      if (!response.ok) {
        const errorText = await response.text()
        let errorMessage = `HTTP error! status: ${response.status}`

        try {
          const errorData = JSON.parse(errorText)
          errorMessage = errorData.detail || errorMessage
        } catch {
          errorMessage = errorText || errorMessage
        }

        throw new Error(errorMessage)
      }

      const result = await response.json()
      console.log("Fetched contracts:", result) // Debug log
      return result
    } catch (error) {
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error(
          "Cannot connect to backend server. Please ensure your FastAPI server is running on http://localhost:8000",
        )
      }
      throw error
    }
  }

  // Get a specific contract by ID
  static async getContract(contractId: number): Promise<AnalysisResult> {
    try {
      const response = await fetch(`${API_BASE_URL}/contracts/${contractId}`, {
        method: "GET",
      })

      if (!response.ok) {
        const errorText = await response.text()
        let errorMessage = `HTTP error! status: ${response.status}`

        try {
          const errorData = JSON.parse(errorText)
          errorMessage = errorData.detail || errorMessage
        } catch {
          errorMessage = errorText || errorMessage
        }

        throw new Error(errorMessage)
      }

      const result = await response.json()
      return result
    } catch (error) {
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error(
          "Cannot connect to backend server. Please ensure your FastAPI server is running on http://localhost:8000",
        )
      }
      throw error
    }
  }

  // Delete a contract
  static async deleteContract(contractId: number): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/contracts/${contractId}`, {
        method: "DELETE",
      })

      if (!response.ok) {
        const errorText = await response.text()
        let errorMessage = `HTTP error! status: ${response.status}`

        try {
          const errorData = JSON.parse(errorText)
          errorMessage = errorData.detail || errorMessage
        } catch {
          errorMessage = errorText || errorMessage
        }

        throw new Error(errorMessage)
      }
    } catch (error) {
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error(
          "Cannot connect to backend server. Please ensure your FastAPI server is running on http://localhost:8000",
        )
      }
      throw error
    }
  }
}

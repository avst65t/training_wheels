"use client"

import { useState, useCallback, useEffect } from "react"
import { ContractAPI, type AnalysisResult } from "../lib/api"

export function useContracts() {
  const [contracts, setContracts] = useState<AnalysisResult[]>([])
  const [loading, setLoading] = useState(true) // Start with loading true
  const [error, setError] = useState<string | null>(null)

  // Load all contracts from database on component mount
  const loadContracts = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      console.log("Loading contracts from database...")

      const allContracts = await ContractAPI.getAllContracts()
      setContracts(allContracts)
      console.log("Loaded contracts:", allContracts)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to load contracts"
      console.error("Error loading contracts:", err)

      // Don't set error for connection issues - just use empty array
      if (errorMessage.includes("Cannot connect to backend")) {
        console.warn("Backend not available, starting with empty contracts list")
        setContracts([])
      } else {
        setError(errorMessage)
        setContracts([])
      }
    } finally {
      setLoading(false)
    }
  }, [])

  // Load contracts on mount
  useEffect(() => {
    loadContracts()
  }, [loadContracts])

  // Upload and analyze contract
  const analyzeContract = useCallback(
    async (file: File): Promise<AnalysisResult> => {
      try {
        setError(null)

        // Check if we already have this file (simple filename check)
        const existingContract = contracts.find((c) => c.filename === file.name)
        if (existingContract) {
          return existingContract
        }

        // Upload and analyze new contract
        const result = await ContractAPI.analyzeContract(file)

        // Add to local state (prepend to show newest first)
        setContracts((prev) => [result, ...prev])

        return result
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : "Failed to analyze contract"
        setError(errorMessage)
        throw new Error(errorMessage)
      }
    },
    [contracts],
  )

  // Refresh contracts from database
  const refreshContracts = useCallback(async () => {
    await loadContracts()
  }, [loadContracts])

  // Clear error
  const clearError = useCallback(() => {
    setError(null)
  }, [])

  // Remove contract (delete from database and local state)
  const removeContract = useCallback(async (id: number) => {
    try {
      await ContractAPI.deleteContract(id)
      setContracts((prev) => prev.filter((c) => c.id !== id))
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to delete contract"
      setError(errorMessage)
    }
  }, [])

  return {
    contracts,
    loading,
    error,
    analyzeContract,
    refreshContracts,
    clearError,
    removeContract,
  }
}

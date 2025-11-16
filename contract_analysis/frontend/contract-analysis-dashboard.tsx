"use client"

import type React from "react"
import { useState } from "react"
import {
  Upload,
  FileText,
  Calendar,
  DollarSign,
  Users,
  AlertTriangle,
  CheckCircle,
  Clock,
  Search,
  Eye,
  AlertCircle,
  X,
  MapPin,
  CreditCard,
  Building,
  RefreshCw,
  Loader2,
  Trash2,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useContracts } from "./hooks/use-contracts"
import type { AnalysisResult } from "./lib/api"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"

export default function ContractAnalysisDashboard() {
  const { contracts, loading, error, analyzeContract, refreshContracts, clearError, removeContract } = useContracts()
  const [selectedContract, setSelectedContract] = useState<AnalysisResult | null>(null)
  const [searchTerm, setSearchTerm] = useState("")
  const [dragActive, setDragActive] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [showDetailsModal, setShowDetailsModal] = useState(false)
  const [modalContract, setModalContract] = useState<AnalysisResult | null>(null)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [deletingIds, setDeletingIds] = useState<Set<number>>(new Set())

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0])
    }
  }

  const handleFileUpload = async (file: File) => {
    if (file.type !== "application/pdf") {
      setUploadError("Please upload a PDF file")
      return
    }

    if (file.size > 10 * 1024 * 1024) {
      setUploadError("File size must be less than 10MB")
      return
    }

    setIsUploading(true)
    setUploadError(null)
    clearError()

    try {
      const result = await analyzeContract(file)
      console.log("Upload result:", result) // Debug log
      setSelectedContract(result)

      // Automatically open the modal to show results
      setModalContract(result)
      setShowDetailsModal(true)
    } catch (err) {
      console.error("Upload error:", err) // Debug log
      setUploadError(err instanceof Error ? err.message : "Failed to upload contract")
    } finally {
      setIsUploading(false)
    }
  }

  const handleRefresh = async () => {
    setIsRefreshing(true)
    try {
      await refreshContracts()
    } finally {
      setIsRefreshing(false)
    }
  }

  const handleDelete = async (contractId: number, event: React.MouseEvent) => {
    event.stopPropagation() // Prevent opening the modal

    setDeletingIds((prev) => new Set(prev).add(contractId))

    try {
      await removeContract(contractId)
      console.log(`Contract ${contractId} deleted successfully`)
    } catch (error) {
      console.error("Failed to delete contract:", error)
    } finally {
      setDeletingIds((prev) => {
        const newSet = new Set(prev)
        newSet.delete(contractId)
        return newSet
      })
    }
  }

  const filteredContracts = contracts.filter(
    (contract) =>
      contract.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
      contract.company_name.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  const openDetailsModal = (contract: AnalysisResult) => {
    console.log("Opening modal for contract:", contract) // Debug log
    setModalContract(contract)
    setShowDetailsModal(true)
  }

  // Helper function to check if costing entry is a service cost object
  const isServiceCost = (value: any): value is { "Cost (Monthly)": string; "Billing Cycle": string } => {
    return value && typeof value === "object" && "Cost (Monthly)" in value && "Billing Cycle" in value
  }

  // Helper function to render text with proper line breaks as HTML
  const renderFormattedTextAsHTML = (text: string | null | undefined) => {
    if (!text) return "N/A"

    // Split by newlines and process each line
    const lines = text.split("\n")
    const processedLines = lines
      .map((line, index) => {
        const trimmedLine = line.trim()

        // Handle empty lines - create spacing
        if (trimmedLine === "") {
          return "<br />"
        }

        // Handle headers (lines ending with :)
        if (trimmedLine.endsWith(":") && trimmedLine.length > 1) {
          return `<div style="font-weight: 600; margin-bottom: 8px; margin-top: ${index > 0 ? "12px" : "0"};">${trimmedLine}</div>`
        }

        // Handle numbered list items (- 1., - 2., etc.)
        if (trimmedLine.match(/^-\s*\d+\./)) {
          const content = trimmedLine.substring(trimmedLine.indexOf(".") + 1).trim()
          const number = trimmedLine.match(/\d+/)?.[0] || ""
          return `<div style="display: flex; margin-bottom: 6px; margin-left: 16px;"><span style="margin-right: 8px; font-weight: 500; color: #374151;">${number}.</span><span style="flex: 1;">${content}</span></div>`
        }

        // Handle bullet points (-, •, *, etc.)
        if (trimmedLine.match(/^[-•*]\s/)) {
          const content = trimmedLine.substring(2)
          return `<div style="display: flex; margin-bottom: 6px; margin-left: 16px;"><span style="margin-right: 8px; color: #6B7280;">•</span><span style="flex: 1;">${content}</span></div>`
        }

        // Regular line
        if (trimmedLine) {
          return `<div style="margin-bottom: 4px;">${trimmedLine}</div>`
        }

        return ""
      })
      .filter((line) => line !== "") // Remove empty strings

    return processedLines.join("")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="container mx-auto p-4 sm:p-6 max-w-7xl">
        {/* Header */}
        <div className="mb-6 sm:mb-8">
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-slate-800 mb-2">Contract Analysis</h1>
          <p className="text-sm sm:text-base text-slate-600">Upload and analyze contracts with AI-powered extraction</p>
        </div>

        {/* Global Error Alert */}
        {error && (
          <Alert className="mb-4 sm:mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-700 flex items-center justify-between">
              <span className="text-sm sm:text-base">{error}</span>
              <Button variant="ghost" size="sm" onClick={clearError}>
                <X className="h-4 w-4" />
              </Button>
            </AlertDescription>
          </Alert>
        )}

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-4 sm:gap-6">
          {/* Upload Section */}
          <div className="xl:col-span-2">
            <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg sm:text-xl text-slate-800">Upload Contract</CardTitle>
                <CardDescription className="text-sm sm:text-base">
                  Drag and drop your PDF contract or click to browse
                </CardDescription>
              </CardHeader>
              <CardContent>
                {/* Upload Error Alert */}
                {uploadError && (
                  <Alert className="mb-4 border-red-200 bg-red-50">
                    <AlertCircle className="h-4 w-4 text-red-600" />
                    <AlertDescription className="text-red-700 flex items-center justify-between">
                      <span className="text-sm">{uploadError}</span>
                      <Button variant="ghost" size="sm" onClick={() => setUploadError(null)}>
                        <X className="h-4 w-4" />
                      </Button>
                    </AlertDescription>
                  </Alert>
                )}

                <div
                  className={`relative border-2 border-dashed rounded-xl p-6 sm:p-8 text-center transition-all duration-200 ${
                    dragActive
                      ? "border-blue-400 bg-blue-50"
                      : "border-slate-300 hover:border-slate-400 hover:bg-slate-50"
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    disabled={isUploading}
                  />

                  {isUploading ? (
                    <div className="space-y-4">
                      <Clock className="h-10 sm:h-12 w-10 sm:w-12 text-blue-500 mx-auto animate-spin" />
                      <div>
                        <p className="text-sm sm:text-base text-slate-600 mb-2">Uploading and analyzing contract...</p>
                        <p className="text-xs sm:text-sm text-slate-500">This may take a few moments</p>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <Upload className="h-10 sm:h-12 w-10 sm:w-12 text-slate-400 mx-auto" />
                      <div>
                        <p className="text-base sm:text-lg font-medium text-slate-700">Drop your contract here</p>
                        <p className="text-sm sm:text-base text-slate-500">
                          or click to browse files (PDF only, max 10MB)
                        </p>
                      </div>
                      <Button variant="outline" className="mt-4" size="sm">
                        Choose File
                      </Button>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Quick Results Preview */}
            {selectedContract && (
              <Card className="mt-4 sm:mt-6 border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                <CardHeader className="pb-4">
                  <CardTitle className="text-lg sm:text-xl text-slate-800">Latest Analysis</CardTitle>
                  <CardDescription className="text-sm sm:text-base">
                    Quick preview for {selectedContract.filename}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="flex items-center space-x-3 p-3 bg-slate-50 rounded-lg">
                      <Building className="h-5 w-5 text-slate-600 flex-shrink-0" />
                      <div className="min-w-0">
                        <p className="text-sm font-medium text-slate-700">Company</p>
                        <p className="text-sm text-slate-600 truncate">{selectedContract.company_name || "N/A"}</p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3 p-3 bg-slate-50 rounded-lg">
                      <Calendar className="h-5 w-5 text-slate-600 flex-shrink-0" />
                      <div className="min-w-0">
                        <p className="text-sm font-medium text-slate-700">End Date</p>
                        <p className="text-sm text-slate-600 truncate">{selectedContract.end_date || "N/A"}</p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-4">
                    <Button onClick={() => openDetailsModal(selectedContract)} className="w-full" size="sm">
                      View Full Analysis
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* History Section */}
          <div>
            <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg sm:text-xl text-slate-800 flex items-center justify-between">
                  <span>Contract History</span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleRefresh}
                    disabled={isRefreshing}
                    className="h-8 w-8 p-0"
                  >
                    {isRefreshing ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
                  </Button>
                </CardTitle>
                <CardDescription className="text-sm sm:text-base">
                  {loading ? "Loading contracts..." : `${contracts.length} contracts in database`}
                </CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                <div className="p-4 border-b">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                    <Input
                      placeholder="Search contracts..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10 text-sm"
                      disabled={loading}
                    />
                  </div>
                </div>

                <ScrollArea className="h-80 sm:h-96">
                  {loading ? (
                    <div className="p-4 text-center">
                      <Loader2 className="h-6 sm:h-8 w-6 sm:w-8 mx-auto mb-2 text-slate-400 animate-spin" />
                      <p className="text-xs sm:text-sm text-slate-500">Loading contracts from database...</p>
                    </div>
                  ) : filteredContracts.length === 0 ? (
                    <div className="p-4 text-center">
                      <FileText className="h-6 sm:h-8 w-6 sm:w-8 mx-auto mb-2 text-slate-400" />
                      <p className="text-xs sm:text-sm text-slate-500">
                        {searchTerm ? "No contracts match your search" : "No contracts found in database"}
                      </p>
                      <p className="text-xs text-slate-400 mt-1">Upload a PDF to get started</p>
                    </div>
                  ) : (
                    <div className="p-4 space-y-3">
                      {filteredContracts.map((contract) => (
                        <div
                          key={contract.id}
                          className={`p-3 rounded-lg border transition-all duration-200 cursor-pointer hover:shadow-md ${
                            selectedContract?.id === contract.id
                              ? "bg-blue-50 border-blue-200"
                              : "bg-white border-slate-200 hover:border-slate-300"
                          }`}
                          onClick={() => openDetailsModal(contract)}
                        >
                          <div className="flex items-start justify-between">
                            <div className="flex-1 min-w-0 mr-2">
                              <div className="flex items-center space-x-2 mb-1">
                                <CheckCircle className="h-4 w-4 text-emerald-500 flex-shrink-0" />
                                <p className="text-sm font-medium text-slate-800 truncate">{contract.filename}</p>
                              </div>
                              <p className="text-xs text-slate-600 truncate">{contract.company_name}</p>
                              <div className="flex items-center justify-between mt-2">
                                <Badge
                                  variant="outline"
                                  className="bg-emerald-50 text-emerald-700 border-emerald-200 text-xs"
                                >
                                  Analyzed
                                </Badge>
                              </div>
                            </div>

                            <div className="flex items-center space-x-1">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={(e) => {
                                  e.stopPropagation()
                                  openDetailsModal(contract)
                                }}
                                className="h-8 w-8 p-0"
                              >
                                <Eye className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={(e) => handleDelete(contract.id, e)}
                                disabled={deletingIds.has(contract.id)}
                                className="h-8 w-8 p-0 text-red-600 hover:text-red-700 hover:bg-red-50"
                              >
                                {deletingIds.has(contract.id) ? (
                                  <Loader2 className="h-4 w-4 animate-spin" />
                                ) : (
                                  <Trash2 className="h-4 w-4" />
                                )}
                              </Button>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </ScrollArea>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Contract Details Modal */}
        <Dialog open={showDetailsModal} onOpenChange={setShowDetailsModal}>
          <DialogContent className="max-w-[95vw] sm:max-w-6xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle className="text-lg sm:text-xl text-slate-800">Contract Analysis Results</DialogTitle>
              <DialogDescription className="text-sm sm:text-base">
                Detailed analysis for {modalContract?.filename}
              </DialogDescription>
            </DialogHeader>

            {modalContract ? (
              <div className="space-y-4 sm:space-y-6">
                {/* Company Information */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
                  <div className="flex items-start space-x-3 p-4 bg-slate-50 rounded-lg">
                    <Building className="h-5 sm:h-6 w-5 sm:w-6 text-slate-600 mt-1 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-700">Company Name</p>
                      <p className="text-sm sm:text-base text-slate-800 font-semibold break-words">
                        {modalContract.company_name || "N/A"}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-3 p-4 bg-slate-50 rounded-lg">
                    <MapPin className="h-5 sm:h-6 w-5 sm:w-6 text-slate-600 mt-1 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-700">Address</p>
                      <div
                        className="text-slate-800 text-sm leading-relaxed break-words"
                        dangerouslySetInnerHTML={{
                          __html: renderFormattedTextAsHTML(modalContract.address),
                        }}
                      />
                    </div>
                  </div>
                </div>

                {/* Services */}
                {modalContract.services && Object.keys(modalContract.services).length > 0 && (
                  <div className="space-y-4">
                    <h4 className="text-base sm:text-lg font-semibold text-slate-800 flex items-center">
                      <FileText className="h-4 sm:h-5 w-4 sm:w-5 mr-2" />
                      Services Provided
                    </h4>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                      {Object.entries(modalContract.services).map(([serviceName, serviceDetails]) => (
                        <div key={serviceName} className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                          <h5 className="font-semibold text-blue-800 mb-3 text-sm sm:text-base break-words">
                            {serviceName}
                          </h5>
                          <ul className="space-y-2">
                            {Array.isArray(serviceDetails) &&
                              serviceDetails.map((detail, index) => (
                                <li key={index} className="text-blue-700 text-sm flex items-start">
                                  <span className="text-blue-500 mr-2 mt-1 flex-shrink-0">•</span>
                                  <span className="flex-1 break-words">{detail}</span>
                                </li>
                              ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Costing Information */}
                {modalContract.costing && (
                  <div className="space-y-4">
                    <h4 className="text-base sm:text-lg font-semibold text-slate-800 flex items-center">
                      <DollarSign className="h-4 sm:h-5 w-4 sm:w-5 mr-2" />
                      Cost Breakdown
                    </h4>

                    {/* Service Costs */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                      {Object.entries(modalContract.costing)
                        .filter(([key, value]) => isServiceCost(value))
                        .map(([serviceName, costDetails]) => {
                          const details = costDetails as { "Cost (Monthly)": string; "Billing Cycle": string }
                          return (
                            <div key={serviceName} className="p-4 bg-green-50 border border-green-200 rounded-lg">
                              <h5 className="font-semibold text-green-800 mb-3 text-sm sm:text-base break-words">
                                {serviceName}
                              </h5>
                              <div className="space-y-2">
                                <div className="flex justify-between items-center">
                                  <span className="text-green-700 text-sm font-medium">Monthly Cost:</span>
                                  <span className="text-green-800 font-bold text-sm sm:text-base">
                                    {details["Cost (Monthly)"]}
                                  </span>
                                </div>
                                <div className="flex justify-between items-center">
                                  <span className="text-green-700 text-sm font-medium">Billing Cycle:</span>
                                  <Badge
                                    variant="outline"
                                    className="bg-green-100 text-green-800 border-green-300 text-xs"
                                  >
                                    {details["Billing Cycle"]}
                                  </Badge>
                                </div>
                              </div>
                            </div>
                          )
                        })}
                    </div>

                    {/* Total Cost and Payment Terms */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                      {modalContract.costing["Total Estimated Annual Cost"] && (
                        <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
                          <div className="flex items-center space-x-3">
                            <DollarSign className="h-6 sm:h-8 w-6 sm:w-8 text-purple-600 flex-shrink-0" />
                            <div className="min-w-0">
                              <p className="text-sm font-medium text-purple-700">Total Annual Cost</p>
                              <p className="text-purple-800 font-bold text-lg sm:text-xl break-words">
                                {modalContract.costing["Total Estimated Annual Cost"]}
                              </p>
                            </div>
                          </div>
                        </div>
                      )}

                      {modalContract.costing["Payment Terms"] && (
                        <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
                          <div className="flex items-start space-x-3">
                            <CreditCard className="h-5 sm:h-6 w-5 sm:w-6 text-indigo-600 mt-1 flex-shrink-0" />
                            <div className="min-w-0">
                              <p className="text-sm font-medium text-indigo-700 mb-1">Payment Terms</p>
                              <div
                                className="text-indigo-800 text-sm leading-relaxed break-words"
                                dangerouslySetInnerHTML={{
                                  __html: renderFormattedTextAsHTML(modalContract.costing["Payment Terms"]),
                                }}
                              />
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Signers */}
                {modalContract.signer && (modalContract.signer.Company || modalContract.signer.Client) && (
                  <div className="space-y-4">
                    <h4 className="text-base sm:text-lg font-semibold text-slate-800 flex items-center">
                      <Users className="h-4 sm:h-5 w-4 sm:w-5 mr-2" />
                      Contract Signatories
                    </h4>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                      {modalContract.signer.Company && (
                        <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
                          <div className="flex items-center space-x-2 mb-3">
                            <Building className="h-4 sm:h-5 w-4 sm:w-5 text-amber-600" />
                            <p className="text-sm font-semibold text-amber-800">Company Representative</p>
                          </div>
                          <div className="space-y-2 text-sm">
                            <div className="flex justify-between">
                              <span className="font-medium text-amber-700">Name:</span>
                              <span className="text-amber-800 break-words">{modalContract.signer.Company.Name}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="font-medium text-amber-700">Title:</span>
                              <span className="text-amber-800 break-words">{modalContract.signer.Company.Title}</span>
                            </div>
                          </div>
                        </div>
                      )}

                      {modalContract.signer.Client && (
                        <div className="p-4 bg-teal-50 border border-teal-200 rounded-lg">
                          <div className="flex items-center space-x-2 mb-3">
                            <Users className="h-4 sm:h-5 w-4 sm:w-5 text-teal-600" />
                            <p className="text-sm font-semibold text-teal-800">Client Representative</p>
                          </div>
                          <div className="space-y-2 text-sm">
                            <div className="flex justify-between">
                              <span className="font-medium text-teal-700">Name:</span>
                              <span className="text-teal-800 break-words">{modalContract.signer.Client.Name}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="font-medium text-teal-700">Title:</span>
                              <span className="text-teal-800 break-words">{modalContract.signer.Client.Title}</span>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                <Separator />

                {/* Contract Terms */}
                <div className="space-y-4">
                  <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                    <div className="flex items-center space-x-2 mb-3">
                      <Calendar className="h-4 sm:h-5 w-4 sm:w-5 text-red-600" />
                      <p className="text-sm font-semibold text-red-800">Contract End Date</p>
                    </div>
                    <p className="text-red-700 font-semibold text-base sm:text-lg break-words">
                      {modalContract.end_date || "N/A"}
                    </p>
                  </div>

                  <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                    <div className="flex items-start space-x-2 mb-3">
                      <AlertTriangle className="h-4 sm:h-5 w-4 sm:w-5 text-orange-600 mt-1 flex-shrink-0" />
                      <p className="text-sm font-semibold text-orange-800">Termination Clause</p>
                    </div>
                    <div
                      className="text-orange-700 text-sm leading-relaxed break-words"
                      dangerouslySetInnerHTML={{
                        __html: renderFormattedTextAsHTML(modalContract.termination_clause),
                      }}
                    />
                  </div>
                </div>

                {/* Contract Metadata */}
                <div className="border-t pt-4">
                  <h4 className="text-sm font-medium text-slate-700 mb-3">File Information</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
                    <div>
                      <p className="text-slate-500">Contract ID</p>
                      <p className="text-slate-700 font-mono">#{modalContract.id}</p>
                    </div>
                    <div>
                      <p className="text-slate-500">File Hash</p>
                      <p className="text-slate-700 font-mono text-xs break-all">
                        {modalContract.file_hash.substring(0, 12)}...
                      </p>
                    </div>
                    <div>
                      <p className="text-slate-500">Status</p>
                      <Badge variant="outline" className="bg-emerald-50 text-emerald-700 border-emerald-200 text-xs">
                        Completed
                      </Badge>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <AlertCircle className="h-10 sm:h-12 w-10 sm:w-12 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-600">No contract data available</p>
              </div>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}

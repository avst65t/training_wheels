"use client"

import { useState, useCallback } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle } from "@/components/ui/sheet"
import { Upload, FileText, CheckCircle, Copy, Calendar, DollarSign, Users, AlertTriangle, Download } from "lucide-react"
import { FileUploadZone } from "@/components/file-upload-zone"
import { ContractResults } from "@/components/contract-results"
import { ContractHistory } from "@/components/contract-history"

interface Contract {
  id: string
  filename: string
  uploadTime: string
  status: "analyzing" | "analyzed" | "duplicate" | "failed"
  extractedData?: {
    companyName: string
    services: string[]
    totalValue: string
    signerDetails: {
      name: string
      title: string
      email: string
    }
    endDate: string
    terminationClause: string
    keyTerms: string[]
  }
}

export function ContractDashboard() {
  const [contracts, setContracts] = useState<Contract[]>([
    {
      id: "1",
      filename: "service-agreement-2024.pdf",
      uploadTime: "2024-01-15T10:30:00Z",
      status: "analyzed",
      extractedData: {
        companyName: "TechCorp Solutions Inc.",
        services: ["Software Development", "Technical Consulting", "System Integration"],
        totalValue: "$125,000",
        signerDetails: {
          name: "Sarah Johnson",
          title: "Chief Technology Officer",
          email: "sarah.johnson@techcorp.com",
        },
        endDate: "2024-12-31",
        terminationClause: "30-day written notice required by either party",
        keyTerms: ["Intellectual Property Rights", "Confidentiality Agreement", "Payment Terms"],
      },
    },
    {
      id: "2",
      filename: "vendor-contract-q1.pdf",
      uploadTime: "2024-01-14T14:22:00Z",
      status: "analyzed",
      extractedData: {
        companyName: "Global Supplies Ltd.",
        services: ["Equipment Rental", "Maintenance Services"],
        totalValue: "$75,500",
        signerDetails: {
          name: "Michael Chen",
          title: "Operations Manager",
          email: "michael.chen@globalsupplies.com",
        },
        endDate: "2024-06-30",
        terminationClause: "14-day notice period with penalty clause",
        keyTerms: ["Service Level Agreement", "Equipment Warranty", "Liability Coverage"],
      },
    },
    {
      id: "3",
      filename: "partnership-agreement.pdf",
      uploadTime: "2024-01-13T09:15:00Z",
      status: "duplicate",
    },
  ])

  const [selectedContract, setSelectedContract] = useState<Contract | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)

  const handleFileUpload = useCallback(
    async (files: File[]) => {
      const file = files[0]
      if (!file) return

      // Check for duplicates (simplified)
      const isDuplicate = contracts.some((contract) => contract.filename === file.name)

      const newContract: Contract = {
        id: Date.now().toString(),
        filename: file.name,
        uploadTime: new Date().toISOString(),
        status: isDuplicate ? "duplicate" : "analyzing",
      }

      setContracts((prev) => [newContract, ...prev])

      if (isDuplicate) {
        // Find existing contract data
        const existingContract = contracts.find((c) => c.filename === file.name && c.extractedData)
        if (existingContract?.extractedData) {
          setContracts((prev) =>
            prev.map((c) =>
              c.id === newContract.id ? { ...c, status: "analyzed", extractedData: existingContract.extractedData } : c,
            ),
          )
        }
        return
      }

      // Simulate analysis process
      setIsAnalyzing(true)
      setUploadProgress(0)

      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + Math.random() * 15
        })
      }, 200)

      // Simulate API call
      setTimeout(() => {
        clearInterval(progressInterval)
        setUploadProgress(100)

        setTimeout(() => {
          const mockExtractedData = {
            companyName: "Acme Corporation",
            services: ["Consulting Services", "Project Management"],
            totalValue: "$95,000",
            signerDetails: {
              name: "Jane Smith",
              title: "Director of Operations",
              email: "jane.smith@acme.com",
            },
            endDate: "2024-09-30",
            terminationClause: "60-day written notice required",
            keyTerms: ["Non-Disclosure Agreement", "Payment Schedule", "Deliverables"],
          }

          setContracts((prev) =>
            prev.map((contract) =>
              contract.id === newContract.id
                ? { ...contract, status: "analyzed", extractedData: mockExtractedData }
                : contract,
            ),
          )

          setIsAnalyzing(false)
          setUploadProgress(0)
        }, 1000)
      }, 3000)
    },
    [contracts],
  )

  const analyzedContracts = contracts.filter((c) => c.status === "analyzed").length
  const totalValue = contracts
    .filter((c) => c.extractedData?.totalValue)
    .reduce((sum, c) => {
      const value = Number.parseInt(c.extractedData!.totalValue.replace(/[$,]/g, ""))
      return sum + value
    }, 0)

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="border-b border-slate-200/60 bg-white/80 backdrop-blur-xl px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Contract Analysis</h1>
              <p className="text-slate-600 mt-1">Upload and analyze your contracts with AI-powered insights</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-slate-500">Total Analyzed</p>
                <p className="text-2xl font-bold text-slate-900">{analyzedContracts}</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-slate-500">Total Value</p>
                <p className="text-2xl font-bold text-green-600">${totalValue.toLocaleString()}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
            {/* Upload Section */}
            <div className="lg:col-span-2 space-y-6">
              <Card className="border-slate-200/60 shadow-sm bg-white/80 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-900">
                    <Upload className="h-5 w-5 text-blue-600" />
                    Upload Contract
                  </CardTitle>
                  <CardDescription>Drag and drop your contract files or click to browse</CardDescription>
                </CardHeader>
                <CardContent>
                  <FileUploadZone onFileUpload={handleFileUpload} isAnalyzing={isAnalyzing} progress={uploadProgress} />
                </CardContent>
              </Card>

              {/* Analysis Results */}
              {contracts.length > 0 && contracts[0].status === "analyzed" && contracts[0].extractedData && (
                <ContractResults contract={contracts[0]} className="animate-in slide-in-from-bottom-4 duration-500" />
              )}
            </div>

            {/* Contract History */}
            <div className="space-y-6">
              <ContractHistory contracts={contracts} onContractSelect={setSelectedContract} />
            </div>
          </div>
        </div>
      </div>

      {/* Contract Detail Sheet */}
      <Sheet open={!!selectedContract} onOpenChange={() => setSelectedContract(null)}>
        <SheetContent className="w-[600px] sm:max-w-[600px] bg-white/95 backdrop-blur-xl border-slate-200/60">
          <SheetHeader className="pb-6 border-b border-slate-200/60">
            <SheetTitle className="text-xl font-semibold text-slate-900">Contract Details</SheetTitle>
            <SheetDescription className="text-slate-600">{selectedContract?.filename}</SheetDescription>
          </SheetHeader>

          {selectedContract?.extractedData && (
            <div className="py-6 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <p className="text-sm font-medium text-slate-500">Status</p>
                  <Badge variant="secondary" className="bg-green-50 text-green-700 border-green-200">
                    <CheckCircle className="h-3 w-3 mr-1" />
                    Analyzed
                  </Badge>
                </div>
                <div className="space-y-2">
                  <p className="text-sm font-medium text-slate-500">Upload Date</p>
                  <p className="text-sm text-slate-900">{new Date(selectedContract.uploadTime).toLocaleDateString()}</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="p-4 rounded-xl bg-slate-50/80 border border-slate-200/60">
                  <h3 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
                    <Users className="h-4 w-4 text-blue-600" />
                    Company Information
                  </h3>
                  <p className="text-slate-700">{selectedContract.extractedData.companyName}</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50/80 border border-slate-200/60">
                  <h3 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
                    <DollarSign className="h-4 w-4 text-green-600" />
                    Contract Value
                  </h3>
                  <p className="text-2xl font-bold text-green-600">{selectedContract.extractedData.totalValue}</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50/80 border border-slate-200/60">
                  <h3 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
                    <FileText className="h-4 w-4 text-purple-600" />
                    Services
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedContract.extractedData.services.map((service, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {service}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-50/80 border border-slate-200/60">
                  <h3 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-orange-600" />
                    Contract End Date
                  </h3>
                  <p className="text-slate-700">{selectedContract.extractedData.endDate}</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50/80 border border-slate-200/60">
                  <h3 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
                    <AlertTriangle className="h-4 w-4 text-red-600" />
                    Termination Clause
                  </h3>
                  <p className="text-slate-700 text-sm">{selectedContract.extractedData.terminationClause}</p>
                </div>
              </div>

              <div className="flex gap-3 pt-4 border-t border-slate-200/60">
                <Button variant="outline" size="sm" className="flex-1">
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
                <Button variant="outline" size="sm" className="flex-1">
                  <Copy className="h-4 w-4 mr-2" />
                  Copy
                </Button>
              </div>
            </div>
          )}
        </SheetContent>
      </Sheet>
    </div>
  )
}

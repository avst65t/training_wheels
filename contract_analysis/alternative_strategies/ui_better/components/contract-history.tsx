"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Clock, CheckCircle, XCircle, Copy, FileText, Loader2, Eye } from "lucide-react"
import { cn } from "@/lib/utils"

interface Contract {
  id: string
  filename: string
  uploadTime: string
  status: "analyzing" | "analyzed" | "duplicate" | "failed"
  extractedData?: any
}

interface ContractHistoryProps {
  contracts: Contract[]
  onContractSelect: (contract: Contract) => void
}

export function ContractHistory({ contracts, onContractSelect }: ContractHistoryProps) {
  const getStatusIcon = (status: Contract["status"]) => {
    switch (status) {
      case "analyzing":
        return <Loader2 className="h-4 w-4 text-blue-600 animate-spin" />
      case "analyzed":
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case "duplicate":
        return <Copy className="h-4 w-4 text-orange-600" />
      case "failed":
        return <XCircle className="h-4 w-4 text-red-600" />
    }
  }

  const getStatusBadge = (status: Contract["status"]) => {
    switch (status) {
      case "analyzing":
        return (
          <Badge variant="secondary" className="bg-blue-50 text-blue-700 border-blue-200">
            Analyzing
          </Badge>
        )
      case "analyzed":
        return (
          <Badge variant="secondary" className="bg-green-50 text-green-700 border-green-200">
            Analyzed
          </Badge>
        )
      case "duplicate":
        return (
          <Badge variant="secondary" className="bg-orange-50 text-orange-700 border-orange-200">
            Duplicate
          </Badge>
        )
      case "failed":
        return (
          <Badge variant="secondary" className="bg-red-50 text-red-700 border-red-200">
            Failed
          </Badge>
        )
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return {
      date: date.toLocaleDateString(),
      time: date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    }
  }

  return (
    <Card className="border-slate-200/60 shadow-sm bg-white/80 backdrop-blur-sm h-fit">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-slate-900">
          <Clock className="h-5 w-5 text-slate-600" />
          Contract History
        </CardTitle>
        <CardDescription>Recently uploaded and analyzed contracts</CardDescription>
      </CardHeader>

      <CardContent className="space-y-3">
        {contracts.length === 0 ? (
          <div className="text-center py-8 text-slate-500">
            <FileText className="h-12 w-12 mx-auto mb-3 text-slate-300" />
            <p className="text-sm">No contracts uploaded yet</p>
          </div>
        ) : (
          contracts.map((contract, index) => {
            const { date, time } = formatDate(contract.uploadTime)

            return (
              <div
                key={contract.id}
                className={cn(
                  "group p-4 rounded-xl border border-slate-200/60 bg-slate-50/30 hover:bg-slate-50/60 transition-all duration-200 cursor-pointer hover:shadow-sm",
                  "animate-in slide-in-from-right-2 fade-in-0",
                  contract.status === "analyzed" && "hover:border-green-200/60",
                )}
                style={{ animationDelay: `${index * 100}ms` }}
                onClick={() => contract.status === "analyzed" && onContractSelect(contract)}
              >
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 mt-0.5">{getStatusIcon(contract.status)}</div>

                  <div className="flex-1 min-w-0 space-y-2">
                    <div className="flex items-start justify-between gap-2">
                      <p className="font-medium text-slate-900 text-sm truncate group-hover:text-slate-800">
                        {contract.filename}
                      </p>
                      {getStatusBadge(contract.status)}
                    </div>

                    <div className="flex items-center gap-4 text-xs text-slate-500">
                      <span>{date}</span>
                      <span>{time}</span>
                    </div>

                    {contract.extractedData && (
                      <div className="pt-2 border-t border-slate-200/60">
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-slate-600">{contract.extractedData.companyName}</span>
                          <span className="text-xs font-medium text-green-600">
                            {contract.extractedData.totalValue}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>

                  {contract.status === "analyzed" && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="opacity-0 group-hover:opacity-100 transition-opacity h-8 w-8 p-0"
                      onClick={(e) => {
                        e.stopPropagation()
                        onContractSelect(contract)
                      }}
                    >
                      <Eye className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </div>
            )
          })
        )}
      </CardContent>
    </Card>
  )
}

"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Building2, DollarSign, Calendar, User, AlertTriangle, FileText, Copy, Download, Eye } from "lucide-react"
import { cn } from "@/lib/utils"

interface ContractResultsProps {
  contract: {
    filename: string
    extractedData: {
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
  className?: string
}

export function ContractResults({ contract, className }: ContractResultsProps) {
  const { extractedData } = contract

  return (
    <Card className={cn("border-slate-200/60 shadow-sm bg-white/80 backdrop-blur-sm", className)}>
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2 text-slate-900">
              <FileText className="h-5 w-5 text-green-600" />
              Analysis Complete
            </CardTitle>
            <CardDescription className="mt-1">Key information extracted from {contract.filename}</CardDescription>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Eye className="h-4 w-4 mr-2" />
              View Full
            </Button>
            <Button variant="outline" size="sm">
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-gradient-to-br from-blue-50 to-blue-100/50 border border-blue-200/60">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-blue-600 flex items-center justify-center">
                <Building2 className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm font-medium text-blue-900">Company</p>
                <p className="text-lg font-semibold text-blue-800 truncate">{extractedData.companyName}</p>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-gradient-to-br from-green-50 to-green-100/50 border border-green-200/60">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-green-600 flex items-center justify-center">
                <DollarSign className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm font-medium text-green-900">Total Value</p>
                <p className="text-lg font-semibold text-green-800">{extractedData.totalValue}</p>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-gradient-to-br from-orange-50 to-orange-100/50 border border-orange-200/60">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-orange-600 flex items-center justify-center">
                <Calendar className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm font-medium text-orange-900">End Date</p>
                <p className="text-lg font-semibold text-orange-800">{extractedData.endDate}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Services */}
        <div className="space-y-3">
          <h3 className="font-semibold text-slate-900 flex items-center gap-2">
            <FileText className="h-4 w-4 text-purple-600" />
            Services Provided
          </h3>
          <div className="flex flex-wrap gap-2">
            {extractedData.services.map((service, index) => (
              <Badge
                key={index}
                variant="secondary"
                className="bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100 transition-colors"
              >
                {service}
              </Badge>
            ))}
          </div>
        </div>

        {/* Signer Details */}
        <div className="space-y-3">
          <h3 className="font-semibold text-slate-900 flex items-center gap-2">
            <User className="h-4 w-4 text-blue-600" />
            Authorized Signatory
          </h3>
          <div className="p-4 rounded-xl bg-slate-50/80 border border-slate-200/60">
            <div className="space-y-2">
              <p className="font-medium text-slate-900">{extractedData.signerDetails.name}</p>
              <p className="text-sm text-slate-600">{extractedData.signerDetails.title}</p>
              <p className="text-sm text-slate-500">{extractedData.signerDetails.email}</p>
            </div>
          </div>
        </div>

        {/* Termination Clause */}
        <div className="space-y-3">
          <h3 className="font-semibold text-slate-900 flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 text-red-600" />
            Termination Clause
          </h3>
          <div className="p-4 rounded-xl bg-red-50/50 border border-red-200/60">
            <p className="text-sm text-red-800">{extractedData.terminationClause}</p>
          </div>
        </div>

        {/* Key Terms */}
        <div className="space-y-3">
          <h3 className="font-semibold text-slate-900">Key Terms & Conditions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {extractedData.keyTerms.map((term, index) => (
              <div
                key={index}
                className="flex items-center gap-2 p-3 rounded-lg bg-slate-50/80 border border-slate-200/60"
              >
                <div className="h-2 w-2 rounded-full bg-slate-400" />
                <span className="text-sm text-slate-700">{term}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-3 pt-4 border-t border-slate-200/60">
          <Button variant="outline" size="sm" className="flex-1">
            <Copy className="h-4 w-4 mr-2" />
            Copy Summary
          </Button>
          <Button
            size="sm"
            className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
          >
            <Download className="h-4 w-4 mr-2" />
            Download Report
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

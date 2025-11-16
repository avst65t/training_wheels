"use client"

import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button"
import { Upload, FileText, Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface FileUploadZoneProps {
  onFileUpload: (files: File[]) => void
  isAnalyzing: boolean
  progress: number
  className?: string
}

export function FileUploadZone({ onFileUpload, isAnalyzing, progress, className }: FileUploadZoneProps) {
  const [isDragActive, setIsDragActive] = useState(false)

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      onFileUpload(acceptedFiles)
    },
    [onFileUpload],
  )

  const { getRootProps, getInputProps, open } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/msword": [".doc"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
    },
    multiple: false,
    noClick: true,
    onDragEnter: () => setIsDragActive(true),
    onDragLeave: () => setIsDragActive(false),
    onDropAccepted: () => setIsDragActive(false),
    onDropRejected: () => setIsDragActive(false),
  })

  return (
    <div className={cn("space-y-4", className)}>
      <Card
        {...getRootProps()}
        className={cn(
          "relative overflow-hidden border-2 border-dashed transition-all duration-300 cursor-pointer group",
          isDragActive
            ? "border-blue-400 bg-blue-50/50 scale-[1.02]"
            : "border-slate-300 hover:border-blue-300 hover:bg-slate-50/50",
          isAnalyzing && "pointer-events-none",
        )}
      >
        <input {...getInputProps()} />

        <div className="p-12 text-center space-y-6">
          {isAnalyzing ? (
            <div className="space-y-4">
              <div className="flex justify-center">
                <div className="relative">
                  <div className="h-16 w-16 rounded-full bg-blue-100 flex items-center justify-center">
                    <Loader2 className="h-8 w-8 text-blue-600 animate-spin" />
                  </div>
                  <div className="absolute inset-0 rounded-full border-2 border-blue-200 animate-pulse" />
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-slate-900">Analyzing Contract...</h3>
                <p className="text-slate-600">AI is extracting key information from your document</p>
                <div className="max-w-xs mx-auto">
                  <Progress value={progress} className="h-2" />
                  <p className="text-sm text-slate-500 mt-2">{Math.round(progress)}% complete</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex justify-center">
                <div
                  className={cn(
                    "h-16 w-16 rounded-full bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center transition-all duration-300 group-hover:scale-110",
                    isDragActive && "scale-110 from-blue-200 to-indigo-200",
                  )}
                >
                  <Upload
                    className={cn("h-8 w-8 text-blue-600 transition-all duration-300", isDragActive && "scale-110")}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-slate-900">
                  {isDragActive ? "Drop your contract here" : "Upload Contract Document"}
                </h3>
                <p className="text-slate-600">Drag and drop your PDF or Word document, or click to browse</p>
              </div>

              <div className="flex items-center justify-center gap-4 text-sm text-slate-500">
                <div className="flex items-center gap-1">
                  <FileText className="h-4 w-4" />
                  PDF
                </div>
                <div className="flex items-center gap-1">
                  <FileText className="h-4 w-4" />
                  DOC
                </div>
                <div className="flex items-center gap-1">
                  <FileText className="h-4 w-4" />
                  DOCX
                </div>
              </div>

              <Button
                onClick={open}
                className="mt-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg hover:shadow-xl transition-all duration-300"
              >
                <Upload className="h-4 w-4 mr-2" />
                Choose File
              </Button>
            </div>
          )}
        </div>

        {/* Animated background effect */}
        <div
          className={cn(
            "absolute inset-0 bg-gradient-to-r from-blue-600/5 to-indigo-600/5 opacity-0 transition-opacity duration-300",
            isDragActive && "opacity-100",
          )}
        />
      </Card>
    </div>
  )
}

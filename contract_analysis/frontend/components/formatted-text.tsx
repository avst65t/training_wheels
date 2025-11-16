interface FormattedTextProps {
  text: string | null | undefined
  className?: string
  fallback?: string
}

export function FormattedText({ text, className = "", fallback = "N/A" }: FormattedTextProps) {
  if (!text) {
    return <span className={className}>{fallback}</span>
  }

  // Handle different types of formatting
  const formatText = (text: string) => {
    return text.split("\n").map((line, index) => {
      // Handle empty lines
      if (line.trim() === "") {
        return <br key={index} />
      }

      // Handle bullet points and numbered lists
      const trimmedLine = line.trim()

      // Check for bullet points (-, •, *, etc.)
      if (trimmedLine.match(/^[-•*]\s/)) {
        return (
          <div key={index} className="flex items-start mb-1">
            <span className="text-current mr-2 mt-0.5 flex-shrink-0">•</span>
            <span className="flex-1">{trimmedLine.substring(2)}</span>
          </div>
        )
      }

      // Check for numbered lists
      if (trimmedLine.match(/^\d+\.\s/)) {
        const match = trimmedLine.match(/^(\d+)\.\s(.*)/)
        if (match) {
          return (
            <div key={index} className="flex items-start mb-1">
              <span className="text-current mr-2 mt-0.5 flex-shrink-0 font-medium">{match[1]}.</span>
              <span className="flex-1">{match[2]}</span>
            </div>
          )
        }
      }

      // Handle headers (lines ending with :)
      if (trimmedLine.endsWith(":") && trimmedLine.length > 1) {
        return (
          <div key={index} className="font-semibold text-current mb-2 mt-3 first:mt-0">
            {trimmedLine}
          </div>
        )
      }

      // Regular line
      return (
        <div key={index} className="mb-1">
          {trimmedLine}
        </div>
      )
    })
  }

  return <div className={className}>{formatText(text)}</div>
}

// Alternative simpler version using CSS
export function SimpleFormattedText({ text, className = "", fallback = "N/A" }: FormattedTextProps) {
  if (!text) {
    return <span className={className}>{fallback}</span>
  }

  return <div className={`whitespace-pre-line ${className}`}>{text}</div>
}

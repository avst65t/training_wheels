"use client"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { ContractDashboard } from "@/components/contract-dashboard"

export default function HomePage() {
  return (
    <SidebarProvider defaultOpen={true}>
      <div className="flex min-h-screen w-full bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20">
        <AppSidebar />
        <main className="flex-1 overflow-hidden">
          <ContractDashboard />
        </main>
      </div>
    </SidebarProvider>
  )
}

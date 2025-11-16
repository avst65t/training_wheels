import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import { FileText, BarChart3, Settings, Users, Shield, Sparkles } from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

const menuItems = [
  {
    title: "Contract Analysis",
    url: "#",
    icon: FileText,
    isActive: true,
  },
  {
    title: "Analytics",
    url: "#",
    icon: BarChart3,
  },
  {
    title: "Team Management",
    url: "#",
    icon: Users,
  },
  {
    title: "Security",
    url: "#",
    icon: Shield,
  },
  {
    title: "Settings",
    url: "#",
    icon: Settings,
  },
]

export function AppSidebar() {
  return (
    <Sidebar className="border-r border-slate-200/60 bg-white/80 backdrop-blur-xl">
      <SidebarHeader className="border-b border-slate-200/60 p-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-lg">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-slate-900">ContractAI</h1>
            <p className="text-sm text-slate-500">Analysis Suite</p>
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent className="px-4 py-6">
        <SidebarGroup>
          <SidebarGroupLabel className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-3">
            Main Menu
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu className="space-y-1">
              {menuItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton
                    asChild
                    isActive={item.isActive}
                    className="h-11 rounded-xl transition-all duration-200 hover:bg-slate-100/80 data-[active=true]:bg-gradient-to-r data-[active=true]:from-blue-50 data-[active=true]:to-indigo-50 data-[active=true]:text-blue-700 data-[active=true]:shadow-sm"
                  >
                    <a href={item.url} className="flex items-center gap-3 px-3">
                      <item.icon className="h-5 w-5" />
                      <span className="font-medium">{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="border-t border-slate-200/60 p-4">
        <div className="flex items-center gap-3 rounded-xl bg-slate-50/80 p-3 transition-colors hover:bg-slate-100/80">
          <Avatar className="h-8 w-8">
            <AvatarImage src="/placeholder.svg?height=32&width=32" />
            <AvatarFallback className="bg-gradient-to-br from-blue-600 to-indigo-600 text-white text-sm font-medium">
              JD
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-slate-900 truncate">John Doe</p>
            <p className="text-xs text-slate-500 truncate">john@company.com</p>
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}

import { useState } from "react";
import { useAuth } from "@/domains/users/auth/AuthContext";
import { SignOutButton } from "@/domains/users/components/SignOutButton";
import { Button } from "@/shared/ui/Button";
import { cn } from "@/shared/lib/utils";

interface NavigationProps {
  currentPage: string;
  onPageChange: (page: string) => void;
}

export function Navigation({ currentPage, onPageChange }: NavigationProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: "🏠" },
    { id: "settings", label: "Settings", icon: "⚙️" },
  ];

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="shrink-0">
              <h1 className="text-xl font-bold text-gray-900">App</h1>
            </div>
            
            {/* Desktop Navigation */}
            <div className="hidden md:ml-6 md:flex md:space-x-8">
              {/** show nav only when authenticated */}
              {(() => {
                const { currentUser } = useAuth();
                if (!currentUser) return null;
                return navItems.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => onPageChange(item.id)}
                    className={cn(
                      "inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors",
                      currentPage === item.id
                        ? "border-blue-500 text-gray-900"
                        : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
                    )}
                  >
                    <span className="mr-2">{item.icon}</span>
                    {item.label}
                  </button>
                ));
              })()}
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {(() => {
              const { currentUser } = useAuth();
              return currentUser ? <SignOutButton /> : null;
            })()}
            
            {/* Mobile menu button */}
            <div className="md:hidden">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                aria-label="Toggle mobile menu"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </Button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden">
            <div className="pt-2 pb-3 space-y-1">
              {(() => {
                const { currentUser } = useAuth();
                if (!currentUser) return null;
                return navItems.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => {
                      onPageChange(item.id);
                      setIsMobileMenuOpen(false);
                    }}
                    className={cn(
                      "block w-full text-left px-3 py-2 rounded-md text-base font-medium transition-colors",
                      currentPage === item.id
                        ? "bg-blue-50 border-blue-500 text-blue-700"
                        : "text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                    )}
                  >
                    <span className="mr-2">{item.icon}</span>
                    {item.label}
                  </button>
                ));
              })()}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}

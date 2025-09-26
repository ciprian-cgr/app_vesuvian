import { useState } from "react";
import { Authenticated, Unauthenticated, useQuery } from "convex/react";
import { api } from "../convex/_generated/api";
import { SignInForm } from "./SignInForm";
import { Layout } from "./components/layout/Layout";
import { Dashboard } from "./components/pages/Dashboard";
import { Settings } from "./components/pages/Settings";
import { LoadingSpinner } from "./components/ui/LoadingSpinner";
import { useLocalStorage } from "./hooks/useLocalStorage";
import { ROUTES, STORAGE_KEYS } from "./utils/constants";
import { Toaster } from "sonner";

export default function App() {
  const loggedInUser = useQuery(api.auth.loggedInUser);
  const [currentPage, setCurrentPage] = useLocalStorage<string>(STORAGE_KEYS.CURRENT_PAGE, ROUTES.DASHBOARD);

  const handlePageChange = (page: string) => {
    setCurrentPage(page);
  };

  const renderPage = () => {
    switch (currentPage) {
      case ROUTES.SETTINGS:
        return <Settings />;
      case ROUTES.DASHBOARD:
      default:
        return <Dashboard />;
    }
  };

  if (loggedInUser === undefined) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Authenticated>
        <Layout currentPage={currentPage} onPageChange={handlePageChange}>
          {renderPage()}
        </Layout>
      </Authenticated>

      <Unauthenticated>
        <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full space-y-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome</h1>
              <p className="text-gray-600">Sign in to access your account</p>
            </div>
            <SignInForm />
          </div>
        </div>
      </Unauthenticated>

      <Toaster position="top-right" />
    </div>
  );
}

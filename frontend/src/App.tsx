import React, { useState, useEffect } from "react";
import { SignInForm } from "./SignInForm";
import { Layout } from "./components/layout/Layout";
import { Dashboard } from "./components/pages/Dashboard";
import { Settings } from "./components/pages/Settings";
import { LoadingSpinner } from "./components/ui/LoadingSpinner";
import { useLocalStorage } from "./hooks/useLocalStorage";
import { ROUTES, STORAGE_KEYS } from "./utils/constants";
import { Toaster } from "sonner";
import { useAuth } from "./auth/AuthContext";
import type { Settings as SettingsType } from "./types";

const API_PREFIX = import.meta.env.VITE_API_PREFIX || "/api/v1";

export default function App(): React.ReactElement {
  const { currentUser, loading, token } = useAuth();
  const [settings, setSettings] = useState<SettingsType | null | undefined>(undefined);
  const [currentPage, setCurrentPage] = useLocalStorage<string>(STORAGE_KEYS.CURRENT_PAGE, ROUTES.DASHBOARD);

  const handlePageChange = (page: string) => setCurrentPage(page);

  useEffect(() => {
    let mounted = true;
    const fetchSettings = async () => {
      if (!currentUser) {
        setSettings(null);
        return;
      }
      setSettings(undefined);
      try {
        const api = (await import("./lib/api")).api;
        const data = await api.get<SettingsType>("/users/settings", token);
        if (!mounted) return;
        setSettings(data ?? null);
      } catch (err) {
        console.error(err);
        if (mounted) setSettings(null);
      }
    };
    void fetchSettings();
    return () => {
      mounted = false;
    };
  }, [currentUser, token]);

  const renderPage = () => {
    switch (currentPage) {
      case ROUTES.SETTINGS:
        return <Settings />;
      case ROUTES.DASHBOARD:
      default:
        return <Dashboard />;
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="min-h-screen bg-gray-50">
      {currentUser ? (
        <Layout currentPage={currentPage} onPageChange={handlePageChange}>
          {renderPage()}
        </Layout>
      ) : (
        <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full space-y-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome</h1>
              <p className="text-gray-600">Sign in to access your account</p>
            </div>
            <SignInForm />
          </div>
        </div>
      )}

      <Toaster position="top-right" />
    </div>
  );
}

import React, { useState, useEffect } from "react";
import { SignInForm } from "@/domains/users/components/SignInForm";
import { Layout } from "@/shared/layout/Layout";
import { Dashboard } from "@/domains/users/pages/Dashboard";
import { Settings } from "@/domains/users/pages/Settings";
import { LoadingSpinner } from "@/shared/ui/LoadingSpinner";
import { useLocalStorage } from "@/shared/hooks/useLocalStorage";
import { ROUTES, STORAGE_KEYS } from "@/shared/utils/constants";
import { Toaster } from "sonner";
import { useAuth } from "@/domains/users/auth/AuthContext";
import { api } from "@/shared/lib/api";
import { useUserRepository } from "@/domains/users/hooks/useUserRepository";
import type { Settings as SettingsType } from "@/shared/types";

const API_PREFIX = import.meta.env.VITE_API_PREFIX || "/api/v1";

export default function App(): React.ReactElement {
  const { currentUser, loading, token } = useAuth();
  const [settings, setSettings] = useState<SettingsType | null | undefined>(undefined);
  const [currentPage, setCurrentPage] = useLocalStorage<string>(STORAGE_KEYS.CURRENT_PAGE, ROUTES.DASHBOARD);

  const handlePageChange = (page: string) => setCurrentPage(page);

  const repo = useUserRepository();

  useEffect(() => {
    let mounted = true;
    const fetchSettings = async () => {
      if (!currentUser) {
        setSettings(null);
        return;
      }
      setSettings(undefined);
      try {
        const data = await repo.getSettings(token);
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
  }, [currentUser, token, repo]);

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

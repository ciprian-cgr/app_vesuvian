import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/Card";
import { Button } from "@/shared/ui/Button";
import { Select } from "@/shared/ui/Select";
import { LoadingSpinner } from "@/shared/ui/LoadingSpinner";
import { ErrorMessage } from "@/shared/ui/ErrorMessage";
import { toast } from "sonner";
import { useAuth } from "@/domains/users/auth/AuthContext";
import { useUserRepository } from "@/domains/users/hooks/useUserRepository";
import type { Settings as SettingsType } from "@/shared/types";

export function Settings(): React.ReactElement {
  const { currentUser, token } = useAuth();
  const repo = useUserRepository();
  const [settings, setSettings] = useState<SettingsType | null | undefined>(undefined);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [formData, setFormData] = useState<{ theme: string; notifications: boolean; language: string }>({ theme: "system", notifications: true, language: "en" });

  useEffect(() => {
    let mounted = true;

    const fetchSettings = async () => {
      if (!currentUser) return setSettings(null);
      setSettings(undefined);
      try {
        const data = await repo.getSettings(token);
        if (!mounted) return;
        setSettings(data ?? null);
        const themeVal: string = data && typeof (data as SettingsType).theme === "string" ? (data as SettingsType).theme as string : "system";
        const notificationsVal: boolean = data && typeof (data as SettingsType).notifications === "boolean" ? (data as SettingsType).notifications as boolean : true;
        const languageVal: string = data && typeof (data as SettingsType).language === "string" ? (data as SettingsType).language as string : "en";
        setFormData({ theme: themeVal, notifications: notificationsVal, language: languageVal });
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

  if (settings === undefined) return <LoadingSpinner />;
  if (settings === null) return <ErrorMessage message="Please sign in to view your settings." />;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
  try {
  await repo.updateSettings(token, formData);
      toast.success("Settings updated successfully!");
    } catch (error) {
      toast.error("Failed to update settings. Please try again.");
      console.error("Settings update error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const themeOptions = [
    { value: "light", label: "Light" },
    { value: "dark", label: "Dark" },
    { value: "system", label: "System" },
  ];

  const languageOptions = [
    { value: "en", label: "English" },
    { value: "es", label: "Spanish" },
    { value: "fr", label: "French" },
    { value: "de", label: "German" },
  ];

  return (
    <div className="space-y-loose">
      <div>
        <h1 className="text-h1 text-text-primary">Settings</h1>
        <p className="mt-1 text-body text-text-secondary">Manage your account preferences and settings.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Preferences</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-default">
            <Select
              label="Theme"
              options={themeOptions}
              value={formData.theme}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setFormData({ ...formData, theme: e.target.value })}
            />

            <Select label="Language" options={languageOptions} value={formData.language} onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setFormData({ ...formData, language: e.target.value })} />

            <div className="space-y-tight">
              <label className="text-body text-text-secondary">Notifications</label>
              <div className="flex items-center space-x-2 pt-1">
                <input
                  type="checkbox"
                  id="notifications"
                  checked={formData.notifications}
                  onChange={(e) => setFormData({ ...formData, notifications: e.target.checked })}
                  className="h-4 w-4 appearance-none rounded-sm border border-surface-light bg-surface-dark checked:bg-yellow checked:border-yellow focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-yellow focus-visible:ring-offset-2 focus-visible:ring-offset-background-dark"
                />
                <label htmlFor="notifications" className="text-body text-text-secondary">Enable email notifications</label>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <Button variant="primary" type="submit" loading={isLoading}>Save Changes</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

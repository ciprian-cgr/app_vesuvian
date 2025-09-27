import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { Button } from "../ui/Button";
import { Select } from "../ui/Select";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import { ErrorMessage } from "../ui/ErrorMessage";
import { toast } from "sonner";
import { useAuth } from "../../auth/AuthContext";
import { api } from "../../lib/api";
import type { Settings as SettingsType } from "../../types";

export function Settings(): React.ReactElement {
  const { currentUser, token } = useAuth();
  const [settings, setSettings] = useState<SettingsType | null | undefined>(undefined);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [formData, setFormData] = useState<{ theme: string; notifications: boolean; language: string }>({ theme: "system", notifications: true, language: "en" });

  useEffect(() => {
    let mounted = true;
    const fetchSettings = async () => {
      if (!currentUser) return setSettings(null);
      setSettings(undefined);
      try {
    const data = await api.get<SettingsType | null>("/users/settings", token);
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
      await api.put("/users/settings", token, formData);
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
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="mt-1 text-sm text-gray-600">Manage your account preferences and settings.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Preferences</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <Select
              label="Theme"
              options={themeOptions}
              value={formData.theme}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setFormData({ ...formData, theme: e.target.value })}
            />

            <Select label="Language" options={languageOptions} value={formData.language} onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setFormData({ ...formData, language: e.target.value })} />

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Notifications</label>
              <div className="flex items-center space-x-2">
                <input type="checkbox" id="notifications" checked={formData.notifications} onChange={(e) => setFormData({ ...formData, notifications: e.target.checked })} className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                <label htmlFor="notifications" className="text-sm text-gray-600">Enable email notifications</label>
              </div>
            </div>

            <div className="flex justify-end">
              <Button type="submit" loading={isLoading}>Save Changes</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

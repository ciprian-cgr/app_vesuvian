import { useState } from "react";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { Button } from "../ui/Button";
import { Select } from "../ui/Select";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import { ErrorMessage } from "../ui/ErrorMessage";
import { toast } from "sonner";

export function Settings() {
  const settings = useQuery(api.users.getUserSettings);
  const updateSettings = useMutation(api.users.updateUserSettings);
  const [isLoading, setIsLoading] = useState(false);

  const [formData, setFormData] = useState({
    theme: settings?.theme || "system" as const,
    notifications: settings?.notifications ?? true,
    language: settings?.language || "en",
  });

  // Update form data when settings load
  if (settings && formData.theme !== settings.theme) {
    setFormData({
      theme: settings.theme,
      notifications: settings.notifications ?? true,
      language: settings.language,
    });
  }

  if (settings === undefined) {
    return <LoadingSpinner />;
  }

  if (settings === null) {
    return <ErrorMessage message="Please sign in to view your settings." />;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await updateSettings(formData);
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
        <p className="mt-1 text-sm text-gray-600">
          Manage your account preferences and settings.
        </p>
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
              onChange={(e) => setFormData({ ...formData, theme: e.target.value as any })}
            />

            <Select
              label="Language"
              options={languageOptions}
              value={formData.language}
              onChange={(e) => setFormData({ ...formData, language: e.target.value })}
            />

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Notifications</label>
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="notifications"
                  checked={formData.notifications}
                  onChange={(e) => setFormData({ ...formData, notifications: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="notifications" className="text-sm text-gray-600">
                  Enable email notifications
                </label>
              </div>
            </div>

            <div className="flex justify-end">
              <Button type="submit" loading={isLoading}>
                Save Changes
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

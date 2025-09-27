import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import { ErrorMessage } from "../ui/ErrorMessage";
import { useAuth } from "../../auth/AuthContext";

export function Dashboard() {
  const { currentUser } = useAuth();
  const [settings, setSettings] = useState<any | null | undefined>(undefined);

  const { token } = useAuth();

  useEffect(() => {
    let mounted = true;
    const fetchSettings = async () => {
      if (!currentUser) return setSettings(null);
      setSettings(undefined);
      try {
        const data = await (await import("../../lib/api")).api.get("/users/settings", token);
        if (!mounted) return;
        setSettings(data);
      } catch (err) {
        console.error(err);
        if (mounted) setSettings(null);
      }
    };
    void fetchSettings();
    return () => {
      mounted = false;
    };
  }, [currentUser]);

  if (currentUser === undefined || settings === undefined) return <LoadingSpinner />;

  if (currentUser === null) return <ErrorMessage message="Please sign in to view your dashboard." />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-600">
          Welcome back, {currentUser.email || "User"}!
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <p className="text-sm text-gray-600">Email: {currentUser.email}</p>
              <p className="text-sm text-gray-600">
                Member since: {new Date(currentUser.created_at || Date.now()).toLocaleDateString()}
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Settings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <p className="text-sm text-gray-600">Theme: {settings?.theme || "System"}</p>
              <p className="text-sm text-gray-600">
                Notifications: {settings?.notifications ? "Enabled" : "Disabled"}
              </p>
              <p className="text-sm text-gray-600">Language: {settings?.language || "English"}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <p className="text-sm text-gray-600">Everything looks good!</p>
              <p className="text-sm text-gray-600">No actions needed.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

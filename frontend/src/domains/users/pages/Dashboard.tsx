import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/Card";
import { LoadingSpinner } from "@/shared/ui/LoadingSpinner";
import { ErrorMessage } from "@/shared/ui/ErrorMessage";
import { useAuth } from "@/domains/users/auth/AuthContext";
import { useUserRepository } from "@/domains/users/hooks/useUserRepository";

export function Dashboard() {
  const { currentUser } = useAuth();
  const [settings, setSettings] = useState<any | null | undefined>(undefined);
  const { token } = useAuth();
  const repo = useUserRepository();

  useEffect(() => {
    let mounted = true;
    const fetchSettings = async () => {
      if (!currentUser) return setSettings(null);
      setSettings(undefined);
      try {
        const data = await repo.getSettings(token);
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
    <div className="space-y-loose">
      <div>
        <h1 className="text-h1 text-text-primary">Dashboard</h1>
        <p className="mt-1 text-body text-text-secondary">
          Welcome back, {currentUser.email || "User"}!
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-default">
        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-tight">
              <p className="text-body text-text-secondary">Email: {currentUser.email}</p>
              <p className="text-caption text-text-tertiary">
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
            <div className="space-y-tight">
              <p className="text-body text-text-secondary">Theme: {settings?.theme || "System"}</p>
              <p className="text-body text-text-secondary">
                Notifications: {settings?.notifications ? "Enabled" : "Disabled"}
              </p>
              <p className="text-body text-text-secondary">Language: {settings?.language || "English"}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-tight">
              <p className="text-body text-text-secondary">Everything looks good!</p>
              <p className="text-caption text-text-tertiary">No actions needed.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

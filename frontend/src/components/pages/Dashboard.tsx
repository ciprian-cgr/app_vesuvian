import { useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import { ErrorMessage } from "../ui/ErrorMessage";

export function Dashboard() {
  const user = useQuery(api.users.getCurrentUser);
  const settings = useQuery(api.users.getUserSettings);

  if (user === undefined || settings === undefined) {
    return <LoadingSpinner />;
  }

  if (user === null) {
    return <ErrorMessage message="Please sign in to view your dashboard." />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-600">
          Welcome back, {user.email || "User"}!
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <p className="text-sm text-gray-600">Email: {user.email}</p>
              <p className="text-sm text-gray-600">
                Member since: {new Date(user._creationTime).toLocaleDateString()}
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

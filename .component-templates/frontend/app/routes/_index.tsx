import type { Route } from "./+types/home";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "{{ project-name }}" },
    { name: "description", content: "Welcome to {{ project-name }}!" },
  ];
}

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>{{ project-name }}</CardTitle>
          <CardDescription>
            Welcome to your new project! This is a starter template with shadcn/ui components.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Start building your application by editing this file and exploring the available components.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

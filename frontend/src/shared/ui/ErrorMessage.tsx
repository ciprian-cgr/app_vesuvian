import { cn } from "@/shared/lib/utils";

interface ErrorMessageProps {
  message: string;
  className?: string;
}

export function ErrorMessage({ message, className }: ErrorMessageProps) {
  return (
    <div className={cn("flex justify-center items-center p-4", className)}>
      <div className="text-center space-y-2">
        <div className="text-4xl">⚠️</div>
        <p className="text-error text-body-lg font-medium">{message}</p>
      </div>
    </div>
  );
}
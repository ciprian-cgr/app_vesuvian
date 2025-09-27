import { cn } from "@/shared/lib/utils";

interface ErrorMessageProps {
  message: string;
  className?: string;
}

export function ErrorMessage({ message, className }: ErrorMessageProps) {
  return (
    <div className={cn("flex justify-center items-center p-8", className)}>
      <div className="text-center">
        <div className="text-red-500 text-4xl mb-4">⚠️</div>
        <p className="text-red-600 font-medium">{message}</p>
      </div>
    </div>
  );
}

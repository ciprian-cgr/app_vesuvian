import { InputHTMLAttributes, forwardRef } from "react";
import { cn } from "@/shared/lib/utils";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, id, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="space-y-tight">
        {label && (
          <label htmlFor={inputId} className="text-body text-text-secondary">
            {label}
          </label>
        )}
        <input
          id={inputId}
          className={cn(
            "flex h-11 w-full rounded border border-surface-light bg-surface-dark px-3 py-2 text-body-lg text-text-primary placeholder:text-text-tertiary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-yellow focus-visible:ring-offset-2 focus-visible:ring-offset-background-dark disabled:cursor-not-allowed disabled:opacity-50",
            error && "border-error focus-visible:ring-error",
            className
          )}
          ref={ref}
          {...props}
        />
        {error && <p className="text-caption text-error">{error}</p>}
      </div>
    );
  }
);

Input.displayName = "Input";

export { Input };
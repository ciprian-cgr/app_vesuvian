import { ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "@/shared/lib/utils";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "tertiary" | "outline";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "secondary", size = "md", loading, children, disabled, ...props }, ref) => {
    const baseClasses =
      "inline-flex items-center justify-center rounded font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-yellow focus-visible:ring-offset-2 focus-visible:ring-offset-background-dark disabled:pointer-events-none disabled:opacity-50";

    const variants = {
      primary: "bg-yellow text-background-dark hover:bg-yellow/90",
      secondary: "bg-surface-dark text-text-primary hover:bg-surface-light",
      tertiary: "text-text-secondary hover:bg-surface-dark hover:text-text-primary",
      outline: "border border-surface-light bg-transparent text-text-secondary hover:bg-surface-light hover:text-text-primary",
    };

    const sizes = {
      // Heights are h-11 (44px), h-12 (48px), h-14 (56px) to meet 44px touch target
      sm: "h-11 px-3 text-body",
      md: "h-12 px-4 text-body-lg",
      lg: "h-14 px-5 text-h3",
    };

    return (
      <button
        className={cn(baseClasses, variants[variant], sizes[size], className)}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";

export { Button };
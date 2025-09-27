import { SelectHTMLAttributes, forwardRef } from "react";
import { cn } from "@/shared/lib/utils";

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  options: { value: string; label: string }[];
}

const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, options, id, ...props }, ref) => {
    const selectId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="space-y-tight">
        {label && (
          <label htmlFor={selectId} className="text-body text-text-secondary">
            {label}
          </label>
        )}
        <select
          id={selectId}
          className={cn(
            "flex h-11 w-full rounded border border-surface-light bg-surface-dark px-3 py-2 text-body-lg text-text-primary placeholder:text-text-tertiary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-yellow focus-visible:ring-offset-2 focus-visible:ring-offset-background-dark disabled:cursor-not-allowed disabled:opacity-50",
            // Adding an explicit background for the options for better browser compatibility
            "[&_option]:bg-surface-dark [&_option]:text-text-primary",
            error && "border-error focus-visible:ring-error",
            className
          )}
          ref={ref}
          {...props}
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        {error && <p className="text-caption text-error">{error}</p>}
      </div>
    );
  }
);

Select.displayName = "Select";

export { Select };
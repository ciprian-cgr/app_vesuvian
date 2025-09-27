"use client";
import React, { FormEvent, useState } from "react";
import { toast } from "sonner";
import { useAuthActions } from "./auth/AuthContext";

export function SignInForm(): React.ReactElement {
  const { signIn, register } = useAuthActions();
  const [flow, setFlow] = useState<"signIn" | "signUp">("signIn");
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmitting(true);
    const form = e.currentTarget as HTMLFormElement;
    const formData = new FormData(form);
    const email = String(formData.get("email") || "").trim();
    const password = String(formData.get("password") || "");
    const username = email;

    try {
      if (flow === "signIn") {
        await signIn(username, password);
        toast.success("Signed in");
      } else {
        if (register) {
          await register(email, username, password);
          toast.success("Registered \u2014 please sign in");
          setFlow("signIn");
        } else {
          toast.error("Registration not supported");
        }
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error ?? "Authentication failed");
      toast.error(message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="w-full">
      <form className="flex flex-col gap-form-field" onSubmit={onSubmit}>
        <input className="auth-input-field" type="email" name="email" placeholder="Email" required />
        <input className="auth-input-field" type="password" name="password" placeholder="Password" required />
        <button className="auth-button" type="submit" disabled={submitting}>
          {flow === "signIn" ? "Sign in" : "Sign up"}
        </button>
        <div className="text-center text-sm text-secondary">
          <span>{flow === "signIn" ? "Don't have an account? " : "Already have an account? "}</span>
          <button
            type="button"
            className="text-primary hover:text-primary-hover hover:underline font-medium cursor-pointer"
            onClick={() => setFlow(flow === "signIn" ? "signUp" : "signIn")}
          >
            {flow === "signIn" ? "Sign up instead" : "Sign in instead"}
          </button>
        </div>
      </form>
    </div>
  );
}

import React, { createContext, useContext } from "react";
import type { UserRepository } from "@/domains/users/repositories/userRepository";
import { HttpUserRepository } from "@/domains/users/repositories/httpUserRepository";

export interface Repositories {
  userRepository: UserRepository;
}

const defaultRepositories: Repositories = {
  userRepository: new HttpUserRepository(),
};

const RepositoriesContext = createContext<Repositories | undefined>(undefined);

export function RepositoryProvider({ children, repositories }: { children: React.ReactNode; repositories?: Partial<Repositories> }) {
  const value: Repositories = { ...defaultRepositories, ...(repositories ?? {}) };
  return <RepositoriesContext.Provider value={value}>{children}</RepositoriesContext.Provider>;
}

export function useRepositories(): Repositories {
  const ctx = useContext(RepositoriesContext);
  if (!ctx) return defaultRepositories; // fallback to defaults if provider not used
  return ctx;
}

export default RepositoryProvider;

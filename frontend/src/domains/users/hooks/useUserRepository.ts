import { useMemo } from "react";
import { HttpUserRepository } from "../repositories/httpUserRepository";
import type { UserRepository } from "../repositories/userRepository";
import { useRepositories } from "@/shared/providers/RepositoryProvider";

export function useUserRepository(): UserRepository {
  const repos = useRepositories();
  // If provider present, use its repository; otherwise use a memoized default
  if (repos && repos.userRepository) return repos.userRepository;
  return useMemo(() => new HttpUserRepository(), []);
}

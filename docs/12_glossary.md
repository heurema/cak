# 12 — Glossary

## CAK

Causal Agent Kernel. The public project name.

CAK is a typed semantic control layer for agent behavior, learning artifacts, replay, governance, provider portability, and cost control.

## CAK Spec

Human-facing declarative surface format for CAK. Legacy alias: TraceLang.

## CAK IR

Canonical machine-facing Agent Learning IR. Legacy alias: TLIR.

## TaskCapsule

Portable unit of agent execution containing goal, env references, policy constraints, budgets, provider profile, verifier plan, and artifact dependencies.

## Agent VM

Guarded runtime that accepts model proposals, verifies them, executes allowed actions, records traces, and manages transactions.

## Trace

Event-sourced record of agent execution.

## EvidenceSpec

Artifact proving why a memory, effect, skill, or patch is trusted.

## ScopeSpec

Applicability boundary for artifacts: tenant, environment, model, provider, time, role, data, and policy scope.

## EffectSpec

Guarded action-effect hypothesis with preconditions, effects, exceptions, confidence, evidence, and reversibility.

## SkillSpec

Reusable executable behavior contract with trigger, preconditions, steps, postconditions, verifier tests, rollback, risk, evidence, scope, and lifecycle state.

## ArtifactGraph

Dependency graph connecting traces, evidence, effects, skills, policies, provider profiles, evals, incidents, and patches.

## CARE-Bench

Benchmark family for Causal Adaptation, Replay, and Enforcement.

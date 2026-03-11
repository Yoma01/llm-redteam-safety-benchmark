# llm-redteam-safety-benchmark
1. Problem

LLMs can fail under adversarial or indirect requests, and many safety evaluations remain anecdotal or non-reproducible.

2. Solution

A modular automated framework that generates attacks, executes them against models, scores safety outcomes, benchmarks defenses, and maps results to governance risks.

3. Features

adversarial prompt generation

multi-turn testing

structured scoring

defense benchmarking

governance mapping

dashboard visualization

4. Architecture diagram

Simple flow:
Attack Engine → Model Harness → Response Logs → Scoring Engine → Defense Benchmark → Risk Mapper → Dashboard

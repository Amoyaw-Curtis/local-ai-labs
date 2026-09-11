from planner import plan_step
from executor import execute_step
from tools import run_tests

def run_agent(goal: str, max_iterations: int = 10):
    print("Goal:", goal)

    print("\nRunning initial tests...")
    test_result = run_tests()
    print("Initial test result:", test_result)

    history = [
        {
            "action": "run_tests",
            "args": {},
            "result": test_result.get("output", "")
        }
    ]

    for i in range(1, max_iterations + 1):
        print(f"\n=== Iteration {i} ===")

        step = plan_step(goal, history)

        if step.get("done"):
            print("Planner signaled done.")
            break

        result = execute_step(step)
        action = step.get("action")
        args = step.get("args", {})

        history.append({
            "action": action,
            "args": args,
            "result": str(result)
        })

        if action in ("write_file", "replace_in_file"):
            print("\nRe-running tests after code change...")
            test_result = run_tests()
            print("Test result:", test_result)

            output = test_result.get("output", "")
            history.append({
                "action": "run_tests",
                "args": {},
                "result": output
            })

            if test_result.get("ok") and "FAIL" not in output:
                print("\nVitest reports all tests passing. Stopping.")
                break

    print("\nDone.")

if __name__ == "__main__":
    goal = "Fix failing tests in this project using iterative edits."
    run_agent(goal)
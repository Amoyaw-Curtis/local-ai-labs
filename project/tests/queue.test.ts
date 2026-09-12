import { describe, it, expect } from "vitest";
import { TaskQueue } from "../src/queue.js";

describe("TaskQueue", () => {
    it("executes tasks within concurrency limits", async () => {
        const queue = new TaskQueue(2);
        let maxConcurrentObserved = 0;
        let currentConcurrent = 0;

        const makeTask = (id: string, delayMs: number) => ({
            id,
            run: async () => {
                currentConcurrent++;
                maxConcurrentObserved = Math.max(maxConcurrentObserved, currentConcurrent);
                await new Promise((r) => setTimeout(r, delayMs));
                currentConcurrent--;
                return id;
            },
        });

        const results = await Promise.all([
            queue.runTask(makeTask("1", 40)),
            queue.runTask(makeTask("2", 40)),
            queue.runTask(makeTask("3", 20)),
            queue.runTask(makeTask("4", 20)),
        ]);

        expect(results).toEqual(["1", "2", "3", "4"]);
        expect(maxConcurrentObserved).toBeLessThanOrEqual(2);
    });

    it("drains all waiting tasks after earlier tasks complete", async () => {
        const queue = new TaskQueue(1);
        const order: number[] = [];

        await Promise.all([
            queue.runTask({ id: "a", run: async () => { order.push(1); } }),
            queue.runTask({ id: "b", run: async () => { order.push(2); } }),
        ]);

        expect(order).toEqual([1, 2]);
        expect(queue.activeCount).toBe(0);
    });
});
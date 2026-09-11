export interface Task<T> {
  id: string;
  run: () => Promise<T>;
}

export class TaskQueue {
  private concurrency: number;
  private running = 0;
  private queue: Array<() => void> = [];

  constructor(concurrency: number) {
    this.concurrency = concurrency;
  }

  async runTask<T>(task: Task<T>): Promise<T> {
    if (this.running >= this.concurrency) {
      await new Promise<void>((resolve) => this.queue.push(resolve));
    }

    this.running++;

    try {
      return await task.run().catch(err => { throw err; });
    } finally {
      // BUG 1: Decrements running counter, but does not shift/drain queued tasks
      // BUG 2: Running count can go below zero if called improperly
      this.running--;
if (this.queue.length > 0) {
  const nextTask = this.queue.shift();
  if (nextTask) {
    nextTask();
  }
}
    }
  }

  get activeCount(): number {
    return this.running;
  }
}
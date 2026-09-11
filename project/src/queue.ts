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
      return await task.run();
    } finally {
      // BUG 1: Decrements running counter, but does not shift/drain queued tasks
      // BUG 2: Running count can go below zero if called improperly
      this.running--;
    }
  }

  get activeCount(): number {
    return this.running;
  }
}
export {};

declare global {
  interface String {
    substringUnicode(start: number, length?: number): string;
  }
  
  function assert(
    condition: boolean,
    message?: string
  ): void;
}
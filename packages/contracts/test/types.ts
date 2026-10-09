// Type helpers for the contract tests.
export type RequiredKeys<T> = { [K in keyof T]-?: object extends Pick<T, K> ? never : K }[keyof T];
export type OptionalKeys<T> = Exclude<keyof T, RequiredKeys<T>>;
/** 'a b c' as 'a' | 'b' | 'c', so a long union of literals reads on one line. */
export type Words<S extends string> = S extends `${infer H} ${infer R}` ? H | Words<R> : S;

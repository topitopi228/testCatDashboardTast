// types.ts
export interface Cat {
  id: number;
  name: string;
  years_of_experience: number;
  breed: string;
  salary: number;
}

export type CatCreate = Omit<Cat, "id">;
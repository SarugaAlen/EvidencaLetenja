import { describe, it, expect, afterEach } from "vitest";
import { writable } from "svelte/store";

const mockPiloti = [
  { idPilot: 1, ime: "Janez", priimek: "Novak" },
  { idPilot: 2, ime: "Ana", priimek: "Horvat" },
  { idPilot: 3, ime: "Marko", priimek: "Kovač" },
  { idPilot: 4, ime: "Iva", priimek: "Zupan" },
];

describe("Pilot Table Filtering", () => {
  let piloti = writable(mockPiloti);
  let searchQuery = writable("");
  let filteredPiloti = writable<typeof mockPiloti>([]);

  const setupFiltering = () => {
    searchQuery.subscribe((query) => {
      filteredPiloti.set(
        mockPiloti.filter(
          (pilot) =>
            pilot.ime.toLowerCase().includes(query.toLowerCase()) ||
            pilot.priimek.toLowerCase().includes(query.toLowerCase())
        )
      );
    });
  };

  setupFiltering();

  afterEach(() => {
    searchQuery.set("");
    filteredPiloti.set([]);
  });

  it("should return all pilots when search query is empty", async () => {
    searchQuery.set("");
    await new Promise((resolve) => {
      filteredPiloti.subscribe((result) => {
        if (result.length === mockPiloti.length) {
          expect(result).toEqual(mockPiloti);
          resolve(true);
        }
      });
    });
  });

  it("should filter pilots by string", async () => {
    searchQuery.set("ana");

    await new Promise((resolve) => {
      filteredPiloti.subscribe((result) => {
        if (result.length === 1) {
          expect(result).toEqual([
            { idPilot: 2, ime: "Ana", priimek: "Horvat" },
          ]);
          resolve(true);
        }
      });
    });
  });
});

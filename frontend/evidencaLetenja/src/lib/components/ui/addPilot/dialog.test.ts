import "@testing-library/jest-dom";
import { render, fireEvent, screen } from "@testing-library/svelte";
import { vi } from "vitest";
import PilotDialog from "./addPilotDialog.svelte";

test("save button triggers onSave with pilot data", async () => {
 const onSave = vi.fn();
 render(PilotDialog, {
   pilot: { idPilot: 4, ime: "Janez", priimek: "Novak" },
   onSave
 });

 await fireEvent.click(screen.getByText("Dodaj"));
 await fireEvent.click(screen.getByText("Shrani"));

 expect(onSave).toHaveBeenCalledWith({ 
   ime: "Janez", 
   priimek: "Novak" 
 });
});
import { render, fireEvent, screen } from '@testing-library/svelte';
import '@testing-library/jest-dom';
import { expect, test} from 'vitest';
import AddFlightDialog from "$lib/components/ui/addFlight/addFlightDialog.svelte";

test('AddFlightDialog button can be clicked', async () => {
    render(AddFlightDialog);

    const button = screen.getByRole('button', { name: /Dodaj/i });
    expect(button).toBeInTheDocument();
  });

test('AddFlightDialog button can be clicked', async () => {
    render(AddFlightDialog);

    const button = screen.getByRole('button', { name: /Dodaj/i });
    expect(button).toBeInTheDocument();

    await fireEvent.click(button);

    const dialog = screen.getByRole('dialog');
    expect(dialog).toBeInTheDocument();
});


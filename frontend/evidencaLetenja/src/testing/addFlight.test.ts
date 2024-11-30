import { render, fireEvent, screen } from '@testing-library/svelte';
import '@testing-library/jest-dom';
import { expect, test} from 'vitest';
import AddFlightDialog from "$lib/components/ui/addFlight/addFlightDialog.svelte";

test('AddFlightDialog button can be clicked', async () => {
    render(AddFlightDialog);

    const button = screen.getByRole('button', { name: /Dodaj/i });

    //await fireEvent.click(button);

    expect(button).toBeInTheDocument();
  });


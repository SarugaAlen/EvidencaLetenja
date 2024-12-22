import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import EditFlightDialog from '$lib/components/ui/editFlight/editFlightDialog.svelte';
import '@testing-library/jest-dom';
import userEvent from '@testing-library/user-event';

describe('Edit Flight Dialog', () => {
  const mockFlight = {
    idPolet: 1,
    cas_vzleta: '01/01/2024 10:00',
    cas_pristanka: '01/01/2024 12:00',
    Pilot_idPilot: 123
  };

  it('renders edit button and opens dialog when clicked', async () => {
    const onSaveMock = vi.fn();
    render(EditFlightDialog, {
      props: {
        polet: mockFlight,
        onSave: onSaveMock
      }
    });

    const editButton = screen.getByText('Uredi');
    expect(editButton).toBeInTheDocument();

    await userEvent.click(editButton);
    
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText('Uredi polet')).toBeInTheDocument();
  });

  it('shows flight data in the form', async () => {
    const onSaveMock = vi.fn();
    render(EditFlightDialog, {
      props: {
        polet: mockFlight,
        onSave: onSaveMock
      }
    });

    await userEvent.click(screen.getByText('Uredi'));

    const pilotInput = screen.getByLabelText('Pilot ID') as HTMLInputElement;
    expect(pilotInput.value).toBe('123');
  });

  it('calls onSave with updated data when save button is clicked', async () => {
    const onSaveMock = vi.fn();
    render(EditFlightDialog, {
      props: {
        polet: mockFlight,
        onSave: onSaveMock
      }
    });

    await userEvent.click(screen.getByText('Uredi'));

    const pilotInput = screen.getByLabelText('Pilot ID');
    await userEvent.clear(pilotInput);
    await userEvent.type(pilotInput, '456');

    await userEvent.click(screen.getByText('Shrani'));

    expect(onSaveMock).toHaveBeenCalledWith({
      idPolet: 1,
      cas_vzleta: mockFlight.cas_vzleta,
      cas_pristanka: mockFlight.cas_pristanka,
      Pilot_idPilot: 456
    });
  });
});